"""
Script principal para análise do projeto CapTool.
"""

import asyncio
import os
import shutil
import stat
from pathlib import Path
import structlog
from analyzers.code_analyzer import CodeAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from analyzers.ai_providers import OllamaProvider
from analyzers.refactool_analyzer import RefactoolAnalyzer
from analyzers.github_manager import GitHubManager

logger = structlog.get_logger()

def remove_readonly(func, path, _):
    """Remove atributo somente leitura e tenta a operação novamente."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

async def analyze_with_timeout(analyzer: RefactoolAnalyzer, repo_url: str, timeout: int = 300) -> str:
    """
    Executa a análise com timeout.
    
    Args:
        analyzer: Instância do analisador
        repo_url: URL do repositório
        timeout: Timeout em segundos
        
    Returns:
        Relatório da análise
    """
    try:
        # Configura o timeout
        result = await asyncio.wait_for(
            analyzer.analyze_project(repo_url),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        logger.error("Timeout durante análise")
        return "Erro: A análise excedeu o tempo limite."
    except Exception as e:
        logger.error(f"Erro durante análise: {str(e)}")
        return f"Erro durante análise: {str(e)}"

async def main():
    """Função principal."""
    github = None
    try:
        # Configura logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer()
            ]
        )
        
        # URL do repositório
        repo_url = "https://github.com/gabrielsalvesdev/captool"
        repo_name = repo_url.split('/')[-1]
        temp_dir = os.path.join('temp', repo_name)
        
        # Limpa diretório temporário se existir
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, onerror=remove_readonly)
            except Exception as e:
                logger.error(f"Erro ao limpar diretório temporário: {str(e)}")
                
        # Cria diretório temporário
        os.makedirs(temp_dir, exist_ok=True)
            
        # Clona repositório
        github = GitHubManager()
        await github.start()
        await github.clone_repository(repo_url, temp_dir)
        
        # Inicializa analisadores
        code_analyzer = CodeAnalyzer()
        ollama = OllamaProvider(model="llama2:13b", timeout=60)
        ai_analyzer = AIAnalyzer(ollama)
        
        # Inicializa analisador principal
        analyzer = RefactoolAnalyzer(code_analyzer, ai_analyzer)
        
        # Executa análise
        result = await analyzer.analyze_project(temp_dir)
        
        # Imprime resultado
        print("\n" + result + "\n")
        
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
        print(f"\nErro fatal: {str(e)}\n")
    finally:
        # Finaliza GitHub
        if github:
            await github.stop()
            
        # Limpa diretório temporário
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, onerror=remove_readonly)
            except Exception as e:
                logger.error(f"Erro ao limpar diretório temporário: {str(e)}")

if __name__ == "__main__":
    # Configura o Git se necessário
    git_path = os.getenv("GIT_PYTHON_GIT_EXECUTABLE")
    if not git_path:
        git_path = r"C:\Program Files\Git\bin\git.exe"
        os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = git_path
    
    # Executa o loop de eventos
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAnálise interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro fatal: {str(e)}\n") 