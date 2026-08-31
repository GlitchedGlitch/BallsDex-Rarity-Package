"""
settings cuz why not
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings.models import Settings


def load_settings(settings_obj: "Settings") -> dict[str, str]:
    """
    Load rarity settings from the Django Settings model.
    """
    return {
        "embed_color": getattr(settings_obj, "rarity_embed_color", "") or "",
        "style": getattr(settings_obj, "rarity_style", "container") or "container",
        "buttons_inside": "true" if getattr(settings_obj, "rarity_buttons_inside", True) else "false",
    }


def get_embed_color(settings_obj: "Settings") -> str:
    return load_settings(settings_obj)["embed_color"]


def get_style(settings_obj: "Settings") -> str:
    return load_settings(settings_obj)["style"]


def get_buttons_inside(settings_obj: "Settings") -> bool:
    return load_settings(settings_obj)["buttons_inside"] == "true"
