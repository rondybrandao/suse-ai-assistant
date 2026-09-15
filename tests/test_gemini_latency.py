import time

from google import genai

from app.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


def test_gemini_latency():

    prompt = """
Responda em uma frase:

O que é uma ordem de serviço?
"""

    inicio = time.perf_counter()

    response = client.interactions.create(
        model=settings.gemini_model,
        input=prompt,
    )

    tempo = time.perf_counter() - inicio

    print()
    print("=== GEMINI LATENCY ===")
    print(f"Modelo: {settings.gemini_model}")
    print(f"Tempo: {tempo:.2f}s")
    print(f"Resposta: {response.output_text}")