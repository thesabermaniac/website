# Generated by Django 3.0.6 on 2021-01-21 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0040_auto_20210121_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='H',
            field=models.SmallIntegerField(default=0, verbose_name='Hits Allowed'),
        ),
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='TBF',
            field=models.SmallIntegerField(default=0, verbose_name='Total Batters Faced'),
        ),
    ]