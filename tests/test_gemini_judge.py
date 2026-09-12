from google import genai

from app.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Responda apenas: TESTE FUNCIONANDO",
    generation_config={
        "thinking_level": "minimal",
    },
)

print()
print("========================================")
print("TESTE GEMINI JUDGE")
print("========================================")

print("Status:")
print(interaction.status)

print()
print("Output:")
print(repr(interaction.output_text))

print()
print("Uso de tokens:")
print(interaction.usage)

print("========================================")