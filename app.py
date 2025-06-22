# app.py - Arquivo Completo Comentado (Atualizado com Tool Mermaid Agent)

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

from typing import Dict, Any, List, Optional
# Type hints para melhor documentação
# Dict, Any: tipos para estruturas de dados flexíveis

import uvicorn
# Servidor ASGI para aplicações Python assíncronas
# Usado para executar FastAPI em produção

# Imports dos agentes adaptados
from agents.mcp_agent import MCPAgent
from agents.workflow_agent import WorkflowAgent
from agents.rag_agent import RAGAgent
from agents.externo_agent import ExternoAgent
from agents.tool_mermaid_agent import ToolMermaidAgent
# Importação dos cinco tipos de agentes desenvolvidos
# Modularização: cada agente em arquivo separado
# ToolMermaidAgent: novo agente para geração de diagramas Mermaid

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Agentes de IA - FIA",
    # Título da API (aparece na documentação)
    description="Plataforma com cinco agentes especializados em pesquisa, análise, RAG, integrações externas e geração de diagramas",
    # Descrição atualizada para incluir agente Mermaid
    version="1.3.0"
    # Versionamento atualizado para nova funcionalidade
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
rag_agent = None
externo_agent = None
tool_mermaid_agent = None
# Variáveis globais para instâncias dos agentes
# None inicial: agentes serão inicializados no startup
# tool_mermaid_agent: nova instância para agente de diagramas

class ChatRequest(BaseModel):
    """Modelo para requisições de chat"""
    message: str
    # Mensagem do usuário (campo obrigatório)
    agent_type: str  # "mcp", "workflow", "rag", "externo" ou "mermaid"
    # Tipo de agente a ser usado (validação manual)
    # Atualizado para incluir "mermaid"
    diagram_type: Optional[str] = "sequence"
    # Tipo de diagrama para agente Mermaid (opcional, padrão sequence)

class ChatResponse(BaseModel):
    """Modelo para respostas de chat"""
    response: str
    # Resposta processada pelo agente
    agent_type: str
    # Tipo de agente que processou
    status: str
    # Status da operação (success/error)
    sources: Optional[List[Dict[str, Any]]] = None
    # Fontes utilizadas (específico para RAG)
    confidence: Optional[float] = None
    # Nível de confiança (específico para RAG)

class RAGKnowledgeRequest(BaseModel):
    """Modelo para adicionar conhecimento ao RAG"""
    url: Optional[str] = None
    # URL para scraping (opcional)
    text: Optional[str] = None
    # Texto direto (opcional)
    source_id: Optional[str] = None
    # ID da fonte (obrigatório para texto)

