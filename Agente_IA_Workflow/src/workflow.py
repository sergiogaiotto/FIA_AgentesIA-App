# Imports para type hints - fundamentais para code quality e IDE support
from typing import Dict, Any
# Dict[str, Any]: Especifica dicionário com chaves string e valores de qualquer tipo
# Any: Tipo genérico quando tipo específico não pode ser determinado estaticamente

# Core do LangGraph para criação de workflows baseados em grafos
from langgraph.graph import StateGraph, END
# StateGraph: Implementa máquina de estados finita para workflows complexos
# END: Constante que indica término do workflow (estado final)

# Wrapper LangChain para modelos OpenAI
from langchain_openai import ChatOpenAI
# ChatOpenAI: Abstração padronizada para modelos de chat da OpenAI

# Classes base para mensagens no formato LangChain
from langchain_core.messages import HumanMessage, SystemMessage
# HumanMessage: Representa input do usuário no conversation flow
# SystemMessage: Define comportamento e contexto do assistente

# Imports locais - modelos de dados Pydantic para type safety
from .models import ResearchState, CompanyInfo, CompanyAnalysis
# ResearchState: Estado global do workflow (query, resultados, análise)
# CompanyInfo: Modelo para informações estruturadas de empresa
# CompanyAnalysis: Modelo para análise detalhada de empresa

# Serviço de integração com Firecrawl API
from .firecrawl import FirecrawlService
# FirecrawlService: Encapsula operações de web scraping e search

# Container de prompts organizados por funcionalidade
from .prompts import DeveloperToolsPrompts
# DeveloperToolsPrompts: Classe com templates de prompts para LLM


