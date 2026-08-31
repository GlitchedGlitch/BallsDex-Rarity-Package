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
        editable=False,  # Hide from admin form
    )
    
    class Style(models.TextChoices):
        EMBED = "embed", "Embed"
        CONTAINER = "container", "Container"

    embed_color = models.CharField(
        max_length=7,
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
        verbose_name = "Rarity Settings"
        verbose_name_plural = "Rarity Settings"

    def __str__(self) -> str:
        return "Rarity Settings"
