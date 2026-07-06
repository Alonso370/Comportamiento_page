from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.config import PROCESSED_DIR


TASKS_FILE = PROCESSED_DIR / "mural_tareas_recomendaciones.json"


def _ensure_file() -> None:
    """Crea la carpeta y el archivo del mural si todavía no existen."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def load_tasks() -> list[dict]:
    """Carga todas las tareas pendientes del mural."""
    _ensure_file()

    try:
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Guarda la lista actualizada de tareas."""
    _ensure_file()
    TASKS_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def task_summary(content: str, max_chars: int = 120) -> str:
    """Crea un resumen corto para mostrar en el mural."""
    clean = (
        content.replace("#", "")
        .replace("*", "")
        .replace("\n", " ")
        .strip()
    )

    if len(clean) <= max_chars:
        return clean

    return clean[:max_chars] + "..."


def infer_priority(content: str) -> str:
    """
    Clasifica la prioridad de forma simple según el texto generado por la IA.
    Luego se puede mejorar usando reglas o IA.
    """
    text = content.lower()

    if "crítica" in text or "critica" in text or "urgente" in text:
        return "Crítica"

    if "alta" in text or "riesgo" in text:
        return "Alta"

    if "media" in text:
        return "Media"

    return "Pendiente"


def add_recommendation_task(
    sede: str,
    content: str,
    mode: str = "ia",
) -> dict:
    """
    Guarda automáticamente una recomendación generada por ChatGPT
    como tarea pendiente en el mural.
    """
    tasks = load_tasks()

    now = datetime.now()
    task = {
        "id": now.strftime("%Y%m%d%H%M%S%f"),
        "sede": sede,
        "titulo": task_summary(content, max_chars=90),
        "contenido": content,
        "prioridad": infer_priority(content),
        "estado": "Pendiente",
        "modo": mode,
        "fecha_creacion": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    tasks.insert(0, task)
    save_tasks(tasks)

    return task


def complete_task(task_id: str) -> None:
    """
    Elimina una tarea del mural cuando el jefe la marca como completada.
    """
    tasks = load_tasks()
    tasks = [task for task in tasks if task.get("id") != task_id]
    save_tasks(tasks)


def count_tasks_by_sede(sede: str | None = None) -> int:
    """Cuenta tareas pendientes, opcionalmente por sede."""
    tasks = load_tasks()

    if sede:
        tasks = [task for task in tasks if task.get("sede") == sede]

    return len(tasks)