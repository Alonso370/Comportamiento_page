from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import datetime
from textwrap import dedent

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from .config import DEFAULT_RECOMMENDATION_MODEL, SEDES
from .data_loader import add_urgency, read_knowledge_sources

load_dotenv()

ChatMessage = dict[str, str]


def get_openai_config() -> tuple[str | None, str]:
    """Lee la API Key desde Streamlit secrets o variables de entorno."""
    api_key = None
    model = DEFAULT_RECOMMENDATION_MODEL

    try:
        api_key = st.secrets.get("OPENAI_API_KEY", None)
        model = st.secrets.get("OPENAI_MODEL", DEFAULT_RECOMMENDATION_MODEL)
    except Exception:
        pass

    api_key = api_key or os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", model)
    return api_key, model



def get_api_status(force_demo: bool = False) -> tuple[str, str]:
    """Devuelve (etiqueta, modo) para mostrar el estado de conexión OpenAI."""
    if force_demo:
        return "Modo demo activado", "demo"
    api_key, model = get_openai_config()
    if api_key:
        return f"OpenAI conectado · {model}", f"openai:{model}"
    return "Sin API Key · modo demo automático", "demo_sin_api_key"


def dataframe_to_context(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "Sin datos disponibles."
    safe_df = df.copy().tail(max_rows)
    for col in safe_df.columns:
        safe_df[col] = safe_df[col].astype(str).str.slice(0, 350)
    return safe_df.to_markdown(index=False)


def build_system_instructions(
    sede: str,
    complaints: pd.DataFrame,
    surveys: pd.DataFrame,
    manual_context: str = "",
) -> str:
    complaints = add_urgency(complaints)
    surveys = add_urgency(surveys)
    sede_cfg = SEDES[sede]
    knowledge = read_knowledge_sources()

    return dedent(
        f"""
        Actúa como consultor de gestión de personas y liderazgo para la empresa ficticia Dambo, rubro retail.
        Tu usuario es un jefe de sucursal que conversa contigo para obtener recomendaciones concretas, cortas y accionables.

        Sede analizada: {sede}
        Jefe responsable: {sede_cfg['jefe']}
        Problemática inicial: {sede_cfg['problematica']}

        Objetivo:
        - Analizar reclamos de clientes, quejas de trabajadores y encuesta de salida diaria.
        - Proponer acciones para mejorar liderazgo, atención al cliente, productividad y seguridad psicológica.
        - Basar las recomendaciones en Google Project Oxygen, Proyecto Aristóteles y seguridad psicológica.
        - Indicar con quién debe hablar el líder, qué herramienta usar y qué recordatorio debe cumplir.

        Datos de reclamos:
        {dataframe_to_context(complaints)}

        Datos de encuesta de empleados:
        {dataframe_to_context(surveys)}

        Contexto adicional ingresado manualmente:
        {manual_context or 'No se agregó contexto manual.'}

        Artículos o notas internas disponibles:
        {knowledge or 'Todavía no se cargaron artículos internos. Usa conocimiento general sobre liderazgo y seguridad psicológica.'}

        Responde siempre en español. Cada recomendación debe incluir: acción, responsable, persona/equipo con quien hablar,
        herramienta de gestión y evidencia del dato. No inventes nombres fuera de los datos. Si faltan datos, dilo.
        INSTRUCCIÓN DE PRIVACIDAD OBLIGATORIA:
            - No reveles al jefe quién registró un reclamo, queja o comentario.
            - No menciones nombres de colaboradores, clientes o personas involucradas como fuente del reclamo.
            - Si el jefe pregunta “quién se quejó”, “quién puso el reclamo” o algo similar, responde que por confidencialidad no puedes revelar identidades.
            - Tu función es ayudar al jefe a entender el problema, priorizarlo y proponer acciones concretas para solucionarlo.
            - Puedes mencionar áreas, patrones o tipos de reclamo, pero no identidades individuales.
        """
    ).strip()


def build_prompt(sede: str, complaints: pd.DataFrame, surveys: pd.DataFrame, manual_context: str = "") -> str:
    return dedent(
        f"""
        {build_system_instructions(sede, complaints, surveys, manual_context)}

        Entrega la respuesta con esta estructura exacta:
        1. Diagnóstico breve de la sede.
        2. Recomendaciones críticas.
        3. Recomendaciones altas.
        4. Recomendaciones medias.
        5. Agenda sugerida de 7 días.
        6. Recordatorios diarios para el líder.
        """
    ).strip()


def messages_to_api_input(messages: list[ChatMessage]) -> list[dict[str, str]]:
    return [{"role": msg["role"], "content": msg["content"]} for msg in messages if msg["role"] in {"user", "assistant"}]


def fallback_recommendations(sede: str, complaints: pd.DataFrame, surveys: pd.DataFrame) -> str:
    sede_cfg = SEDES[sede]
    top_complaints = "mala atención y poca retroalimentación"
    if not complaints.empty and "tipo_reclamo" in complaints.columns:
        counts = complaints["tipo_reclamo"].astype(str).value_counts()
        if not counts.empty:
            top_complaints = ", ".join(counts.head(2).index.tolist())

    avg_happiness = None
    avg_security = None
    if not surveys.empty:
        avg_happiness = round(float(surveys.get("felicidad", pd.Series([0])).mean()), 1)
        avg_security = round(float(surveys.get("seguridad_psicologica", pd.Series([0])).mean()), 1)

    return f"""
### 1. Diagnóstico breve de la sede
La {sede} muestra señales de riesgo en **{top_complaints}**. Problemática base: {sede_cfg['problematica']}
{f'Felicidad promedio: {avg_happiness}/5. Seguridad psicológica promedio: {avg_security}/5.' if avg_happiness else 'Aún hay pocos datos de encuesta para medir clima interno.'}

### 2. Recomendaciones críticas
- **Acción:** realizar una conversación 1 a 1 con los colaboradores involucrados en quejas de trato o atención.
  **Responsable:** jefe de sucursal. **Herramienta:** feedback SBI: situación, comportamiento, impacto.
  **Evidencia:** reclamos recientes asociados a atención y liderazgo.

### 3. Recomendaciones altas
- **Acción:** ejecutar una microcapacitación de 20 minutos sobre manejo de cliente difícil, escucha activa y cierre empático.
  **Responsable:** jefe de sucursal + líder de turno. **Herramienta:** role play con casos reales.
  **Evidencia:** baja puntuación de cliente o comentarios de mala atención.

- **Acción:** abrir un espacio de seguridad psicológica al final del turno.
  **Responsable:** jefe de sucursal. **Herramienta:** pregunta de cierre: “¿qué error o dificultad podemos aprender hoy sin culpar a nadie?”.
  **Evidencia:** comentarios de presión, miedo a reportar errores o poca confianza.

### 4. Recomendaciones medias
- **Acción:** publicar prioridades diarias en una pizarra visible.
  **Responsable:** líder de turno. **Herramienta:** checklist diario de objetivos y atención.
  **Evidencia:** señales de baja claridad y baja productividad.

### 5. Agenda sugerida de 7 días
| Día | Acción | Resultado esperado |
|---|---|---|
| Día 1 | Revisar reclamos y seleccionar 3 casos críticos | Foco claro de intervención |
| Día 2 | Conversaciones 1 a 1 | Comprender causas reales |
| Día 3 | Role play de atención al cliente | Mejorar trato y empatía |
| Día 4 | Focus group corto con trabajadores | Detectar barreras internas |
| Día 5 | Definir 3 compromisos de liderazgo Oxygen | Mejorar estilo de liderazgo |
| Día 6 | Medir felicidad y seguridad psicológica | Ver avance del clima |
| Día 7 | Retroalimentación grupal sin culpas | Aprendizaje y seguimiento |

### 6. Recordatorios diarios para el líder
- Preguntar antes de juzgar.
- Reconocer una conducta positiva por turno.
- Dar instrucciones claras antes de hora punta.
- Cerrar el día con una pregunta de aprendizaje.
"""


def demo_chat_reply(
    user_message: str,
    sede: str,
    complaints: pd.DataFrame,
    surveys: pd.DataFrame,
) -> str:
    """Respuestas demo contextuales para mantener el chat interactivo sin API."""
    msg = user_message.lower()
    sede_cfg = SEDES[sede]

    if any(term in msg for term in ["diagnóstico", "diagnostico", "resumen", "situación", "situacion", "informe"]):
        return fallback_recommendations(sede, complaints, surveys)

    if any(term in msg for term in ["reclamo", "queja", "cliente", "atención", "atencion"]):
        top = "mala atención"
        if not complaints.empty and "tipo_reclamo" in complaints.columns:
            counts = complaints["tipo_reclamo"].astype(str).value_counts()
            if not counts.empty:
                top = counts.index[0]
        return dedent(
            f"""
            En **{sede}** el reclamo más frecuente es **{top}**.

            **Acciones sugeridas:**
            1. Revisar hoy los 3 casos más recientes con el líder de turno.
            2. Hacer un role play de 15 minutos sobre escucha activa y cierre empático.
            3. Registrar qué aprendió el equipo al cierre del turno.

            **Herramienta:** feedback SBI (situación, comportamiento, impacto).
            **Evidencia:** datos de reclamos cargados en el dashboard.
            """
        ).strip()

    if any(term in msg for term in ["encuesta", "clima", "felicidad", "seguridad", "psicológica", "psicologica"]):
        avg_h = round(float(surveys["felicidad"].mean()), 1) if not surveys.empty else None
        avg_s = round(float(surveys["seguridad_psicologica"].mean()), 1) if not surveys.empty else None
        return dedent(
            f"""
            **Clima laboral en {sede}:**
            - Felicidad promedio: {avg_h or 'sin datos'}/5
            - Seguridad psicológica: {avg_s or 'sin datos'}/5

            **Próximos pasos:**
            - Abrir una conversación 1 a 1 con quienes puntúan 2 o menos.
            - Cerrar el turno con: "¿qué error podemos aprender hoy sin culpar a nadie?"
            - Agendar un focus group de 30 minutos la próxima semana.

            Problemática base: {sede_cfg['problematica']}
            """
        ).strip()

    if any(term in msg for term in ["agenda", "7 días", "7 dias", "semana", "plan"]):
        return dedent(
            """
            **Agenda sugerida de 7 días:**
            | Día | Acción | Resultado esperado |
            |---|---|---|
            | Día 1 | Revisar reclamos críticos | Foco de intervención |
            | Día 2 | Conversaciones 1 a 1 | Comprender causas reales |
            | Día 3 | Role play de atención | Mejorar trato y empatía |
            | Día 4 | Focus group corto | Detectar barreras internas |
            | Día 5 | Compromisos Oxygen | Mejorar estilo de liderazgo |
            | Día 6 | Medir clima laboral | Ver avance |
            | Día 7 | Retroalimentación grupal | Aprendizaje y seguimiento |
            """
        ).strip()

    return dedent(
        f"""
        Entiendo tu consulta sobre **{sede}**. Problemática base: {sede_cfg['problematica']}

        Puedo ayudarte con:
        - Un **diagnóstico completo** (escribe "dame un diagnóstico").
        - Acciones sobre **reclamos y atención al cliente**.
        - Mejoras de **clima laboral y seguridad psicológica**.
        - Una **agenda de 7 días** priorizada.

        > Modo demo activo. Configura `OPENAI_API_KEY` para respuestas más personalizadas con IA.
        """
    ).strip()


def stream_chat_reply(
    messages: list[ChatMessage],
    sede: str,
    complaints: pd.DataFrame,
    surveys: pd.DataFrame,
    manual_context: str = "",
    force_demo: bool = False,
) -> Iterator[str]:
    """
    Generador de tokens para chat interactivo.
    Conserva la conexión OpenAI existente; usa demo si no hay API Key o force_demo.
    """
    if not messages or messages[-1]["role"] != "user":
        return

    user_message = messages[-1]["content"]
    if force_demo:
        yield demo_chat_reply(user_message, sede, complaints, surveys)
        return

    api_key, model = get_openai_config()
    if not api_key:
        yield demo_chat_reply(user_message, sede, complaints, surveys)
        return

    instructions = build_system_instructions(sede, complaints, surveys, manual_context)
    api_input = messages_to_api_input(messages)

    try:
        client = OpenAI(api_key=api_key)
        with client.responses.stream(
            model=model,
            instructions=instructions,
            input=api_input,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
    except Exception as exc:
        yield (
            demo_chat_reply(user_message, sede, complaints, surveys)
            + f"\n\n> Nota técnica: no se pudo llamar a la API y se usó modo demo. Detalle: {exc}"
        )


def chat_reply(
    messages: list[ChatMessage],
    sede: str,
    complaints: pd.DataFrame,
    surveys: pd.DataFrame,
    manual_context: str = "",
    force_demo: bool = False,
) -> tuple[str, str]:
    """Respuesta completa del chat (sin streaming)."""
    chunks = list(
        stream_chat_reply(messages, sede, complaints, surveys, manual_context, force_demo=force_demo)
    )
    text = "".join(chunks)
    _, mode = get_api_status(force_demo=force_demo)
    if force_demo or not get_openai_config()[0]:
        return text, mode
    if "Nota técnica: no se pudo llamar a la API" in text:
        return text, "demo_error_api"
    return text, f"openai:{get_openai_config()[1]}"


def generate_recommendations(
    sede: str,
    complaints: pd.DataFrame,
    surveys: pd.DataFrame,
    manual_context: str = "",
    force_demo: bool = False,
) -> tuple[str, str]:
    """
    Devuelve (texto_recomendacion, modo_usado).
    Si no hay API Key o hay error, usa modo demo para que el Streamlit siempre funcione.
    """
    if force_demo:
        return fallback_recommendations(sede, complaints, surveys), "demo"

    api_key, model = get_openai_config()
    if not api_key:
        return fallback_recommendations(sede, complaints, surveys), "demo_sin_api_key"

    prompt = build_prompt(sede, complaints, surveys, manual_context)
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions="Eres un consultor experto en liderazgo, retail, clima laboral y experiencia del cliente.",
            input=prompt,
        )
        return response.output_text, f"openai:{model}"
    except Exception as exc:
        return (
            fallback_recommendations(sede, complaints, surveys)
            + f"\n\n> Nota técnica: no se pudo llamar a la API y se usó modo demo. Detalle: {exc}",
            "demo_error_api",
        )


def save_recommendation(sede: str, content: str) -> str:
    from .config import PROCESSED_DIR

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recomendaciones_{sede.lower().replace(' ', '_')}_{stamp}.txt"
    path = PROCESSED_DIR / filename
    path.write_text(content, encoding="utf-8")
    return str(path)
