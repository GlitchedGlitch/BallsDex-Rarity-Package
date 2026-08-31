from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rarity", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="raritysettings",
            name="tier_mode",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="entries_per_page",
            field=models.PositiveIntegerField(default=7),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="special_rarity",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="search_enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="rarity_search_enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="ephemeral_enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="hidden_balls",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="show_thumbnail",
            field=models.BooleanField(default=True),
        ),
    ]
