"""
settings cuz why not
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import RaritySettings


async def load_settings() -> dict[str, str]:
    """
    Load rarity settings from the Django RaritySettings model.
    Falls back to defaults if no instance exists.
    """
    from settings.models import Settings
    from .models import RaritySettings

    settings_obj = await Settings.objects.prefetch_related("rarity_settings").afirst()
    
    if not settings_obj:
        return {
            "embed_color": "",
            "style": "container",
            "buttons_inside": "true",
        }

    rarity: RaritySettings | None = getattr(settings_obj, "rarity_settings", None)
    
    if not rarity:
        return {
            "embed_color": "",
            "style": "container",
            "buttons_inside": "true",
        }

    return {
        "embed_color": rarity.embed_color or "",
        "style": rarity.style,
        "buttons_inside": "true" if rarity.buttons_inside else "false",
    }


async def get_embed_color() -> str:
    s = await load_settings()
    return s["embed_color"]


async def get_style() -> str:
    s = await load_settings()
    return s["style"]


async def get_buttons_inside() -> bool:
    s = await load_settings()
    return s["buttons_inside"] == "true"
