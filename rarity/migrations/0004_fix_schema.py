from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rarity", "0003_add_reload_flag"),
    ]

    operations = [
        # Remove old fields that no longer exist in model
        migrations.RemoveField(
            model_name="raritysettings",
            name="_reload_tree_on_change",
        ),
        migrations.RemoveField(
            model_name="raritysettings",
            name="special_rarity",
        ),
        # Remove old hidden_balls text field
        migrations.RemoveField(
            model_name="raritysettings",
            name="hidden_balls",
        ),
        # Add new ManyToMany fields
        migrations.AddField(
            model_name="raritysettings",
            name="hidden_balls",
            field=models.ManyToManyField(
                blank=True,
                related_name="hidden_from_rarity",
                to="bd_models.ball",
            ),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="hidden_specials",
            field=models.ManyToManyField(
                blank=True,
                related_name="hidden_from_rarity",
                to="bd_models.special",
            ),
        ),
        # Create RarityTag model
        migrations.CreateModel(
            name="RarityTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rarity_value", models.FloatField()),
                ("is_tier_tag", models.BooleanField(default=False)),
                ("tag_text", models.CharField(max_length=64)),
            ],
            options={
                "db_table": "rarity_raritytag",
                "verbose_name": "Rarity Tag",
                "verbose_name_plural": "Rarity Tags",
            },
        ),
    ]
