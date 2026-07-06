from __future__ import annotations

import plotly.graph_objects as go

from .config import TAMBO_COLORS


def apply_tambo_theme(fig: go.Figure, height: int = 360) -> go.Figure:
    """Aplica la paleta Tambo a gráficos Plotly."""
    fig.update_layout(
        height=height,
        paper_bgcolor=TAMBO_COLORS["white"],
        plot_bgcolor=TAMBO_COLORS["white"],
        font={"family": "Arial, sans-serif", "color": TAMBO_COLORS["text"], "size": 13},
        title={"font": {"size": 16, "color": TAMBO_COLORS["purple_dark"]}},
        margin={"l": 24, "r": 24, "t": 48, "b": 24},
        xaxis={
            "gridcolor": TAMBO_COLORS["border"],
            "linecolor": TAMBO_COLORS["border"],
            "tickfont": {"color": TAMBO_COLORS["text_muted"]},
        },
        yaxis={
            "gridcolor": TAMBO_COLORS["border"],
            "linecolor": TAMBO_COLORS["border"],
            "tickfont": {"color": TAMBO_COLORS["text_muted"]},
        },
        legend={"bgcolor": "rgba(255,255,255,0.8)"},
    )
    return fig


def urgency_color_map() -> dict[str, str]:
    return TAMBO_COLORS["urgency"]
