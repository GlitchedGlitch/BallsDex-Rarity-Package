from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import RaritySettings, RarityTag


class RarityTagInline(admin.TabularInline):
    model = RarityTag
    extra = 1
    fields = ("rarity_value", "is_tier_tag", "tag_text")
    
    def get_formset(self, request, obj=None, **kwargs):
        # Auto-assign rarity_settings on new tags
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields["rarity_settings"].initial = obj
        return formset


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
        ("Display", {
            "fields": (
                "tier_mode",
                "entries_per_page",
                "show_thumbnail",
            ),
            "description": "Configure list display options.",
        }),
        ("Command Options", {
            "fields": (
                "search_enabled",
                "rarity_search_enabled",
                "ephemeral_enabled",
            ),
            "description": "Toggle command parameters.",
        }),
        ("Filtering", {
            "fields": (
                "hidden_balls",
                "hidden_specials",
            ),
            "description": "Hide specific balls/specials from the rarity list.",
        }),
    )
    inlines = [RarityTagInline]
    
    def has_add_permission(self, request):
        return not RaritySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "settings" in form.base_fields:
            del form.base_fields["settings"]
        return form
    
    def save_model(self, request, obj, form, change):
        # Auto-assign settings if not set
        if obj.settings_id is None:
            from settings.models import Settings
            global_settings = Settings.objects.first()
            if global_settings:
                obj.settings = global_settings
            else:
                self.message_user(
                    request,
                    "No global Settings instance found! Please create one first.",
                    messages.ERROR,
                )
                return
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        # Auto-assign rarity_settings to new tags
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, RarityTag) and instance.rarity_settings_id is None:
                instance.rarity_settings = form.instance
            instance.save()
        formset.save_m2m()
    
    def changelist_view(self, request, extra_context=None):
        try:
            obj = RaritySettings.objects.select_related("settings").get()
            return HttpResponseRedirect(
                reverse("admin:settings_raritysettings_change", args=[obj.pk])
            )
        except (ObjectDoesNotExist, RaritySettings.MultipleObjectsReturned):
            pass
        return super().changelist_view(request, extra_context=extra_context)
