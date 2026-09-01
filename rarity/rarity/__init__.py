from __future__ import annotations
import logging
from typing import TYPE_CHECKING
from .cog import RarityCog, build_rarity_command

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.rarity")


async def setup(bot: "BallsDexBot") -> None:
    await bot.add_cog(RarityCog(bot))
    
    from settings.models import settings
    balls_cog = bot.get_cog("Balls")

    if balls_cog is not None and hasattr(balls_cog, '__cog_app_commands_group__') and balls_cog.__cog_app_commands_group__:
        group = balls_cog.__cog_app_commands_group__
        existing = group.get_command("rarity")
        if existing is not None:
            group.remove_command("rarity")
        group.add_command(build_rarity_command(bot))
    else:
        log.warning(
            "Balls cog not found - rarity command will not be registered. "
            "Ensure the balls package loads before rarity."
        )
    
    # Check if command tree needs reload after settings change
    try:
        from rarity.models import RaritySettings
        rarity_settings = await RaritySettings.objects.select_related("settings").afirst()
        if rarity_settings and rarity_settings._reload_tree_on_change:
            log.info("Reloading command tree due to rarity settings change...")
            await bot.tree.sync()
            from ballsdex.settings import settings as bot_settings
            for guild_id in bot_settings.admin_guild_ids:
                await bot.tree.sync(guild=discord.Object(id=guild_id))
            rarity_settings._reload_tree_on_change = False
            await rarity_settings.asave(update_fields=["_reload_tree_on_change"])
            log.info("Command tree reloaded successfully.")
    except Exception as e:
        log.warning(f"Failed to check/reload command tree: {e}")


async def teardown(bot: "BallsDexBot") -> None:
    balls_cog = bot.get_cog("Balls")
    if balls_cog is not None and hasattr(balls_cog, '__cog_app_commands_group__') and balls_cog.__cog_app_commands_group__:
        try:
            balls_cog.__cog_app_commands_group__.remove_command("rarity")
        except Exception:
            pass
