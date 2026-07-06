from __future__ import annotations

import streamlit as st

from .config import TAMBO_COLORS

C = TAMBO_COLORS


def apply_styles() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --tambo-purple: {C['purple']};
            --tambo-purple-dark: {C['purple_dark']};
            --tambo-purple-light: {C['purple_light']};
            --tambo-yellow: {C['yellow']};
            --tambo-yellow-light: {C['yellow_light']};
            --tambo-text: {C['text']};
            --tambo-muted: {C['text_muted']};
            --tambo-border: {C['border']};
            --tambo-white: {C['white']};
            --tambo-bg: {C['bg']};
            --tambo-surface: {C['surface']};
        }}

        .stApp {{
            background-color: var(--tambo-bg) !important;
            color: var(--tambo-text) !important;
        }}

        .main .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 2.5rem;
            max-width: 1280px;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--tambo-purple-dark) !important;
        }}

        /* =========================
           SIDEBAR
        ========================= */

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--tambo-purple-dark) 0%, var(--tambo-purple) 100%) !important;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stCaption {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > div,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > span {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        [data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.20) !important;
        }}

        /* Selectbox cerrado */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.45) !important;
            border-radius: 12px !important;
            min-height: 46px !important;
        }}

        [data-testid="stSidebar"] div[data-baseweb="select"] * {{
            color: #1A0A2E !important;
            -webkit-text-fill-color: #1A0A2E !important;
        }}

        [data-testid="stSidebar"] div[data-baseweb="select"] svg {{
            color: #5C0599 !important;
            fill: #5C0599 !important;
        }}

        /* Inputs */
        [data-testid="stSidebar"] input {{
            background: #ffffff !important;
            color: #1A0A2E !important;
            -webkit-text-fill-color: #1A0A2E !important;
            border-radius: 12px !important;
        }}

        [data-testid="stSidebar"] input:disabled {{
            background: #ffffff !important;
            color: #5C5470 !important;
            -webkit-text-fill-color: #5C5470 !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebar"] input::placeholder {{
            color: #8B7A99 !important;
            -webkit-text-fill-color: #8B7A99 !important;
            opacity: 1 !important;
        }}

        /* Botones del sidebar */
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] div[data-testid="stButton"] > button,
        [data-testid="stSidebar"] div[data-testid="stButton"] button,
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button {{
            background: #ffffff !important;
            color: #5C0599 !important;
            -webkit-text-fill-color: #5C0599 !important;
            border: 1px solid rgba(255,255,255,0.45) !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
        }}

        [data-testid="stSidebar"] .stButton > button *,
        [data-testid="stSidebar"] div[data-testid="stButton"] button *,
        section[data-testid="stSidebar"] .stButton > button *,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button * {{
            color: #5C0599 !important;
            -webkit-text-fill-color: #5C0599 !important;
            font-weight: 800 !important;
        }}

        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
        section[data-testid="stSidebar"] .stButton > button:hover,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
            background: #FFF8E1 !important;
            color: #3D0466 !important;
            -webkit-text-fill-color: #3D0466 !important;
            border-color: #FFCC00 !important;
        }}

        [data-testid="stSidebar"] .stButton > button:hover *,
        [data-testid="stSidebar"] div[data-testid="stButton"] button:hover *,
        section[data-testid="stSidebar"] .stButton > button:hover *,
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover * {{
            color: #3D0466 !important;
            -webkit-text-fill-color: #3D0466 !important;
        }}

        /* Toggle: no convertirlo en botón blanco */
        [data-testid="stSidebar"] [data-testid="stToggle"] button {{
            background: rgba(255,255,255,0.20) !important;
            border: none !important;
        }}

        [data-testid="stSidebar"] [data-testid="stToggle"] button * {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        /* Alertas del sidebar */
        [data-testid="stSidebar"] [data-testid="stSuccess"],
        [data-testid="stSidebar"] [data-testid="stInfo"],
        [data-testid="stSidebar"] [data-testid="stWarning"] {{
            background: rgba(255,255,255,0.14) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 12px !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSuccess"] *,
        [data-testid="stSidebar"] [data-testid="stInfo"] *,
        [data-testid="stSidebar"] [data-testid="stWarning"] * {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        /* Dropdown abierto */
        div[data-baseweb="popover"] ul,
        div[role="listbox"] {{
            background: #ffffff !important;
        }}

        div[data-baseweb="popover"] *,
        div[role="listbox"] * {{
            color: #1A0A2E !important;
            -webkit-text-fill-color: #1A0A2E !important;
        }}

        /* =========================
           HERO
        ========================= */

        .hero {{
            padding: 1.6rem 1.8rem;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--tambo-purple-dark) 0%, var(--tambo-purple) 60%, var(--tambo-purple) 100%);
            border-left: 6px solid var(--tambo-yellow);
            color: white;
            margin-bottom: 1.2rem;
            box-shadow: 0 10px 28px rgba(92, 5, 153, 0.18);
        }}

        .hero h1 {{
            color: #ffffff !important;
            margin: 0;
            font-size: 1.85rem;
            font-weight: 800;
        }}

        .hero p {{
            color: rgba(255,255,255,0.92) !important;
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            line-height: 1.55;
        }}

        /* =========================
           CARDS
        ========================= */

        .card {{
            background: #ffffff !important;
            border: 1px solid var(--tambo-border) !important;
            border-radius: 16px !important;
            padding: 20px 22px !important;
            margin-bottom: 14px !important;
            color: var(--tambo-text) !important;
            box-shadow: 0 4px 16px rgba(92, 5, 153, 0.06) !important;
        }}

        .card,
        .card * {{
            color: var(--tambo-text) !important;
        }}

        .card b,
        .card h1,
        .card h2,
        .card h3,
        .card h4 {{
            color: var(--tambo-purple-dark) !important;
            font-weight: 800 !important;
        }}

        .card .small-muted {{
            color: var(--tambo-muted) !important;
        }}

        .sede-banner {{
            background: #ffffff !important;
            border: 1px solid var(--tambo-border) !important;
            border-left: 5px solid var(--tambo-yellow) !important;
            border-radius: 16px !important;
            padding: 18px 22px !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 14px rgba(92, 5, 153, 0.07) !important;
        }}

        .sede-banner .sede-title {{
            color: var(--tambo-purple-dark) !important;
            font-size: 1.15rem;
            font-weight: 800;
            margin: 0;
        }}

        .sede-banner .sede-sub {{
            color: var(--tambo-muted) !important;
            font-size: 0.95rem;
            margin: 6px 0 0 0;
            line-height: 1.5;
        }}

        /* =========================
           KPI
        ========================= */

        .highlight-kpi {{
            background: linear-gradient(145deg, var(--tambo-purple-light) 0%, #ffffff 100%) !important;
            border: 1px solid var(--tambo-border) !important;
            border-top: 3px solid var(--tambo-purple) !important;
            border-radius: 16px !important;
            padding: 18px 20px !important;
            text-align: center !important;
            box-shadow: 0 4px 14px rgba(92, 5, 153, 0.06) !important;
        }}

        .highlight-kpi .label {{
            color: var(--tambo-muted) !important;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 6px;
        }}

        .highlight-kpi .value {{
            color: var(--tambo-purple-dark) !important;
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1.1;
        }}

        .highlight-kpi .hint {{
            color: var(--tambo-muted) !important;
            font-size: 0.85rem;
            margin-top: 4px;
        }}

        [data-testid="stMetric"] {{
            background: #ffffff !important;
            border: 1px solid var(--tambo-border) !important;
            border-radius: 14px !important;
            padding: 18px 20px !important;
            box-shadow: 0 4px 14px rgba(92, 5, 153, 0.05) !important;
        }}

        [data-testid="stMetric"] * {{
            color: var(--tambo-text) !important;
        }}

        [data-testid="stMetricLabel"] p {{
            color: var(--tambo-muted) !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--tambo-purple-dark) !important;
            font-weight: 800 !important;
        }}

        [data-testid="stMetricDelta"] {{
            background: var(--tambo-yellow-light) !important;
            border-radius: 999px !important;
            padding: 3px 10px !important;
            width: fit-content !important;
        }}

        [data-testid="stMetricDelta"] * {{
            color: var(--tambo-purple-dark) !important;
            font-weight: 700 !important;
        }}

        /* =========================
           TABS
        ========================= */

        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px;
            background: var(--tambo-surface) !important;
            border-radius: 14px;
            padding: 6px;
            border: 1px solid var(--tambo-border);
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px;
            color: var(--tambo-muted) !important;
            font-weight: 700;
        }}

        .stTabs [data-baseweb="tab"] * {{
            color: var(--tambo-muted) !important;
        }}

        .stTabs [aria-selected="true"] {{
            background: var(--tambo-purple) !important;
            color: #ffffff !important;
        }}

        .stTabs [aria-selected="true"] * {{
            color: #ffffff !important;
        }}

        /* =========================
           FORMULARIOS E INPUTS
        ========================= */

        .stForm {{
            background: #ffffff !important;
            border: 1px solid var(--tambo-border) !important;
            border-radius: 18px !important;
            padding: 20px !important;
            box-shadow: 0 4px 14px rgba(92, 5, 153, 0.05) !important;
        }}

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        div[data-baseweb="input"] input {{
            background: #ffffff !important;
            color: var(--tambo-text) !important;
            -webkit-text-fill-color: var(--tambo-text) !important;
            border: 1px solid var(--tambo-border) !important;
            border-radius: 12px !important;
        }}

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {{
            color: var(--tambo-muted) !important;
            -webkit-text-fill-color: var(--tambo-muted) !important;
            opacity: 1 !important;
        }}

        div[data-baseweb="select"] > div {{
            background: #ffffff !important;
            color: var(--tambo-text) !important;
            border: 1px solid var(--tambo-border) !important;
            border-radius: 12px !important;
        }}

        div[data-baseweb="select"] * {{
            color: var(--tambo-text) !important;
            -webkit-text-fill-color: var(--tambo-text) !important;
        }}

        label,
        .stSelectbox label,
        .stTextInput label,
        .stTextArea label,
        .stSlider label {{
            color: var(--tambo-purple-dark) !important;
            font-weight: 700 !important;
        }}

        /* =========================
           BOTONES GENERALES
        ========================= */

        .stButton > button {{
            border-radius: 12px !important;
            font-weight: 700 !important;
        }}

        .stButton > button[kind="primary"] {{
            background: var(--tambo-purple) !important;
            border: 1px solid var(--tambo-purple) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        .stButton > button[kind="primary"] * {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background: var(--tambo-purple-dark) !important;
            border-color: var(--tambo-purple-dark) !important;
        }}

        .stButton > button[kind="secondary"] {{
            background: #ffffff !important;
            border: 1px solid var(--tambo-purple) !important;
            color: var(--tambo-purple) !important;
            -webkit-text-fill-color: var(--tambo-purple) !important;
        }}

        .stButton > button[kind="secondary"] * {{
            color: var(--tambo-purple) !important;
            -webkit-text-fill-color: var(--tambo-purple) !important;
        }}

        /* =========================
           EXPANDERS / CHAT / ALERTAS
        ========================= */

        div[data-testid="stExpander"] {{
            border: 1px solid var(--tambo-border) !important;
            border-radius: 12px !important;
            background: #ffffff !important;
        }}

        div[data-testid="stExpander"] * {{
            color: var(--tambo-text) !important;
        }}

        div[data-testid="stChatMessage"] {{
            background: #ffffff !important;
            border: 1px solid var(--tambo-border) !important;
            border-radius: 14px !important;
        }}

        [data-testid="stSuccess"],
        [data-testid="stInfo"],
        [data-testid="stWarning"] {{
            border-radius: 12px !important;
        }}

        [data-testid="stSuccess"] {{
            background: #F4ECFB !important;
            color: var(--tambo-purple-dark) !important;
            border: 1px solid var(--tambo-border) !important;
        }}

        [data-testid="stInfo"] {{
            background: #F4ECFB !important;
            color: var(--tambo-purple-dark) !important;
            border: 1px solid var(--tambo-border) !important;
        }}

        [data-testid="stWarning"] {{
            background: #FFF8E1 !important;
            color: var(--tambo-purple-dark) !important;
            border: 1px solid #FFE082 !important;
        }}

        [data-testid="stSuccess"] *,
        [data-testid="stInfo"] *,
        [data-testid="stWarning"] * {{
            color: var(--tambo-purple-dark) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="card">
            <h4 style="margin-top:0;color:{C['purple_dark']};font-weight:800;">{title}</h4>
            <p class="small-muted" style="margin:0;line-height:1.65;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sede_banner(company: str, sede: str, problematica: str) -> None:
    st.markdown(
        f"""
        <div class="sede-banner">
            <p class="sede-title">{company} · {sede}</p>
            <p class="sede-sub">Problemática de trabajo inicial: {problematica}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str) -> None:
    st.markdown(
        f"""
        <div class="section-header">
            <span class="dot"></span>
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def highlight_kpi(label: str, value: str, hint: str = "") -> None:
    hint_html = f'<div class="hint">{hint}</div>' if hint else ""
    st.markdown(
        f"""
        <div class="highlight-kpi">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {hint_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
