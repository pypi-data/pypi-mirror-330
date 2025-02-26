"""
Script de exemplo para análise do projeto CapTool usando Refactool.
"""

import os
import asyncio
import structlog
from dotenv import load_dotenv
from pathlib import Path

# Adiciona o diretório pai ao PYTHONPATH
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in os.sys.path:
    os.sys.path.append(parent_dir)

from refactool_analyzer import RefactoolAnalyzer
from github_integration import GitHubManager

logger = structlog.get_logger()

async def analyze_captool():
    """Analisa o projeto CapTool."""
    try:
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Configura gerenciadores
        github = GitHubManager(os.getenv("GITHUB_TOKEN"))
        analyzer = RefactoolAnalyzer()
        
        # Inicia análise
        logger.info("analyze_captool.starting")
        
        # Analisa o repositório e cria PR com sugestões
        results = await analyzer.analyze_github_repo(
            "gabrielsalvesdev/captool",
            create_pull_request=True,
            pr_title="refactor: Melhorias sugeridas pela Refactool",
            pr_body="""
# Análise Automática da Refactool

Esta análise foi realizada automaticamente pela Refactool e inclui:
- Análise estática de código
- Detecção de code smells
- Sugestões de melhoria
- Análise semântica com IA

## Principais Pontos
- Estrutura do projeto
- Qualidade do código
- Padrões de desenvolvimento
- Oportunidades de melhoria

Por favor, revise as sugestões e faça os ajustes necessários.
            """
        )
        
        logger.info(
            "analyze_captool.completed",
            results=results
        )
        
    except Exception as e:
        logger.error(
            "analyze_captool.error",
            error=str(e),
            exc_info=True
        )
        raise

def main():
    """Função principal."""
    if not os.getenv("GITHUB_TOKEN"):
        print("Erro: GITHUB_TOKEN não configurado no arquivo .env")
        return
    
    asyncio.run(analyze_captool())

if __name__ == "__main__":
    main() 