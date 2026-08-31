from django.db import models
from settings.models import Settings


class RaritySettings(models.Model):
    """
    Rarity-specific settings stored separately but linked to global Settings.
    """
    settings = models.OneToOneField(
        Settings,
        on_delete=models.CASCADE,
        related_name="rarity_settings",
    )
    embed_color = models.CharField(
        max_length=7,
        blank=True,
        default="",
        help_text="Hex color for the line, leave empty for no color",
    )
    style = models.CharField(
        max_length=10,
        blank=True,
        default="container",
        help_text="Rarity list display style: 'embed' or 'container'",
    )
    buttons_inside = models.BooleanField(
        default=True,
        help_text="Place pagination buttons inside the container (only applies to container style)",
    )

    class Meta:
        verbose_name = "Rarity Settings"
        verbose_name_plural = "Rarity Settings"

    def __str__(self) -> str:
        return "Rarity Settings"
