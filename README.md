# Ejecución de la aplicación Streamlit

## Objetivo

Este proyecto se ejecuta con **Streamlit** desde el archivo principal `app.py`. Antes de iniciar la aplicación, se debe crear un entorno virtual dentro de la carpeta del proyecto, activarlo e instalar las dependencias del archivo `requirements.txt`.

## Paso 1: Abrir el proyecto

Puedes hacerlo de dos formas:

### Opción 1: Desde un editor de código

1. Abre **Visual Studio Code** u otro editor.
2. Selecciona la carpeta del proyecto.
3. Abre una terminal dentro del editor:

   * En VS Code: **Terminal > New Terminal** (O usar **Ctr + J**).
4. Verifica que estás en la misma ubicación donde se encuentra `app.py`.

### Opción 2: Desde la terminal

1. Abre **CMD**, **PowerShell** o **Terminal**.
2. Ingresa a la carpeta del proyecto con:

```bash
cd ruta/del/proyecto
```

## Paso 2: Crear el entorno virtual

Dentro de la carpeta del proyecto, ejecuta:

```bash
python -m venv venv
```

Esto creará una carpeta llamada `venv`, donde se instalarán las dependencias del proyecto.

## Paso 3: Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

En Mac o Linux:

```bash
source venv/bin/activate
```

Cuando esté activado, normalmente aparecerá `(venv)` al inicio de la línea de la terminal.

## Paso 4: Instalar dependencias

Con el entorno virtual activado, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

## Paso 5: Ejecutar la aplicación

Finalmente, ejecuta Streamlit con:

```bash
streamlit run app.py
```

La aplicación se abrirá en el navegador. Si no se abre automáticamente, copia el enlace que aparece en la terminal, normalmente:

```bash
http://localhost:8501
```

## Nota importante

Siempre que vuelvas a trabajar en el proyecto, primero entra a la carpeta, activa el entorno virtual y luego ejecuta:

```bash
streamlit run app.py
```
