# Agente Workflow - Pesquisa estruturada e análise comparativa
import os
import json
from typing import Dict, Any, List, Optional

# Imports para workflow estruturado
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Imports dos modelos Pydantic
from pydantic import BaseModel

# Carregamento de variáveis
from dotenv import load_dotenv

# Biblioteca Firecrawl
from firecrawl import FirecrawlApp, ScrapeOptions

# Carrega variáveis de ambiente
load_dotenv()


# ===============================
# MODELOS PYDANTIC
# ===============================

class CompanyAnalysis(BaseModel):
    """Modelo para análise estruturada de empresa/produto"""
    pricing_model: str
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []


class CompanyInfo(BaseModel):
    """Modelo completo para informações de empresa"""
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    developer_experience_rating: Optional[str] = None


class ResearchState(BaseModel):
    """Modelo para estado global do workflow"""
    query: str
    extracted_tools: List[str] = []
    companies: List[CompanyInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None


# ===============================
# PROMPTS ORGANIZADOS
# ===============================

class DeveloperToolsPrompts:
    """Container para prompts organizados por categoria"""
    
    # Tool extraction prompts
    TOOL_EXTRACTION_SYSTEM = """Você é um pesquisador de preços, promoções, ofertas e valores. Extraia nomes específicos de ferramentas, bibliotecas, plataformas ou serviços de artigos.
Concentre-se em produtos/ferramentas/soluções/serviços reais que consumidores demonstrem interesse e podem usar."""

    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
Conteúdo do Artigo: {content}

Extraia uma lista de nomes de produtos/ferramentas/soluções/serviços específicos mencionados neste conteúdo que sejam relevantes para "{query}".

Rules:
- Incluir apenas nomes de produtos reais, sem termos genéricos
- Foco em ferramentas/soluções/serviços que os consumidores podem comprar, obter, assinar, usar e consumir diretamente
- Incluir opções comerciais e de código aberto
- Limitar às 5 resultados mais relevantes
- Retornar apenas os nomes dos produtos/ferramentas/soluções/serviços, um por linha, sem descrições

Formato de exemplo:
Amazon
MercadoLivre
Picpay
Nubank
Microsoft
"""

    # Company analysis prompts
    TOOL_ANALYSIS_SYSTEM = """Você está analisando preços, promoções, ofertas e valores de produtos/ferramentas/soluções/serviços com base na categoria informada pelo usuário.
Concentre-se em extrair informações relevantes para consumidores de produtos/ferramentas/soluções/serviços.
Preste atenção especial nas condições, descontos, modelo comercial, pré-requisitos, tecnologia, APIs, SDKs e modos de utilização."""

    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""Empresa/Ferramenta: {company_name}
Conteúdo do Website: {content[:2500]}

Analise este conteúdo da perspectiva de um consumidor e forneça:
- pricing_model: "Gratuito", "Freemium", "Pago", "Empresarial", "Assinatura" ou "Desconhecido"
- is_open_source: verdadeiro se for de código aberto, falso se for proprietário, nulo se não estiver claro
- tech_stack: tecnologia adotada para produtos/ferramentas/soluções/serviços oferecido
- description: breve descrição de uma frase com foco no que esta produtos/ferramentas/soluções/serviços entrega para o consumidor
- api_available: verdadeiro se API REST, GraphQL, SDK ou acesso programático forem mencionados
- language_support: Lista de linguagens de programação explicitamente suportadas
- integration_capabilities: Lista de ferramentas/plataformas com as quais se integra
"""

    # Recommendations prompts
    RECOMMENDATIONS_SYSTEM = """Você é um pesquisador sênior que fornece recomendações técnicas rápidas e concisas.
Mantenha as respostas breves e práticas - no máximo 3 a 4 frases no total."""

    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Consumer Query: {query}
Ferramentas/Tecnologias Analisadas: {company_data}

Forneça uma breve recomendação (máximo de 3 a 4 frases) abrangendo:
- Qual ferramenta é a melhor e por quê
- Principais considerações sobre custo/preço
- Principal vantagem técnica
- A melhor oferta, preços e condições

Não são necessárias longas explicações."""


# ===============================
# SERVIÇO FIRECRAWL
# ===============================

class FirecrawlService:
    """Serviço para integração com Firecrawl API"""
    
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY não encontrada")
        self.app = FirecrawlApp(api_key=api_key)

    def search_companies(self, query: str, num_results: int = 5):
        """Busca empresas/produtos usando Firecrawl"""
        try:
            result = self.app.search(
                query=f"{query} preços, ofertas e valores",
                limit=num_results,
                scrape_options=ScrapeOptions(formats=["markdown"])
            )
            return result
        except Exception as e:
            print(f"Erro na busca: {e}")
            return []

    def scrape_company_pages(self, url: str):
        """Faz scraping de páginas específicas"""
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(f"Erro no scraping: {e}")
            return None


# ===============================
# AGENTE WORKFLOW PRINCIPAL
# ===============================

class WorkflowAgent:
    """Agente de pesquisa estruturada usando workflows LangGraph"""

    def __init__(self):
        """Inicializa agente com dependências necessárias"""
        
        # Validação de chaves de API
        if not os.getenv("FIRECRAWL_API_KEY"):
            raise ValueError("FIRECRAWL_API_KEY não encontrada")
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY não encontrada")
        
        # Inicializa serviços
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)
        self.prompts = DeveloperToolsPrompts()
        
        # Constrói workflow
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Constrói workflow como máquina de estados"""
        graph = StateGraph(ResearchState)
        
        # Adiciona nós do workflow
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)
        
        # Define transições
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        
        return graph.compile()

    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        """Primeiro passo: extrai ferramentas de artigos"""
        print(f"🔍 Buscando artigos sobre: {state.query}")

        # Busca artigos relevantes
        article_query = f"{state.query} comparação de melhores alternativas"
        search_results = self.firecrawl.search_companies(article_query, num_results=3)

        # Extrai conteúdo dos artigos
        all_content = ""
        if hasattr(search_results, 'data'):
            for result in search_results.data:
                url = result.get("url", "")
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped and hasattr(scraped, 'markdown'):
                    all_content += scraped.markdown[:1500] + "\n\n"

        # Usa LLM para extrair ferramentas
        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            tool_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            print(f"Ferramentas encontradas: {', '.join(tool_names[:5])}")
            return {"extracted_tools": tool_names}
        except Exception as e:
            print(f"Erro na extração: {e}")
            return {"extracted_tools": []}

    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        """Analisa conteúdo de empresa usando structured output"""
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(f"Erro na análise: {e}")
            return CompanyAnalysis(
                pricing_model="Desconhecido",
                is_open_source=None,
                tech_stack=[],
                description="Análise falhou",
                api_available=None,
                language_support=[],
                integration_capabilities=[]
            )

    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        """Segundo passo: pesquisa detalhada de cada ferramenta"""
        extracted_tools = getattr(state, "extracted_tools", [])

        # Fallback se não extraiu ferramentas
        if not extracted_tools:
            print("Fazendo busca direta...")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            if hasattr(search_results, 'data'):
                tool_names = [
                    result.get("metadata", {}).get("title", "Unknown")
                    for result in search_results.data
                ]
            else:
                tool_names = []
        else:
            tool_names = extracted_tools[:4]

        print(f"🔬 Pesquisando: {', '.join(tool_names)}")

        companies = []
        for tool_name in tool_names:
            # Busca site oficial
            tool_search_results = self.firecrawl.search_companies(
                tool_name + " site oficial", num_results=1
            )

            if hasattr(tool_search_results, 'data') and tool_search_results.data:
                result = tool_search_results.data[0]
                url = result.get("url", "")

                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""),
                    website=url
                )

                # Scraping detalhado
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped and hasattr(scraped, 'markdown'):
                    content = scraped.markdown
                    analysis = self._analyze_company_content(company.name, content)

                    # Atualiza informações
                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities

                companies.append(company)

        return {"companies": companies}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        """Terceiro passo: gera recomendações finais"""
        print("📊 Gerando recomendações...")

        # Serializa dados das empresas
        company_data = ", ".join([
            company.model_dump_json() for company in state.companies
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
        ]

        try:
            response = self.llm.invoke(messages)
            return {"analysis": response.content}
        except Exception as e:
            print(f"Erro nas recomendações: {e}")
            return {"analysis": "Não foi possível gerar recomendações no momento."}

    async def process_query(self, query: str) -> str:
        """
        Processa query do usuário usando workflow estruturado
        
        Args:
            query: Consulta do usuário
            
        Returns:
            Resposta formatada com resultados e recomendações
        """
        try:
            # Executa workflow
            initial_state = ResearchState(query=query)
            final_state = self.workflow.invoke(initial_state)
            result = ResearchState(**final_state)

            # Formata resposta
            response_parts = []
            response_parts.append(f"📋 **Resultados para: {query}**\n")

            if result.companies:
                response_parts.append("🏢 **Empresas/Ferramentas Encontradas:**\n")
                
                for i, company in enumerate(result.companies, 1):
                    company_info = [
                        f"**{i}. {company.name}**",
                        f"🌐 Website: {company.website}",
                        f"💰 Preços: {company.pricing_model or 'N/A'}",
                        f"📖 Open Source: {'Sim' if company.is_open_source else 'Não' if company.is_open_source is False else 'N/A'}"
                    ]

                    if company.tech_stack:
                        company_info.append(f"🛠️ Tecnologias: {', '.join(company.tech_stack[:3])}")

                    if company.language_support:
                        company_info.append(f"💻 Linguagens: {', '.join(company.language_support[:3])}")

                    if company.api_available is not None:
                        api_status = "✅ Disponível" if company.api_available else "❌ Não disponível"
                        company_info.append(f"🔌 API: {api_status}")

                    if company.description and company.description != "Análise falhou":
                        company_info.append(f"📝 Descrição: {company.description}")

                    response_parts.append("\n".join(company_info) + "\n")

            if result.analysis:
                response_parts.append(f"💡 **Recomendações:**\n{result.analysis}")

            return "\n".join(response_parts)

        except Exception as e:
            return f"❌ Erro ao processar consulta: {str(e)}"

    def get_workflow_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o workflow"""
        return {
            "name": "Research Workflow Agent",
            "version": "1.0.0",
            "steps": ["extract_tools", "research", "analyze"],
            "capabilities": [
                "Extração de ferramentas de artigos",
                "Pesquisa detalhada de empresas",
                "Análise comparativa",
                "Recomendações técnicas"
            ]
        }