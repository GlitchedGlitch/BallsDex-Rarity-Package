from django.apps import AppConfig


class RarityConfig(AppConfig):
    name = "rarity"
    verbose_name = "Rarity"
    default_auto_field = "django.db.models.BigAutoField"
    dpy_package = "rarity.rarity"

    def ready(self):
        from settings.models import Settings
        from rarity.models import RaritySettings
        
        try:
            global_settings = Settings.objects.first()
            if global_settings:
                RaritySettings.objects.get_or_create(
                    settings=global_settings,
                    defaults={
                        "embed_color": "",
                        "style": RaritySettings.Style.CONTAINER,
                        "buttons_inside": True,
                        "tier_mode": False,
                        "entries_per_page": 7,
                        "search_enabled": True,
                        "rarity_search_enabled": True,
                        "ephemeral_enabled": True,
                        "show_thumbnail": True,
                    }
                )
        except Exception:
            pass