# Classe principal que orquestra workflow de pesquisa usando padrão de máquina de estados
class Workflow:
    # Inicializador que configura dependências e constrói workflow
    def __init__(self):
        # Instancia serviço Firecrawl para web scraping
        self.firecrawl = FirecrawlService()
        # Instancia modelo LLM com configurações otimizadas para análise
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)
        # Temperature 0.1 = quase determinístico mas com leve criatividade
        
        # Instancia container de prompts
        self.prompts = DeveloperToolsPrompts()
        # Constrói e compila workflow como grafo de estados
        self.workflow = self._build_workflow()

    # Método privado que define estrutura do workflow como State Machine
    def _build_workflow(self):
        # Cria grafo de estados com ResearchState como estrutura de dados compartilhada
        graph = StateGraph(ResearchState)
        
        # Define nós (estados) do workflow com suas respectivas funções
        graph.add_node("extract_tools", self._extract_tools_step)
        # Nó 1: Extrai ferramentas/produtos relevantes de artigos
        graph.add_node("research", self._research_step)
        # Nó 2: Pesquisa detalhada de cada ferramenta identificada
        graph.add_node("analyze", self._analyze_step)
        # Nó 3: Analisa dados coletados e gera recomendações
        
        # Define ponto de entrada do workflow
        graph.set_entry_point("extract_tools")
        
        # Define transições entre estados (edges do grafo)
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        # Workflow linear: extract → research → analyze → fim
        
        # Compila grafo em executor otimizado
        return graph.compile()

    # Primeiro passo: extrai nomes de ferramentas/produtos de artigos relevantes
    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        # Log informativo para tracking do progresso
        print(f"🔍 Encontrar artigos sobre: {state.query}")

        # Monta query otimizada para encontrar artigos comparativos
        article_query = f"{state.query} comparação de melhores alternativas para produtos/ferramentas/soluções/serviços"
        # Busca artigos com limite de 3 para performance
        search_results = self.firecrawl.search_companies(article_query, num_results=3)

        # Concatena conteúdo de todos os artigos encontrados
        all_content = ""
        for result in search_results.data:
            # Extrai URL do resultado da busca
            url = result.get("url", "")
            # Faz scraping da página para obter conteúdo completo
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped:
                # Limita a 1500 chars por artigo para controle de token
                all_content + scraped.markdown[:1500] + "\n\n"

        # Constrói conversa para LLM com system + user message
        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
        ]

        # Bloco try-catch para tratamento robusto de erros LLM
        try:
            # Invoca LLM para extrair nomes de ferramentas
            response = self.llm.invoke(messages)
            # Processa resposta: split por linha e remove espaços
            tool_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()  # Remove linhas vazias
            ]
            # Log dos resultados para debugging
            print(f"Produtos/ferramentas/soluções/serviços: {', '.join(tool_names[:5])}")
            # Retorna update para o estado do workflow
            return {"extracted_tools": tool_names}
        except Exception as e:
            # Fallback em caso de erro: continua workflow com lista vazia
            print(e)
            return {"extracted_tools": []}

    # Método para análise detalhada de conteúdo de empresa usando structured output
    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        # Configura LLM para retornar output estruturado (Pydantic model)
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)
        # with_structured_output força LLM a retornar dados no formato do modelo

        # Constrói prompt específico para análise de empresa
        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        # Tratamento de erro com fallback estruturado
        try:
            # Invoca LLM e força retorno como CompanyAnalysis
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(e)
            # Retorna análise vazia mas válida em caso de erro
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Falhou",
                api_available=None,
                language_support=[],
                integration_capabilities=[],
            )


    # Segundo passo: pesquisa detalhada de cada ferramenta identificada
    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        # Acessa ferramentas extraídas do passo anterior
        extracted_tools = getattr(state, "extracted_tools", [])

        # Estratégia de fallback se extração falhou
        if not extracted_tools:
            print("Nenhuma produtos/ferramentas/soluções/serviços extraída encontrada, retornando à pesquisa direta")
            # Busca direta baseada na query original
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            # Extrai títulos como nomes de ferramentas
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            # Usa ferramentas extraídas, limitando a 4 para performance
            tool_names = extracted_tools[:4]

        # Log do progresso para tracking
        print(f"Pesquisando produtos/ferramentas/soluções/serviços específicas: {', '.join(tool_names)}")

        # Lista para acumular informações das empresas
        companies = []
        # Loop para pesquisar cada ferramenta individualmente
        for tool_name in tool_names:
            # Busca site oficial da ferramenta
            tool_search_results = self.firecrawl.search_companies(tool_name + " site oficial", num_results=1)

            # Processa resultado se encontrado
            if tool_search_results:
                # Pega primeiro resultado da busca
                result = tool_search_results.data[0]
                # Extrai URL do site oficial
                url = result.get("url", "")

                # Cria objeto CompanyInfo com dados básicos
                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""),
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                # Faz scraping detalhado do site da empresa
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    # Obtém conteúdo em markdown
                    content = scraped.markdown
                    # Analisa conteúdo usando LLM estruturado
                    analysis = self._analyze_company_content(company.name, content)

                    # Atualiza objeto company com análise detalhada
                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities

                # Adiciona empresa à lista de resultados
                companies.append(company)

        # Retorna update do estado com empresas pesquisadas
        return {"companies": companies}

    # Terceiro passo: gera análise final e recomendações
    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        # Log do progresso
        print("Gerando recomendações")

        # Serializa dados das empresas para análise LLM
        company_data = ", ".join([
            company.json() for company in state.companies
        ])

        # Constrói prompt para geração de recomendações
        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
        ]

        # Invoca LLM para análise final
        response = self.llm.invoke(messages)
        # Retorna análise como string
        return {"analysis": response.content}

    # Método público que executa workflow completo
    def run(self, query: str) -> ResearchState:
        # Cria estado inicial com query do usuário
        initial_state = ResearchState(query=query)
        # Executa workflow passando estado inicial
        final_state = self.workflow.invoke(initial_state)
        # Retorna estado final como ResearchState validado
        return ResearchState(**final_state)