"""
settings cuz why not
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rarity.models import RaritySettings


async def load_settings() -> dict[str, str | int | bool | set[int]]:
    from settings.models import Settings
    from rarity.models import RaritySettings, RarityTag

    settings_obj = await Settings.objects.prefetch_related("rarity_settings").afirst()
    
    defaults = {
        "embed_color": "",
        "style": "container",
        "buttons_inside": True,
        "tier_mode": False,
        "entries_per_page": 7,
        "search_enabled": True,
        "rarity_search_enabled": True,
        "ephemeral_enabled": True,
        "hidden_balls": set(),
        "hidden_specials": set(),
        "show_thumbnail": True,
        "rarity_tags": {},
    }

    if not settings_obj:
        return defaults

    rarity = getattr(settings_obj, "rarity_settings", None)
    if not rarity:
        return defaults

    # Load rarity tags
    tags = {}
    async for tag in RarityTag.objects.all():
        key = (tag.rarity_value, tag.is_tier_tag)
        tags[key] = tag.tag_text

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
        "hidden_specials": rarity.get_hidden_specials_set(),
        "show_thumbnail": rarity.show_thumbnail,
        "rarity_tags": tags,
    }
