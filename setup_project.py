#!/usr/bin/env python3
"""
Script de configuração automática do projeto
Execute: python setup_project.py
"""

import os
import sys
from pathlib import Path

def create_directory(path):
    """Cria diretório se não existir"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretório criado: {path}")

def create_file(filepath, content):
    """Cria arquivo com conteúdo"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Arquivo criado: {filepath}")

def main():
    print("🚀 CONFIGURAÇÃO AUTOMÁTICA - Agentes de IA FIA")
    print("=" * 50)
    
    # Verifica se está no diretório correto
    if not os.path.exists('app.py'):
        print("❌ Erro: Execute este script no diretório raiz do projeto (onde está app.py)")
        sys.exit(1)
    
    print("📁 Criando estrutura de diretórios...")
    
    # Criar diretórios necessários
    create_directory('agents')
    create_directory('templates')
    create_directory('static')
    
    print("\n📝 Criando arquivos necessários...")
    
    # Requirements.txt corrigido
    requirements_content = """firecrawl-py==0.0.20
langchain==0.3.7
langchain-openai==0.2.8
langgraph==0.2.34
pydantic==2.9.2
langchain-mcp-adapters==0.1.2
python-dotenv==1.0.1
fastapi==0.115.4
uvicorn[standard]==0.32.0
jinja2==3.1.4"""
    
    # Backup do requirements.txt atual
    if os.path.exists('requirements.txt'):
        os.rename('requirements.txt', 'requirements.txt.backup')
        print("📦 Backup criado: requirements.txt.backup")
    
    create_file('requirements.txt', requirements_content)
    
    # .env.example
    env_example_content = """# Configurações dos Agentes de IA - FIA
# Copie este arquivo para .env e preencha com suas chaves de API

# Firecrawl API Key (obrigatória)
# Obtenha em: https://firecrawl.dev
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# OpenAI API Key (obrigatória) 
# Obtenha em: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Porta para o servidor (opcional - padrão: 8000)
PORT=8000

# Ambiente de execução (opcional)
ENVIRONMENT=production"""
    
    if not os.path.exists('.env.example'):
        create_file('.env.example', env_example_content)
    
    # agents/__init__.py
    agents_init_content = """# Módulo agents - Agentes de IA para pesquisa e análise

__version__ = "1.0.0"
__author__ = "FIA.LabData - Prof Sergio Gaiotto"

from .mcp_agent import MCPAgent
from .workflow_agent import WorkflowAgent

__all__ = ["MCPAgent", "WorkflowAgent"]
"""
    
    create_file('agents/__init__.py', agents_init_content)
    
    print("\n✅ Configuração concluída!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. ✅ Faça download dos arquivos completos dos artifacts gerados")
    print("2. ✅ Copie o conteúdo de 'agents/mcp_agent.py' do artifact")
    print("3. ✅ Copie o conteúdo de 'agents/workflow_agent.py' do artifact") 
    print("4. ✅ Copie o conteúdo de 'templates/index.html' do artifact")
    print("5. ✅ Configure suas chaves API no .env")
    print("6. ✅ Teste localmente: python app.py")
    print("7. ✅ Faça deploy no Render")
    
    print(f"\n🎯 ESTRUTURA FINAL:")
    print("📁 Projeto/")
    print("├── 📄 app.py")
    print("├── 📄 requirements.txt ✅ ATUALIZADO")
    print("├── 📄 .env.example ✅ NOVO")
    print("├── 📁 agents/ ✅ NOVO")
    print("│   ├── 📄 __init__.py ✅ CRIADO")
    print("│   ├── 📄 mcp_agent.py ❗ COPIAR DO ARTIFACT")
    print("│   └── 📄 workflow_agent.py ❗ COPIAR DO ARTIFACT")
    print("└── 📁 templates/ ✅ NOVO")
    print("    └── 📄 index.html ❗ COPIAR DO ARTIFACT")

if __name__ == "__main__":
    main()