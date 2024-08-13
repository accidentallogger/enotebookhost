# Generated by Django 5.0.6 on 2024-08-03 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_experiment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="experiment",
            old_name="account",
            new_name="enotebook",
        ),
        migrations.AlterField(
            model_name="enotebook",
            name="notebook_number",
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="experiment_number",
            field=models.CharField(unique="True"),
        ),
    ]
