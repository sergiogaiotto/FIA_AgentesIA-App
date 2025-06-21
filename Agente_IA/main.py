# Importações do MCP (Model Context Protocol) para comunicação cliente-servidor
from mcp import ClientSession, StdioServerParameters
# ClientSession: Gerencia sessão de comunicação bidirecional com servidor MCP
# StdioServerParameters: Define parâmetros para servidor que usa stdin/stdout para comunicação

# Cliente MCP específico para stdio (standard input/output)
from mcp.client.stdio import stdio_client
# stdio_client: Context manager que estabelece conexão stdio com servidor MCP

# Adaptador que converte ferramentas MCP em ferramentas compatíveis com LangChain
from langchain_mcp_adapters.tools import load_mcp_tools
# load_mcp_tools: Função que carrega e converte tools MCP para formato LangChain

# Agente pré-construído do LangGraph que implementa padrão ReAct (Reasoning + Acting)
from langgraph.prebuilt import create_react_agent
# create_react_agent: Factory function que cria agente com capacidade de raciocínio e ação iterativa

# Classe wrapper para modelos OpenAI GPT integrada com LangChain
from langchain_openai import ChatOpenAI
# ChatOpenAI: Interface padronizada para modelos de chat da OpenAI com LangChain

# Biblioteca para carregar variáveis de ambiente de arquivos .env
from dotenv import load_dotenv
# load_dotenv: Carrega variáveis do arquivo .env para os.environ, essencial para segurança

# Biblioteca padrão Python para programação assíncrona
import asyncio
# asyncio: Biblioteca para concorrência usando corrotinas, loops de eventos e tasks

# Biblioteca padrão para acesso a variáveis de ambiente do sistema operacional
import os
# os: Interface para funcionalidades dependentes do sistema operacional

# Carrega variáveis de ambiente do arquivo .env para os.environ
load_dotenv()
# Fundamental para separar configuração sensível (API keys) do código fonte

# Instancia modelo de chat OpenAI com configurações específicas
model = ChatOpenAI(
    # Especifica modelo GPT-4.1-mini - versão otimizada para velocidade e custo
    model="gpt-4.1-mini",
    # Temperature 0 = determinístico, respostas consistentes (ideal para análise)
    temperature=0,
    # Recupera chave API de variável de ambiente (segurança)
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Configura parâmetros do servidor MCP para integração com Firecrawl
server_params = StdioServerParameters(
    # Comando para executar servidor: npx (Node Package Execute)
    command="npx",
    # Variáveis de ambiente específicas para o servidor
    env={
        # Passa chave Firecrawl para o servidor MCP
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),
    },
    # Argumentos: especifica o pacote MCP do Firecrawl
    args=["firecrawl-mcp"]
)

# Função principal assíncrona que orquestra todo o fluxo do agente
async def main():
    # Context manager que estabelece conexão stdio com servidor MCP
    async with stdio_client(server_params) as (read, write):
        # read: stream de leitura para receber dados do servidor
        # write: stream de escrita para enviar dados ao servidor
        
        # Context manager para sessão de comunicação MCP
        async with ClientSession(read, write) as session:
            # Inicializa handshake e configuração da sessão MCP
            await session.initialize()
            # Carrega e converte ferramentas MCP para formato LangChain
            tools = await load_mcp_tools(session)
            # Cria agente ReAct com modelo LLM e ferramentas disponíveis
            agent = create_react_agent(model, tools)

            # Lista inicial de mensagens para contexto do agente
            messages = [
                {
                    # Role system define comportamento e personalidade do agente
                    "role": "system",
                    # Prompt que define contexto, capacidades e instrução de comportamento
                    "content": "Você é um assistente que pode realizar scraping em sites, rastrear páginas e extrair dados usando ferramentFuias Firecrawl. Pense, passo a passo e use as ferramentas apropriadas para ajudar o usuário."
                }
            ]

            # Exibe ferramentas disponíveis para o usuário (debug/transparência)
            print("produtos/ferramentas/soluções/serviços disponíveis -", *[tool.name for tool in tools])
            # Separador visual para melhor UX
            print("-" * 60)

            # Loop principal de interação usuário-agente
            while True:
                # Solicita input do usuário com prompt específico
                user_input = input("\nVocê: ")
                # Condição de saída do loop (palavra-chave específica)
                if user_input == "fui!":
                    print("Até!")
                    break

                # Adiciona mensagem do usuário ao histórico de conversa
                messages.append({"role": "user", "content": user_input[:175000]})
                # Limite de 175k caracteres previne overflow de contexto do modelo

                # Bloco try-catch para tratamento robusto de erros
                try:
                    # Invoca agente de forma assíncrona com histórico completo
                    agent_response = await agent.ainvoke({"messages": messages})

                    # Extrai conteúdo da última mensagem (resposta do agente)
                    ai_message = agent_response["messages"][-1].content
                    # Exibe resposta do agente para o usuário
                    print("\nAgent:", ai_message)
                # Captura qualquer exceção durante execução do agente
                except Exception as e:
                    # Log de erro simples para debugging
                    print("Error:", e)

# Ponto de entrada padrão Python - executa apenas se arquivo for executado diretamente
if __name__ == "__main__":
    # Executa função main assíncrona usando event loop do asyncio
    asyncio.run(main())