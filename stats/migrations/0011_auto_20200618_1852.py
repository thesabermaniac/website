# Generated by Django 3.0.6 on 2020-06-19 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20200618_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pitchingstatistics',
            old_name='fS',
            new_name='fShO',
        ),
    ]
