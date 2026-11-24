"""
Ejemplo de ingeniería de prompt con Groq.

Instalar dependencias:
    pip install groq python-dotenv

Crear un archivo .env con:
    GROQ_API_KEY=tu_api_key
"""


from groq import Groq


api_key = "" # Pega entre las comillas tu API key de Groq

if not api_key:
    raise RuntimeError("No se encontró GROQ_API_KEY. Configúralo en el archivo .env.")

client = Groq(api_key=api_key)

# La estructura de prompt ayuda a reducir ambigüedades.
instrucciones = """
Actúa como un profesor de programación principiante.
Explica el concepto solicitado en lenguaje sencillo.
Usa máximo 4 ideas y no inventes información.
"""

contexto = """
El estudiante acaba de iniciar un curso de inteligencia artificial.
Busca comprender los conceptos antes de estudiar el código técnico.
"""

# Ejemplos claros ayudan al modelo a inferir el estilo esperado.
ejemplo = """
Entrada: ¿Qué es un modelo de datos?
Salida:
- Es una estructura que organiza cómo se representan los datos.
- Define qué información contiene y cómo se relaciona.
- Sirve como base para trabajar con aplicaciones y bases de datos.
"""

formatosalida = """
Responde únicamente con este formato:

Tema: <nombre del tema>
Explicación:
- <idea 1>
- <idea 2>
- <idea 3>
Resumen: <máximo 15 palabras>
"""

reclamo = "Explica qué es un LLM y por qué es útil."

prompt_completo = f"""
INSTRUCCIONES
{instrucciones}

CONTEXTO
{contexto}

EJEMPLO
{ejemplo}

FORMATO DE SALIDA
{formatosalida}

RECLAMO
{reclamo}
"""

respuesta = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "Eres un asistente especializado en explicar conceptos técnicos de forma clara.",
        },
        {"role": "user", "content": prompt_completo},
    ],
    temperature=0.2,
    max_tokens=180,
)

texto_respuesta = respuesta.choices[0].message.content

print("=== PROMPT ENVIADO ===")
print(prompt_completo)
print("=== RESPUESTA ===")
print(texto_respuesta)
print("\nMotivo de parada:", respuesta.choices[0].finish_reason)
print("Tokens usados:", respuesta.usage.total_tokens)