# Agentes de IA - FIA, Peof Sergio Gaiotto

Plataforma avançada com **cinco agentes especializados** em pesquisa, análise, RAG, integrações externas e geração de diagramas, desenvolvida para demonstrar diferentes abordagens de IA aplicada.

![Agentes de IA](https://img.shields.io/badge/Agentes-5-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.4-green)
![Python](https://img.shields.io/badge/Python-3.11+-brightgreen)
![Version](https://img.shields.io/badge/Version-1.3.0-orange)

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

### 3. **Agente RAG**
- **Especialidade**: Retrieval-Augmented Generation
- **Tecnologia**: Pinecone + OpenAI Embeddings
- **Funcionalidades**:
  - Pesquisa semântica em base de conhecimento
  - Citação de fontes utilizadas
  - Scoring de confiança das respostas
  - Gestão dinâmica da base de conhecimento

### 4. **Agente Externo**
- **Especialidade**: Integração com APIs externas
- **Tecnologia**: aiohttp + Flowise API
- **Funcionalidades**:
  - Comunicação com APIs externas (Flowise)
  - Manutenção de contexto conversacional
  - Processamento especializado via serviços externos
  - Monitoramento de conectividade

### 5. **Tool Mermaid Agent**
- **Especialidade**: Geração de diagramas Mermaid
- **Tecnologia**: OpenAI + Mermaid.js integration
- **Funcionalidades**:
  - Criação de diagramas de sequência, fluxogramas, diagramas de classe
  - Gráficos de Gantt e diagramas ER
  - Explicações detalhadas dos diagramas
  - Sugestões de melhorias
  - Histórico de diagramas gerados

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+ (para MCP Agent)
- Contas nos serviços:
  - [OpenAI](https://platform.openai.com/) (obrigatório)
  - [Firecrawl](https://firecrawl.dev/) (MCP e Workflow)
  - [Pinecone](https://www.pinecone.io/) (RAG Agent)
  - API Flowise (Agente Externo - opcional)

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
ENVIRONMENT=development
```

**Nota**: O Agente Externo e Tool Mermaid não requerem configurações específicas de chaves de API além da OpenAI.

## 🎯 Como Usar

### Execução Local
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:8000`

### Interface Web

1. **Seleção de Agente**: Escolha um dos cinco agentes disponíveis
2. **Chat Interativo**: Faça perguntas naturalmente
3. **Recursos Especiais**:
   - **RAG Agent**: Painel de gestão da base de conhecimento
   - **Agente Externo**: Painel de status e configuração da API
   - **Tool Mermaid**: Painel de tipos de diagrama e histórico
   - **Todas**: Indicadores visuais de progresso

## 🎨 Usando o Tool Mermaid Agent

### Funcionalidades Principais

O Tool Mermaid Agent permite criar diagramas profissionais usando linguagem natural:

#### Tipos de Diagrama Suportados
```
"Crie um diagrama de sequência para login de usuário"
"Fluxograma para processo de aprovação"
"Diagrama de classes para sistema de biblioteca"
"Gráfico de Gantt para projeto de 3 meses"
"Diagrama ER para banco de dados de e-commerce"
```

#### Interface Especializada
1. Selecione "Tool Mermaid Agent"
2. Clique em "Tipos de Diagrama"
3. Escolha o tipo desejado
4. Descreva o diagrama em linguagem natural
5. Visualize o código Mermaid gerado

### Recursos Avançados
- **Explicações Detalhadas**: Cada diagrama vem com explicação completa
- **Sugestões de Melhoria**: Recomendações para otimizar o diagrama
- **Histórico Persistente**: Todos os diagramas são salvos na sessão
- **Exemplos Prontos**: Templates para começar rapidamente

### Integração com Ferramentas
O código Mermaid gerado pode ser usado em:
- GitHub/GitLab (renderização nativa)
- Notion, Obsidian, Typora
- Mermaid.live para visualização online
- Extensões VSCode/Vim

## 🌐 Usando o Agente Externo

### Funcionalidades Principais

O Agente Externo permite integração com APIs externas, especificamente otimizado para Flowise:

#### Processamento de Prompts
```
"Explique conceitos de machine learning de forma simples"
"Como funciona deep learning em visão computacional?"
"Quais são as melhores práticas para prompt engineering?"
```

#### Monitoramento via Interface Web
1. Selecione "Agente Externo"
2. Clique em "Status & Config"
3. Use os controles para:
   - Verificar status da API
   - Resetar contexto conversacional
   - Testar conectividade

### Configuração da API Flowise

O agente está pré-configurado para usar:
- **Endpoint**: `https://gaiotto-flowiseai.hf.space/api/v1/prediction/126dd353-3c69-4304-9542-1263d07c711a`
- **Timeout**: 30 segundos
- **Contexto**: Mantém histórico de 10 mensagens

Para usar uma API Flowise personalizada, modifique o endpoint no código:

```python
# Em agents/externo_agent.py
externo_agent = ExternoAgent(api_url="sua-api-flowise-aqui")
```

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

| Recurso | MCP | Workflow | RAG | Externo | Mermaid |
|---------|-----|----------|-----|---------|---------|
| **Tempo Real** | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Memória Persistente** | ❌ | ❌ | ✅ | ✅* | ✅** |
| **Fontes Citadas** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Análise Estruturada** | ❌ | ✅ | ❌ | ❌ | ✅ |
| **Pesquisa Semântica** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Base Customizável** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **APIs Externas** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Contexto Conversacional** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Geração Visual** | ❌ | ❌ | ❌ | ❌ | ✅ |

*\* Contexto mantido durante a sessão*
*\** Histórico de diagramas gerados*

## 🛠️ Estrutura do Projeto

```
FIA_AgentesIA/
├── agents/
│   ├── __init__.py          # Exports dos agentes
│   ├── mcp_agent.py         # Agente MCP
│   ├── workflow_agent.py    # Agente Workflow  
│   ├── rag_agent.py         # Agente RAG
│   ├── externo_agent.py     # Agente Externo
│   └── tool_mermaid_agent.py # Tool Mermaid Agent
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

# Agentes Externo e Mermaid funcionam apenas com OpenAI
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

### Endpoints Agente Externo
- `GET /externo/status` - Status da API Flowise
- `POST /externo/reset` - Reset contexto conversacional

### Endpoints Tool Mermaid Específicos
- `GET /mermaid/diagram-types` - Tipos de diagrama suportados
- `GET /mermaid/history` - Histórico de diagramas
- `POST /mermaid/reset` - Reset histórico

### Exemplo de Uso da API

```python
import requests

# Chat com Tool Mermaid Agent
response = requests.post("http://localhost:8000/chat", json={
    "message": "Crie um diagrama de sequência para autenticação de usuário",
    "agent_type": "mermaid",
    "diagram_type": "sequence"
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Status: {result['status']}")

# Verificar tipos de diagrama suportados
diagram_types = requests.get("http://localhost:8000/mermaid/diagram-types")
print(f"Tipos disponíveis: {diagram_types.json()}")

# Chat com Agente Externo
response = requests.post("http://localhost:8000/chat", json={
    "message": "Explique machine learning de forma simples",
    "agent_type": "externo"
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Status: {result['status']}")

# Verificar status do Agente Externo
status = requests.get("http://localhost:8000/externo/status")
print(f"Status API: {status.json()}")
```

## 📈 Monitoramento e Estatísticas

### Métricas do RAG Agent
- Total de documentos indexados
- Status do índice Pinecone
- Distribuição de scores de confiança
- Fontes mais utilizadas

### Métricas do Agente Externo
- Status de conectividade com Flowise
- Quantidade de mensagens na sessão
- Tempo de resposta da API
- Histórico conversacional

### Métricas do Tool Mermaid Agent
- Diagramas gerados na sessão
- Tipos de diagrama mais utilizados
- Histórico de criação
- Complexidade dos diagramas

### Health Checks
```bash
# Verificar status geral
curl http://localhost:8000/health

# Estatísticas RAG
curl http://localhost:8000/rag/stats

# Status Agente Externo
curl http://localhost:8000/externo/status

# Tipos de diagrama Mermaid
curl http://localhost:8000/mermaid/diagram-types

# Histórico de diagramas
curl http://localhost:8000/mermaid/history
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

### Tool Mermaid Agent
- Documentação técnica com diagramas
- Modelagem de processos de negócio
- Arquitetura de software visual
- Planejamento de projetos com Gantt
- Mapeamento de jornadas do usuário

### Agente Externo
- Processamento especializado via Flowise
- Integração com pipelines de IA externos
- Análise avançada de linguagem natural
- Prototipagem rápida com APIs externas

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

#### Tool Mermaid Agent sem resposta
- Verificar chave OpenAI válida
- Confirmar que agente foi inicializado
- Testar com prompts simples:
  ```bash
  curl -X POST http://localhost:8000/chat \
       -H "Content-Type: application/json" \
       -d '{"message": "Crie um diagrama simples", "agent_type": "mermaid", "diagram_type": "flowchart"}'
  ```
- Verificar tipos de diagrama suportados
- Usar painel de controle na interface web

#### Agente Externo não responde
- Verificar conectividade com internet
- Testar endpoint Flowise manualmente:
  ```bash
  curl -X POST https://gaiotto-flowiseai.hf.space/api/v1/prediction/126dd353-3c69-4304-9542-1263d07c711a \
       -H "Content-Type: application/json" \
       -d '{"question": "test"}'
  ```
- Usar painel de status na interface web

### Problemas de Performance

#### Aplicação lenta
- Verificar logs do console
- Monitorar uso de CPU/RAM
- Verificar conectividade com APIs externas

#### Respostas demoradas
- Verificar timeouts nas APIs
- Considerar usar endpoints de streaming
- Verificar quality of service das APIs

## 📝 Licença

MIT License - veja LICENSE para detalhes.

## 👨‍🏫 Créditos

**Desenvolvido por**: FIA.LabData - Prof. Sergio Gaiotto

**Instituição**: Fundação Instituto de Administração (FIA)

**Propósito**: Demonstração acadêmica de diferentes arquiteturas de agentes IA

## 🔄 Atualizações Recentes

### v1.3.0 - Tool Mermaid Agent
- ✅ Novo Tool Mermaid Agent para geração de diagramas
- ✅ Suporte a múltiplos tipos de diagrama (sequence, flowchart, class, etc.)
- ✅ Interface especializada com seletor de tipos
- ✅ Histórico de diagramas gerados
- ✅ Exemplos de prompts prontos
- ✅ Explicações detalhadas e sugestões
- ✅ Integração com ferramentas Mermaid existentes

### v1.2.0 - Agente Externo
- ✅ Novo Agente Externo para APIs externas
- ✅ Integração com Flowise API
- ✅ Painel de status e configuração
- ✅ Contexto conversacional mantido
- ✅ Monitoramento de conectividade
- ✅ Interface atualizada com 4 agentes

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

## 🆘 Suporte

### Documentação Adicional
- **Exemplos Mermaid**: `TOOL_MERMAID_EXAMPLES.md`
- **Configuração Ambiente**: `.env.example`
- **Deploy**: `render.yaml`

### Comunidade
- **Issues**: [GitHub Issues](https://github.com/sergiogaiotto/FIA_AgentesIA/issues)
- **Discussões**: [GitHub Discussions](https://github.com/sergiogaiotto/FIA_AgentesIA/discussions)
- **Email**: sergio.gaiotto@fia.com.br

### Recursos Externos
- **OpenAI Documentation**: https://docs.openai.com/
- **Firecrawl Documentation**: https://docs.firecrawl.dev/
- **Pinecone Documentation**: https://docs.pinecone.io/
- **Mermaid Documentation**: https://mermaid.js.org/

---

**🚀 Experimente os cinco agentes e descubra diferentes abordagens para IA aplicada!**

---

## ⭐ Features em Destaque

- 🤖 **5 Agentes Especializados** - Cada um com propósito específico
- 🎨 **Interface Moderna** - Design responsivo e intuitivo
- 🔧 **APIs RESTful** - Integração fácil com outros sistemas
- 📊 **Monitoramento** - Health checks e métricas detalhadas
- 🚀 **Deploy Automático** - Configuração zero no Render
- 📚 **Documentação Completa** - Exemplos e tutoriais detalhados
- 🔒 **Configuração Segura** - Chaves API isoladas por ambiente
- 🌐 **Multi-plataforma** - Funciona em Windows, Mac e Linux

**💡 Perfeito para aprender, experimentar e aplicar diferentes técnicas de IA!**