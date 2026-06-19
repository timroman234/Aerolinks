# frontend/__init__.py
"""AeroLinks Frontend Module"""
from .styles import get_carbon_css, get_header_html, get_section_header_html, COLORS
from .components import (
    create_trajectory_chart,
    create_animated_trajectory_chart,
    render_animated_chart,
    render_metrics_row,
    render_physics_explainer,
)

__all__ = [
    "get_carbon_css",
    "get_header_html",
    "get_section_header_html",
    "COLORS",
    "create_trajectory_chart",
    "create_animated_trajectory_chart",
    "render_animated_chart",
    "render_metrics_row",
    "render_physics_explainer",
]
