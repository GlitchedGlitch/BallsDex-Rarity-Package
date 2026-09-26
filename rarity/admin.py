from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import RaritySettings, RarityTag


class RarityTagInline(admin.TabularInline):
    model = RarityTag
    extra = 1
    fields = ("rarity_value", "is_tier_tag", "tag_text")


@admin.register(RaritySettings)
class RaritySettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ("hidden_balls", "hidden_specials")
    fieldsets = (
        ("Display", {
            "fields": (
                "embed_color",
                "style",
                "buttons_inside",
                "tier_mode",
                "entries_per_page",
                "show_thumbnail",
            ),
            "description": "Configure how the rarity command displays its output.",
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
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if isinstance(instance, RarityTag) and instance.rarity_settings_id is None:
                instance.rarity_settings = form.instance
            instance.save()
        formset.save_m2m()
    
    def changelist_view(self, request, extra_context=None):
        obj = RaritySettings.objects.select_related("settings").first()
        if obj is None:
            from settings.models import Settings
            global_settings = Settings.objects.first()
            if global_settings is None:
                self.message_user(
                    request,
                    "No global Settings instance found! Please create one first.",
                    messages.ERROR,
                )
                return super().changelist_view(request, extra_context=extra_context)
            obj = RaritySettings.objects.create(settings=global_settings)
        return HttpResponseRedirect(
            reverse("admin:settings_raritysettings_change", args=[obj.pk])
        )