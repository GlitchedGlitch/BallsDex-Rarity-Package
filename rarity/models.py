from django.db import models
from settings.models import Settings
from bd_models.models import Ball, Special


class RarityTag(models.Model):
    """
    Custom tags appended to specific rarity values in the rarity list.
    """
    rarity_value = models.FloatField(
        help_text="The rarity value to tag. Use -1 for tier mode tags.",
        verbose_name="Rarity value",
    )
    is_tier_tag = models.BooleanField(
        default=False,
        help_text="If checked, rarity_value is treated as a tier number instead of raw rarity",
        verbose_name="Is tier tag",
    )
    tag_text = models.CharField(
        max_length=64,
        help_text="Text to append (e.g. 'craftable', 'event only')",
        verbose_name="Tag text",
    )

    class Meta:
        app_label = "settings"
        db_table = "rarity_raritytag"
        verbose_name = "Rarity Tag"
        verbose_name_plural = "Rarity Tags"

    def __str__(self) -> str:
        mode = "Tier" if self.is_tier_tag else "Rarity"
        return f"{mode} {self.rarity_value}: {self.tag_text}"


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
    hidden_balls = models.ManyToManyField(
        Ball,
        blank=True,
        related_name="hidden_from_rarity",
        help_text="Balls to hide from the rarity list",
        verbose_name="Hidden balls",
    )
    hidden_specials = models.ManyToManyField(
        Special,
        blank=True,
        related_name="hidden_from_rarity",
        help_text="Specials to hide from the rarity list",
        verbose_name="Hidden specials",
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

    def get_hidden_balls_set(self) -> set[int]:
        """Return a set of hidden ball IDs."""
        return set(self.hidden_balls.values_list("pk", flat=True))

    def get_hidden_specials_set(self) -> set[int]:
        """Return a set of hidden special IDs."""
        return set(self.hidden_specials.values_list("pk", flat=True))


class RaritySettingsProxy:
    """
    Proxy to access RaritySettings singleton safely.
    """
    _instance: RaritySettings | None = None

    @classmethod
    def get_instance(cls) -> RaritySettings | None:
        if cls._instance is None:
            try:
                cls._instance = RaritySettings.objects.select_related("settings").first()
            except Exception:
                pass
        return cls._instance

    @classmethod
    def clear_cache(cls):
        cls._instance = None
