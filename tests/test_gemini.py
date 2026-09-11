from google import genai

from app.config import settings


print("1 - Iniciando Gemini")

client = genai.Client(
    api_key=settings.gemini_api_key
)

print("2 - Cliente Gemini criado")

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Responda apenas: Gemini funcionando.",
)

print("3 - Resposta recebida")
print(interaction.output_text)