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

def _patched_get_inlines(self, request, obj=None):
    inlines = []
    for inline_class in type(self).inlines if hasattr(type(self), 'inlines') else []:
        inlines.append(inline_class)
    inlines.append(RaritySettingsInline)
    return inlines

if not hasattr(SettingsAdmin, '_rarity_patched'):
    SettingsAdmin.get_inlines = _patched_get_inlines
    SettingsAdmin._rarity_patched = True  # type: ignore

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


if not hasattr(SettingsAdmin, '_rarity_save_patched'):
    SettingsAdmin.save_model = _patched_save_model
    SettingsAdmin._rarity_save_patched = True  # type: ignore

try:
    admin.site.unregister(RaritySettings)
except admin.sites.NotRegistered:
    pass
