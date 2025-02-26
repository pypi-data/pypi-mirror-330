"""
Analisador de código para o Refactool.
"""

import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import structlog

from .code_analyzer import CodeAnalyzer, AnalysisConfig, CodeSmell
from .ai_analyzer import AIAnalyzer, AIAnalysisConfig, CodeSuggestion
from .ai_providers import OpenAIProvider, OllamaProvider
from .github_manager import GitHubManager

logger = structlog.get_logger()

class ProjectContext:
    """Contexto do projeto para análise."""
    
    def __init__(self):
        self.languages: Dict[str, int] = {}  # Linguagens usadas e quantidade de arquivos
        self.dependencies: Dict[str, List[str]] = {}  # Dependências por linguagem
        self.frameworks: Dict[str, List[str]] = {}  # Frameworks por linguagem
        self.file_types: Dict[str, int] = {}  # Tipos de arquivo e quantidade
        self.architecture: Dict[str, List[str]] = {}  # Componentes arquiteturais
        self.test_coverage: Dict[str, float] = {}  # Cobertura de testes por componente
        self.documentation: Dict[str, str] = {}  # Documentação encontrada
        self.entry_points: List[str] = []  # Pontos de entrada da aplicação
        self.build_files: List[str] = []  # Arquivos de build/configuração
        self.config_files: List[str] = []  # Arquivos de configuração
        self.api_definitions: List[str] = []  # Definições de API
        self.database_schemas: List[str] = []  # Esquemas de banco de dados

