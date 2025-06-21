# Imports para type hints avançados - essenciais para type safety
from typing import List, Optional, Dict, Any
# List: Especifica lista tipada (ex: List[str] = lista de strings)
# Optional: Indica que campo pode ser None (Optional[bool] = bool ou None)
# Dict: Dicionário tipado (Dict[str, Any] = chaves string, valores qualquer tipo)
# Any: Tipo genérico quando tipo específico não pode ser determinado

# Classe base do Pydantic para validação automática de dados
from pydantic import BaseModel
# BaseModel: Fornece validação automática, serialização e type checking


# Modelo para análise estruturada de empresa/produto
class CompanyAnalysis(BaseModel):
    # Campo obrigatório para modelo de preços
    pricing_model: str
    # String que categoriza modelo de negócio: "Gratuito", "Freemium", etc.
    
    # Campo opcional para indicar se é open source
    is_open_source: Optional[bool] = None
    # Optional[bool]: pode ser True, False ou None (quando não determinado)
    # Default None quando informação não está disponível
    
    # Lista de tecnologias usadas, com default vazio
    tech_stack: List[str] = []
    # List[str]: garante que todos elementos sejam strings
    # Default []: evita erro quando não há tecnologias identificadas
    
    # Descrição da empresa/produto, default string vazia
    description: str = ""
    # String obrigatória mas com default para casos onde descrição falha
    
    # Indicador de disponibilidade de API
    api_available: Optional[bool] = None
    # None quando não determinado, True/False quando confirmado
    
    # Linguagens de programação suportadas
    language_support: List[str] = []
    # Lista tipada para linguagens como ["Python", "JavaScript"]
    
    # Capacidades de integração com outras ferramentas
    integration_capabilities: List[str] = []
    # Lista de plataformas/serviços com integração disponível


# Modelo completo para informações de empresa
class CompanyInfo(BaseModel):
    # Campos obrigatórios (sem default)
    name: str
    # Nome da empresa/produto - sempre obrigatório
    description: str
    # Descrição - obrigatória mas pode ser string vazia
    website: str
    # URL do site - sempre obrigatória para identificação
    
    # Campos opcionais com defaults apropriados
    pricing_model: Optional[str] = None
    # Modelo de preços pode não estar determinado inicialmente
    
    is_open_source: Optional[bool] = None
    # Status open source pode ser indeterminado
    
    tech_stack: List[str] = []
    # Stack tecnológica pode estar vazia inicialmente
    
    competitors: List[str] = []
    # Lista de concorrentes, pode estar vazia
    
    api_available: Optional[bool] = None
    # Disponibilidade de API pode ser indeterminada
    
    language_support: List[str] = []
    # Suporte a linguagens pode estar vazio
    
    integration_capabilities: List[str] = []
    # Capacidades de integração podem estar vazias
    
    developer_experience_rating: Optional[str] = None
    # Rating de experiência do desenvolvedor - campo adicional opcional


# Modelo para estado global do workflow de pesquisa
class ResearchState(BaseModel):
    # Campo obrigatório - query inicial do usuário
    query: str
    # String que contém a consulta original que iniciou o workflow
    
    # Lista de ferramentas extraídas da análise de artigos
    extracted_tools: List[str] = []
    # Default vazio, preenchida durante step de extração
    
    # Lista de empresas pesquisadas e analisadas
    companies: List[CompanyInfo] = []
    # Default vazia, preenchida durante step de research
    # Usa CompanyInfo para garantir estrutura consistente
    
    # Resultados brutos de busca para referência
    search_results: List[Dict[str, Any]] = []
    # Lista de dicionários com resultados de API calls
    # Dict[str, Any] acomoda estruturas variáveis de APIs
    
    # Análise final e recomendações geradas
    analysis: Optional[str] = None
    # String com recomendações finais, None até step final
    # Optional porque só é preenchida no último passo do workflow