"""
Groq (Llama y otros modelos abiertos, plan gratuito) - primera llamada.
Instalar: pip install groq python-dotenv
"""

from groq import Groq

API_KEY="" # Pega entre las comillas tu API key de Groq

# — DÓNDE VA LA API KEY —
# En el archivo .env: GROQ_API_KEY=gsk_...
# (se crea gratis en console.groq.com/keys)
# El SDK la envía como Authorization: Bearer <tu key>.

client = Groq(api_key=API_KEY)

# — LA SOLICITUD —
# Groq usa el mismo formato que OpenAI:
# POST https://api.groq.com/openai/v1/chat/completions

respuesta = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    # (o los modelos cambian: revisa console.groq.com/docs/models)

    messages=[
        {"role": "system", "content": "Eres un profesor claro y breve."},
        {"role": "user", "content": "Explica qué es un LLM en una frase."},
    ],
    temperature=0.7,
    max_tokens=100,
)

# — CÓMO RESPONDE —
# Misma forma que OpenAI:
# {"choices": [{"message": {"role": "assistant", "content": "..."},
# "finish_reason": "stop"}],
# "usage": {"prompt_tokens": 25, "completion_tokens": 30, "total_tokens": 55}}

print("Texto:", respuesta.choices[0].message.content)
print("Motivo de parada:", respuesta.choices[0].finish_reason)
print("Tokens usados:", respuesta.usage.total_tokens)