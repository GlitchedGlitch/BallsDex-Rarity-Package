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

    class Meta:
        app_label = "settings"  # Makes it appear under Settings in admin
        db_table = "rarity_raritysettings"
        verbose_name = "Rarity settings"
        verbose_name_plural = "Rarity settings"

    def __str__(self) -> str:
        return "Rarity Settings"
