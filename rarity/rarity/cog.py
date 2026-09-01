"""
Rarity package for BallsDex v3 :333
"""

from __future__ import annotations

import logging
import math
from collections import defaultdict
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import ActionRow, Button, button

from bd_models.models import Ball, balls as balls_cache, specials as special_cache
from ballsdex.core.discord import LayoutView
from ballsdex.core.utils.menus import Menu
from ballsdex.core.utils.menus.source import ListSource
from ballsdex.core.utils.menus.formatter import ItemFormatter
from ballsdex.core.utils.transformers import BallEnabledTransform, SpecialEnabledTransform
from settings.models import settings

from .rarity_settings import load_settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.rarity")


def _ball_emoji(bot: "BallsDexBot", ball: Ball) -> str:
    if ball.emoji_id:
        emoji = bot.get_emoji(ball.emoji_id)
        if emoji:
            return str(emoji)
    return "⋄"


def _hex_to_color(hex_str: str) -> discord.Color | None:
    hex_str = hex_str.strip().lstrip("#")
    if not hex_str:
        return None
    try:
        return discord.Color(int(hex_str, 16))
    except ValueError:
        return None


def _calculate_tiers(balls_list: list[Ball]) -> dict[int, list[Ball]]:
    """
    Calculate tiers from rarity values using logarithmic scaling.
    T1 = most rare (lowest rarity value), higher tiers = more common.
    """
    if not balls_list:
        return {}

    # Sort by rarity ascending
    sorted_balls = sorted(balls_list, key=lambda b: b.rarity)
    
    rarities = [b.rarity for b in sorted_balls]
    max_r = max(rarities)
    min_r = min(rarities)
    
    if max_r == min_r:
        return {1: sorted_balls}

    log_max = math.log10(max_r) if max_r > 0 else 0
    log_min = math.log10(min_r) if min_r > 0 else 0
    log_range = log_max - log_min if log_max != log_min else 1
    
    tiers: dict[int, list[Ball]] = defaultdict(list)
    
    for ball in sorted_balls:
        if ball.rarity <= 0:
            continue
        log_r = math.log10(ball.rarity) if ball.rarity > 0 else log_min
        normalized = (log_r - log_min) / log_range if log_range > 0 else 0
        tier = max(1, int(normalized * 99) + 1)
        tiers[tier].append(ball)

    return dict(tiers)


def _format_rarity_value(rarity: float, tier_mode: bool) -> str:
    """Format rarity value for display."""
    if tier_mode:
        return f"T{int(rarity)}"
    return str(rarity)


class RarityCog(commands.Cog):
    """Rarity package"""

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot


class RarityItemFormatter(ItemFormatter):
    async def format_page(self, page):
        children = list(self.item.children)
        fixed_top = children[: self.position]
        button_rows = [child for child in children if isinstance(child, ActionRow)]

        for child in children[self.position:]:
            self.item.remove_item(child)

        for section in page:
            self.item.add_item(section)

        if self.footer and self.menu.source.get_max_pages() > 1:
            self.item.add_item(
                discord.ui.TextDisplay(
                    f"-# Page {self.menu.current_page + 1}/{self.menu.source.get_max_pages()}"
                )
            )

        for row in button_rows:
            self.item.add_item(row)


class RarityView(LayoutView):
    """Custom view with permission checking."""

    def __init__(self, user_id: int, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "You are not allowed to interact with this.", ephemeral=True
            )
            return False
        return True


class QuitButtonRow(ActionRow):
    def __init__(self, rarity_view: RarityView):
        super().__init__()
        self.rarity_view = rarity_view

    @button(label="Quit", style=discord.ButtonStyle.danger)
    async def quit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        for item in self.rarity_view.walk_children():
            if hasattr(item, "disabled"):
                item.disabled = True  # type: ignore
        await interaction.edit_original_response(view=self.rarity_view)


