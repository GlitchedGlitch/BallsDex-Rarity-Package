from django.contrib import admin
from settings.models import Settings


_existing_admin = admin.site._registry.get(Settings)


class RaritySettingsAdmin(_existing_admin.__class__ if _existing_admin else admin.ModelAdmin):
    """
    Extend the existing Settings admin to include rarity fields.
    """
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj)) if self.fieldsets else []
        
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
        
        # Insert after first fieldset if exists, otherwise at start
        if fieldsets:
            fieldsets.insert(1, rarity_fieldset)
        else:
            fieldsets = [rarity_fieldset]
        
        return fieldsets


if _existing_admin:
    admin.site.unregister(Settings)
    admin.site.register(Settings, RaritySettingsAdmin)
