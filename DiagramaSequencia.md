sequenceDiagram
    participant U as Usuário
    participant W as Interface Web
    participant API as FastAPI Server
    participant MCP as MCP Agent
    participant WF as Workflow Agent
    participant RAG as RAG Agent
    participant EXT as Agente Externo
    participant MM as Tool Mermaid Agent

    participant FC as Firecrawl API
    participant PC as Pinecone
    participant FL as Flowise API
    participant GPT as OpenAI/GPT-4

    Note over U,GPT: Fluxo Principal da Aplicação

    U->>W: Acessa aplicação (localhost:8000)
    W->>API: GET / (carrega interface)
    API-->>W: Retorna página principal
    W-->>U: Exibe interface com 5 agentes

    Note over U,GPT: Seleção e Configuração de Agente

    U->>W: Seleciona agente específico
    W->>API: GET /agents/info
    API-->>W: Retorna informações dos agentes
    W-->>U: Atualiza interface com painel específico

    Note over U,GPT: Fluxo de Chat - MCP Agent (Scraping em tempo real)

    U->>W: Envia pergunta para MCP Agent
    W->>API: POST /chat {agent: "mcp", message: "..."}
    API->>MCP: Processa solicitação
    MCP->>FC: Solicita scraping via Firecrawl
    FC-->>MCP: Retorna dados extraídos
    MCP->>GPT: Processa com OpenAI
    GPT-->>MCP: Retorna resposta gerada
    MCP-->>API: Resposta final
    API-->>W: JSON response
    W-->>U: Exibe resposta

    Note over U,GPT: Fluxo de Chat - Workflow Agent (Pesquisa estruturada)

    U->>W: Solicita análise comparativa
    W->>API: POST /chat {agent: "workflow", message: "..."}
    API->>WF: Inicia workflow estruturado
    Note over WF: Fluxo 3 etapas: extração → pesquisa → análise
    WF->>GPT: Etapa 1: Extração de critérios
    GPT-->>WF: Critérios identificados
    WF->>GPT: Etapa 2: Pesquisa estruturada
    GPT-->>WF: Dados coletados
    WF->>GPT: Etapa 3: Análise comparativa
    GPT-->>WF: Recomendações técnicas
    WF-->>API: Resultado estruturado
    API-->>W: JSON response com citações
    W-->>U: Exibe análise com fontes

    Note over U,GPT: Fluxo de Chat - RAG Agent (Base de conhecimento)

    U->>W: Pergunta técnica sobre documentação
    W->>API: POST /chat {agent: "rag", message: "..."}
    API->>RAG: Processa query
    RAG->>PC: Busca semântica no Pinecone
    PC-->>RAG: Retorna chunks relevantes
    RAG->>GPT: Gera resposta com contexto
    GPT-->>RAG: Resposta contextualizada
    RAG-->>API: Resposta com citações e score
    API-->>W: JSON response
    W-->>U: Exibe resposta com fontes

    Note over U,GPT: Gestão de Conhecimento - RAG Agent

    U->>W: Acessa "Gerenciar Base"
    W->>API: GET /rag/stats
    API->>RAG: Consulta estatísticas
    RAG->>PC: Verifica status da base
    PC-->>RAG: Retorna métricas
    RAG-->>API: Estatísticas
    API-->>W: JSON response
    W-->>U: Exibe dashboard

    U->>W: Adiciona nova URL de conhecimento
    W->>API: POST /rag/knowledge {url: "..."}
    API->>RAG: Processa novo conteúdo
    RAG->>GPT: Gera embeddings
    GPT-->>RAG: Vetores de embedding
    RAG->>PC: Armazena no Pinecone
    PC-->>RAG: Confirmação
    RAG-->>API: Sucesso
    API-->>W: Status atualizado
    W-->>U: Confirmação visual

    Note over U,GPT: Fluxo de Chat - Agente Externo (API Flowise)

    U->>W: Pergunta sobre machine learning
    W->>API: POST /chat {agent: "externo", message: "..."}
    API->>EXT: Encaminha para API externa
    EXT->>FL: Requisição para Flowise API
    FL-->>EXT: Resposta especializada
    EXT-->>API: Resposta com contexto mantido
    API-->>W: JSON response
    W-->>U: Exibe resposta especializada

    Note over U,GPT: Monitoramento - Agente Externo

    U->>W: Verifica "Status & Config"
    W->>API: GET /externo/status
    API->>EXT: Testa conectividade
    EXT->>FL: Health check
    FL-->>EXT: Status da API
    EXT-->>API: Status consolidado
    API-->>W: JSON response
    W-->>U: Indicador visual de status

    Note over U,GPT: Fluxo de Chat - Tool Mermaid Agent (Geração de diagramas)

    U->>W: Solicita criação de diagrama
    W->>API: POST /chat {agent: "mermaid", message: "..."}
    API->>MM: Processa solicitação
    MM->>GPT: Gera código Mermaid
    GPT-->>MM: Código Mermaid + explicação
    MM-->>API: Diagrama + metadata
    API-->>W: JSON response
    W-->>U: Renderiza diagrama + explicação

    Note over U,GPT: Histórico - Tool Mermaid Agent

    U->>W: Acessa histórico de diagramas
    W->>API: GET /mermaid/history
    API->>MM: Recupera histórico
    MM-->>API: Lista de diagramas
    API-->>W: JSON response
    W-->>U: Exibe galeria de diagramas



    Note over U,GPT: Health Check e Monitoramento

    W->>API: GET /health (periódico)
    API-->>W: Status geral do sistema
    W-->>U: Indicadores visuais de saúde
