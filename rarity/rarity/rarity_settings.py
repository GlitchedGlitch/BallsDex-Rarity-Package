"""
settings cuz why not
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rarity.models import RaritySettings


async def load_settings() -> dict[str, str | int | bool | set[str]]:
    from settings.models import Settings
    from rarity.models import RaritySettings

    settings_obj = await Settings.objects.prefetch_related("rarity_settings").afirst()
    
    if not settings_obj:
        return {
            "embed_color": "",
            "style": "container",
            "buttons_inside": True,
            "tier_mode": False,
            "entries_per_page": 7,
            "search_enabled": True,
            "rarity_search_enabled": True,
            "ephemeral_enabled": True,
            "hidden_balls": set(),
            "show_thumbnail": True,
        }

    rarity = getattr(settings_obj, "rarity_settings", None)
    
    if not rarity:
        return {
            "embed_color": "",
            "style": "container",
            "buttons_inside": True,
            "tier_mode": False,
            "entries_per_page": 7,
            "search_enabled": True,
            "rarity_search_enabled": True,
            "ephemeral_enabled": True,
            "hidden_balls": set(),
            "show_thumbnail": True,
        }

    return {
        "embed_color": rarity.embed_color or "",
        "style": rarity.style,
        "buttons_inside": rarity.buttons_inside,
        "tier_mode": rarity.tier_mode,
        "entries_per_page": rarity.entries_per_page,
        "search_enabled": rarity.search_enabled,
        "rarity_search_enabled": rarity.rarity_search_enabled,
        "ephemeral_enabled": rarity.ephemeral_enabled,
        "hidden_balls": rarity.get_hidden_balls_set(),
        "show_thumbnail": rarity.show_thumbnail,
    }
