"""
Ingeniería de prompt con Groq + parámetros.

Instalar dependencias:
    pip install groq
"""

import json
import time
from collections import Counter

from groq import Groq

api_key = ""  # Pega entre las comillas tu API key de Groq

if not api_key:
    raise RuntimeError("Falta la API key. Pégala en la variable api_key.")

client = Groq(api_key=api_key)

MODELO = "openai/gpt-oss-120b"
REPETICIONES = 3  # veces que se repite cada configuración
PAUSA = 0.5  # segundos entre llamadas (cuida el límite del plan gratuito)

# ---------------------------------------------------------------------------
# PROMPT EN 5 PARTES (el mismo para todos los experimentos)
# ---------------------------------------------------------------------------
instrucciones = """
Clasifica el reclamo de un cliente.
Indica el tema, la urgencia y escribe una respuesta breve para el cliente
(máximo 1 frase, tono amable). No inventes datos que el cliente no dio.
"""

contexto = """
Eres analista de servicio al cliente de una tienda de bicicletas.
La clasificación la leerá el jefe de soporte para priorizar casos.
"""

# Ejemplos variados: cubren casos distintos para que el modelo no copie un solo patrón.
ejemplos = """
<example>
Entrada: Llegó rota la llanta.
Salida: {"tema": "daño", "urgencia": "alta", "respuesta_cliente": "Lamentamos el daño; enviaremos una llanta nueva esta semana."}
</example>
<example>
Entrada: ¿Tienen cascos talla M?
Salida: {"tema": "consulta", "urgencia": "baja", "respuesta_cliente": "Sí, te confirmamos disponibilidad en un momento."}
</example>
<example>
Entrada: Me cobraron dos veces el mismo pedido.
Salida: {"tema": "cobro", "urgencia": "alta", "respuesta_cliente": "Revisaremos el cobro doble y te devolveremos el excedente."}
</example>
"""

formato_salida = """
Responde únicamente con JSON, sin texto adicional ni bloques de código:
{"tema": "<una o dos palabras>", "urgencia": "alta|media|baja", "respuesta_cliente": "<1 frase>"}
"""

# Reclamo ambiguo a propósito: así la urgencia puede variar entre llamadas.
reclamo = "Me llegó la bicicleta, pero el timbre no suena como en la foto. No sé si vale la pena reclamar."

prompt_completo = f"""
<instrucciones>{instrucciones}</instrucciones>

<contexto>{contexto}</contexto>

<examples>{ejemplos}</examples>

<formato_salida>{formato_salida}</formato_salida>

<reclamo>
{reclamo}
</reclamo>
"""

SYSTEM = "Eres un asistente que clasifica reclamos y responde siempre con JSON válido."


# ---------------------------------------------------------------------------
# FUNCIONES
# ---------------------------------------------------------------------------
def extraer_json(texto: str):
    """Intenta convertir la respuesta en dict. Devuelve None si no es JSON válido."""
    limpio = texto.replace("```json", "").replace("```", "").strip()
    inicio, fin = limpio.find("{"), limpio.rfind("}")
    if inicio == -1 or fin == -1:
        return None
    try:
        return json.loads(limpio[inicio : fin + 1])
    except json.JSONDecodeError:
        return None


def llamar(temperature: float, top_p: float, max_tokens: int) -> dict:
    """Una llamada a Groq con los parámetros indicados."""
    r = client.chat.completions.create(
        model=MODELO,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt_completo},
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    texto = (r.choices[0].message.content or "").strip()
    return {
        "texto": texto,
        "json": extraer_json(texto),
        "motivo": r.choices[0].finish_reason,  # "stop" = terminó; "length" = lo cortó max_tokens
        "tokens": r.usage.total_tokens,
    }


RESUMEN = []  # aquí se acumulan las estadísticas de cada configuración


