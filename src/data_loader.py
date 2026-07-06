from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import INCOMING_DIR, KNOWLEDGE_DIR, SEDES


COMPLAINT_COLUMNS = [
    "fecha",
    "sede",
    "canal",
    "tipo_reclamo",
    "colaborador",
    "lider",
    "texto",
    "puntuacion_cliente",
    "urgencia_reportada",
]

SURVEY_COLUMNS = [
    "fecha",
    "sede",
    "colaborador",
    "lider",
    "felicidad",
    "seguridad_psicologica",
    "claridad_objetivos",
    "feedback_lider",
    "carga_laboral",
    "comentario",
]

AGENDA_COLUMNS = ["fecha", "sede", "estrategia", "responsable", "estado", "prioridad"]

INDICATOR_COLUMNS = [
    "periodo",
    "sede",
    "lider",
    "ventas_mes",
    "meta_ventas",
    "productividad_pct",
    "clientes_atendidos",
    "ticket_promedio",
    "reclamos_mes",
    "capacitaciones_programadas",
    "capacitaciones_completadas",
    "cumplimiento_capacitacion",
    "tasa_ausentismo",
    "rotacion_personal",
]

OXYGEN_COLUMNS = ["periodo", "sede", "lider", "comportamiento", "cumplimiento_estimado", "observacion"]


def ensure_directories() -> None:
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)


def _read_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    return pd.DataFrame()


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("á", "a").replace("é", "e")
        .replace("í", "i").replace("ó", "o").replace("ú", "u")
        for c in df.columns
    ]
    return df


def load_matching_files(keywords: Iterable[str]) -> pd.DataFrame:
    ensure_directories()
    frames: list[pd.DataFrame] = []
    keywords = [k.lower() for k in keywords]
    for path in sorted(INCOMING_DIR.glob("*")):
        if path.suffix.lower() not in [".csv", ".xlsx", ".xls"]:
            continue
        name = path.name.lower()
        if any(keyword in name for keyword in keywords):
            try:
                df = _normalize_columns(_read_file(path))
                df["archivo_origen"] = path.name
                frames.append(df)
            except Exception:
                continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def load_complaints() -> pd.DataFrame:
    """
    Carga los reclamos usados por KPIs, tablas y asistente IA.

    Ahora prioriza los reclamos registrados desde el formulario:
    - reclamos_registros.csv
    - reclamo_registros.csv

    Ya no usa el histórico como fuente principal.
    """

    posibles_archivos = [
        INCOMING_DIR / "reclamos_registros.csv",
        INCOMING_DIR / "reclamo_registros.csv",
    ]

    for path in posibles_archivos:
        if path.exists():
            df = pd.read_csv(path)
            df["archivo_origen"] = path.name

            if "fecha" in df.columns:
                df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

            return df

    return pd.DataFrame(columns=COMPLAINT_COLUMNS)


def load_surveys() -> pd.DataFrame:

    registros_path = INCOMING_DIR / "encuesta_salida_registros.csv"
    historico_path = INCOMING_DIR / "encuesta_salida_historico_dambo.csv"

    if registros_path.exists():
        df = pd.read_csv(registros_path)
        df["archivo_origen"] = "encuesta_salida_registros.csv"
    elif historico_path.exists():
        df = pd.read_csv(historico_path)
        df["archivo_origen"] = "encuesta_salida_historico_dambo.csv"
    else:
        return pd.DataFrame()

    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    return df


