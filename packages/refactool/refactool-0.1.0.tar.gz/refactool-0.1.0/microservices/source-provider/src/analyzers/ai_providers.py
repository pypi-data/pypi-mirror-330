"""
Provedores de IA para análise de código.
"""

from abc import ABC, abstractmethod
import json
from typing import Dict, List, Optional
import aiohttp
import structlog
import asyncio
import logging
import os
import traceback

logger = structlog.get_logger()

class AIProvider(ABC):
    """Classe base para provedores de IA."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def start(self):
        """Inicializa o provedor."""
        if not self._session:
            self._session = aiohttp.ClientSession()
            logger.info(f"{self.__class__.__name__}.started")
    
    async def stop(self):
        """Finaliza o provedor."""
        if self._session:
            await self._session.close()
            self._session = None
            logger.info(f"{self.__class__.__name__}.stopped")
    
    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> str:
        """Gera uma completação para o prompt."""
        pass

class DeepSeekProvider(AIProvider):
    """Provedor usando DeepSeek."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: str = "https://api.deepseek.com/v1/completions",
        model: str = "deepseek-coder-33b-instruct"
    ):
        super().__init__(api_key)
        self.api_url = api_url
        self.model = model
    
    async def complete(self, prompt: str, **kwargs) -> str:
        """Gera uma completação usando DeepSeek."""
        if not self._session:
            await self.start()
            
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.95),
            "stream": False
        }
        
        try:
            async with self._session.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get("timeout", 30)
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result["choices"][0]["text"]
                
        except Exception as e:
            logger.error(
                "deepseek_provider.completion_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            raise

class OllamaProvider(AIProvider):
    """Provedor usando Ollama."""
    
    def __init__(
        self,
        model: str = "llama2:13b",
        api_url: str = "http://localhost:11434/api/generate",
        timeout: int = 60
    ):
        super().__init__()
        self.api_url = api_url
        self.model = model
        self.timeout = timeout
        
    async def complete(self, prompt: str, **kwargs) -> str:
        """Gera uma completação usando Ollama."""
        if not self._session:
            await self.start()
            
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        logger.info(
            "OllamaProvider.sending_request",
            model=self.model,
            prompt_length=len(prompt)
        )
        
        try:
            async with self._session.post(
                self.api_url,
                json=data,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result["response"]
                
        except Exception as e:
            logger.error(
                "ollama_provider.completion_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            raise

class OpenAIProvider:
    """Provedor OpenAI."""
    
    def __init__(
        self,
        api_key: str = None,
        api_url: str = "https://api.openai.com/v1/chat/completions",
        model: str = "gpt-3.5-turbo"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_url = api_url
        self.model = model
        self.session = None
        
    async def start(self):
        """Inicializa o provedor."""
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
    async def stop(self):
        """Finaliza o provedor."""
        if self.session:
            await self.session.close()
            
    async def analyze_code(self, content: str) -> List[str]:
        """
        Analisa o código usando OpenAI.
        
        Args:
            content: Conteúdo a ser analisado
            
        Returns:
            Lista de sugestões
        """
        try:
            # Prepara o prompt
            messages = [
                {"role": "system", "content": "Você é um analista de código experiente que fornece sugestões de melhoria em português do Brasil."},
                {"role": "user", "content": content}
            ]
            
            # Faz a requisição
            async with self.session.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            ) as response:
                result = await response.json()
                
                if "choices" in result and result["choices"]:
                    suggestions = result["choices"][0]["message"]["content"].split("\n")
                    return [s for s in suggestions if s.strip()]
                    
                return ["Não foi possível gerar sugestões."]
                
        except Exception as e:
            logger.error(f"Erro na análise OpenAI: {str(e)}")
            return [f"Erro na análise: {str(e)}"]

class GeminiProvider:
    """Provedor usando Google Gemini."""
    
    def __init__(
        self,
        api_key: str = None,
        api_url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        model: str = "gemini-2.0-flash"
    ):
        if not api_key:
            raise ValueError("API key é obrigatória para o Gemini")
            
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.session = None
        
        logger.info("GeminiProvider inicializado", 
                   model=model,
                   api_url=api_url,
                   api_key_length=len(api_key))
        
    async def start(self):
        """Inicializa o provedor."""
        self.session = aiohttp.ClientSession()
        logger.info("Sessão Gemini iniciada")
        
    async def stop(self):
        """Finaliza o provedor."""
        if self.session:
            await self.session.close()
            logger.info("Sessão Gemini finalizada")
            
    async def analyze_code(self, content: str) -> List[str]:
        """
        Analisa o código usando Gemini.
        
        Args:
            content: Conteúdo a ser analisado
            
        Returns:
            Lista de sugestões
        """
        try:
            logger.info("Iniciando análise Gemini", content_length=len(content))
            
            # Prepara o prompt
            data = {
                "contents": [{
                    "parts": [{
                        "text": f"""Por favor, analise este código e forneça sugestões de melhoria em português do Brasil:

{content}

Forneça suas sugestões em formato de lista, focando em:
1. Boas práticas de programação
2. Possíveis problemas de segurança
3. Oportunidades de otimização
4. Melhorias na estrutura do projeto"""
                    }]
                }]
            }
            
            # Faz a requisição
            url = f"{self.api_url}?key={self.api_key}"
            logger.info("Enviando requisição para Gemini", url=url)
            
            async with self.session.post(url, json=data) as response:
                response_text = await response.text()
                logger.info("Resposta Gemini recebida", 
                          status=response.status,
                          response_text=response_text)
                
                result = await response.json()
                
                if "candidates" in result and result["candidates"]:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    suggestions = text.split("\n")
                    valid_suggestions = [s for s in suggestions if s.strip()]
                    logger.info("Sugestões geradas", count=len(valid_suggestions))
                    return valid_suggestions
                    
                logger.warning("Sem sugestões na resposta Gemini", result=result)
                return ["Não foi possível gerar sugestões."]
                
        except Exception as e:
            logger.error("Erro na análise Gemini", 
                        error=str(e),
                        error_type=type(e).__name__,
                        traceback=traceback.format_exc())
            return [f"Erro na análise: {str(e)}"] 