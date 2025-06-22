# Agentes de IA - FIA

Plataforma avançada com **três agentes especializados** em pesquisa, análise e Retrieval-Augmented Generation (RAG), desenvolvida para demonstrar diferentes abordagens de IA aplicada.

## 🤖 Agentes Disponíveis

### 1. **Agente MCP** 
- **Especialidade**: Integração dinâmica com ferramentas externas
- **Tecnologia**: Model Context Protocol (MCP) + Firecrawl
- **Funcionalidades**:
  - Scraping em tempo real
  - Integração conversacional
  - Acesso dinâmico a APIs externas

### 2. **Agente Workflow**
- **Especialidade**: Pesquisa estruturada e análise comparativa
- **Tecnologia**: LangGraph + workflows estruturados
- **Funcionalidades**:
  - Fluxo de pesquisa em 3 etapas (extração → pesquisa → análise)
  - Análise comparativa de produtos/serviços
  - Recomendações técnicas objetivas

### 3. **Agente RAG** ⭐ *NOVO*
- **Especialidade**: Retrieval-Augmented Generation
- **Tecnologia**: Pinecone + OpenAI Embeddings
- **Funcionalidades**:
  - Pesquisa semântica em base de conhecimento
  - Citação de fontes utilizadas
  - Scoring de confiança das respostas
  - Gestão dinâmica da base de conhecimento

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+ (para MCP Agent)
- Contas nos serviços:
  - [OpenAI](https://platform.openai.com/) (obrigatório)
  - [Firecrawl](https://firecrawl.dev/) (MCP e Workflow)
  - [Pinecone](https://www.pinecone.io/) (RAG Agent)

### 1. Clone do Repositório
```bash
git clone https://github.com/sergiogaiotto/FIA_AgentesIA
cd FIA_AgentesIA
```

### 2. Ambiente Virtual (Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalação de Dependências

#### Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Node.js (para MCP Agent)
```bash
npm install -g firecrawl-mcp
```

### 4. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# APIs Obrigatórias
OPENAI_API_KEY=sk-your-openai-key-here

# APIs Opcionais (por agente)
FIRECRAWL_API_KEY=fc-your-firecrawl-key-here  # MCP + Workflow
PINECONE_API_KEY=your-pinecone-key-here       # RAG Agent

# Configuração do Servidor
PORT=8000
```

## 🎯 Como Usar

### Execução Local
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:8000`

### Interface Web

1. **Seleção de Agente**: Escolha um dos três agentes disponíveis
2. **Chat Interativo**: Faça perguntas naturalmente
3. **Recursos Especiais**:
   - **RAG Agent**: Painel de gestão da base de conhecimento
   - **Todas**: Indicadores visuais de progresso
   - **RAG**: Fontes citadas e score de confiança

## 🧠 Usando o Agente RAG

### Gestão da Base de Conhecimento

O Agente RAG permite gerenciar dinamicamente sua base de conhecimento:

#### Adicionar via URL
```python
# Exemplo programático
await rag_agent.add_knowledge_from_url("https://docs.python.org/3/tutorial/")
```

#### Adicionar Texto Direto
```python
# Exemplo programático  
await rag_agent.add_knowledge_from_text(
    text="Python é uma linguagem de programação...",
    source_id="python-basics"
)
```

#### Via Interface Web
1. Selecione "Agente RAG"
2. Clique em "Gerenciar Base"
3. Use os formulários para adicionar:
   - URLs de documentação
   - Textos diretos
   - Fontes sugeridas

### Exemplos de Consultas RAG

```
"Como funciona list comprehension em Python?"
"Qual a diferença entre async e await?"
"Melhores práticas para tratamento de exceções"
```

## 📊 Comparação dos Agentes

| Recurso | MCP | Workflow | RAG |
|---------|-----|----------|-----|
| **Tempo Real** | ✅ | ✅ | ❌ |
| **Memória Persistente** | ❌ | ❌ | ✅ |
| **Fontes Citadas** | ❌ | ✅ | ✅ |
| **Análise Estruturada** | ❌ | ✅ | ❌ |
| **Pesquisa Semântica** | ❌ | ❌ | ✅ |
| **Base Customizável** | ❌ | ❌ | ✅ |

## 🛠️ Estrutura do Projeto

```
FIA_AgentesIA/
├── agents/
│   ├── __init__.py          # Exports dos agentes
│   ├── mcp_agent.py         # Agente MCP
│   ├── workflow_agent.py    # Agente Workflow  
│   └── rag_agent.py         # Agente RAG ⭐
├── pages/
│   └── index.html           # Interface web atualizada
├── static/
│   ├── style.css           # Estilos
│   └── script.js           # JavaScript
├── app.py                  # FastAPI server
├── requirements.txt        # Dependências Python
├── render.yaml            # Configuração deploy
└── README.md              # Este arquivo
```

## 🌐 Deploy no Render

### Configuração Automática

1. **Fork** este repositório
2. Conecte ao [Render](https://render.com)
3. Configure as variáveis de ambiente:
   ```
   OPENAI_API_KEY=sk-...
   FIRECRAWL_API_KEY=fc-...
   PINECONE_API_KEY=...
   ```
4. Deploy automático via `render.yaml`

### Variáveis de Ambiente no Render

```bash
# Obrigatórias
OPENAI_API_KEY=sk-your-openai-key

# Opcionais (habilitam agentes específicos)
FIRECRAWL_API_KEY=fc-your-firecrawl-key  
PINECONE_API_KEY=your-pinecone-key
```

## 🔧 APIs Disponíveis

### Endpoints Principais
- `POST /chat` - Chat com agentes
- `POST /chat/stream` - Streaming de respostas
- `GET /agents/info` - Informações dos agentes
- `GET /health` - Health check

### Endpoints RAG Específicos
- `POST /rag/knowledge` - Adicionar conhecimento
- `GET /rag/stats` - Estatísticas da base
- `GET /rag/suggest-sources/{domain}` - Sugerir fontes

### Exemplo de Uso da API

```python
import requests

# Chat com RAG Agent
response = requests.post("http://localhost:8000/chat", json={
    "message": "Como funciona machine learning?",
    "agent_type": "rag"
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Confiança: {result['confidence']}")
print(f"Fontes: {len(result['sources'])}")
```

## 📈 Monitoramento e Estatísticas

### Métricas do RAG Agent
- Total de documentos indexados
- Status do índice Pinecone
- Distribuição de scores de confiança
- Fontes mais utilizadas

### Health Checks
```bash
# Verificar status geral
curl http://localhost:8000/health

# Estatísticas RAG
curl http://localhost:8000/rag/stats
```

## 🎓 Casos de Uso

### Agente MCP
- Pesquisa de produtos em tempo real
- Extração de dados de sites específicos
- Análise conversacional de conteúdo web

### Agente Workflow  
- Comparação estruturada de ferramentas
- Análise de mercado sistematizada
- Recomendações técnicas baseadas em critérios

### Agente RAG
- Suporte técnico com base de conhecimento
- Q&A sobre documentação interna
- Pesquisa semântica em artigos/manuais

## 🚨 Troubleshooting

### Problemas Comuns

#### RAG Agent não inicializa
```bash
# Verificar chave Pinecone
echo $PINECONE_API_KEY

# Verificar conectividade
curl -H "Api-Key: $PINECONE_API_KEY" \
     https://api.pinecone.io/indexes
```

#### MCP Agent falha
```bash
# Verificar instalação Node.js
npm list -g firecrawl-mcp

# Reinstalar se necessário
npm install -g firecrawl-mcp
```

#### Workflow Agent sem resultados
- Verificar chave Firecrawl válida
- Confirmar conectividade de rede
- Testar com queries mais específicas

## 📝 Licença

MIT License - veja LICENSE para detalhes.

## 👨‍🏫 Créditos

**Desenvolvido por**: FIA.LabData - Prof. Sergio Gaiotto

**Instituição**: Fundação Instituto de Administração (FIA)

**Propósito**: Demonstração acadêmica de diferentes arquiteturas de agentes IA

---

## 🔄 Atualizações Recentes

### v1.1.0 - Agente RAG
- ✅ Novo Agente RAG com Pinecone
- ✅ Interface de gestão de conhecimento
- ✅ Citação de fontes e scoring
- ✅ APIs específicas para RAG
- ✅ Documentação atualizada

### v1.0.0 - Versão Inicial
- ✅ Agente MCP com Model Context Protocol
- ✅ Agente Workflow com LangGraph
- ✅ Interface web responsiva
- ✅ Deploy automatizado no Render

---

**🚀 Experimente os três agentes e descubra diferentes abordagens para IA aplicada!**
