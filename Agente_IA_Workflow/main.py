# Biblioteca para carregar variáveis de ambiente de arquivos .env
from dotenv import load_dotenv
# load_dotenv: Fundamental para separar configuração sensível do código

# Import da classe principal do workflow local
from src.workflow import Workflow
# Import relativo da classe Workflow que orquestra todo o processo

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
# Execução imediata garante que API keys estejam disponíveis

# Função principal que implementa interface de linha de comando
def main():
    # Instancia workflow - inicializa todos os serviços e dependências
    workflow = Workflow()
    # Workflow.__init__() configura Firecrawl, OpenAI LLM e prompts
    
    # Header informativo para o usuário
    print("Agente de Pesquisa")

    # Loop principal de interação usuário-sistema
    while True:
        # Solicita input do usuário com prompt específico
        query = input("\n Consulta: ").strip()
        # .strip() remove espaços em branco das extremidades
        
        # Condições de saída do loop - múltiplas opções para UX
        if query.lower() in {"fui!", "sair"}:
            # .lower() torna comparação case-insensitive
            # Set {"fui!", "sair"} permite múltiplas palavras de saída
            break

        # Verifica se query não está vazia após strip
        if query:
            # Executa workflow completo passando query do usuário
            result = workflow.run(query)
            # result é ResearchState com todas as informações coletadas
            
            # Cabeçalho dos resultados com query original
            print(f"\n Resultados para: {query}")
            # Separador visual para melhor legibilidade
            print("=" * 60)

            # Itera através das empresas encontradas com numeração
            for i, company in enumerate(result.companies, 1):
                # enumerate(, 1) inicia contagem em 1 em vez de 0
                
                # Exibe informações básicas da empresa com emojis para UX
                print(f"\n{i}. 🏢 {company.name}")
                print(f"   🌐 Website: {company.website}")
                print(f"   💰 Valores: {company.pricing_model}")
                print(f"   📖 Open Source: {company.is_open_source}")

                # Exibe tech stack se disponível
                if company.tech_stack:
                    # Lista apenas primeiros 5 elementos para não poluir output
                    print(f"   🛠️  Tecnologia: {', '.join(company.tech_stack[:5])}")

                # Exibe linguagens suportadas se disponível
                if company.language_support:
                    # Join converte lista em string separada por vírgulas
                    print(
                        f"   💻 Suporte: {', '.join(company.language_support[:5])}"
                    )

                # Exibe status de API com validação de None
                if company.api_available is not None:
                    # Operador ternário para emoji baseado em boolean
                    api_status = (
                        "✅ Disponível" if company.api_available else "❌ Não disponível"
                    )
                    print(f"   🔌 API: {api_status}")

                # Exibe capacidades de integração se disponível
                if company.integration_capabilities:
                    # Limita a 4 integrações para legibilidade
                    print(
                        f"   🔗 Integrações: {', '.join(company.integration_capabilities[:4])}"
                    )

                # Exibe descrição se válida (não vazia e não indicador de falha)
                if company.description and company.description != "Falhou":
                    print(f"   📝 Descrição: {company.description}")

                # Linha vazia para separar empresas visualmente
                print()

            # Seção de recomendações se análise foi gerada
            if result.analysis:
                print("Recomendações: ")
                # Separador visual menor para subsection
                print("-" * 40)
                # Exibe análise/recomendações geradas pelo LLM
                print(result.analysis)


# Ponto de entrada padrão Python
if __name__ == "__main__":
    # Executa função main apenas se arquivo for executado diretamente
    main()
    # Não executa se arquivo for importado como módulo