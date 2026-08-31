from django.db import models
from settings.models import Settings


class RaritySettings(models.Model):
    """
    Rarity-specific settings
    """
    settings = models.OneToOneField(
        Settings,
        on_delete=models.CASCADE,
        related_name="rarity_settings",
        editable=False,
    )
    
    class Style(models.TextChoices):
        EMBED = "embed", "Embed"
        CONTAINER = "container", "Container"

    embed_color = models.CharField(
        max_length=6,
        blank=True,
        default="",
        help_text="Hex color for the line, leave empty for no color",
        verbose_name="Embed color",
    )
    style = models.CharField(
        max_length=10,
        choices=Style,
        default=Style.CONTAINER,
        help_text="How the rarity list message will appear",
        verbose_name="Style",
    )
    buttons_inside = models.BooleanField(
        default=True,
        help_text="Place pagination buttons inside the container (only applies to container style)",
        verbose_name="Buttons inside",
    )

    # NEW FIELDS
    tier_mode = models.BooleanField(
        default=False,
        help_text="Group balls by calculated tiers instead of raw rarity values",
        verbose_name="Tier mode",
    )
    entries_per_page = models.PositiveIntegerField(
        default=7,
        help_text="Number of rarity groups shown per page",
        verbose_name="Entries per page",
    )
    special_rarity = models.BooleanField(
        default=False,
        help_text="Enable the option to show special event rarities instead of ball rarities",
        verbose_name="Special rarity mode",
    )
    search_enabled = models.BooleanField(
        default=True,
        help_text="Enable the search parameter",
        verbose_name="Search enabled",
    )
    rarity_search_enabled = models.BooleanField(
        default=True,
        help_text="Allow searching by rarity value. Disable to search by ball name only.",
        verbose_name="Rarity search enabled",
    )
    ephemeral_enabled = models.BooleanField(
        default=True,
        help_text="Enable the ephemeral parameter",
        verbose_name="Ephemeral enabled",
    )
    hidden_balls = models.TextField(
        blank=True,
        default="",
        help_text="Semicolon-separated list of ball names to hide from the rarity list",
        verbose_name="Hidden balls",
    )
    show_thumbnail = models.BooleanField(
        default=True,
        help_text="Show the bot's profile picture as thumbnail on all pages",
        verbose_name="Show bot thumbnail",
    )

    class Meta:
        app_label = "settings"
        db_table = "rarity_raritysettings"
        verbose_name = "Rarity settings"
        verbose_name_plural = "Rarity settings"

    def __str__(self) -> str:
        return "Rarity Settings"

    def get_hidden_balls_set(self) -> set[str]:
        """Return a set of hidden ball names (case-insensitive)."""
        if not self.hidden_balls:
            return set()
        return {name.strip().lower() for name in self.hidden_balls.split(";") if name.strip()}
