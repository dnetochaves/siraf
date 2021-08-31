# Generated by Django 3.2.5 on 2021-08-31 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('juridico', '0025_auto_20210827_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metafisico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature_date', models.DateField(blank=True, null=True)),
                ('validity', models.IntegerField(blank=True, null=True)),
                ('end_validity', models.DateField(blank=True, null=True)),
                ('official_diary', models.CharField(blank=True, max_length=50, null=True)),
                ('percentage', models.FloatField(blank=True, null=True)),
                ('aditivo_value', models.FloatField(blank=True, null=True)),
                ('difference', models.FloatField(blank=True, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='juridico.contrato')),
            ],
        ),
    ]
