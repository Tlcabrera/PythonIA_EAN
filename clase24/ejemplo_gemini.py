"""Google (Gemini) - primera llamada.  Instalar: pip install google-genai python-dotenv"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ── DÓNDE VA LA API KEY ─────────────────────────────────────────────
# En el archivo .env:  GEMINI_API_KEY=AIza...   (se crea gratis en aistudio.google.com/apikey)
# El SDK la envía en el header  x-goog-api-key.
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# ── LA SOLICITUD ────────────────────────────────────────────────────
# El SDK hace por debajo:
# POST https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent
respuesta = client.models.generate_content(
    model="gemini-2.5-flash",  # confirma modelos vigentes en ai.google.dev/gemini-api/docs/models
    contents="Explica qué es un LLM en una frase.",  # aquí va tu prompt ("contents", no "messages")
    config=types.GenerateContentConfig(
        system_instruction="Eres un profesor claro y breve.",
        temperature=0.7,
        max_output_tokens=100,   # en Gemini se llama max_output_tokens
    ),
)

# ── CÓMO RESPONDE ───────────────────────────────────────────────────
# JSON resumido:
# {
#   "candidates": [{"content": {"parts": [{"text": "..."}]}, "finishReason": "STOP"}],
#   "usageMetadata": {"promptTokenCount": 25, "totalTokenCount": 55}
# }
# El SDK ofrece el atajo .text para candidates[0].content.parts[0].text
print("Texto:", respuesta.text)
print("Motivo de parada:", respuesta.candidates[0].finish_reason)
print("Tokens usados:", respuesta.usage_metadata.total_token_count)
