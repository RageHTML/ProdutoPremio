import os
import re
import json
import requests
import litellm
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, WebSearchTool, Tool
from bs4 import BeautifulSoup

load_dotenv()


model = LiteLLMModel(model_id="groq/llama-3.1-8b-instant")

# Padroes url descrevem a forma que a url deve ter, utilizando regex, informacao na docs

PADROES_URL_PRODUTO = [
    r'-i\.\d+\.\d+',            #Padrao shoppe    
    r'/MLB-?\d+',               #Padrao mercado livre
    r'/dp/[A-Z0-9]{10}',        #Padrao amazon 
]

PADRAO_PRECO = re.compile(r'R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?') # Padrao de preco

# Identifica se o texto de ancora parece se referir a um produto específico de e-commerce
# E um caso especifico caso o href nao seja um padrao de url de produto, mas o texto de ancora seja um nome de produto, entao a funcao retorna true

def identificar_produto(texto_ancora: str) -> bool:
    if not texto_ancora:
        return False

    prompt = (
        f'O texto a seguir é o texto de um link de uma página web: "{texto_ancora}". '
        'Esse texto parece se referir a um PRODUTO específico de e-commerce '
        '(não categoria, não blog, não menu)? Responda APENAS "sim" ou "nao".'
    )

    try:
        resposta = litellm.completion(
            model="groq/llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
        )
        texto = resposta.choices[0].message.content.strip().lower()
        return texto.startswith("sim")
    except Exception as e:
        print(f"Erro ao identificar produto: {e}")
        return False


# Filtro de links, o parametro href e o url da tag <a> e o parametro texto_ancora e o texto que esta dentro da tag <a>
# -> garante que a resposta da funcao seja um booleano (true/false) 
# o loop percorre a lista de padroes, re.search verifica se o padrao esta presente no href, se sim retorna true
# Caso contrario, envia o texto_ancora para indentificar_produto

def parece_link_de_produto(href: str, texto_ancora: str = "") -> bool:
    for padrao in PADROES_URL_PRODUTO:
        if re.search(padrao, href):
            return True
        else:
            return identificar_produto(texto_ancora)
        


class ExtrairUrlsTool(Tool):
    name = "extrair_urls"
    description = "Extrai todas as URLs válidas (começadas com http ou https) de um bloco de texto usando Regex."

    inputs = {
        "texto": {
            "type": "string",
            "description": "O texto bruto de onde os links devem ser extraídos."
        }
    }
    output_type = "array"

    def forward(self, texto: str) -> list:
        pattern = r'https?://[^\s,;)\]"\'<>]+'
        return re.findall(pattern, texto)


class RasparConteudoTool(Tool):
    name = "raspar_conteudo"
    description = (
        "Faz uma requisição HTTP em uma lista de URLs, remove tags irrelevantes "
        "(header, footer, nav, script, style), analisa as tags <a> das páginas e "
        "retorna apenas os hrefs que parecem ser links de produtos (com base em "
        "padrões de URL de marketplaces conhecidos ou presença de preço no texto "
        "do link)."
    )
    inputs = {
        "urls": {
            "type": "array",
            "description": "Lista de URLs para realizar o scraping."
        }
    }
    output_type = "array"

    def forward(self, urls: list) -> list:
        hrefs_encontrados = []
        headers_fake = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        for url in urls:
            try:
                response = requests.get(url, headers=headers_fake, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    for tag in soup.find_all(['header', 'footer', 'nav', 'script', 'style']):
                        tag.extract()

                    elementos = soup.find_all('a')

                    for el in elementos:
                        href = el.get('href')

                        if not href or not href.startswith(('http://', 'https://', '/')):
                            continue

                        texto_ancora = el.get_text(strip=True)

                        if parece_link_de_produto(href, texto_ancora):
                            hrefs_encontrados.append(href)

            except Exception as e:
                print(f"Erro ao raspar a URL {url}: {e}")

        return hrefs_encontrados


class SalvarLinksTool(Tool):
    name = "salvar_links"
    description = (
        "Recebe uma lista de links (hrefs) e salva no arquivo links.json. "
        "Se o arquivo não existir, cria (junto das pastas necessárias). "
        "Se existir, adiciona os novos links e remove duplicados automaticamente."
    )
    inputs = {
        "hrefs": {
            "type": "array",
            "description": "Lista de links (hrefs) a serem salvos."
        }
    }
    output_type = "string"

    CAMINHO_ARQUIVO = "/mnt/SteamGames/Pyhton/ProdutoPremio/ProdutoPremio/dashboard/services/links.json"  # <- fixo, não exposto ao LLM

    def forward(self, hrefs: list) -> str:
        caminho = self.CAMINHO_ARQUIVO

        os.makedirs(os.path.dirname(caminho), exist_ok=True)

        links_existentes = []
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    links_existentes = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                links_existentes = []

        todos_links = links_existentes + hrefs
        links_unicos = list(dict.fromkeys(todos_links))

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(links_unicos, f, ensure_ascii=False, indent=2)

        novos = len(links_unicos) - len(links_existentes)
        return f"{novos} novo(s) link(s) salvo(s). Total no arquivo: {len(links_unicos)}."

agente_tendencias = CodeAgent(
    tools=[WebSearchTool(), ExtrairUrlsTool(), RasparConteudoTool(), SalvarLinksTool()],
    additional_authorized_imports=['re', 'requests', 'bs4', 'json'],
    model=model,
    max_steps=10,
    verbosity_level=2,
    instructions=(
        "Para QUALQUER pergunta que envolva pesquisar um assunto, tendência, notícia "
        "ou tópico atual, siga SEMPRE este fluxo fixo, nesta ordem:\n"
        "1. Use web_search com o assunto pedido como query.\n"
        "2. Use extrair_urls no resultado da busca para obter a lista de URLs.\n"
        "3. Use raspar_conteudo passando essas URLs, para obter a lista de hrefs "
        "de produtos encontrados nas páginas.\n"
        "4. Use salvar_links passando essa lista de hrefs, para persistir os links "
        "em arquivo.\n"
        "5. Na resposta final, resuma o que foi encontrado e informe quantos links "
        "novos foram salvos."
    ),
)


if __name__ == "__main__":
    resposta = agente_tendencias.run("Produtos mais vendidos da Shopee 2026")
    print(resposta)