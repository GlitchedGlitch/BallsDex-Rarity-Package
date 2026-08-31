from django.contrib import admin
from .models import RaritySettings


@admin.register(RaritySettings)
class RaritySettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "settings",
                "embed_color",
                "style",
                "buttons_inside",
            ),
        }),
    )
    list_display = ("settings", "style", "buttons_inside")
