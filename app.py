# app.py - Comentado Linha a Linha

from fastapi import FastAPI, Request, HTTPException
# FastAPI: framework web moderno para APIs Python
# Request: objeto que representa requisição HTTP
# HTTPException: exceção específica para erros HTTP

from fastapi.staticfiles import StaticFiles
# StaticFiles: middleware para servir arquivos estáticos (CSS, JS, imagens)
# Necessário para servir frontend junto com API

from fastapi.templating import Jinja2Templates
# Jinja2Templates: engine de templates para renderizar HTML
# Permite separação entre lógica Python e apresentação HTML

from fastapi.responses import HTMLResponse, StreamingResponse
# HTMLResponse: resposta HTTP específica para conteúdo HTML
# StreamingResponse: resposta para streaming de dados (Server-Sent Events)

from pydantic import BaseModel
# BaseModel: classe base Pydantic para validação de dados
# Usado para definir schemas de request/response

import json
# Módulo padrão para manipulação JSON
# Usado para serialização em streaming

import asyncio
# Biblioteca para programação assíncrona
# Necessária para operações não-bloqueantes

import os
# Módulo para interação com sistema operacional
# Usado para acessar variáveis de ambiente

from typing import Dict, Any
# Type hints para melhor documentação
# Dict, Any: tipos para estruturas de dados flexíveis

import uvicorn
# Servidor ASGI para aplicações Python assíncronas
# Usado para executar FastAPI em produção

# Imports dos agentes adaptados
from agents.mcp_agent import MCPAgent
from agents.workflow_agent import WorkflowAgent
# Importação dos dois tipos de agentes desenvolvidos
# Modularização: cada agente em arquivo separado

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Agentes de IA - FIA",
    # Título da API (aparece na documentação)
    description="Plataforma com dois agentes especializados em pesquisa e análise",
    # Descrição detalhada para documentação
    version="1.0.0"
    # Versionamento da API para controle de releases
)

# Configuração de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
# Mount: anexa aplicação ASGI para path específico
# "/static": URL path que servirá arquivos estáticos
# directory="static": diretório físico com arquivos
# name="static": nome interno para referência

templates = Jinja2Templates(directory="pages")
# Configuração do engine de templates
# directory="pages": pasta com arquivos HTML

# Instâncias dos agentes (inicializadas globalmente)
mcp_agent = None
workflow_agent = None
# Variáveis globais para instâncias dos agentes
# None inicial: agentes serão inicializados no startup

class ChatRequest(BaseModel):
    """Modelo para requisições de chat"""
    message: str
    # Mensagem do usuário (campo obrigatório)
    agent_type: str  # "mcp" ou "workflow"
    # Tipo de agente a ser usado (validação manual)

class ChatResponse(BaseModel):
    """Modelo para respostas de chat"""
    response: str
    # Resposta processada pelo agente
    agent_type: str
    # Tipo de agente que processou
    status: str
    # Status da operação (success/error)

# Inicialização dos agentes
async def initialize_agents():
    """Inicializa os agentes de forma assíncrona"""
    # Função assíncrona para setup dos agentes
    # Async: permite inicialização não-bloqueante
    
    global mcp_agent, workflow_agent
    # Global: modifica variáveis no escopo global
    # Necessário para compartilhar instâncias entre requests
    
    try:
        # Inicializa agente MCP (se chaves estão disponíveis)
        if os.getenv("FIRECRAWL_API_KEY") and os.getenv("OPENAI_API_KEY"):
            # Verifica se todas as chaves necessárias estão disponíveis
            # Evita inicialização parcial/falha
            
            mcp_agent = MCPAgent()
            # Instancia agente MCP
            print("✅ MCP Agent inicializado")
            # Feedback visual para logs/debugging
        
        # Inicializa agente Workflow
        if os.getenv("FIRECRAWL_API_KEY") and os.getenv("OPENAI_API_KEY"):
            # Mesma verificação para agente Workflow
            workflow_agent = WorkflowAgent()
            print("✅ Workflow Agent inicializado")
            
    except Exception as e:
        print(f"❌ Erro ao inicializar agentes: {e}")
        # Log de erro para debugging
        # Aplicação continua funcionando mesmo com falha na inicialização

# Event handler para startup
@app.on_event("startup")
async def startup_event():
    await initialize_agents()
# Decorator FastAPI: executa função no startup da aplicação
# Garante que agentes sejam inicializados antes de processar requests

# Rota principal - página de chat
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# GET route para página inicial
# response_class=HTMLResponse: especifica tipo de resposta
# templates.TemplateResponse: renderiza template HTML
# {"request": request}: context necessário para Jinja2

