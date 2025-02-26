"""
Script para análise de repositórios.
"""

import argparse
import asyncio
import json
import os
import shutil
import stat
from pathlib import Path
import structlog
from config import DEFAULT_CONFIG
from analyzers.code_analyzer import CodeAnalyzer
from analyzers.ai_analyzer import AIAnalyzer, AIAnalysisConfig
from analyzers.ai_providers import OllamaProvider, OpenAIProvider, DeepSeekProvider, GeminiProvider
from analyzers.refactool_analyzer import RefactoolAnalyzer
from analyzers.github_manager import GitHubManager
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Verifica se as variáveis foram carregadas
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")

logger = structlog.get_logger()

def remove_readonly(func, path, _):
    """Remove atributo somente leitura e tenta a operação novamente."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def load_config(config_file: str = None) -> dict:
    """Carrega configuração do arquivo ou usa padrão."""
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG

async def setup_ai_provider(config: dict) -> AIAnalyzer:
    """Configura o provedor de IA baseado nas configurações."""
    # Usa o Gemini
    provider = GeminiProvider(
        api_key=gemini_key
    )
    
    return AIAnalyzer(provider=provider, config=AIAnalysisConfig(
        temperature=config.get("providers", {}).get("gemini", {}).get("temperature", 0.7),
        max_tokens=4096
    ))

async def analyze_repository(repo_url: str, output_file: str = None, config_file: str = None) -> dict:
    """Analisa um repositório Git."""
    # Carregar configuração
    config = load_config(config_file)
    
    # Configurar diretório temporário
    temp_dir = Path("temp") / datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Clonar repositório
        print(f"Clonando repositório: {repo_url}")
        github_manager = GitHubManager()
        repo_path = await github_manager.clone_repository(repo_url, temp_dir)
        
        # Configurar analisador de código
        print("Configurando analisador de código...")
        code_analyzer = CodeAnalyzer(
            max_method_lines=config.get("analysis", {}).get("max_method_lines", 30),
            max_complexity=config.get("analysis", {}).get("max_complexity", 10)
        )
        
        # Configurar provedor de IA
        print("Configurando provedor de IA...")
        ai_analyzer = await setup_ai_provider(config)
        
        # Iniciar análise
        print("Iniciando análise...")
        analyzer = RefactoolAnalyzer(code_analyzer, ai_analyzer)
        result = await analyzer.analyze_repository(repo_path)
        
        # Salvar resultado
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Relatório salvo em: {output_file}")
        
        return result
    finally:
        # Limpar diretório temporário
        print("Limpando diretório temporário...")
        try:
            shutil.rmtree(temp_dir, onerror=remove_readonly)
        except Exception as e:
            print(f"Erro ao limpar diretório temporário: {str(e)}")

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description="Analisador de código com IA")
    parser.add_argument("repo_url", help="URL do repositório Git a ser analisado")
    parser.add_argument("-o", "--output", help="Arquivo de saída para o relatório JSON")
    parser.add_argument("-c", "--config", help="Arquivo de configuração JSON")
    parser.add_argument("--provider", help="Provedor de IA a ser usado (gemini, openai, deepseek, ollama)")
    parser.add_argument("--providers", help="Lista de provedores de IA separados por vírgula")
    parser.add_argument("--dirs", help="Lista de diretórios a serem analisados, separados por vírgula")
    
    args = parser.parse_args()
    
    try:
        # Executar análise de forma assíncrona
        result = asyncio.run(analyze_repository(
            args.repo_url,
            args.output,
            args.config
        ))
        print("\n" + result["report"] + "\n")
    except KeyboardInterrupt:
        print("\nAnálise interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro fatal: {str(e)}\n")

if __name__ == "__main__":
    main() 