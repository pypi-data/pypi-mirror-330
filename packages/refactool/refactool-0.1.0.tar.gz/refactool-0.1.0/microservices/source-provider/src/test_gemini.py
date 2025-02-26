import aiohttp
import asyncio
import os
from dotenv import load_dotenv

async def test_gemini():
    # Carrega as variáveis de ambiente
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Configura a URL e os dados
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    data = {
        "contents": [{
            "parts": [{
                "text": "Explique como a IA funciona em português simples"
            }]
        }]
    }
    
    print("Enviando requisição para Gemini...")
    print(f"URL: {url}")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            print(f"Status: {response.status}")
            response_text = await response.text()
            print(f"Resposta:\n{response_text}")

if __name__ == "__main__":
    asyncio.run(test_gemini()) 