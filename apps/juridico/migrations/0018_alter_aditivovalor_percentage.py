# Generated by Django 3.2.5 on 2021-08-08 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juridico', '0017_alter_aditivovalor_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aditivovalor',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
