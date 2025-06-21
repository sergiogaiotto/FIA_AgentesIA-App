# Agente MCP - Integração com Model Context Protocol para scraping dinâmico
import os
import asyncio
from typing import List, Dict, Any, Optional

# Imports do MCP (Model Context Protocol)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Adaptador MCP para LangChain
from langchain_mcp_adapters.tools import load_mcp_tools

# LangGraph para agentes ReAct
from langgraph.prebuilt import create_react_agent

# Modelo OpenAI
from langchain_openai import ChatOpenAI

# Carregamento de variáveis de ambiente
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class MCPAgent:
    """
    Agente MCP que utiliza Model Context Protocol para integração 
    dinâmica com ferramentas externas como Firecrawl
    """

    def __init__(self):
        """Inicializa agente MCP com configurações necessárias"""
        
        # Validação de chaves de API
        self.firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        if not self.firecrawl_key:
            raise ValueError("FIRECRAWL_API_KEY não encontrada nas variáveis de ambiente")
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        
        # Configuração do modelo LLM
        self.model = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
            openai_api_key=self.openai_key
        )
        
        # Configuração do servidor MCP
        self.server_params = StdioServerParameters(
            command="npx",
            env={
                "FIRECRAWL_API_KEY": self.firecrawl_key,
            },
            args=["firecrawl-mcp"]
        )
        
        # Histórico de mensagens para contexto
        self.message_history: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": """Você é um assistente especializado em pesquisa e análise de produtos, ferramentas, soluções e serviços.

Você pode:
- Fazer scraping de sites para extrair informações
- Buscar e comparar produtos/serviços
- Analisar preços, características e ofertas
- Fornecer recomendações técnicas objetivas

Use as ferramentas Firecrawl disponíveis para:
- Fazer scraping de páginas específicas
- Buscar informações relevantes na web
- Extrair dados estruturados de sites

Sempre forneça respostas úteis, concisas e bem estruturadas."""
            }
        ]

    async def process_message(self, user_message: str) -> str:
        """
        Processa mensagem do usuário usando agente MCP
        
        Args:
            user_message: Mensagem/consulta do usuário
            
        Returns:
            Resposta processada pelo agente
        """
        
        # Adiciona mensagem do usuário ao histórico
        self.message_history.append({
            "role": "user", 
            "content": user_message[:175000]  # Limite para evitar overflow
        })
        
        try:
            # Estabelece conexão MCP e processa mensagem
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Inicializa sessão MCP
                    await session.initialize()
                    
                    # Carrega ferramentas MCP
                    tools = await load_mcp_tools(session)
                    
                    # Cria agente ReAct com ferramentas
                    agent = create_react_agent(self.model, tools)
                    
                    # Processa mensagem através do agente
                    agent_response = await agent.ainvoke({
                        "messages": self.message_history
                    })
                    
                    # Extrai resposta do agente
                    ai_message = agent_response["messages"][-1].content
                    
                    # Adiciona resposta ao histórico
                    self.message_history.append({
                        "role": "assistant",
                        "content": ai_message
                    })
                    
                    return ai_message
                    
        except Exception as e:
            error_message = f"❌ Erro ao processar mensagem: {str(e)}"
            print(f"Erro MCP Agent: {e}")
            return error_message

    def reset_conversation(self):
        """Reseta histórico de conversa mantendo apenas system message"""
        self.message_history = [self.message_history[0]]  # Mantém apenas system message

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retorna histórico da conversa"""
        return self.message_history.copy()

    async def check_tools_availability(self) -> Dict[str, Any]:
        """
        Verifica disponibilidade das ferramentas MCP
        
        Returns:
            Dicionário com status das ferramentas
        """
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await load_mcp_tools(session)
                    
                    return {
                        "status": "available",
                        "tools_count": len(tools),
                        "tool_names": [tool.name for tool in tools]
                    }
                    
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tools_count": 0,
                "tool_names": []
            }