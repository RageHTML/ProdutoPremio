from smolagents import LiteLLMModel,ToolCallingAgent, WebSearchTool
model = LiteLLMModel(
    model_id="ollama_chat/hf.co/GnLOLot/MiniCPM5-1B-Claude-Opus-Fable5-V2-Thinking-GGUF:latest",
    api_base="http://localhost:11434",
)

agente_suporte = ToolCallingAgent(
    tools=[],
    model=model,
    verbosity_level=2,
)

resultado = agente_suporte.run("Qual o resultado de 2 + 1")
print(resultado)