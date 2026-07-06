from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.config import APP_NAME, SEDES
from src.data_loader import COMPLAINT_COLUMNS, SURVEY_COLUMNS, append_row_csv, make_sample_files
from src.styles import apply_styles, hero, card

st.set_page_config(
    page_title=f"Encuesta y quejas · {APP_NAME}",
    page_icon="📝",
    layout="wide",
)

apply_styles()
make_sample_files()

hero(
    "Encuesta y quejas Dambo",
    "Registra percepciones de trabajadores al salir de la jornada y quejas de clientes o empleados. "
    "La información guardada alimenta los KPIs y el asistente de liderazgo.",
)

intro1, intro2 = st.columns(2)
with intro1:
    card(
        "Encuesta de salida",
        "Sirve para medir felicidad, seguridad psicológica, claridad de objetivos, feedback del líder y carga laboral percibida."
    )
with intro2:
    card(
        "Quejas y reclamos",
        "Permite registrar situaciones de mala atención, liderazgo, comunicación o productividad para analizarlas y generar acciones."
    )

form_tab, complaint_tab = st.tabs(
    ["🙂 Encuesta de salida del empleado", "📣 Formulario de quejas/reclamos"]
)

with form_tab:
    st.subheader("Encuesta de salida laboral")

    with st.form("employee_exit_survey", clear_on_submit=True):
        st.markdown("#### Datos del colaborador")
        c1, c2 = st.columns(2)

        with c1:
            sede = st.selectbox("Sede", list(SEDES.keys()), key="survey_sede")
            colaborador = st.text_input("Nombre del colaborador", placeholder="Ej. Ana Torres")
            lider = st.text_input("Líder o jefe directo", value=SEDES[sede]["jefe"])

        with c2:
            comentario = st.text_area(
                "Comentario breve",
                height=145,
                placeholder="¿Qué debería mejorar el líder o la tienda mañana?"
            )

        st.markdown("#### Evaluación de la jornada")
        c3, c4 = st.columns(2)

        with c3:
            felicidad = st.slider("Nivel de felicidad al salir", 1, 5, 3)
            claridad = st.slider("Claridad de objetivos del día", 1, 5, 3)

        with c4:
            seguridad = st.slider("Seguridad psicológica percibida", 1, 5, 3)
            feedback = st.slider("Feedback recibido del líder", 1, 5, 3)

        carga = st.slider(
            "Carga laboral percibida",
            1, 5, 3,
            help="1 = baja, 5 = muy alta"
        )

        submitted = st.form_submit_button("Guardar encuesta", type="primary")

    if submitted:
        row = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sede": sede,
            "colaborador": colaborador or "Anónimo",
            "lider": lider or SEDES[sede]["jefe"],
            "felicidad": felicidad,
            "seguridad_psicologica": seguridad,
            "claridad_objetivos": claridad,
            "feedback_lider": feedback,
            "carga_laboral": carga,
            "comentario": comentario,
        }
        path = append_row_csv("encuesta_salida_registros.csv", row, SURVEY_COLUMNS)
        st.cache_data.clear()
        st.success(f"Encuesta guardada correctamente en: {path}")

with complaint_tab:
    st.subheader("Registro de quejas y reclamos")

    with st.form("complaints_form", clear_on_submit=True):
        st.markdown("#### Datos generales")
        c1, c2 = st.columns(2)

        with c1:
            sede_q = st.selectbox("Sede", list(SEDES.keys()), key="complaint_sede")
            canal = st.selectbox("¿Quién registra?", ["Cliente", "Trabajador", "Líder", "RR. HH."])
            tipo = st.selectbox(
                "Tipo de reclamo",
                [
                    "Mala atención",
                    "Demora",
                    "Falta de empatía",
                    "Liderazgo",
                    "Comunicación",
                    "Productividad",
                    "Seguridad psicológica",
                    "Otro",
                ],
            )

        with c2:
            colaborador = st.text_input("Colaborador involucrado", placeholder="Puede ser anónimo")
            lider_q = st.text_input("Líder asociado", value=SEDES[sede_q]["jefe"])
            score = st.slider("Puntuación del cliente o percepción", 1, 5, 3)

        texto = st.text_area(
            "Detalle de la queja o situación",
            height=160,
            placeholder="Describe qué ocurrió, cómo afectó al cliente/equipo y qué debería cambiar."
        )

        urgencia = st.selectbox("Urgencia reportada", ["Baja", "Media", "Alta", "Crítica"])

        submitted_q = st.form_submit_button("Guardar queja/reclamo", type="primary")

    if submitted_q:
        row = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sede": sede_q,
            "canal": canal,
            "tipo_reclamo": tipo,
            "colaborador": colaborador or "No especificado",
            "lider": lider_q or SEDES[sede_q]["jefe"],
            "texto": texto,
            "puntuacion_cliente": score,
            "urgencia_reportada": urgencia,
        }
        path = append_row_csv("reclamos_registros.csv", row, COMPLAINT_COLUMNS)
        st.cache_data.clear()
        st.success(f"Reclamo guardado correctamente en: {path}")