class GoToPageModal(discord.ui.Modal, title="Go to page"):
    page = discord.ui.TextInput(label="Page", placeholder="Enter a number", min_length=1)

    def __init__(self, paginator: "EmbedPaginatorView"):
        super().__init__()
        self.paginator = paginator
        as_string = str(len(paginator.pages))
        self.page.placeholder = f"Enter a number between 1 and {as_string}"
        self.page.max_length = len(as_string)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            page = int(self.page.value)
        except ValueError:
            await interaction.response.send_message("Expected a number", ephemeral=True)
            return
        if page < 1:
            await interaction.response.send_message("Minimum value is 1", ephemeral=True)
        elif page > len(self.paginator.pages):
            await interaction.response.send_message(
                f"Maximum value is {len(self.paginator.pages)}", ephemeral=True
            )
        else:
            await self.paginator.show_page(interaction, page - 1)


class EmbedPaginatorView(discord.ui.View):
    def __init__(
        self,
        user_id: int,
        pages: list[discord.Embed],
        buttons_inside: bool,
        *,
        timeout: float | None = 180,
    ):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.pages = pages
        self.current_page = 0
        self.buttons_inside = buttons_inside
        self._build()

    def _build(self):
        self.clear_items()
        multi_page = len(self.pages) > 1

        if multi_page:
            self.first_btn = Button(label="≪", style=discord.ButtonStyle.grey)
            self.first_btn.callback = self._go_first
            self.add_item(self.first_btn)

            self.prev_btn = Button(label="Back", style=discord.ButtonStyle.blurple)
            self.prev_btn.callback = self._go_prev
            self.add_item(self.prev_btn)

            self.goto_btn = Button(
                label=f"{self.current_page + 1} (go to)", style=discord.ButtonStyle.blurple
            )
            self.goto_btn.callback = self._go_to
            self.add_item(self.goto_btn)

            self.next_btn = Button(label="Next", style=discord.ButtonStyle.blurple)
            self.next_btn.callback = self._go_next
            self.add_item(self.next_btn)

            self.last_btn = Button(label="≫", style=discord.ButtonStyle.grey)
            self.last_btn.callback = self._go_last
            self.add_item(self.last_btn)

            self._edit_buttons()

        quit_btn = Button(label="Quit", style=discord.ButtonStyle.danger)
        quit_btn.callback = self._quit
        self.add_item(quit_btn)

    def _edit_buttons(self):
        max_page = len(self.pages)
        self.goto_btn.label = f"{self.current_page + 1} (go to)"

        if self.current_page > 0:
            self.prev_btn.label = str(self.current_page)
            self.prev_btn.disabled = False
            self.first_btn.disabled = False
        else:
            self.prev_btn.label = "Back"
            self.prev_btn.disabled = True
            self.first_btn.disabled = True

        if self.current_page < max_page - 1:
            self.next_btn.label = str(self.current_page + 2)
            self.next_btn.disabled = False
            self.last_btn.disabled = False
        else:
            self.next_btn.label = "Next"
            self.next_btn.disabled = True
            self.last_btn.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "You are not allowed to interact with this.", ephemeral=True
            )
            return False
        return True

    async def show_page(self, interaction: discord.Interaction, page: int):
        self.current_page = page
        self._edit_buttons()
        if interaction.response.is_done():
            await interaction.edit_original_response(embed=self.pages[page], view=self)
        else:
            await interaction.response.edit_message(embed=self.pages[page], view=self)

    async def _go_first(self, interaction: discord.Interaction):
        await self.show_page(interaction, 0)

    async def _go_prev(self, interaction: discord.Interaction):
        await self.show_page(interaction, self.current_page - 1)

    async def _go_to(self, interaction: discord.Interaction):
        await interaction.response.send_modal(GoToPageModal(self))

    async def _go_next(self, interaction: discord.Interaction):
        await self.show_page(interaction, self.current_page + 1)

    async def _go_last(self, interaction: discord.Interaction):
        await self.show_page(interaction, len(self.pages) - 1)

    async def _quit(self, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True  # type: ignore
        await interaction.response.edit_message(view=self)
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True  # type: ignore


def _build_rarity_command_describe(
    pkg_settings: dict,
) -> dict[str, app_commands.describe]:
    """
    Build describe decorators dynamically based on settings.
    Returns a dict of parameter names to describe objects.
    """
    describes = {}

    if pkg_settings["search_enabled"]:
        describes["search"] = app_commands.describe(
            search=f"Search a specific {settings.collectible_name}'s rarity"
        )

    # Special is always a user option
    describes["special"] = app_commands.describe(
        special="Show the special event rarity list instead of balls"
    )

    if pkg_settings["ephemeral_enabled"]:
        describes["ephemeral"] = app_commands.describe(
            ephemeral="Whether or not to send the command ephemerally"
        )

    describes["reverse"] = app_commands.describe(
        reverse="Reverse the output of the rarity list"
    )

    return describes


def build_rarity_command(bot: "BallsDexBot") -> app_commands.Command:
    """
    Build the rarity command with all configurable options.
    Dynamically adds/removes parameters based on admin settings.
    """

    # Load settings at command build time to determine parameters
    # Note: This is sync, but settings are cached. For truly dynamic,
    # we'd need to rebuild the command on settings change.
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        pkg_settings = loop.run_until_complete(load_settings())
    except RuntimeError:
        # Fallback defaults
        pkg_settings = {
            "search_enabled": True,
            "ephemeral_enabled": True,
            "tier_mode": False,
            "entries_per_page": 7,
            "special_rarity": False,
            "rarity_search_enabled": True,
            "hidden_balls": set(),
            "show_thumbnail": True,
            "embed_color": "",
            "style": "container",
            "buttons_inside": True,
        }

    # Build the command signature dynamically
    params = []
    if pkg_settings["search_enabled"]:
        params.append("search: str | None = None")
    
    # Special is always available as user option
    params.append("special: bool = False")
    
    params.append("reverse: bool = False")
    
    if pkg_settings["ephemeral_enabled"]:
        params.append("ephemeral: bool = False")

    # We need to use exec to build the function with dynamic signature
    # But that's messy. Instead, we'll define all params and check settings inside.
    
    @app_commands.command(
        name="rarity",
        description="Check the rarity list of the bot",
    )
    async def rarity(
        interaction: discord.Interaction,
        search: str | None = None,
        special: bool = False,
        reverse: bool = False,
        ephemeral: bool = False,
    ):
        plural = settings.plural_collectible_name.capitalize()
        pkg_settings = await load_settings()

        # Check if ephemeral is enabled in settings
        if not pkg_settings["ephemeral_enabled"]:
            ephemeral = False

        # Check if search is used but disabled
        if search is not None and not pkg_settings["search_enabled"]:
            await interaction.response.send_message(
                "Search is disabled for this command.",
                ephemeral=True,
            )
            return

        # Determine which model to use
        # "special" parameter is user choice, overrides default
        use_specials = special

        if use_specials:
            # Special rarity mode
            all_items = [s for s in special_cache.values() if s.rarity > 0 and not s.hidden]
            item_name_key = lambda x: x.name
            item_emoji_key = lambda x: x.emoji or "N/A"
            item_rarity_key = lambda x: float(x.rarity)
            list_title = f"{settings.bot_name} Special Rarity List"
        else:
            # Ball rarity mode
            hidden_balls = pkg_settings["hidden_balls"]
            all_items = [b for b in balls_cache.values() if b.enabled and b.rarity > 0]
            all_items = [b for b in all_items if b.country.lower() not in hidden_balls]
            item_name_key = lambda x: x.country
            item_emoji_key = lambda x: _ball_emoji(bot, x)
            item_rarity_key = lambda x: float(x.rarity)
            list_title = f"{settings.bot_name} Rarity List"

        if not all_items:
            await interaction.response.send_message(
                f"No {'specials' if use_specials else settings.plural_collectible_name} are currently available.",
                ephemeral=True,
            )
            return

        # ── Search mode ───────────────────────────────────────────────────────
        if search:
            # Try rarity value search (if enabled)
            is_rarity_search = False
            if pkg_settings["rarity_search_enabled"]:
                try:
                    rarity_value = float(search.replace(",", "."))
                    is_rarity_search = True
                except ValueError:
                    is_rarity_search = False

            if is_rarity_search:
                # Search by rarity value
                if pkg_settings["tier_mode"]:
                    try:
                        tier_num = int(search)
                        tiers = _calculate_tiers(all_items)
                        matches = tiers.get(tier_num, [])
                    except ValueError:
                        matches = []
                else:
                    matches = [b for b in all_items if abs(item_rarity_key(b) - rarity_value) < 0.0001]

                if not matches:
                    await interaction.response.send_message(
                        f"No {'specials' if use_specials else settings.collectible_name} found with rarity `{search}`.",
                        ephemeral=True,
                    )
                    return

                lines = [f"{item_emoji_key(b)} {item_name_key(b)}" for b in matches]
                if pkg_settings["tier_mode"]:
                    await interaction.response.send_message(
                        f"T{search} {'specials' if use_specials else plural}:\n" + "\n".join(lines),
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        f"{'Specials' if use_specials else plural} with rarity `{search}`:\n" + "\n".join(lines),
                        ephemeral=True,
                    )
                return

            # Search by name
            match = next((b for b in all_items if item_name_key(b).lower() == search.lower()), None)
            if not match:
                match = next((b for b in all_items if search.lower() in item_name_key(b).lower()), None)
            if not match:
                await interaction.response.send_message(
                    f"No {'special' if use_specials else settings.collectible_name} found matching `{search}`.",
                    ephemeral=True,
                )
                return

            emoji = item_emoji_key(match)
            name = item_name_key(match)
            rarity_val = item_rarity_key(match)

            if pkg_settings["tier_mode"]:
                tiers = _calculate_tiers(all_items)
                tier_num = None
                for t, items in tiers.items():
                    if match in items:
                        tier_num = t
                        break
                rarity_display = f"T{tier_num}" if tier_num else "N/A"
            else:
                rarity_display = _format_rarity_value(rarity_val, False)

            await interaction.response.send_message(
                f"{emoji} **{name}**\nRarity: `{rarity_display}`",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=ephemeral)

        # Build rarity map
        if pkg_settings["tier_mode"]:
            rarity_map = _calculate_tiers(all_items)
            sorted_keys = sorted(rarity_map.keys())
        else:
            rarity_map: dict[float, list] = defaultdict(list)
            for b in all_items:
                rarity_map[item_rarity_key(b)].append(b)
            sorted_keys = sorted(rarity_map.keys(), reverse=reverse)

        if not sorted_keys:
            await interaction.followup.send(
                f"No {'specials' if use_specials else settings.plural_collectible_name} are currently available.",
                ephemeral=ephemeral,
            )
            return

        line_color = _hex_to_color(pkg_settings["embed_color"])
        use_embed_style = pkg_settings["style"] == "embed"
        buttons_inside = pkg_settings["buttons_inside"]
        entries_per_page = pkg_settings["entries_per_page"]
        show_thumbnail = pkg_settings["show_thumbnail"]

        # Get bot avatar URL
        bot_avatar = bot.user.display_avatar.url if bot.user else None

        if use_embed_style:
            # Embed style
            entries: list[tuple[str, str]] = []
            for key in sorted_keys:
                group_items = rarity_map[key]
                lines = "\n".join(
                    f"⋄ {item_emoji_key(b)} {item_name_key(b)}" for b in group_items
                )
                if pkg_settings["tier_mode"]:
                    entries.append((f"∥ T{key}", lines))
                else:
                    entries.append((f"∥ Rarity: {key}", lines))

            chunks = [
                entries[i : i + entries_per_page]
                for i in range(0, len(entries), entries_per_page)
            ]
            total_pages = len(chunks)

            embed_pages: list[discord.Embed] = []
            for page_num, chunk in enumerate(chunks, start=1):
                e = discord.Embed(
                    title=list_title,
                    color=line_color if line_color is not None else discord.Color(0xFFFFFF),
                )
                if show_thumbnail and bot_avatar:
                    e.set_thumbnail(url=bot_avatar)
                for name, value in chunk:
                    e.add_field(name=name, value=value, inline=False)
                if total_pages > 1:
                    e.set_footer(text=f"Page {page_num}/{total_pages}")
                embed_pages.append(e)

            view = EmbedPaginatorView(interaction.user.id, embed_pages, buttons_inside)

            await interaction.followup.send(
                embed=embed_pages[0], view=view, ephemeral=ephemeral
            )
            return

        # Container style
        all_components: list[discord.ui.Item] = []
        for key in sorted_keys:
            group_items = rarity_map[key]
            lines = "\n".join(
                f"⋄ {item_emoji_key(b)} {item_name_key(b)}" for b in group_items
            )
            if pkg_settings["tier_mode"]:
                all_components.append(discord.ui.TextDisplay(f"**∥ T{key}**\n{lines}"))
            else:
                all_components.append(discord.ui.TextDisplay(f"**∥ Rarity: {key}**\n{lines}"))

        pages: list[list[discord.ui.Item]] = [
            all_components[i : i + entries_per_page]
            for i in range(0, len(all_components), entries_per_page)
        ]

        view = RarityView(interaction.user.id)
        container = discord.ui.Container()
        if line_color is not None:
            container.accent_color = line_color

        # Build title with thumbnail as first item if enabled
        title_parts = []
        if show_thumbnail and bot_avatar:
            # Use markdown image syntax for thumbnail-like display in container
            title_parts.append(f"![thumbnail]({bot_avatar})")
        title_parts.append(f"# {list_title}")
        
        title_text = "\n".join(title_parts) if title_parts else f"# {list_title}"
        container.add_item(discord.ui.TextDisplay(title_text))
        container.add_item(discord.ui.Separator())
        header_item_count = 2

        view.add_item(container)

        source = ListSource(pages)
        formatter = RarityItemFormatter(container, position=header_item_count)
        menu = Menu(bot, view, source, formatter)

        await menu.init(container=container, position=header_item_count)

        quit_row = QuitButtonRow(view)

        if buttons_inside:
            container.add_item(quit_row)
        else:
            for child in list(container.children):
                if isinstance(child, ActionRow):
                    container.remove_item(child)
                    view.add_item(child)
            view.add_item(quit_row)

        first_page = await source.get_page(0)
        await formatter.format_page(first_page)

        await interaction.followup.send(view=view, ephemeral=ephemeral)

    @rarity.autocomplete("search")
    async def rarity_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        pkg_settings = await load_settings()
        
        if not pkg_settings["search_enabled"]:
            return []

        use_specials = interaction.namespace.special if hasattr(interaction.namespace, "special") else False
        hidden_balls = pkg_settings["hidden_balls"]

        results: list[app_commands.Choice[str]] = []

        if use_specials:
            for s in special_cache.values():
                if s.rarity > 0 and not s.hidden:
                    if current.lower() in s.name.lower():
                        results.append(app_commands.Choice(name=s.name, value=s.name))
                        if len(results) >= 25:
                            break
        else:
            for b in balls_cache.values():
                if b.enabled and b.rarity > 0 and b.country.lower() not in hidden_balls:
                    if current.lower() in b.country.lower():
                        results.append(app_commands.Choice(name=b.country, value=b.country))
                        if len(results) >= 25:
                            break

        return results

    return rarity
