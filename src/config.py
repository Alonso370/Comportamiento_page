from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
INCOMING_DIR = DATA_DIR / "incoming"
PROCESSED_DIR = DATA_DIR / "processed"
CATALOG_DIR = DATA_DIR / "catalogos"
KNOWLEDGE_DIR = ROOT_DIR / "knowledge_base" / "articulos_liderazgo"

APP_NAME = "Guía para líderes de Dambo"
COMPANY_NAME = "Dambo"

SEDES = {
    "Sede Centro": {
        "jefe": "Jefe demo - Centro",
        "problematica": "Personal experimentado, pero con baja adopción digital. \n"
                        "Predomina un liderazgo tradicional que mantiene métodos manuales, "
                 "      frena la innovación y genera cuellos de botella en horas punta.\n",
        "ventas_mes": 128500,
        "meta_ventas": 145000,
    },
    "Sede Norte": {
        "jefe": "Jefe demo - Norte",
        "problematica":"Equipo joven y con alta adaptación tecnológica, pero con bajo bienestar emocional.\n "
            "La presión en horas punta y la falta de contención de líderes experimentados "
            "provocan estrés, mala atención y caída en la calidad del servicio.\n",
        "ventas_mes": 106800,
        "meta_ventas": 118000,
    },
    "Sede Sur": {
        "jefe": "Jefe demo - Sur",
        "problematica":  "Fuerza laboral mixta con choque generacional.\n "
            "La falta de liderazgo mediador ha fragmentado al equipo, "
        "afectando la cohesión, el clima laboral y los estándares de servicio.\n",
        "ventas_mes": 97200,
        "meta_ventas": 110000,
    },
}

OXYGEN_BEHAVIORS = [
    "Buen coach",
    "Empodera al equipo",
    "Crea un entorno inclusivo",
    "Productivo y orientado a resultados",
    "Buen comunicador",
    "Apoya el desarrollo profesional",
    "Tiene visión clara",
    "Posee habilidades técnicas relevantes",
]

URGENCY_ORDER = ["Crítica", "Alta", "Media", "Baja"]

DEFAULT_RECOMMENDATION_MODEL = "gpt-5.5"

# Paleta inspirada en Tambo: morado, amarillo y fondo blanco
TAMBO_COLORS = {
    "purple": "#5C0599",
    "purple_dark": "#3D0466",
    "purple_light": "#EDE7F6",
    "yellow": "#FFCC00",
    "yellow_light": "#FFF8E1",
    "white": "#FFFFFF",
    "bg": "#FFFFFF",
    "surface": "#FAFAFA",
    "text": "#1A0A2E",
    "text_muted": "#5C5470",
    "border": "#E8E0F0",
    "urgency": {
        "Crítica": "#5C0599",
        "Alta": "#FF9800",
        "Media": "#FFCC00",
        "Baja": "#C4B5D4",
    },
}
