"""OpenAI (GPT) - primera llamada.  Instalar: pip install openai python-dotenv"""
import os
from dotenv import load_dotenv   # lee el archivo .env y lo carga como variables de entorno
from openai import OpenAI

load_dotenv()

# ── DÓNDE VA LA API KEY ─────────────────────────────────────────────
# En el archivo .env:  OPENAI_API_KEY=sk-...
# Aquí solo se LEE de la variable de entorno; nunca la escribas en el código.
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ── LA SOLICITUD ────────────────────────────────────────────────────
# El SDK hace por debajo: POST https://api.openai.com/v1/chat/completions
# con el header  Authorization: Bearer <tu key>
respuesta = client.chat.completions.create(
    model="gpt-4o-mini",  # los nombres de modelo cambian: confírmalo en platform.openai.com/docs/models
    messages=[
        {"role": "system", "content": "Eres un profesor claro y breve."},  # instrucciones generales
        {"role": "user", "content": "Explica qué es un LLM en una frase."},  # tu pregunta
    ],
    temperature=0.7,   # 0 = más predecible, valores altos = más variado
    max_tokens=100,    # tope de tokens de la respuesta
)

# ── CÓMO RESPONDE ───────────────────────────────────────────────────
# JSON resumido:
# {
#   "choices": [{"message": {"role": "assistant", "content": "..."}, "finish_reason": "stop"}],
#   "usage": {"prompt_tokens": 25, "completion_tokens": 30, "total_tokens": 55}
# }
print("Texto:", respuesta.choices[0].message.content)        # choices[0].message.content
print("Motivo de parada:", respuesta.choices[0].finish_reason)  # "stop" = terminó; "length" = se cortó por max_tokens
print("Tokens usados:", respuesta.usage.total_tokens)
