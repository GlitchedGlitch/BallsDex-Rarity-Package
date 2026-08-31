from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("settings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="rarity_embed_color",
            field=models.CharField(
                max_length=7,
                blank=True,
                default="",
                help_text="Hex color for the line, leave empty for no color",
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="rarity_style",
            field=models.CharField(
                max_length=10,
                blank=True,
                default="container",
                help_text="Rarity list display style: 'embed' or 'container'",
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="rarity_buttons_inside",
            field=models.BooleanField(
                default=True,
                help_text="Place pagination buttons inside the container (only applies to container style)",
            ),
        ),
    ]
