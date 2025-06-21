# agents/mcp_agent.py - Comentado Linha a Linha

# Agente MCP - Integração com Model Context Protocol para scraping dinâmico
# Comentário descritivo: define propósito específico do módulo
# MCP (Model Context Protocol): protocolo para integração de ferramentas externas com LLMs

import os
# Módulo padrão Python para interação com sistema operacional
# Usado para acessar variáveis de ambiente (API keys)

import asyncio
# Biblioteca para programação assíncrona em Python
# Necessária para operações I/O não bloqueantes (web scraping, API calls)

from typing import List, Dict, Any, Optional
# Type hints para melhor documentação e verificação de tipos
# List, Dict, Any: tipos genéricos para estruturas de dados
# Optional: indica valores que podem ser None
# Benefício: IDE support, debugging, documentação

# Imports do MCP (Model Context Protocol)
from mcp import ClientSession, StdioServerParameters
# ClientSession: classe para gerenciar sessão MCP
# StdioServerParameters: configuração para comunicação via stdio
# MCP: protocolo que permite LLMs usar ferramentas externas

from mcp.client.stdio import stdio_client
# Cliente MCP para comunicação via standard input/output
# Padrão de comunicação entre processos usando streams

# Adaptador MCP para LangChain
from langchain_mcp_adapters.tools import load_mcp_tools
# Adaptador que converte ferramentas MCP em format LangChain
# Bridge pattern: conecta MCP com ecossistema LangChain

# LangGraph para agentes ReAct
from langgraph.prebuilt import create_react_agent
# LangGraph: framework para criar fluxos de agentes complexos
# ReAct: pattern de Reasoning + Acting para agentes LLM
# Prebuilt: agentes pré-configurados para casos comuns

# Modelo OpenAI
from langchain_openai import ChatOpenAI
# Integração LangChain com API OpenAI
# ChatOpenAI: wrapper para modelos de chat da OpenAI

# Carregamento de variáveis de ambiente
from dotenv import load_dotenv
# Biblioteca para carregar variáveis de arquivo .env
# Best practice: separar configuração sensível do código

# Carrega variáveis de ambiente
load_dotenv()
# Executa carregamento das variáveis do arquivo .env
# Deve ser chamado antes de acessar os.getenv()


