# Generated by Django 3.2.5 on 2021-07-21 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juridico', '0004_alter_item_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='signature_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='validity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
