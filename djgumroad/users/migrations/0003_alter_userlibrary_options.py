# Generated by Django 4.0.10 on 2023-03-23 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userlibrary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlibrary',
            options={'verbose_name_plural': 'UserLibraries'},
        ),
    ]