from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
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
        if "settings" in form.base_fields:
            form.base_fields["settings"].widget = admin.widgets.AdminHiddenInput()
        return form
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to the edit page if instance exists, otherwise to add."""
        try:
            obj = RaritySettings.objects.select_related("settings").get()
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(
                reverse("admin:rarity_raritysettings_change", args=[obj.pk])
            )
        except ObjectDoesNotExist:
            pass
        return super().changelist_view(request, extra_context=extra_context)
