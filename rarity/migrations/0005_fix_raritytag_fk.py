from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rarity", "0004_fix_schema"),
    ]

    operations = [
        migrations.AddField(
            model_name="raritytag",
            name="rarity_settings",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tags",
                to="settings.raritysettings",
            ),
            preserve_default=False,
        ),
    ]