class RefactoolAnalyzer:
    """Analisador principal do Refactool."""
    
    # Mapeamento de extensões para linguagens
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.h': 'C/C++ Header'
    }
    
    # Arquivos importantes para análise
    IMPORTANT_FILES = {
        'build': [
            'setup.py', 'requirements.txt', 'package.json', 'Cargo.toml',
            'build.gradle', 'pom.xml', 'Makefile', 'CMakeLists.txt'
        ],
        'config': [
            '.env', 'config.yaml', 'config.json', '.gitignore', 'docker-compose.yml',
            'Dockerfile', 'nginx.conf', 'webpack.config.js', 'tsconfig.json'
        ],
        'docs': [
            'README.md', 'CONTRIBUTING.md', 'API.md', 'CHANGELOG.md',
            'docs/', 'wiki/', 'specifications/'
        ],
        'tests': [
            'test/', 'tests/', 'spec/', '__tests__/',
            'pytest.ini', 'jest.config.js', 'phpunit.xml'
        ],
        'ci': [
            '.github/workflows/', '.gitlab-ci.yml', 'Jenkinsfile',
            'azure-pipelines.yml', '.travis.yml', '.circleci/'
        ]
    }
    
    def __init__(self, code_analyzer: CodeAnalyzer, ai_analyzer: AIAnalyzer):
        self.code_analyzer = code_analyzer
        self.ai_analyzer = ai_analyzer
        
        # Cache de arquivos analisados
        self._analyzed_files: Set[str] = set()
        self._analysis_results: Dict[str, List[CodeSmell]] = {}
        self._suggestions: Dict[str, List[CodeSuggestion]] = {}
        
        # Contexto do projeto
        self.context = ProjectContext()
        
        self.ollama_provider = OllamaProvider()
        self.github = GitHubManager()
    
    async def start(self):
        """Inicializa os analisadores."""
        await self.ollama_provider.start()
        await self.github.start()
    
    async def stop(self):
        """Finaliza os analisadores."""
        await self.ollama_provider.stop()
        await self.github.stop()
    
    async def analyze_project(self, root_dir: str) -> str:
        """
        Analisa um projeto completo.
        
        Args:
            root_dir: Diretório raiz do projeto
            
        Returns:
            Relatório da análise em formato string
        """
        try:
            # Inicializa contadores
            total_files = 0
            total_lines = 0
            total_functions = 0
            total_classes = 0
            languages = {}
            important_files = []
            
            # Analisa cada arquivo
            root_path = Path(root_dir)
            for file_path in root_path.rglob('*'):
                if not file_path.is_file():
                    continue
                    
                file_ext = file_path.suffix
                if not file_ext:
                    continue
                    
                # Lê o arquivo
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    logger.warning(
                        "refactool_analyzer.file_read_failed",
                        file=str(file_path)
                    )
                    continue
                
                # Analisa o arquivo
                analysis = self.code_analyzer.analyze_file(content, file_ext)
                
                # Atualiza contadores
                total_files += 1
                total_lines += analysis.total_lines
                total_functions += analysis.total_functions
                total_classes += analysis.total_classes
                
                # Atualiza linguagens
                lang = self.code_analyzer.LANGUAGE_EXTENSIONS.get(file_ext, 'Unknown')
                if lang in languages:
                    languages[lang] += 1
                else:
                    languages[lang] = 1
                    
                # Verifica se é um arquivo importante
                if analysis.total_functions > 0 or analysis.total_classes > 0:
                    important_files.append({
                        'path': str(file_path.relative_to(root_path)),
                        'analysis': analysis
                    })
            
            # Gera relatório
            report = self._generate_analysis_report(
                total_files=total_files,
                total_lines=total_lines,
                total_functions=total_functions,
                total_classes=total_classes,
                languages=languages,
                important_files=important_files
            )
            
            return report
            
        except Exception as e:
            logger.error(
                "refactool_analyzer.analysis_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            return "Erro ao analisar projeto"
    
    def _generate_analysis_report(
        self,
        total_files: int,
        total_lines: int,
        total_functions: int,
        total_classes: int,
        languages: Dict[str, int],
        important_files: List[Dict]
    ) -> str:
        """Gera o relatório de análise."""
        
        # Visão geral do projeto
        report = [
            "# Relatório de Análise do Projeto",
            "",
            "## Visão Geral",
            f"- Total de arquivos: {total_files}",
            f"- Total de linhas de código: {total_lines}",
            f"- Total de funções: {total_functions}", 
            f"- Total de classes: {total_classes}",
            "",
            "## Linguagens Utilizadas"
        ]
        
        # Lista linguagens
        for lang, count in languages.items():
            report.append(f"- {lang}: {count} arquivo(s)")
            
        # Analisa arquivos importantes
        if important_files:
            report.extend([
                "",
                "## Arquivos Importantes"
            ])
            
            for file_info in important_files:
                path = file_info['path']
                analysis = file_info['analysis']
                
                report.extend([
                    f"\n### {path}",
                    f"- Linhas totais: {analysis.total_lines}",
                    f"- Linhas em branco: {analysis.metrics.blank_lines}",
                    f"- Linhas de código: {analysis.metrics.code_lines}",
                    f"- Tamanho máximo de linha: {analysis.metrics.max_line_length}",
                    f"- Tamanho médio de linha: {analysis.metrics.avg_line_length:.1f}",
                    f"- Complexidade: {analysis.metrics.complexity:.1f}"
                ])
                
                if analysis.functions:
                    report.append("\nFunções:")
                    for func in analysis.functions:
                        report.append(f"- {func}")
                        
                if analysis.classes:
                    report.append("\nClasses:")
                    for cls in analysis.classes:
                        report.append(f"- {cls}")
                        
        return "\n".join(report)

    def _generate_ai_suggestions(self, metrics: dict) -> List[str]:
        """
        Gera sugestões de melhoria usando IA.
        """
        try:
            if not self.ai_analyzer:
                return []
            
            # Prepara o prompt para a IA
            prompt = f"""
            Analise este projeto e forneça sugestões de melhoria em português. Detalhes do projeto:
            
            - Total de arquivos: {metrics['total_files']}
            - Total de linhas: {metrics['total_lines']}
            - Linguagens: {', '.join(f'{lang} ({count})' for lang, count in metrics['languages'].items())}
            
            Arquivos principais:
            {chr(10).join(f'- {file["path"]}: {file["lines"]} linhas ({file["language"]})' for file in metrics['files'])}
            
            Por favor, forneça:
            1. Uma análise geral do projeto
            2. Pontos fortes identificados
            3. Sugestões de melhoria específicas
            4. Recomendações de boas práticas
            """
            
            # Obtém sugestões da IA
            suggestions = self.ai_analyzer.analyze_code(prompt)
            if suggestions:
                return suggestions
            
            return ["Não foi possível gerar sugestões de IA para este projeto."]
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões de IA: {str(e)}")
            return ["Erro ao gerar sugestões de IA."]

    async def analyze_code(self, repo_url: str, target_dir: str = None) -> dict:
        """
        Analisa o código do repositório.
        
        Args:
            repo_url: URL do repositório
            target_dir: Diretório onde o repositório está clonado (opcional)
            
        Returns:
            Dicionário com o relatório e métricas
        """
        try:
            # Usa o diretório fornecido ou clona o repositório
            if not target_dir:
                target_dir = self.github.clone_repository(repo_url)
            
            # Inicializa métricas
            metrics = {
                'total_files': 0,
                'total_lines': 0,
                'total_functions': 0,
                'total_classes': 0,
                'languages': {},
                'files': [],
                'ai_suggestions': []
            }
            
            # Analisa os arquivos
            for root, _, files in os.walk(target_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Análise básica
                            lines = len(content.splitlines())
                            ext = os.path.splitext(file)[1]
                            lang = self.LANGUAGE_EXTENSIONS.get(ext, 'Unknown')
                            
                            # Atualiza métricas
                            metrics['total_files'] += 1
                            metrics['total_lines'] += lines
                            metrics['languages'][lang] = metrics['languages'].get(lang, 0) + 1
                            
                            # Adiciona detalhes do arquivo
                            metrics['files'].append({
                                'path': os.path.relpath(file_path, target_dir),
                                'lines': lines,
                                'language': lang
                            })
                            
                    except Exception as e:
                        logger.error("refactool_analyzer.file_read_failed", file=file_path)
            
            # Gera sugestões de IA
            try:
                prompt = f"""
                Analise este projeto e forneça sugestões de melhoria em português. Detalhes do projeto:
                
                - Total de arquivos: {metrics['total_files']}
                - Total de linhas: {metrics['total_lines']}
                - Linguagens: {', '.join(f'{lang} ({count})' for lang, count in metrics['languages'].items())}
                
                Arquivos principais:
                {chr(10).join(f'- {file["path"]}: {file["lines"]} linhas ({file["language"]})' for file in metrics['files'])}
                
                Por favor, forneça:
                1. Uma análise geral do projeto
                2. Pontos fortes identificados
                3. Sugestões de melhoria específicas
                4. Recomendações de boas práticas
                """
                
                ai_suggestions = await self.ai_analyzer.analyze_code(prompt)
                if isinstance(ai_suggestions, list):
                    metrics['ai_suggestions'] = ai_suggestions
                else:
                    metrics['ai_suggestions'] = [str(ai_suggestions)]
            except Exception as e:
                logger.error(f"Erro ao gerar sugestões de IA: {str(e)}")
                metrics['ai_suggestions'] = [f"Erro ao gerar sugestões de IA: {str(e)}"]
            
            # Gera relatório
            report = [
                "# Relatório de Análise do Projeto\n",
                "## Visão Geral",
                f"- Total de arquivos: {metrics['total_files']}",
                f"- Total de linhas de código: {metrics['total_lines']}",
                f"- Total de funções: {metrics['total_functions']}",
                f"- Total de classes: {metrics['total_classes']}\n",
                "## Linguagens Utilizadas"
            ]
            
            # Adiciona linguagens
            for lang, count in metrics['languages'].items():
                report.append(f"- {lang}: {count} arquivo(s)")
            
            # Adiciona arquivos
            if metrics['files']:
                report.append("\n## Arquivos Analisados")
                for file in metrics['files']:
                    report.append(f"- {file['path']}: {file['lines']} linhas ({file['language']})")
            
            # Adiciona sugestões da IA
            if metrics['ai_suggestions']:
                report.append("\n## Sugestões de Melhoria (IA)")
                for suggestion in metrics['ai_suggestions']:
                    report.append(f"\n{suggestion}")
            
            return {
                'report': "\n".join(report),
                'metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"Erro na análise: {str(e)}")
            return {
                'report': f"Erro na análise: {str(e)}",
                'metrics': None
            }

async def analyze_refactool():
    """Função principal para análise da Refactool."""
    analyzer = RefactoolAnalyzer()
    await analyzer.analyze_project()

if __name__ == "__main__":
    asyncio.run(analyze_refactool()) 