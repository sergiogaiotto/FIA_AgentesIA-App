# Agente_IA

Agente_IA é um agente inteligente que utiliza LLMs (Modelos de Linguagem de Grande Escala) e integração com ferramentas externas via MCP (model context protocol) para realizar pesquisas, scraping e extração de dados de sites, fornecendo respostas rápidas e precisas para consultas sobre produtos, ferramentas, soluções e serviços.

## Funcionalidades

- Pesquisa automatizada de produtos, ferramentas, soluções e serviços a partir de uma consulta do usuário.
- Extração de informações relevantes de sites usando Firecrawl via MCP.
- Análise e comparação de alternativas disponíveis no mercado.
- Recomendações técnicas e objetivas para consumidores e desenvolvedores.

## Instalação

1. Clone este repositório:
    ```sh
    git clone https://github.com/sergiogaiotto/FIA_AgentesIA
    cd Agente_IA
    ```

2. (Opcional) Crie um ambiente virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente:

    - Preencha o arquivo `.env` com suas chaves de API do Firecrawl e OpenAI.

## Uso

Execute o agente pelo terminal:

    ```sh
    - python main.py

# Agente_IA_Workflow

Agente_IA_Workflow é um agente de pesquisa automatizado que utiliza LLMs (Modelos de Linguagem), scraping inteligente e prompts otimizados para comparar produtos, ferramentas, soluções e serviços, fornecendo recomendações técnicas rápidas e concisas para consumidores e desenvolvedores.

## Funcionalidades

- Pesquisa automatizada de produtos/ferramentas/soluções/serviços a partir de uma consulta do usuário.
- Extração de informações relevantes de sites e artigos usando Firecrawl.
- Análise detalhada de empresas/ferramentas, incluindo modelo de preços, open source, stack tecnológica, APIs, integrações e mais.
- Recomendações técnicas objetivas e práticas baseadas nos dados coletados.

## Instalação

1. Clone este repositório:
    ```sh
    git clone https://github.com/sergiogaiotto/FIA_AgentesIA
    cd Agente_IA_Workflow
2. Crie um ambiente virtual (opcional, mas recomendado):
    ```sh
    python -m venv venv
    source venv/bin/activate
3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
4. Configure as variáveis de ambiente:

Preencha o .env com as chaves necessárias (ou edite o arquivo .env existente).
Insira suas chaves de API do Firecrawl e OpenAI.
Uso
Execute o agente de pesquisa pelo terminal:

O agente irá buscar, analisar e recomendar as melhores opções disponíveis.

Para sair, digite fui! ou sair.

## Estrutura do Projeto

- main.py: Ponto de entrada do agente de pesquisa.
- src/workflow.py: Lógica principal do fluxo de pesquisa e análise.
- src/firecrawl.py: Integração com a API Firecrawl para busca e scraping.
- src/models.py: Modelos de dados (Pydantic) para empresas, análises e estado da pesquisa.
- src/prompts.py: Prompts utilizados para extração e análise via LLM.

Requisitos
- Python 3.9+
- Chave de API do Firecrawl
- Chave de API do OpenAI

Licença
- MIT

Desenvolvido por FIA.LabData - Prof Sergio Gaiotto.