def load_agenda() -> pd.DataFrame:
    df = load_matching_files(["agenda", "estrategia", "capacitacion"])
    if df.empty:
        return pd.DataFrame(
            [
                ["2026-07-05", "Sede Centro", "Microcapacitación en manejo de cliente difícil", "Jefe demo - Centro", "Pendiente", "Alta"],
                ["2026-07-08", "Sede Norte", "Focus group de comunicación y confianza", "Jefe demo - Norte", "En planificación", "Media"],
                ["2026-07-10", "Sede Sur", "Sesión de seguridad psicológica", "Jefe demo - Sur", "Pendiente", "Alta"],
            ],
            columns=AGENDA_COLUMNS,
        )
    for col in AGENDA_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def load_indicators() -> pd.DataFrame:
    df = load_matching_files(["indicador", "kpi", "ventas", "productividad"])
    if df.empty:
        return pd.DataFrame(columns=INDICATOR_COLUMNS + ["archivo_origen"])
    for col in INDICATOR_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col in ["periodo", "sede", "lider"] else 0
    numeric_cols = [
        "ventas_mes",
        "meta_ventas",
        "productividad_pct",
        "clientes_atendidos",
        "ticket_promedio",
        "reclamos_mes",
        "capacitaciones_programadas",
        "capacitaciones_completadas",
        "cumplimiento_capacitacion",
        "tasa_ausentismo",
        "rotacion_personal",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["sede"] = df["sede"].replace("", "Sede Centro").fillna("Sede Centro")
    return df


def load_oxygen() -> pd.DataFrame:
    df = load_matching_files(["oxygen", "oxigeno", "oxígeno"])
    if df.empty:
        return pd.DataFrame(columns=OXYGEN_COLUMNS + ["archivo_origen"])
    for col in OXYGEN_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col in ["periodo", "sede", "lider", "comportamiento", "observacion"] else 0
    df["cumplimiento_estimado"] = pd.to_numeric(df["cumplimiento_estimado"], errors="coerce").fillna(0)
    df["sede"] = df["sede"].replace("", "Sede Centro").fillna("Sede Centro")
    return df


def append_row_csv(filename: str, row: dict, columns: list[str]) -> Path:
    ensure_directories()
    path = INCOMING_DIR / filename
    row_df = pd.DataFrame([row], columns=columns)
    if path.exists():
        old_df = pd.read_csv(path)
        df = pd.concat([old_df, row_df], ignore_index=True)
    else:
        df = row_df
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def filter_by_sede(df: pd.DataFrame, sede: str) -> pd.DataFrame:
    if df.empty or "sede" not in df.columns:
        return df
    return df[df["sede"].astype(str).str.lower() == sede.lower()].copy()


def calculate_kpis(sede: str, complaints: pd.DataFrame, surveys: pd.DataFrame, indicators: pd.DataFrame | None = None, oxygen: pd.DataFrame | None = None) -> dict:
    sede_cfg = SEDES[sede]
    complaints_sede = filter_by_sede(complaints, sede)
    surveys_sede = filter_by_sede(surveys, sede)

    if not surveys_sede.empty:
        felicidad = round(float(surveys_sede["felicidad"].mean()), 1)
        seguridad = round(float(surveys_sede["seguridad_psicologica"].mean()), 1)
    else:
        felicidad = 3.6
        seguridad = 3.2

    if not complaints_sede.empty:
        satisfaccion_cliente = round(float(complaints_sede["puntuacion_cliente"].mean()), 1)
        reclamos_mes = int(len(complaints_sede))
    else:
        satisfaccion_cliente = 3.4
        reclamos_mes = 9

    ventas_mes = sede_cfg["ventas_mes"]
    meta_ventas = sede_cfg["meta_ventas"]
    productividad = round((ventas_mes / meta_ventas) * 100, 1)
    clientes_atendidos = 0
    ticket_promedio = 0.0
    cumplimiento_capacitacion = 0.0
    tasa_ausentismo = 0.0
    rotacion_personal = 0.0

    if indicators is not None and not indicators.empty:
        indicators_sede = filter_by_sede(indicators, sede)
        if not indicators_sede.empty:
            indicators_sede = indicators_sede.copy()
            latest = indicators_sede.sort_values("periodo").iloc[-1]
            ventas_mes = float(latest.get("ventas_mes", ventas_mes))
            meta_ventas = float(latest.get("meta_ventas", meta_ventas)) or meta_ventas
            productividad = round(float(latest.get("productividad_pct", (ventas_mes / meta_ventas) * 100)), 1)
            clientes_atendidos = int(latest.get("clientes_atendidos", 0))
            ticket_promedio = round(float(latest.get("ticket_promedio", 0)), 2)
            reclamos_mes = int(latest.get("reclamos_mes", reclamos_mes))
            cumplimiento_capacitacion = round(float(latest.get("cumplimiento_capacitacion", 0)), 1)
            tasa_ausentismo = round(float(latest.get("tasa_ausentismo", 0)), 1)
            rotacion_personal = round(float(latest.get("rotacion_personal", 0)), 1)

    oxygen_pct = 50.0
    if oxygen is not None and not oxygen.empty:
        oxygen_sede = filter_by_sede(oxygen, sede)
        if not oxygen_sede.empty and "cumplimiento_estimado" in oxygen_sede.columns:
            oxygen_pct = round(float(oxygen_sede["cumplimiento_estimado"].mean()), 1)
    elif not surveys_sede.empty:
        claridad = float(surveys_sede["claridad_objetivos"].mean())
        feedback = float(surveys_sede["feedback_lider"].mean())
        oxygen_pct = round(((seguridad + claridad + feedback) / 15) * 100, 1)

    return {
        "oxygen_pct": oxygen_pct,
        "ventas_mes": ventas_mes,
        "meta_ventas": meta_ventas,
        "felicidad": felicidad,
        "seguridad_psicologica": seguridad,
        "satisfaccion_cliente": satisfaccion_cliente,
        "reclamos_mes": reclamos_mes,
        "productividad_pct": productividad,
        "clientes_atendidos": clientes_atendidos,
        "ticket_promedio": ticket_promedio,
        "cumplimiento_capacitacion": cumplimiento_capacitacion,
        "tasa_ausentismo": tasa_ausentismo,
        "rotacion_personal": rotacion_personal,
    }


def urgency_from_text(text: str, score: float | int | str = 0) -> str:
    text = str(text).lower()
    score_value = pd.to_numeric(pd.Series([score]), errors="coerce").fillna(0).iloc[0]
    critical_terms = ["agres", "insulto", "amenaza", "discrimin", "acoso", "grit", "humill"]
    high_terms = ["mala atención", "mal trato", "reclamo", "queja", "no me escuch", "jefe", "lider", "presión"]
    if any(term in text for term in critical_terms) or score_value <= 1:
        return "Crítica"
    if any(term in text for term in high_terms) or score_value <= 2:
        return "Alta"
    if score_value <= 3:
        return "Media"
    return "Baja"


def add_urgency(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    if "texto" in df.columns:
        score_col = "puntuacion_cliente" if "puntuacion_cliente" in df.columns else None
        df["urgencia_calculada"] = df.apply(
            lambda r: urgency_from_text(r.get("texto", ""), r.get(score_col, 0) if score_col else 0),
            axis=1,
        )
    elif "comentario" in df.columns:
        df["urgencia_calculada"] = df.apply(
            lambda r: urgency_from_text(r.get("comentario", ""), r.get("felicidad", 0)),
            axis=1,
        )
    return df


def read_knowledge_sources() -> str:
    ensure_directories()
    chunks: list[str] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")) + sorted(KNOWLEDGE_DIR.glob("*.txt")):
        try:
            text = path.read_text(encoding="utf-8")
            clean = re.sub(r"\s+", " ", text).strip()
            chunks.append(f"Fuente interna: {path.name}\n{clean[:3500]}")
        except Exception:
            continue
    return "\n\n".join(chunks)


def make_sample_files() -> None:
    ensure_directories()
    complaints_path = INCOMING_DIR / "reclamos_demo.csv"
    survey_path = INCOMING_DIR / "encuesta_salida_demo.csv"
    agenda_path = INCOMING_DIR / "agenda_estrategias_demo.csv"

    has_complaints = any(k in path.name.lower() for path in INCOMING_DIR.glob("*") for k in ["reclamo", "queja", "complaint"] if path.suffix.lower() in [".csv", ".xlsx", ".xls"])
    has_surveys = any(k in path.name.lower() for path in INCOMING_DIR.glob("*") for k in ["encuesta", "survey", "salida"] if path.suffix.lower() in [".csv", ".xlsx", ".xls"])
    has_agenda = any(k in path.name.lower() for path in INCOMING_DIR.glob("*") for k in ["agenda", "estrategia", "capacitacion"] if path.suffix.lower() in [".csv", ".xlsx", ".xls"])

    if not has_complaints and not complaints_path.exists():
        complaints = pd.DataFrame(
            [
                ["2026-07-01", "Sede Centro", "Cliente", "Mala atención", "Ana Torres", "Jefe demo - Centro", "El trabajador respondió con poca empatía y no explicó la solución del reclamo.", 2, "Alta"],
                ["2026-07-01", "Sede Centro", "Trabajador", "Liderazgo", "Luis Ramos", "Jefe demo - Centro", "El equipo siente presión por productividad y poca retroalimentación positiva.", 3, "Media"],
                ["2026-06-30", "Sede Norte", "Trabajador", "Comunicación", "Marta Ruiz", "Jefe demo - Norte", "No queda claro qué espera el líder y las prioridades cambian sin aviso.", 3, "Media"],
                ["2026-06-29", "Sede Sur", "Cliente", "Mala atención", "Carlos Díaz", "Jefe demo - Sur", "La atención fue fría y el colaborador parecía muy cansado durante el proceso.", 2, "Alta"],
                ["2026-06-28", "Sede Sur", "Trabajador", "Seguridad psicológica", "Rosa León", "Jefe demo - Sur", "Algunos colaboradores no se atreven a reportar errores por miedo a ser culpados.", 2, "Alta"],
            ],
            columns=COMPLAINT_COLUMNS,
        )
        complaints.to_csv(complaints_path, index=False, encoding="utf-8-sig")

    if not has_surveys and not survey_path.exists():
        surveys = pd.DataFrame(
            [
                ["2026-07-01", "Sede Centro", "Ana Torres", "Jefe demo - Centro", 3, 3, 4, 2, 4, "Faltan pausas y reconocimiento al cierre del día."],
                ["2026-07-01", "Sede Centro", "Luis Ramos", "Jefe demo - Centro", 4, 3, 3, 3, 5, "Se necesita ordenar mejor la carga en hora punta."],
                ["2026-06-30", "Sede Norte", "Marta Ruiz", "Jefe demo - Norte", 3, 4, 2, 2, 3, "El líder debería dar instrucciones más claras."],
                ["2026-06-29", "Sede Sur", "Carlos Díaz", "Jefe demo - Sur", 2, 2, 3, 2, 5, "No todos se sienten cómodos hablando de errores."],
                ["2026-06-29", "Sede Sur", "Rosa León", "Jefe demo - Sur", 3, 2, 3, 3, 4, "Necesitamos reuniones cortas para decir qué está fallando."],
            ],
            columns=SURVEY_COLUMNS,
        )
        surveys.to_csv(survey_path, index=False, encoding="utf-8-sig")

    if not has_agenda and not agenda_path.exists():
        agenda = pd.DataFrame(
            [
                ["2026-07-05", "Sede Centro", "Capacitación corta: atención empática y contención de reclamos", "Jefe demo - Centro", "Pendiente", "Alta"],
                ["2026-07-08", "Sede Norte", "Focus group: claridad de objetivos y prioridades", "Jefe demo - Norte", "Pendiente", "Media"],
                ["2026-07-10", "Sede Sur", "Dinámica de seguridad psicológica y aprendizaje de errores", "Jefe demo - Sur", "Pendiente", "Alta"],
            ],
            columns=AGENDA_COLUMNS,
        )
        agenda.to_csv(agenda_path, index=False, encoding="utf-8-sig")
