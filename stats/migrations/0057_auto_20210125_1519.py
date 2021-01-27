# Generated by Django 3.0.6 on 2021-01-25 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0056_auto_20210124_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hittingstatistics',
            options={'verbose_name_plural': 'Hitting Statistics'},
        ),
        migrations.AlterModelOptions(
            name='pitchingstatistics',
            options={'verbose_name_plural': 'Pitching Statistics'},
        ),
        migrations.RemoveField(
            model_name='hittingstatistics',
            name='fTotal',
        ),
        migrations.RemoveField(
            model_name='pitchingstatistics',
            name='fTotal',
        ),
    ]
