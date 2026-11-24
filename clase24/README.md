# Clase 24: uso de los scripts de Groq

## Descripcion de la clase

Esta clase presenta los primeros pasos para utilizar la API de Groq desde Python.
Los ejemplos muestran como realizar una solicitud sencilla a un modelo de lenguaje
y como estructurar un prompt con instrucciones, contexto, ejemplos y formato de salida.

Esta carpeta contiene dos scripts de Python que utilizan la API de Groq:

- `mi_primer_prompt.py`: realiza una primera llamada sencilla al modelo.
- `ingenieria_prompt.py`: muestra una solicitud estructurada con instrucciones, contexto y formato de salida.

## 1. Abrir la carpeta

Desde la terminal, entra en la carpeta del proyecto:

```bash
cd /workspaces/PythonIA_EAN/clase24
```

Si estás trabajando desde otro entorno, reemplaza la ruta por la ubicación de esta carpeta.

## 2. Crear el entorno virtual

### Linux, macOS o Codespaces

```bash
python3 -m venv .venv
```

### Windows

Desde PowerShell o CMD:

```powershell
py -m venv .venv
```

El entorno virtual se crea dentro de la carpeta `clase24` en una carpeta llamada `.venv`.

## 3. Activar el entorno virtual

### Linux, macOS o Codespaces

```bash
source .venv/bin/activate
```

### Windows con PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows con CMD

```bat
.venv\Scripts\activate.bat
```

Cuando el entorno esté activo, la terminal mostrará `(.venv)` al inicio de la línea.

## 4. Instalar la librería de Groq

Con el entorno activo, ejecuta:

```bash
python -m pip install --upgrade pip
python -m pip install groq python-dotenv
```

Estas librerías permiten utilizar el SDK de Groq y cargar variables desde un archivo `.env`.

## 5. Obtener y configurar la API Key

1. Crea una cuenta en https://console.groq.com.
2. Genera una API Key en https://console.groq.com/keys.
3. Copia la clave.

Los scripts actuales utilizan una variable dentro del archivo Python:

### En `mi_primer_prompt.py`

Busca:

```python
API_KEY = ""
```

Reemplázala por:

```python
API_KEY = "tu_api_key"
```

### En `ingenieria_prompt.py`

Busca:

```python
api_key = ""
```

Reemplázala por:

```python
api_key = "tu_api_key"
```

No publiques ni compartas tu API Key. No subas al repositorio archivos que contengan la clave real.

## 6. Ejecutar los scripts

Asegúrate de que el entorno virtual esté activo y ejecuta:

```bash
python mi_primer_prompt.py
```

Para ejecutar el segundo ejemplo:

```bash
python ingenieria_prompt.py
```

Puedes ejecutar ambos desde la carpeta `clase24`:

```bash
python mi_primer_prompt.py && python ingenieria_prompt.py
```

## 7. Desactivar el entorno virtual

Cuando termines:

```bash
deactivate
```
