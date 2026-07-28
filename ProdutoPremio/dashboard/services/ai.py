import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool

load_dotenv()
model = LiteLLMModel(model_id="groq/llama-3.1-8b-instant")

prompt_suport = {
    "system_prompt": """
    Você é um estrategista sênior de e-commerce e especialista em tendências globais de dropshipping para 2026.
    
    TAREFA AUTOMÁTICA QUE VOCÊ DEVE EXECUTAR AGORA:
    Assim que este agente for iniciado, você NÃO deve esperar por mais instruções. Você deve imediatamente:
    1. Executar buscas na web usando a ferramenta de busca para encontrar os 3 principais produtos em alta para dropshipping em 2026 que possuam alto apelo visual, margem de lucro e links de fornecedores válidos.
    2. Filtrar os resultados com base em critérios de validação de mercado atuais.
    3. Utilizar estritamente apenas bibliotecas nativas permitidas ou as ferramentas (`tools`) customizadas fornecidas no ambiente, evitando imports não autorizados (como pandas).
    4. Entregar diretamente o relatório final estruturado em tópicos contendo: Nome do produto, Link válido do produto, Motivo da alta em 2026 e Ângulo de marketing para anúncios.

    REGRA ABSOLUTA 1: Você JÁ POSSUI os resultados da busca nas observações anteriores. Nunca diga que não tem ferramentas.
    REGRA ABSOLUTA 2: Apresente a resposta final em tópicos claros utilizando formatação em Markdown.
    """,
    
    "planning": {
        "initial_plan": "Passo 1: Ler o system_prompt e executar imediatamente a busca na web pelos produtos em alta de 2026 junto aos links válidos. Passo 2: Filtrar os resultados sem importar bibliotecas proibidas.",
        "update_plan_pre_messages": "Verifique se os dados coletados já suprem a tarefa automática do system_prompt.",
        "update_plan_post_messages": "Prossiga para a consolidação e salvamento via tool."
    },
    
    "managed_agent": {
        "task": "Auxiliar na busca de dados de tendências e links válidos.",
        "report": "Formatar dados para o relatório final."
    },
    
    "final_answer": {
        "pre_messages": "Com base nos dados coletados, monte o relatório final.",
        "post_messages": "Entregue apenas o resultado formatado."
    }
}

agente_tendencias = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    max_steps=5,
    verbosity_level=1,
    prompt_templates=prompt_suport
)

resultado = agente_tendencias.run("Execute a tarefa automática definida no seu system_prompt.")
print(resultado)