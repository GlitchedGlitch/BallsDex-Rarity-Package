from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import RaritySettings


@admin.register(RaritySettings)
class RaritySettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "embed_color",
                "style",
                "buttons_inside",
            ),
            "description": "Configure how the rarity command displays its output.",
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent adding more than one instance."""
        return not RaritySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion."""
        return False
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Remove settings field from form entirely
        if "settings" in form.base_fields:
            del form.base_fields["settings"]
        return form
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to the edit page if instance exists."""
        try:
            obj = RaritySettings.objects.select_related("settings").get()
            return HttpResponseRedirect(
                reverse("admin:rarity_raritysettings_change", args=[obj.pk])
            )
        except (ObjectDoesNotExist, RaritySettings.MultipleObjectsReturned):
            pass
        return super().changelist_view(request, extra_context=extra_context)
