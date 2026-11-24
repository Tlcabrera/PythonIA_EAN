"""Anthropic (Claude) - primera llamada.  Instalar: pip install anthropic python-dotenv"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ── DÓNDE VA LA API KEY ─────────────────────────────────────────────
# En el archivo .env:  ANTHROPIC_API_KEY=sk-ant-...
# El SDK la envía en el header  x-api-key  (y agrega anthropic-version por ti).
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── LA SOLICITUD ────────────────────────────────────────────────────
# El SDK hace por debajo: POST https://api.anthropic.com/v1/messages
respuesta = client.messages.create(
    model="claude-haiku-5-5",  # confirma modelos vigentes en docs.claude.com
    max_tokens=100,            # OBLIGATORIO en Anthropic
    system="Eres un profesor claro y breve.",  # el system va aparte, NO dentro de messages
    messages=[
        {"role": "user", "content": "Explica qué es un LLM en una frase."},
    ],
    temperature=0.7,
)

# ── CÓMO RESPONDE ───────────────────────────────────────────────────
# JSON resumido:
# {
#   "content": [{"type": "text", "text": "..."}],
#   "stop_reason": "end_turn",
#   "usage": {"input_tokens": 25, "output_tokens": 30}
# }
# content es una LISTA de bloques (puede haber texto, uso de herramientas, etc.)
print("Texto:", respuesta.content[0].text)                 # content[0].text
print("Motivo de parada:", respuesta.stop_reason)          # "end_turn" = terminó; "max_tokens" = se cortó
print("Tokens:", respuesta.usage.input_tokens, "entrada /", respuesta.usage.output_tokens, "salida")
