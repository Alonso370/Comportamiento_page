from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import APP_NAME, COMPANY_NAME, OXYGEN_BEHAVIORS, SEDES, TAMBO_COLORS, URGENCY_ORDER
from src.data_loader import (
    add_urgency,
    calculate_kpis,
    filter_by_sede,
    load_agenda,
    load_complaints,
    load_indicators,
    load_oxygen,
    load_surveys,
    make_sample_files,
)
from src.gpt_recommender import (
    get_api_status,
    stream_chat_reply,
)

from src.task_board import (
    add_recommendation_task,
    complete_task,
    count_tasks_by_sede,
    load_tasks,
)
from src.charts import apply_tambo_theme, urgency_color_map
from src.styles import apply_styles, card, hero, highlight_kpi, section_header, sede_banner

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

C = TAMBO_COLORS
apply_styles()
make_sample_files()

hero(
    "Guía para líderes de Dambo",
    "En esta pagina como lider de sede tendras a tu disposicion las siguientes herramientas: organigrama, KPIs, reclamos, clima laboral y recomendaciones de liderazgo con apoyo de IA. Aprende de las recomendaciones para superar los retos operativos y tener los mejores resultados",
)

with st.sidebar:
    st.markdown("### 🛒 DAMBO")
    st.subheader("Modo jefe de sucursal")
    sede = st.selectbox("Selecciona una sede", list(SEDES.keys()))
    jefe_demo = SEDES[sede]["jefe"]
    st.text_input("Usuario demo", value=jefe_demo, disabled=True)
    st.caption("Más adelante este selector se puede reemplazar por cuentas reales con usuario y contraseña.")
    st.divider()
    force_demo = st.toggle("Usar recomendaciones demo", value=False)
    st.caption("Actívalo si aún no configuraste tu API Key de OpenAI.")
    api_label, _ = get_api_status(force_demo=force_demo)
    if force_demo or "Sin API Key" in api_label:
        st.warning(api_label)
    else:
        st.success(api_label)
    if st.button("Actualizar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.write("**Datos usados**")
    st.caption("Archivos CSV/XLSX en `data/incoming/` que contengan: reclamo, queja, encuesta o survey.")

complaints_all = load_complaints()
surveys_all = load_surveys()
indicators_all = load_indicators()
oxygen_all = load_oxygen()

complaints = filter_by_sede(complaints_all, sede)
surveys = filter_by_sede(surveys_all, sede)
indicators = filter_by_sede(indicators_all, sede)
oxygen = filter_by_sede(oxygen_all, sede)

filtered_complaints = complaints.copy()
filtered_surveys = surveys.copy()

sede_banner(COMPANY_NAME, sede, SEDES[sede]["problematica"])

tab_org, tab_kpis, tab_reco, tab_mural = st.tabs(
    [
        "🏢 Organigrama",
        "📊 KPIs y tablas",
        "💬 Asistente IA",
        "🧩 Mural de tareas",
    ]
)
with tab_org:
    st.subheader("Organigrama operativo de la sucursal")

    left, right = st.columns([1.25, 1])

    with left:
        dot = f'''
        digraph {{
            graph [
                rankdir=TB,
                bgcolor="transparent",
                splines=ortho,
                nodesep=0.6,
                ranksep=0.7
            ]

            node [
                shape=box,
                style="rounded,filled",
                fontname="Arial",
                fontsize=11,
                color="{C['purple']}",
                fillcolor="{C['purple_light']}",
                fontcolor="{C['purple_dark']}"
            ]

            jefe [
                label="{jefe_demo}\\nJefe de sucursal",
                fillcolor="{C['purple']}",
                fontcolor="white",
                color="{C['purple_dark']}"
            ]

            caja [label="Equipo de caja"]
            reposicion [label="Equipo de reposición y piso"]
            atencion [label="Equipo de atención al cliente"]

            jefe -> caja [color="{C['yellow']}", penwidth=2]
            jefe -> reposicion [color="{C['yellow']}", penwidth=2]
            jefe -> atencion [color="{C['yellow']}", penwidth=2]
        }}
        '''

        st.graphviz_chart(dot, use_container_width=True)

    with right:
        card(
            "Organigrama",
            "Hola, como jefe de sucursal tienes a tu cargo un equipo de trabajo. Desde esta vista puede identificar qué áreas requieren seguimiento, capacitación o apoyo a partir de sus opiniones y de los clientes."
        )

        card(
            "Guia de uso",
            "Se registran encuestas de salida y quejas de clientes y tus trabajadores. Podras ver medidores de tu desempeño par conocer tus puntos fuertes y debiles. Finalmente, tienes un asistente IA que te guiara para ser un mejor lider y desarrollar a tu equipo."
        )

    st.subheader("Roles y responsabilidades")

    roles = pd.DataFrame(
        [
            [
                "Jefe de sucursal",
                "Revisar alertas, apoyar en las operaciones, ejecutar recomendaciones y agendar estrategias."
            ],
            [
                "Equipo de caja",
                "Atender pagos, resolver dudas rápidas y reportar situaciones de presión o mala atención."
            ],
            [
                "Equipo de reposición y piso",
                "Mantener orden de tienda, disponibilidad de productos y reportar problemas operativos."
            ],
            [
                "Equipo de atención al cliente",
                "Gestionar consultas, reclamos y situaciones difíciles con clientes."
            ],
        ],
        columns=["Puesto", "Responsabilidades del puesto"],
    )

    st.dataframe(roles, use_container_width=True, hide_index=True)

with tab_kpis:
    st.subheader("Indicadores principales de la sede")

    with st.container(border=True):
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            if not complaints.empty and "fecha" in complaints.columns:
                min_date = complaints["fecha"].min().date()
                max_date = complaints["fecha"].max().date()
            elif not surveys.empty and "fecha" in surveys.columns:
                min_date = surveys["fecha"].min().date()
                max_date = surveys["fecha"].max().date()
            else:
                min_date = max_date = datetime.now().date()
            date_range = st.date_input(
                "Rango de fechas",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key=f"date_range_{sede}",
            )
        with filter_col2:
            urgency_options = ["Todas"] + URGENCY_ORDER
            urgency_filter = st.selectbox("Filtrar reclamos por urgencia", urgency_options, key=f"urgency_{sede}")
        with filter_col3:
            if not complaints.empty and "tipo_reclamo" in complaints.columns:
                type_options = ["Todos"] + sorted(complaints["tipo_reclamo"].dropna().astype(str).unique().tolist())
            else:
                type_options = ["Todos"]
            type_filter = st.selectbox("Filtrar por tipo de reclamo", type_options, key=f"type_{sede}")

    filtered_complaints = complaints.copy()
    filtered_surveys = surveys.copy()

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        if not filtered_complaints.empty and "fecha" in filtered_complaints.columns:
            mask = filtered_complaints["fecha"].dt.date.between(start_date, end_date)
            filtered_complaints = filtered_complaints[mask]
        if not filtered_surveys.empty and "fecha" in filtered_surveys.columns:
            mask = filtered_surveys["fecha"].dt.date.between(start_date, end_date)
            filtered_surveys = filtered_surveys[mask]

    if urgency_filter != "Todas":
        filtered_complaints = add_urgency(filtered_complaints)
        if "urgencia_calculada" in filtered_complaints.columns:
            filtered_complaints = filtered_complaints[filtered_complaints["urgencia_calculada"] == urgency_filter]

    if type_filter != "Todos" and not filtered_complaints.empty:
        filtered_complaints = filtered_complaints[filtered_complaints["tipo_reclamo"].astype(str) == type_filter]

    filtered_kpis = calculate_kpis(sede, filtered_complaints, filtered_surveys, indicators, oxygen)

    h1, h2, h3 = st.columns(3)
    with h1:
        highlight_kpi("Productividad", f"{filtered_kpis['productividad_pct']}%", "Ventas vs meta")
    with h2:
        highlight_kpi("Felicidad del equipo", f"{filtered_kpis['felicidad']}/5", "Encuesta de salida")
    with h3:
        highlight_kpi("Reclamos activos", str(filtered_kpis["reclamos_mes"]), "Según filtros")

    section_header("Desempeño comercial")
    c1, c2, c3 = st.columns(3)
    c1.metric("Ventas del mes", f"S/ {filtered_kpis['ventas_mes']:,.0f}")
    c2.metric("Ticket promedio", f"S/ {filtered_kpis['ticket_promedio']:,.2f}")
    c3.metric("Capacitación completada", f"{filtered_kpis['cumplimiento_capacitacion']}%")

    section_header("Clima y liderazgo")
    c4, c5, c6 = st.columns(3)
    c4.metric("Seguridad psicológica", f"{filtered_kpis['seguridad_psicologica']}/5", "Meta: 4/5")
    c5.metric("Satisfacción del cliente", f"{filtered_kpis['satisfaccion_cliente']}/5")
    c6.metric("Comportamientos Oxygen", f"{filtered_kpis['oxygen_pct']}%", "Meta: 80%")

    st.divider()
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("#### Reclamos por tipo")
        if filtered_complaints.empty:
            st.warning("No hay reclamos para esta sede con los filtros seleccionados.")
        else:
            type_counts = filtered_complaints["tipo_reclamo"].fillna("Sin tipo").value_counts().reset_index()
            type_counts.columns = ["tipo_reclamo", "cantidad"]
            fig = px.bar(
                type_counts,
                x="tipo_reclamo",
                y="cantidad",
                text="cantidad",
                title="Problemas frecuentes",
                color="cantidad",
                color_continuous_scale=[C["purple_light"], C["purple"]],
            )
            fig.update_layout(coloraxis_showscale=False)
            apply_tambo_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Clima laboral promedio")
        if filtered_surveys.empty:
            st.warning("No hay encuestas para esta sede con los filtros seleccionados.")
        else:
            survey_metrics = filtered_surveys[
                ["felicidad", "seguridad_psicologica", "claridad_objetivos", "feedback_lider", "carga_laboral"]
            ].mean().reset_index()
            survey_metrics.columns = ["métrica", "promedio"]
            fig = px.bar_polar(
                survey_metrics,
                r="promedio",
                theta="métrica",
                range_r=[0, 5],
                title="Radar de clima laboral /5",
                color="promedio",
                color_continuous_scale=[C["yellow_light"], C["purple"]],
            )
            fig.update_layout(coloraxis_showscale=False, polar={"bgcolor": C["white"]})
            apply_tambo_theme(fig, height=380)
            st.plotly_chart(fig, use_container_width=True)

    col_chart_c, col_chart_d = st.columns(2)
    with col_chart_c:
        st.markdown("#### Semáforo de urgencia")
        urgent_chart_df = add_urgency(filtered_complaints)
        if urgent_chart_df.empty or "urgencia_calculada" not in urgent_chart_df.columns:
            st.caption("Sin datos suficientes para calcular urgencia.")
        else:
            urgency_counts = (
                urgent_chart_df["urgencia_calculada"]
                .value_counts()
                .reindex(URGENCY_ORDER)
                .fillna(0)
                .astype(int)
                .reset_index()
            )
            urgency_counts.columns = ["urgencia", "cantidad"]
            fig = px.bar(
                urgency_counts,
                x="urgencia",
                y="cantidad",
                text="cantidad",
                title="Reclamos por urgencia",
                color="urgencia",
                color_discrete_map=urgency_color_map(),
            )
            apply_tambo_theme(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)

    with col_chart_d:
        st.markdown("#### Comportamientos Oxygen")
        if oxygen.empty:
            oxygen_chart = pd.DataFrame(
                {"Comportamiento": OXYGEN_BEHAVIORS, "Cumplimiento": [50] * len(OXYGEN_BEHAVIORS)}
            )
        else:
            oxygen_chart = oxygen[["comportamiento", "cumplimiento_estimado"]].rename(
                columns={"comportamiento": "Comportamiento", "cumplimiento_estimado": "Cumplimiento"}
            )
        fig = px.bar(
            oxygen_chart,
            x="Cumplimiento",
            y="Comportamiento",
            orientation="h",
            text="Cumplimiento",
            title="Cumplimiento por comportamiento (%)",
            color="Cumplimiento",
            color_continuous_scale=[C["yellow_light"], C["purple"]],
        )
        fig.update_layout(coloraxis_showscale=False)
        apply_tambo_theme(fig, height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    section_header("Detalle de registros")
    if indicators.empty:
        st.caption("Aún no hay archivo de indicadores para esta sede.")
    else:
        st.dataframe(indicators.sort_values("periodo", ascending=False), use_container_width=True, hide_index=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("#### Últimos reclamos/quejas")
        shown = add_urgency(filtered_complaints).sort_values("fecha", ascending=False).head(10) if not filtered_complaints.empty else filtered_complaints
        cols = [c for c in ["fecha", "canal", "tipo_reclamo", "colaborador", "texto", "puntuacion_cliente", "urgencia_calculada", "archivo_origen"] if c in shown.columns]
        st.dataframe(shown[cols], use_container_width=True, hide_index=True)
    with col_d:
        st.markdown("#### Últimas encuestas de salida")
        shown_survey = filtered_surveys.sort_values("fecha", ascending=False).head(10) if not filtered_surveys.empty else filtered_surveys
        cols = [c for c in ["fecha", "colaborador", "lider", "felicidad", "seguridad_psicologica", "feedback_lider", "comentario", "archivo_origen"] if c in shown_survey.columns]
        st.dataframe(shown_survey[cols], use_container_width=True, hide_index=True)

with tab_reco:
    st.subheader("Asistente interactivo de liderazgo")
    st.caption(
        "Conversa con el asistente sobre reclamos, clima laboral y acciones prioritarias. "
        "Usa reclamos, encuestas, contexto manual y artículos en `knowledge_base/articulos_liderazgo/`."
    )

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = {}

    chat_key = sede
    if chat_key not in st.session_state.chat_messages:
        st.session_state.chat_messages[chat_key] = []


    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    quick_prompts = {
        quick_col1: "Dame un diagnóstico completo de la sede con prioridades.",
        quick_col2: "¿Qué debo hacer hoy con los reclamos más urgentes?",
        quick_col3: "Propón acciones para mejorar la seguridad psicológica del equipo.",
        quick_col4: "Arma una agenda de 7 días para esta sucursal.",
    }
    selected_prompt = None
    for col, prompt in quick_prompts.items():
        with col:
            if st.button(prompt.split(".")[0][:28] + "…", use_container_width=True, key=f"quick_{hash(prompt)}_{sede}"):
                selected_prompt = prompt

    action_col1, action_col2 = st.columns([1, 1])
    with action_col1:
        if st.button("Limpiar conversación", use_container_width=True):
            st.session_state.chat_messages[chat_key] = []
            st.session_state.pop("last_recommendation", None)
            st.rerun()
    with action_col2:
        generate = st.button("Generar diagnóstico completo", type="primary", use_container_width=True)

    if generate:
        selected_prompt = "Dame un diagnóstico completo de la sede con recomendaciones priorizadas."

    for message in st.session_state.chat_messages[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = selected_prompt or st.chat_input("Escribe tu pregunta al asistente de liderazgo…")
    if user_input:
        st.session_state.chat_messages[chat_key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_text = st.write_stream(
                stream_chat_reply(
                    st.session_state.chat_messages[chat_key],
                    sede,
                    complaints,
                    surveys,
                    force_demo=force_demo,
                )
            )

        st.session_state.chat_messages[chat_key].append({"role": "assistant", "content": response_text})
        _, mode = get_api_status(force_demo=force_demo)
        if "Nota técnica: no se pudo llamar a la API" in response_text:
            mode = "demo_error_api"
        st.session_state["last_recommendation"] = response_text
        st.session_state["last_mode"] = mode
        st.session_state["last_sede"] = sede
        st.session_state["last_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        task = add_recommendation_task(
                    sede=sede,
                    content=response_text,
                    mode=mode,
                )

        st.toast(f"Recomendación agregada al mural: {task['prioridad']}")

    
    st.divider()
    st.markdown("#### Semáforo de urgencia actual")
    urgent_df = add_urgency(filtered_complaints if not filtered_complaints.empty else complaints)
    if urgent_df.empty or "urgencia_calculada" not in urgent_df.columns:
        st.caption("Sin datos suficientes para calcular urgencia.")
    else:
        urgency_counts = urgent_df["urgencia_calculada"].value_counts().reindex(URGENCY_ORDER).fillna(0).astype(int).reset_index()
        urgency_counts.columns = ["urgencia", "cantidad"]
        fig = px.bar(
            urgency_counts,
            x="urgencia",
            y="cantidad",
            text="cantidad",
            title="Reclamos clasificados por urgencia",
            color="urgencia",
            color_discrete_map=urgency_color_map(),
        )
        apply_tambo_theme(fig, height=330)
        st.plotly_chart(fig, use_container_width=True)
with tab_mural:
    st.subheader("Mural de tareas por completar")
    st.caption(
        "Aquí aparecen las recomendaciones generadas por el asistente IA. "
        "Puedes abrir cada tarjeta para volver a leerla y marcarla como completa cuando ya se ejecutó."
    )

    all_tasks = load_tasks()

    sede_tasks = [
        task for task in all_tasks
        if task.get("sede") == sede
    ]

    total_sede_tasks = count_tasks_by_sede(sede)

    st.markdown(
        f"""
        <div class="sede-banner">
            <p class="sede-title">Tareas pendientes · {sede}</p>
            <p class="sede-sub">Total de recomendaciones por completar: {total_sede_tasks}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not sede_tasks:
        st.success("No hay tareas pendientes para esta sede.")
    else:
        prioridad_orden = {
            "Crítica": 1,
            "Alta": 2,
            "Media": 3,
            "Pendiente": 4,
        }

        sede_tasks = sorted(
            sede_tasks,
            key=lambda x: prioridad_orden.get(x.get("prioridad", "Pendiente"), 99),
        )

        filtro_prioridad = st.selectbox(
            "Filtrar por prioridad",
            ["Todas", "Crítica", "Alta", "Media", "Pendiente"],
            key=f"filtro_mural_{sede}",
        )

        if filtro_prioridad != "Todas":
            sede_tasks = [
                task for task in sede_tasks
                if task.get("prioridad") == filtro_prioridad
            ]

        for task in sede_tasks:
            prioridad = task.get("prioridad", "Pendiente")
            fecha = task.get("fecha_creacion", "Sin fecha")
            titulo = task.get("titulo", "Recomendación pendiente")
            contenido = task.get("contenido", "")

            if prioridad == "Crítica":
                icono = "🔴"
            elif prioridad == "Alta":
                icono = "🟠"
            elif prioridad == "Media":
                icono = "🟡"
            else:
                icono = "🔵"

            with st.expander(f"{icono} {prioridad} · {titulo}"):
                st.markdown(f"**Sede:** {task.get('sede', sede)}")
                st.markdown(f"**Fecha de creación:** {fecha}")
                st.markdown(f"**Modo:** {task.get('modo', 'ia')}")
                st.divider()

                st.markdown("### Recomendación completa")
                st.markdown(contenido)

                st.divider()

                col_done, col_keep = st.columns([1, 2])

                with col_done:
                    if st.button(
                        "Marcar como completo",
                        key=f"complete_{task['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        complete_task(task["id"])
                        st.toast("Tarea completada y eliminada del mural.")
                        st.rerun()

                with col_keep:
                    st.caption(
                        "La tarea seguirá visible hasta que presiones "
                        "“Marcar como completo”."
                    )