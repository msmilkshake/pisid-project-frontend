# Generated by Django 5.0.3 on 2024-05-05 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailwaglabs', '0002_remove_utilizador_isactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salas_ratos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sala', models.IntegerField(db_column='Sala')),
                ('ratos', models.IntegerField(db_column='Ratos')),
            ],
        ),
    ]