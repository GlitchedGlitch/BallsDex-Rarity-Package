from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rarity", "0003_add_reload_flag"),
        ("bd_models", "__first__"),
    ]

    operations = [
        # Remove fields that no longer exist on the model
        migrations.RemoveField(
            model_name="raritysettings",
            name="special_rarity",
        ),
        migrations.RemoveField(
            model_name="raritysettings",
            name="_reload_tree_on_change",
        ),
        # Remove the old text-based hidden_balls field
        migrations.RemoveField(
            model_name="raritysettings",
            name="hidden_balls",
        ),
        # Bring embed_color/style in line with the current model
        migrations.AlterField(
            model_name="raritysettings",
            name="embed_color",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Hex color for the line, leave empty for no color",
                max_length=6,
                verbose_name="Embed color",
            ),
        ),
        migrations.AlterField(
            model_name="raritysettings",
            name="style",
            field=models.CharField(
                choices=[("embed", "Embed"), ("container", "Container")],
                default="container",
                help_text="How the rarity list message will appear",
                max_length=10,
                verbose_name="Style",
            ),
        ),
        # Re-add hidden_balls as a ManyToMany, and add hidden_specials
        migrations.AddField(
            model_name="raritysettings",
            name="hidden_balls",
            field=models.ManyToManyField(
                blank=True,
                help_text="Balls to hide from the rarity list",
                related_name="hidden_from_rarity",
                to="bd_models.ball",
                verbose_name="Hidden balls",
            ),
        ),
        migrations.AddField(
            model_name="raritysettings",
            name="hidden_specials",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specials to hide from the rarity list",
                related_name="hidden_from_rarity",
                to="bd_models.special",
                verbose_name="Hidden specials",
            ),
        ),
        migrations.CreateModel(
            name="RarityTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rarity_value", models.FloatField(help_text="The rarity value to tag. Use -1 for tier mode tags.", verbose_name="Rarity value")),
                ("is_tier_tag", models.BooleanField(default=False, help_text="If checked, rarity value is treated as a tier number instead of raw rarity", verbose_name="Is tier tag")),
                ("tag_text", models.CharField(help_text="Text to append (e.g. 'craftable', 'event only')", max_length=64, verbose_name="Tag text")),
                ("rarity_settings", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="tags", to="rarity.raritysettings")),
            ],
            options={
                "db_table": "rarity_raritytag",
                "verbose_name": "Rarity Tag",
                "verbose_name_plural": "Rarity Tags",
            },
        ),
    ]