# Endpoint para chat com agentes
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """Endpoint principal para interação com agentes"""
    # POST endpoint para processar mensagens de chat
    # response_model: especifica schema da resposta para documentação
    
    if not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")
    # Validação de entrada: mensagem não pode ser vazia
    # HTTPException: erro HTTP padronizado
    # status_code=400: Bad Request (erro do cliente)
    
    try:
        if chat_request.agent_type == "mcp":
            # Roteamento baseado no tipo de agente
            
            if not mcp_agent:
                return ChatResponse(
                    response="❌ Agente MCP não está disponível. Verifique as configurações.",
                    agent_type="mcp",
                    status="error"
                )
            # Verifica se agente foi inicializado corretamente
            # Retorna erro amigável se indisponível
            
            response = await mcp_agent.process_message(chat_request.message)
            # Processa mensagem usando agente MCP
            # await: operação assíncrona
            
            return ChatResponse(
                response=response,
                agent_type="mcp", 
                status="success"
            )
            # Retorna resposta estruturada
            
        elif chat_request.agent_type == "workflow":
            # Mesmo padrão para agente Workflow
            
            if not workflow_agent:
                return ChatResponse(
                    response="❌ Agente Workflow não está disponível. Verifique as configurações.",
                    agent_type="workflow",
                    status="error"
                )
            
            response = await workflow_agent.process_query(chat_request.message)
            # Método específico do WorkflowAgent
            
            return ChatResponse(
                response=response,
                agent_type="workflow",
                status="success"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Tipo de agente inválido")
            # Validação: agent_type deve ser "mcp" ou "workflow"
            
    except Exception as e:
        return ChatResponse(
            response=f"❌ Erro interno: {str(e)}",
            agent_type=chat_request.agent_type,
            status="error"
        )
        # Tratamento genérico de exceções
        # Retorna erro estruturado em vez de falhar

# Endpoint para streaming de respostas (opcional para UX melhor)
@app.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest):
    """Endpoint para streaming de respostas em tempo real"""
    # Endpoint alternativo para Server-Sent Events
    # Melhora UX: usuário vê progresso em tempo real
    
    async def generate_response():
        """Generator assíncrono para streaming"""
        # Async generator: produz dados incrementalmente
        
        try:
            if chat_request.agent_type == "workflow" and workflow_agent:
                # Streaming específico para Workflow Agent
                
                # Simula streaming do workflow
                yield f"data: {json.dumps({'status': 'processing', 'message': '🔍 Iniciando pesquisa...'})}\n\n"
                # Server-Sent Events format: "data: JSON\n\n"
                # yield: produz dado sem finalizar função
                
                result = await workflow_agent.process_query(chat_request.message)
                # Processa query completa
                
                yield f"data: {json.dumps({'status': 'complete', 'message': result})}\n\n"
                # Envia resultado final
            
            elif chat_request.agent_type == "mcp" and mcp_agent:
                # Streaming para MCP Agent
                
                yield f"data: {json.dumps({'status': 'processing', 'message': '🤖 Processando com MCP...'})}\n\n"
                
                result = await mcp_agent.process_message(chat_request.message)
                
                yield f"data: {json.dumps({'status': 'complete', 'message': result})}\n\n"
            
            else:
                yield f"data: {json.dumps({'status': 'error', 'message': 'Agente não disponível'})}\n\n"
                # Erro quando agente não está disponível
                
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': f'Erro: {str(e)}'})}\n\n"
            # Tratamento de erro no streaming
    
    return StreamingResponse(
        generate_response(),
        # Generator function como fonte dos dados
        media_type="text/plain",
        # MIME type para Server-Sent Events
        headers={
            "Cache-Control": "no-cache",
            # Evita cache do navegador
            "Connection": "keep-alive",
            # Mantém conexão aberta
            "Content-Type": "text/event-stream"
            # Content-Type específico para SSE
        }
    )

# Endpoint de health check para Render
@app.get("/health")
async def health_check():
    """Health check para monitoramento do Render"""
    # Endpoint para verificação de saúde da aplicação
    # Usado por load balancers e monitoring
    
    agent_status = {
        "mcp_agent": mcp_agent is not None,
        # Verifica se agente MCP foi inicializado
        "workflow_agent": workflow_agent is not None,
        # Verifica se agente Workflow foi inicializado
        "environment": {
            "firecrawl_key": bool(os.getenv("FIRECRAWL_API_KEY")),
            # Verifica presença da chave (sem expor valor)
            "openai_key": bool(os.getenv("OPENAI_API_KEY"))
            # Verifica presença da chave OpenAI
        }
    }
    
    return {
        "status": "healthy",
        # Status geral da aplicação
        "agents": agent_status,
        # Detalhes dos agentes
        "version": "1.0.0"
        # Versão para tracking de deploys
    }

# Endpoint para informações dos agentes
@app.get("/agents/info")
async def agents_info():
    """Retorna informações sobre os agentes disponíveis"""
    # Endpoint de metadados sobre capacidades
    # Útil para frontend dinâmico
    
    return {
        "agents": [
            {
                "type": "mcp",
                "name": "Agente MCP",
                "description": "Agente inteligente com integração MCP e Firecrawl para scraping dinâmico",
                "features": ["Scraping em tempo real", "Integração MCP", "Análise conversacional"],
                "available": mcp_agent is not None
                # Status de disponibilidade em tempo real
            },
            {
                "type": "workflow", 
                "name": "Agente Workflow",
                "description": "Agente especializado em pesquisa estruturada e análise comparativa",
                "features": ["Workflow estruturado", "Análise comparativa", "Recomendações técnicas"],
                "available": workflow_agent is not None
            }
        ]
    }
    # Array de objetos com metadados de cada agente

# Configuração para desenvolvimento local
if __name__ == "__main__":
    # Bloco executado apenas quando script é executado diretamente
    # Não executa quando importado como módulo
    
    # Carrega variáveis de ambiente para desenvolvimento
    from dotenv import load_dotenv
    load_dotenv()
    # Carregamento local de .env
    # Em produção, variáveis vêm do ambiente do sistema
    
    # Roda servidor com reload para desenvolvimento
    uvicorn.run(
        "app:app",
        # Módulo:variável da aplicação FastAPI
        host="0.0.0.0",
        # Host 0.0.0.0: aceita conexões de qualquer IP
        # Necessário para containers/deploy
        port=int(os.getenv("PORT", 8000)),
        # Porta configurável via env var
        # Default 8000 para desenvolvimento
        reload=True,
        # Auto-reload quando código muda
        # Apenas para desenvolvimento
        log_level="info"
        # Nível de log para debugging
    )
