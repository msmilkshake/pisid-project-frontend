# Generated by Django 5.0.3 on 2024-05-05 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tailwaglabs', '0005_alter_salas_ratos_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilizador',
            name='isactive',
        ),
    ]
