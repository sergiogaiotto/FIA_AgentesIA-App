# Biblioteca padrão para acesso a variáveis de ambiente do sistema
import os
# os: Interface para funcionalidades dependentes do sistema operacional

# Imports da biblioteca Firecrawl para web scraping e busca
from firecrawl import FirecrawlApp, ScrapeOptions
# FirecrawlApp: Cliente principal para interagir com API Firecrawl
# ScrapeOptions: Classe de configuração para personalizar operações de scraping

# Biblioteca para carregar variáveis de ambiente de arquivos .env
from dotenv import load_dotenv
# load_dotenv: Carrega variáveis do arquivo .env para os.environ

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
# Execução imediata garante que variáveis estejam disponíveis para a classe


# Classe de serviço que encapsula operações Firecrawl
class FirecrawlService:
    # Inicializador que configura cliente Firecrawl com validação de API key
    def __init__(self):
        # Recupera chave API de variável de ambiente
        api_key = os.getenv("FIRECRAWL_API_KEY")
        # Validação explícita da presença da chave API
        if not api_key:
            # Levanta exceção informativa se chave não for encontrada
            raise ValueError("Chave da variável de ambiente FIRECRAWL_API_KEY ausente")
        # Instancia cliente Firecrawl com chave validada
        self.app = FirecrawlApp(api_key=api_key)

    # Método para buscar empresas/produtos usando search engine do Firecrawl
    def search_companies(self, query: str, num_results: int = 5):
        # Bloco try-catch para tratamento robusto de erros de API
        try:
            # Executa busca com query otimizada para encontrar informações de preços
            result = self.app.search(
                # Concatena termos relacionados a preços para melhor targeting
                query=f"{query} preços, ofertas e valores ",
                # Limita número de resultados para controle de performance e custo
                limit=num_results,
                # Configura opções de scraping para os resultados
                scrape_options=ScrapeOptions(
                    # Especifica formato markdown para melhor parsing posterior
                    formats=["markdown"]
                )
                # Markdown é ideal para LLMs processarem conteúdo estruturado
            )
            # Retorna resultados da busca
            return result
        # Captura qualquer exceção durante operação de busca
        except Exception as e:
            # Log simples do erro para debugging
            print(e)
            # Retorna lista vazia como fallback para não quebrar workflow
            return []

    # Método para fazer scraping de páginas específicas
    def scrape_company_pages(self, url: str):
        # Bloco try-catch para tratamento de erros de scraping
        try:
            # Executa scraping da URL fornecida
            result = self.app.scrape_url(
                # URL alvo para scraping
                url,
                # Especifica formato de saída como markdown
                formats=["markdown"]
                # Markdown preserva estrutura do conteúdo para análise LLM
            )
            # Retorna objeto com conteúdo scraped
            return result
        # Captura erros específicos de scraping (timeout, 404, etc.)
        except Exception as e:
            # Log do erro para debugging
            print(e)
            # Retorna None para indicar falha no scraping
            return None