from django.contrib import admin
from settings.admin import SettingsAdmin
from settings.models import Settings


# Extend the existing SettingsAdmin to include rarity fields
class RaritySettingsAdmin(SettingsAdmin):
    fieldsets = list(SettingsAdmin.fieldsets) if hasattr(SettingsAdmin, "fieldsets") else []
    
    # Add rarity settings as a new fieldset
    rarity_fieldset = (
        "Rarity Settings",
        {
            "fields": (
                "rarity_embed_color",
                "rarity_style",
                "rarity_buttons_inside",
            ),
        },
    )
    
    # Try to insert before the first fieldset, or append
    fieldsets.insert(0, rarity_fieldset)
    
    # Also add to list_display if desired
    if hasattr(SettingsAdmin, "list_display"):
        list_display = list(SettingsAdmin.list_display)
        if "rarity_style" not in list_display:
            list_display.append("rarity_style")
        # Re-assign
        SettingsAdmin.list_display = tuple(list_display)


# Monkey-patch the admin class
admin.site.unregister(Settings)
admin.site.register(Settings, RaritySettingsAdmin)
