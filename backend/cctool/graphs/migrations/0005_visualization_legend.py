# Generated by Django 2.0.9 on 2019-04-20 12:08

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0004_auto_20190414_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualization',
            name='legend',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
