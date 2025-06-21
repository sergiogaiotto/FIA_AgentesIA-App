# Linha vazia para separação visual - boa prática de formatação

# Classe container para organizar prompts por categoria funcional
class DeveloperToolsPrompts:
    # Organização em classe facilita manutenção e reutilização de prompts
    
    # Comentário que categoriza próximos prompts
    # Tool extraction prompts
    
    # Prompt de sistema para definir comportamento do LLM na extração
    TOOL_EXTRACTION_SYSTEM = """Você é um pesquisador de preços, promoções, ofertas e valores. Extraia nomes específicos de ferramentas, bibliotecas, plataformas ou serviços de artigos.
Concentre-se em produtos/ferramentas/soluções/serviços reais que consumidores demnonstrem interesse e podem usar."""
    # Prompt de sistema define persona, objetivo e escopo
    # Foco em produtos reais evita entidades abstratas
    # Orientação para consumidores garante relevância prática

    # Método estático para gerar prompt de usuário dinâmico
    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        # @staticmethod: não precisa de instância da classe para ser chamado
        # Permite uso direto: DeveloperToolsPrompts.tool_extraction_user()
        
        # f-string para interpolação de variáveis no template
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
                IBM
                Carrefour
                Ifood
                OpenAI
                Groq
                """
        # Template estruturado com regras claras para LLM
        # Exemplos concretos ajudam LLM entender formato esperado
        # Limitação a 5 resultados controla output e custo
        # Formato linha por linha facilita parsing posterior

    # Comentário que categoriza próximos prompts
    # Company/Tool analysis prompts
    
    # Prompt de sistema para análise detalhada de empresas
    TOOL_ANALYSIS_SYSTEM = """Você está analisando preços, promoções, ofertas e valores de produtos/ferramentas/soluções/serviços com base na categoria informada pelo usuário.
Concentre-se em extrair informações relevantes para consumidores de produtos/ferramentas/soluções/serviços.
Preste atenção especial nas condições, descontos, modelo comercial, pré-requisitos, tecnologia, APIs, SDKs e modos de utilização para compra, obtenção, assinatura, uso e consumo."""
    # Sistema define foco em informações práticas para consumidores
    # Lista específica de elementos a extrair garante consistência
    # Orientação comercial direciona análise para aspectos de negócio

    # Método estático para análise específica de empresa
    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        # Template personalizado com nome da empresa e conteúdo
        return f"""Empresa/Ferramenta: {company_name}
                Conteúdo do Website: {content[:2500]}

                Analise este conteúdo da perspectiva de um consumidor e forneça:
                - pricing_model: "Gratuito", "Freemium", "Pago", "Empresarial", "Assinatura" ou "Desconhecido"
                - is_open_source: verdadeiro se for de código aberto, falso se for proprietário, nulo se não estiver claro
                - tech_stack: tecnologia adotada para produtos/ferramentas/soluções/serviços oferecido
                - description: breve descrição de uma frase com foco no que esta produtos/ferramentas/soluções/serviços entrega para o consumidor
                - api_available: verdadeiro se API REST, GraphQL, SDK ou acesso programático forem mencionados
                - language_support: Lista de linguagens de programação explicitamente suportadas (ex.: Python, JavaScript, Go, etc.)
                - integration_capabilities: Lista de ferramentas/plataformas com as quais se integra (ex.: GitHub, VS Code, Docker, AWS, etc.)
                Foco em recursos relevantes para o consumidor, como produtos/ferramentas/soluções/serviços, bem como modos de uso, integrações com APIs, SDKs, suporte a idiomas, integrações e modos de utlização para compra, obtenção, assinatura, uso e consumo."""
        # content[:2500]: limita conteúdo a 2500 chars para controle de tokens
        # Especificação clara de campos esperados alinha com modelo Pydantic
        # Categorias de pricing_model padronizadas facilitam análise
        # Exemplos concretos (Python, AWS) ajudam LLM entender formato
        # Perspectiva do consumidor mantém foco prático

    # Prompt de sistema para geração de recomendações finais
    RECOMMENDATIONS_SYSTEM = """Você é um pesquisador sênior que fornece recomendações técnicas rápidas e concisas.
    Mantenha as respostas breves e práticas - no máximo 3 a 4 frases no total.."""
    # Persona de "pesquisador sênior" estabelece autoridade
    # Limitação de 3-4 frases força concisão e relevância
    # Foco em "técnicas" direciona para aspectos práticos

    # Método estático para recomendações baseadas em dados coletados
    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        # Template que combina query original com dados analisados
        return f"""Consumer Query: {query}
                Ferramentas/Tecnologias Analisadas: {company_data}

                Forneça uma breve recomendação (máximo de 3 a 4 frases) abrangendo:
                - Qual ferramenta é a melhor e por quê
                - Principais considerações sobre custo/preço
                - Principal vantagem técnica
                - A melhor oferta, preços e condições

                Não são necessárias longas explicações."""
        # Estrutura de bullet points orienta LLM sobre aspectos a cobrir
        # Ênfase em brevidade evita respostas verbosas
        # Foco em "melhor", "custo", "vantagem" força análise comparativa
        # company_data contém JSON serializado das empresas analisadas