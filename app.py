from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import json
import asyncio
import os
from typing import Dict, Any
import uvicorn

# Imports dos agentes adaptados
from agents.mcp_agent import MCPAgent
from agents.workflow_agent import WorkflowAgent

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Agentes de IA - FIA",
    description="Plataforma com dois agentes especializados em pesquisa e análise",
    version="1.0.0"
)

# Configuração de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

# Instâncias dos agentes (inicializadas globalmente)
mcp_agent = None
workflow_agent = None

class ChatRequest(BaseModel):
    message: str
    agent_type: str  # "mcp" ou "workflow"

class ChatResponse(BaseModel):
    response: str
    agent_type: str
    status: str

# Inicialização dos agentes
async def initialize_agents():
    """Inicializa os agentes de forma assíncrona"""
    global mcp_agent, workflow_agent
    
    try:
        # Inicializa agente MCP (se chaves estão disponíveis)
        if os.getenv("FIRECRAWL_API_KEY") and os.getenv("OPENAI_API_KEY"):
            mcp_agent = MCPAgent()
            print("✅ MCP Agent inicializado")
        
        # Inicializa agente Workflow
        if os.getenv("FIRECRAWL_API_KEY") and os.getenv("OPENAI_API_KEY"):
            workflow_agent = WorkflowAgent()
            print("✅ Workflow Agent inicializado")
            
    except Exception as e:
        print(f"❌ Erro ao inicializar agentes: {e}")

# Event handler para startup
@app.on_event("startup")
async def startup_event():
    await initialize_agents()

# Rota principal - página de chat
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para chat com agentes
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """Endpoint principal para interação com agentes"""
    
    if not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")
    
    try:
        if chat_request.agent_type == "mcp":
            if not mcp_agent:
                return ChatResponse(
                    response="❌ Agente MCP não está disponível. Verifique as configurações.",
                    agent_type="mcp",
                    status="error"
                )
            
            response = await mcp_agent.process_message(chat_request.message)
            return ChatResponse(
                response=response,
                agent_type="mcp", 
                status="success"
            )
            
        elif chat_request.agent_type == "workflow":
            if not workflow_agent:
                return ChatResponse(
                    response="❌ Agente Workflow não está disponível. Verifique as configurações.",
                    agent_type="workflow",
                    status="error"
                )
            
            response = await workflow_agent.process_query(chat_request.message)
            return ChatResponse(
                response=response,
                agent_type="workflow",
                status="success"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Tipo de agente inválido")
            
    except Exception as e:
        return ChatResponse(
            response=f"❌ Erro interno: {str(e)}",
            agent_type=chat_request.agent_type,
            status="error"
        )

# Endpoint para streaming de respostas (opcional para UX melhor)
@app.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest):
    """Endpoint para streaming de respostas em tempo real"""
    
    async def generate_response():
        try:
            if chat_request.agent_type == "workflow" and workflow_agent:
                # Simula streaming do workflow
                yield f"data: {json.dumps({'status': 'processing', 'message': '🔍 Iniciando pesquisa...'})}\n\n"
                
                result = await workflow_agent.process_query(chat_request.message)
                
                yield f"data: {json.dumps({'status': 'complete', 'message': result})}\n\n"
            
            elif chat_request.agent_type == "mcp" and mcp_agent:
                yield f"data: {json.dumps({'status': 'processing', 'message': '🤖 Processando com MCP...'})}\n\n"
                
                result = await mcp_agent.process_message(chat_request.message)
                
                yield f"data: {json.dumps({'status': 'complete', 'message': result})}\n\n"
            
            else:
                yield f"data: {json.dumps({'status': 'error', 'message': 'Agente não disponível'})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': f'Erro: {str(e)}'})}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

# Endpoint de health check para Render
@app.get("/health")
async def health_check():
    """Health check para monitoramento do Render"""
    agent_status = {
        "mcp_agent": mcp_agent is not None,
        "workflow_agent": workflow_agent is not None,
        "environment": {
            "firecrawl_key": bool(os.getenv("FIRECRAWL_API_KEY")),
            "openai_key": bool(os.getenv("OPENAI_API_KEY"))
        }
    }
    
    return {
        "status": "healthy",
        "agents": agent_status,
        "version": "1.0.0"
    }

# Endpoint para informações dos agentes
@app.get("/agents/info")
async def agents_info():
    """Retorna informações sobre os agentes disponíveis"""
    return {
        "agents": [
            {
                "type": "mcp",
                "name": "Agente MCP",
                "description": "Agente inteligente com integração MCP e Firecrawl para scraping dinâmico",
                "features": ["Scraping em tempo real", "Integração MCP", "Análise conversacional"],
                "available": mcp_agent is not None
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

# Configuração para desenvolvimento local
if __name__ == "__main__":
    # Carrega variáveis de ambiente para desenvolvimento
    from dotenv import load_dotenv
    load_dotenv()
    
    # Roda servidor com reload para desenvolvimento
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )
