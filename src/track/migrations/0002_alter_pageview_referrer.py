# Generated by Django 5.0.6 on 2024-05-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("track", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pageview",
            name="referrer",
            field=models.URLField(blank=True, null=True),
        ),
    ]
