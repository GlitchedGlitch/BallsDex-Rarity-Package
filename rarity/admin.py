from django.contrib import admin
from settings.admin import SettingsAdmin
from settings.models import Settings
from .models import RaritySettings


class RaritySettingsInline(admin.StackedInline):
    """
    Inline admin for RaritySettings, shown inside the main Settings edit page.
    """
    model = RaritySettings
    can_delete = False
    verbose_name = "Rarity Settings"
    verbose_name_plural = "Rarity Settings"
    fields = ("embed_color", "style", "buttons_inside")
    classes = ("collapse",)

_original_get_inlines = SettingsAdmin.get_inlines


def _patched_get_inlines(self, request, obj=None):
    inlines = list(_original_get_inlines(request, obj)) if callable(_original_get_inlines) else []
    inlines.append(RaritySettingsInline)
    return inlines


SettingsAdmin.get_inlines = _patched_get_inlines

_original_save_model = SettingsAdmin.save_model


def _patched_save_model(self, request, obj, form, change):
    _original_save_model(self, request, obj, form, change)
    RaritySettings.objects.get_or_create(
        settings=obj,
        defaults={
            "embed_color": "",
            "style": RaritySettings.Style.CONTAINER,
            "buttons_inside": True,
        }
    )


SettingsAdmin.save_model = _patched_save_model

try:
    admin.site.unregister(RaritySettings)
except admin.sites.NotRegistered:
    pass
