from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("settings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RaritySettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("embed_color", models.CharField(blank=True, default="", help_text="Hex color for the line, leave empty for no color", max_length=7)),
                ("style", models.CharField(blank=True, default="container", help_text="Rarity list display style: 'embed' or 'container'", max_length=10)),
                ("buttons_inside", models.BooleanField(default=True, help_text="Place pagination buttons inside the container (only applies to container style)")),
                ("settings", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="rarity_settings", to="settings.settings")),
            ],
            options={
                "verbose_name": "Rarity Settings",
                "verbose_name_plural": "Rarity Settings",
            },
        ),
    ]
