# Generated by Django 5.0.6 on 2024-06-03 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("track", "0007_remove_pageview_track_pagev_timesta_4f838d_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="utm",
            name="website",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="utms",
                to="track.website",
            ),
        ),
    ]