class MCPAgent:
    """
    Agente MCP que utiliza Model Context Protocol para integração 
    dinâmica com ferramentas externas como Firecrawl
    """
    # Docstring da classe explicando propósito e funcionalidade
    # MCP permite ao agente usar ferramentas externas dinamicamente

    def __init__(self):
        """Inicializa agente MCP com configurações necessárias"""
        # Docstring do construtor
        
        # Validação de chaves de API
        self.firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
        # Obtém chave API do Firecrawl das variáveis de ambiente
        # os.getenv(): retorna None se variável não existir
        
        self.openai_key = os.getenv("OPENAI_API_KEY")
        # Obtém chave API da OpenAI das variáveis de ambiente
        
        if not self.firecrawl_key:
            raise ValueError("FIRECRAWL_API_KEY não encontrada nas variáveis de ambiente")
        # Validação obrigatória: falha rápida se configuração inválida
        # ValueError: exceção apropriada para dados inválidos
        
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        # Validação redundante mas necessária para segundo serviço
        
        # Configuração do modelo LLM
        self.model = ChatOpenAI(
            model="gpt-4.1-mini",
            # Modelo específico da OpenAI: versão otimizada e mais econômica
            temperature=0,
            # Temperature 0: respostas determinísticas e precisas
            # Para tarefas analíticas, preferível ter consistência
            openai_api_key=self.openai_key
            # Injeção explícita da API key
        )
        
        # Configuração do servidor MCP
        self.server_params = StdioServerParameters(
            command="npx",
            # npx: executador de pacotes Node.js
            # Usado para executar firecrawl-mcp sem instalação global
            env={
                "FIRECRAWL_API_KEY": self.firecrawl_key,
            },
            # Passa variáveis de ambiente para o processo MCP
            # Isolamento: processo MCP recebe apenas o necessário
            args=["firecrawl-mcp"]
            # Argumentos para npx: executa pacote firecrawl-mcp
            # Servidor MCP que expõe ferramentas Firecrawl
        )
        
        # Histórico de mensagens para contexto
        self.message_history: List[Dict[str, str]] = [
            # Type hint explícito para lista de dicionários
            # Mantém contexto conversacional para o agente
            {
                "role": "system",
                # Role system: instruções base para o LLM
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
                # System prompt detalhado definindo:
                # 1. Persona do agente (assistente especializado)
                # 2. Capacidades principais (scraping, análise, comparação)
                # 3. Ferramentas disponíveis (Firecrawl)
                # 4. Estilo de resposta esperado (útil, conciso, estruturado)
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
        # Docstring com documentação completa dos parâmetros
        # Async function: permite operações não-bloqueantes
        
        # Adiciona mensagem do usuário ao histórico
        self.message_history.append({
            "role": "user", 
            # Role user: marca mensagem como vinda do usuário
            "content": user_message[:175000]  # Limite para evitar overflow
            # Truncamento de segurança: evita mensagens muito longas
            # 175000 chars: limite conservador para APIs LLM
        })
        
        try:
            # Estabelece conexão MCP e processa mensagem
            async with stdio_client(self.server_params) as (read, write):
                # Context manager assíncrono para cliente MCP
                # stdio_client: cria streams de comunicação com servidor MCP
                # read, write: streams para comunicação bidirecional
                
                async with ClientSession(read, write) as session:
                    # ClientSession: gerencia protocolo MCP sobre streams
                    # Context manager: garante cleanup automático
                    
                    # Inicializa sessão MCP
                    await session.initialize()
                    # Handshake inicial: estabelece protocolo e capacidades
                    
                    # Carrega ferramentas MCP
                    tools = await load_mcp_tools(session)
                    # Converte ferramentas MCP em formato LangChain
                    # Abstração: tools se tornam chamáveis pelo agente
                    
                    # Cria agente ReAct com ferramentas
                    agent = create_react_agent(self.model, tools)
                    # ReAct pattern: Reasoning + Acting
                    # Agent usa LLM + tools para resolver problemas
                    # self.model: LLM para reasoning
                    # tools: ferramentas para acting
                    
                    # Processa mensagem através do agente
                    agent_response = await agent.ainvoke({
                        "messages": self.message_history
                    })
                    # ainvoke: versão assíncrona de invoke
                    # Passa histórico completo para manter contexto
                    
                    # Extrai resposta do agente
                    ai_message = agent_response["messages"][-1].content
                    # Pega última mensagem (resposta do agente)
                    # [-1]: último elemento da lista
                    # .content: extrai texto da mensagem
                    
                    # Adiciona resposta ao histórico
                    self.message_history.append({
                        "role": "assistant",
                        # Role assistant: marca como resposta do AI
                        "content": ai_message
                    })
                    
                    return ai_message
                    # Retorna resposta para o usuário
                    
        except Exception as e:
            # Tratamento genérico de exceções
            error_message = f"❌ Erro ao processar mensagem: {str(e)}"
            # Emoji visual + descrição técnica
            print(f"Erro MCP Agent: {e}")
            # Log para debugging/monitoramento
            return error_message
            # Retorna mensagem de erro amigável ao usuário

    def reset_conversation(self):
        """Reseta histórico de conversa mantendo apenas system message"""
        # Função utilitária para limpar contexto
        self.message_history = [self.message_history[0]]  # Mantém apenas system message
        # Preserva system prompt mas remove contexto conversacional
        # [0]: primeiro elemento (system message)

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retorna histórico da conversa"""
        # Método de acesso para histórico
        return self.message_history.copy()
        # .copy(): retorna cópia para evitar modificação externa
        # Encapsulamento: protege estado interno

    async def check_tools_availability(self) -> Dict[str, Any]:
        """
        Verifica disponibilidade das ferramentas MCP
        
        Returns:
            Dicionário com status das ferramentas
        """
        # Função de diagnóstico para verificar configuração
        try:
            async with stdio_client(self.server_params) as (read, write):
                # Mesmo pattern de conexão MCP
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await load_mcp_tools(session)
                    
                    return {
                        "status": "available",
                        # Status positivo: ferramentas funcionando
                        "tools_count": len(tools),
                        # Quantidade de ferramentas detectadas
                        "tool_names": [tool.name for tool in tools]
                        # Lista de nomes das ferramentas disponíveis
                        # List comprehension: extrai atributo name de cada tool
                    }
                    
        except Exception as e:
            # Falha na verificação
            return {
                "status": "error",
                # Status de erro
                "error": str(e),
                # Detalhes do erro para debugging
                "tools_count": 0,
                # Zero ferramentas quando há erro
                "tool_names": []
                # Lista vazia quando há erro
            }