# Inicialização dos agentes
async def initialize_agents():
    """Inicializa os agentes de forma assíncrona"""
    # Função assíncrona para setup dos agentes
    # Async: permite inicialização não-bloqueante
    
    global mcp_agent, workflow_agent, rag_agent, externo_agent, tool_mermaid_agent
    # Global: modifica variáveis no escopo global
    # Necessário para compartilhar instâncias entre requests
    # tool_mermaid_agent: incluído nas variáveis globais
    
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
        
        # Inicializa agente RAG
        if (os.getenv("PINECONE_API_KEY") and 
            os.getenv("OPENAI_API_KEY")):
            # RAG requer Pinecone + OpenAI
            # Firecrawl é opcional para RAG
            
            rag_agent = RAGAgent()
            await rag_agent.initialize()
            # Async initialization: configura Pinecone
            print("✅ RAG Agent inicializado")
        
        # Inicializa agente Externo (sempre disponível)
        externo_agent = ExternoAgent()
        # Agente Externo não requer chaves de API específicas
        # Usa API pública do Flowise
        print("✅ Agente Externo inicializado")
        
        # Inicializa agente Tool Mermaid (sempre disponível se OpenAI estiver configurado)
        if os.getenv("OPENAI_API_KEY"):
            tool_mermaid_agent = ToolMermaidAgent()
            # Agente Mermaid requer apenas OpenAI para geração
            print("✅ Tool Mermaid Agent inicializado")
            
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
        
        elif chat_request.agent_type == "rag":
            # Roteamento para agente RAG
            
            if not rag_agent:
                return ChatResponse(
                    response="❌ Agente RAG não está disponível. Verifique as configurações do Pinecone.",
                    agent_type="rag",
                    status="error"
                )
            
            rag_response = await rag_agent.query(chat_request.message)
            # query: método específico do RAGAgent
            
            # Processa fontes para resposta
            sources = []
            if rag_response.sources:
                sources = [
                    {
                        "content": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                        # Trunca conteúdo para preview
                        "score": doc.score,
                        "metadata": doc.metadata
                    }
                    for doc in rag_response.sources
                ]
            
            return ChatResponse(
                response=rag_response.answer,
                agent_type="rag",
                status="success",
                sources=sources,
                # Inclui fontes utilizadas
                confidence=rag_response.confidence
                # Inclui nível de confiança
            )
        
        elif chat_request.agent_type == "externo":
            # Roteamento para agente externo
            
            if not externo_agent:
                return ChatResponse(
                    response="❌ Agente Externo não está disponível. Verifique a conectividade.",
                    agent_type="externo",
                    status="error"
                )
            
            response = await externo_agent.process_message(chat_request.message)
            # process_message: método específico do ExternoAgent
            
            return ChatResponse(
                response=response,
                agent_type="externo",
                status="success"
            )
        
        elif chat_request.agent_type == "mermaid":
            # Novo roteamento para agente Tool Mermaid
            
            if not tool_mermaid_agent:
                return ChatResponse(
                    response="❌ Agente Tool Mermaid não está disponível. Verifique a configuração da OpenAI.",
                    agent_type="mermaid",
                    status="error"
                )
            
            # Determina tipo de diagrama
            diagram_type = getattr(chat_request, 'diagram_type', 'sequence')
            
            response = await tool_mermaid_agent.process_message(
                chat_request.message, 
                diagram_type
            )
            # process_message: método específico do ToolMermaidAgent
            
            return ChatResponse(
                response=response,
                agent_type="mermaid",
                status="success"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Tipo de agente inválido")
            # Validação: agent_type deve ser "mcp", "workflow", "rag", "externo" ou "mermaid"
            
    except Exception as e:
        return ChatResponse(
            response=f"❌ Erro interno: {str(e)}",
            agent_type=chat_request.agent_type,
            status="error"
        )
        # Tratamento genérico de exceções
        # Retorna erro estruturado em vez de falhar

# Endpoint para verificar status do agente externo
@app.get("/externo/status")
async def externo_status():
    """Endpoint para verificar status do agente externo"""
    # Endpoint específico para monitoramento do agente externo
    
    if not externo_agent:
        raise HTTPException(status_code=503, detail="Agente Externo não disponível")
    # 503 Service Unavailable: serviço não configurado
    
    try:
        status = await externo_agent.check_service_availability()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar status: {str(e)}")

# Endpoint para resetar conversa do agente externo
@app.post("/externo/reset")
async def externo_reset():
    """Endpoint para resetar conversa do agente externo"""
    # Endpoint para limpar contexto conversacional
    
    if not externo_agent:
        raise HTTPException(status_code=503, detail="Agente Externo não disponível")
    
    try:
        externo_agent.reset_conversation()
        return {"status": "success", "message": "Conversa resetada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao resetar conversa: {str(e)}")

# Endpoint para listar tipos de diagrama suportados
@app.get("/mermaid/diagram-types")
async def get_diagram_types():
    """Endpoint para listar tipos de diagrama Mermaid suportados"""
    # Endpoint específico para consultar capacidades do agente Mermaid
    
    if not tool_mermaid_agent:
        raise HTTPException(status_code=503, detail="Agente Tool Mermaid não disponível")
    
    try:
        diagram_types = tool_mermaid_agent.get_supported_diagrams()
        return {"supported_diagrams": diagram_types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter tipos de diagrama: {str(e)}")

# Endpoint para histórico de diagramas gerados
@app.get("/mermaid/history")
async def get_diagram_history():
    """Endpoint para obter histórico de diagramas gerados"""
    # Endpoint para consultar histórico do agente Mermaid
    
    if not tool_mermaid_agent:
        raise HTTPException(status_code=503, detail="Agente Tool Mermaid não disponível")
    
    try:
        history = tool_mermaid_agent.get_diagram_history()
        return {"diagram_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico: {str(e)}")

# Endpoint para resetar histórico de diagramas
@app.post("/mermaid/reset")
async def reset_mermaid_history():
    """Endpoint para resetar histórico de diagramas"""
    # Endpoint para limpar histórico do agente Mermaid
    
    if not tool_mermaid_agent:
        raise HTTPException(status_code=503, detail="Agente Tool Mermaid não disponível")
    
    try:
        tool_mermaid_agent.reset_conversation()
        return {"status": "success", "message": "Histórico de diagramas resetado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao resetar histórico: {str(e)}")

# Endpoint para adicionar conhecimento ao RAG
@app.post("/rag/knowledge")
async def add_knowledge(request: RAGKnowledgeRequest):
    """Endpoint para adicionar conhecimento à base RAG"""
    # Endpoint específico para gestão da base de conhecimento
    # Permite expansão dinâmica do conhecimento RAG
    
    if not rag_agent:
        raise HTTPException(status_code=503, detail="Agente RAG não disponível")
    # 503 Service Unavailable: serviço não configurado
    
    try:
        if request.url:
            # Adiciona conhecimento via URL
            success = await rag_agent.add_knowledge_from_url(request.url)
            
            if success:
                return {"status": "success", "message": f"Conhecimento adicionado da URL: {request.url}"}
            else:
                return {"status": "error", "message": "Falha ao adicionar conhecimento da URL"}
        
        elif request.text and request.source_id:
            # Adiciona conhecimento via texto direto
            success = await rag_agent.add_knowledge_from_text(request.text, request.source_id)
            
            if success:
                return {"status": "success", "message": f"Conhecimento adicionado do texto: {request.source_id}"}
            else:
                return {"status": "error", "message": "Falha ao adicionar conhecimento do texto"}
        
        else:
            raise HTTPException(status_code=400, detail="URL ou (texto + source_id) são obrigatórios")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar conhecimento: {str(e)}")

# Endpoint para estatísticas do RAG
@app.get("/rag/stats")
async def rag_stats():
    """Endpoint para estatísticas da base de conhecimento RAG"""
    # Endpoint de monitoramento específico para RAG
    
    if not rag_agent:
        raise HTTPException(status_code=503, detail="Agente RAG não disponível")
    
    try:
        stats = await rag_agent.get_knowledge_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

# Endpoint para sugerir fontes de conhecimento
@app.get("/rag/suggest-sources/{domain}")
async def suggest_sources(domain: str):
    """Endpoint para sugerir fontes de conhecimento para um domínio"""
    # Feature: sugestão automática de fontes relevantes
    
    if not rag_agent:
        raise HTTPException(status_code=503, detail="Agente RAG não disponível")
    
    try:
        suggestions = await rag_agent.suggest_knowledge_sources(domain)
        return {"domain": domain, "suggested_sources": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao sugerir fontes: {str(e)}")

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
            
            elif chat_request.agent_type == "rag" and rag_agent:
                # Streaming para RAG Agent
                
                yield f"data: {json.dumps({'status': 'processing', 'message': '🧠 Buscando na base de conhecimento...'})}\n\n"
                
                result = await rag_agent.query(chat_request.message)
                
                yield f"data: {json.dumps({'status': 'complete', 'message': result.answer})}\n\n"
            
            elif chat_request.agent_type == "externo" and externo_agent:
                # Streaming para Agente Externo
                
                yield f"data: {json.dumps({'status': 'processing', 'message': '🌐 Conectando com Flowise...'})}\n\n"
                
                result = await externo_agent.process_message(chat_request.message)
                
                yield f"data: {json.dumps({'status': 'complete', 'message': result})}\n\n"
            
            elif chat_request.agent_type == "mermaid" and tool_mermaid_agent:
                # Streaming para Tool Mermaid Agent
                
                yield f"data: {json.dumps({'status': 'processing', 'message': '🎨 Gerando diagrama Mermaid...'})}\n\n"
                
                diagram_type = getattr(chat_request, 'diagram_type', 'sequence')
                result = await tool_mermaid_agent.process_message(chat_request.message, diagram_type)
                
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
        "rag_agent": rag_agent is not None,
        # Verifica se agente RAG foi inicializado
        "externo_agent": externo_agent is not None,
        # Verifica se agente Externo foi inicializado
        "tool_mermaid_agent": tool_mermaid_agent is not None,
        # Verifica se agente Tool Mermaid foi inicializado
        "environment": {
            "firecrawl_key": bool(os.getenv("FIRECRAWL_API_KEY")),
            # Verifica presença da chave (sem expor valor)
            "openai_key": bool(os.getenv("OPENAI_API_KEY")),
            # Verifica presença da chave OpenAI
            "pinecone_key": bool(os.getenv("PINECONE_API_KEY"))
            # Verifica presença da chave Pinecone
            # Agente Mermaid requer apenas OpenAI
        }
    }
    
    return {
        "status": "healthy",
        # Status geral da aplicação
        "agents": agent_status,
        # Detalhes dos agentes
        "version": "1.3.0"
        # Versão atualizada para tracking de deploys
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
                "name": "Agente MCP Firecrawl",
                "description": "Agente inteligente com integração MCP e Firecrawl para scraping dinâmico",
                "features": ["Scraping em tempo real", "Integração MCP", "Análise conversacional"],
                "available": mcp_agent is not None
                # Status de disponibilidade em tempo real
            },
            {
                "type": "workflow", 
                "name": "Agente Workflow Firecrawl",
                "description": "Agente especializado em pesquisa estruturada e análise comparativa",
                "features": ["Workflow estruturado", "Análise comparativa", "Recomendações técnicas"],
                "available": workflow_agent is not None
            },
            {
                "type": "rag",
                "name": "Agente RAG",
                "description": "Agente de Retrieval-Augmented Generation com Pinecone para pesquisa semântica",
                "features": ["Pesquisa semântica", "Base de conhecimento", "Citação de fontes", "Scoring de confiança"],
                "available": rag_agent is not None
            },
            {
                "type": "externo",
                "name": "Agente Externo",
                "description": "Agente para integração com APIs externas como Flowise para processamento especializado",
                "features": ["Integração Flowise", "APIs externas", "Contexto conversacional", "Formatação automática"],
                "available": externo_agent is not None
            },
            {
                "type": "mermaid",
                "name": "Tool Mermaid Agent",
                "description": "Agente especializado em geração de diagramas Mermaid para visualização de processos e estruturas",
                "features": ["Diagramas de sequência", "Fluxogramas", "Diagramas de classe", "Gráficos de Gantt", "Diagramas ER"],
                "available": tool_mermaid_agent is not None
                # Agente Mermaid na lista de informações
            }
        ]
    }
    # Array de objetos com metadados de cada agente
    # Atualizado para incluir Tool Mermaid Agent

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