def correr_experimento(titulo: str, objetivo: str, configuraciones: list):
    print("\n" + "=" * 78)
    print(titulo)
    print(objetivo)
    print("=" * 78)

    for cfg in configuraciones:
        t, p, m = cfg["temperature"], cfg["top_p"], cfg["max_tokens"]
        etiqueta = f"temperature={t} | top_p={p} | max_tokens={m}"
        print(f"\n--- {cfg['nombre']}  ({etiqueta})")

        validos, temas, urgencias, motivos, tokens = 0, Counter(), Counter(), Counter(), []

        for i in range(1, REPETICIONES + 1):
            try:
                res = llamar(t, p, m)
            except Exception as e:  # límite de uso, red, parámetro no soportado, etc.
                print(f"  [{i}] ERROR: {e}")
                continue

            motivos[res["motivo"]] += 1
            tokens.append(res["tokens"])
            datos = res["json"]

            if datos:
                validos += 1
                temas[datos.get("tema", "?")] += 1
                urgencias[datos.get("urgencia", "?")] += 1
                print(f"  [{i}] {datos.get('tema')} | {datos.get('urgencia')} | {datos.get('respuesta_cliente')}")
            else:
                vista = res["texto"].replace("\n", " ")[:90]
                print(f"  [{i}] JSON INVÁLIDO ({res['motivo']}): {vista}")

            time.sleep(PAUSA)

        RESUMEN.append(
            {
                "nombre": cfg["nombre"],
                "config": f"T={t} P={p} M={m}",
                "validos": f"{validos}/{REPETICIONES}",
                "temas": len(temas),
                "urgencias": len(urgencias),
                "motivos": ",".join(f"{k}x{v}" for k, v in motivos.items()) or "-",
                "tokens": round(sum(tokens) / len(tokens)) if tokens else 0,
            }
        )


def cfg(nombre, temperature=0.7, top_p=1.0, max_tokens=200):
    return {"nombre": nombre, "temperature": temperature, "top_p": top_p, "max_tokens": max_tokens}


# ---------------------------------------------------------------------------
# EXPERIMENTOS (en cada uno cambia UN solo parámetro)
# ---------------------------------------------------------------------------
print("=== PROMPT ENVIADO (igual en todas las llamadas) ===")
print(prompt_completo)

# 1) temperature: de predecible a variado (top_p y max_tokens fijos)
correr_experimento(
    "EXPERIMENTO 1 · temperature",
    "Qué observar: con 0 las salidas casi no cambian; con 1.5 cambia la redacción, "
    "y puede cambiar la urgencia o romperse el JSON.",
    [
        cfg("Determinista", temperature=0.0),
        cfg("Equilibrado", temperature=0.7),
        cfg("Muy variable", temperature=1.5),
    ],
)

# 2) top_p: recorta las opciones improbables (temperature fija en 1.0)
correr_experimento(
    "EXPERIMENTO 2 · top_p (temperature fija en 1.0)",
    "Qué observar: top_p bajo recorta la 'cola' de opciones raras aunque la temperature sea alta.",
    [
        cfg("Núcleo estrecho", temperature=1.0, top_p=0.1),
        cfg("Núcleo medio", temperature=1.0, top_p=0.5),
        cfg("Sin recorte", temperature=1.0, top_p=1.0),
    ],
)

# 3) max_tokens: el tope corta la respuesta, no la hace más concisa
correr_experimento(
    "EXPERIMENTO 3 · max_tokens (temperature fija en 0.2)",
    "Qué observar: con un tope bajo el JSON queda cortado (finish_reason = length) y no se puede parsear.",
    [
        cfg("Tope muy bajo", temperature=0.2, max_tokens=20),
        cfg("Tope justo", temperature=0.2, max_tokens=60),
        cfg("Tope holgado", temperature=0.2, max_tokens=250),
    ],
)

# 4) Perfiles completos: combinaciones pensadas para un tipo de tarea
correr_experimento(
    "EXPERIMENTO 4 · perfiles según la tarea",
    "Idea: la configuración se elige según el objetivo, no hay un valor único 'mejor'.",
    [
        cfg("Clasificador (datos para un sistema)", temperature=0.0, top_p=1.0, max_tokens=150),
        cfg("Asistente (conversación)", temperature=0.7, top_p=0.9, max_tokens=150),
        cfg("Lluvia de ideas", temperature=1.2, top_p=0.95, max_tokens=150),
    ],
)

# ---------------------------------------------------------------------------
# TABLA FINAL
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("RESUMEN (por configuración, sobre", REPETICIONES, "repeticiones)")
print("=" * 78)
print(f"{'Configuración':<38}{'Parámetros':<20}{'JSON':<6}{'Temas':<7}{'Urg.':<6}{'Motivo':<14}{'Tok'}")
for fila in RESUMEN:
    print(
        f"{fila['nombre'][:36]:<38}{fila['config']:<20}{fila['validos']:<6}"
        f"{fila['temas']:<7}{fila['urgencias']:<6}{fila['motivos']:<14}{fila['tokens']}"
    )

print(
    "\nCómo leer la tabla:"
    "\n- JSON: respuestas que se pudieron parsear (debería ser todas en un clasificador)."
    "\n- Temas / Urg.: valores distintos obtenidos; 1 = estable, más de 1 = variación entre llamadas."
    "\n- Motivo: 'stop' = el modelo terminó; 'length' = lo cortó max_tokens."
    "\n- Tok: promedio de tokens totales (costo) por llamada."
)
