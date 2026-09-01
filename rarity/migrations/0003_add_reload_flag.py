from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rarity", "0002_add_new_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="raritysettings",
            name="_reload_tree_on_change",
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
