# Generated by Django 2.0.9 on 2019-06-02 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0006_auto_20190601_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodeplus',
            name='controllability',
            field=models.CharField(choices=[('N', 'None'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High')], default='N', max_length=1, verbose_name='node controllability'),
        ),
    ]
