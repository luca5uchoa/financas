# Generated by Django 5.1.3 on 2024-11-28 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='categoria',
            field=models.CharField(choices=[('lazer', 'Lazer'), ('saude', 'Saúde'), ('alimentacao', 'Alimentação'), ('transporte', 'Transporte'), ('habituacao', 'Habitação')], max_length=20),
        ),
        migrations.AlterField(
            model_name='despesa',
            name='descricao',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]