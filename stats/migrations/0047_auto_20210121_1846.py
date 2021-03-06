# Generated by Django 3.0.6 on 2021-01-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0046_auto_20210121_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='fERA',
            field=models.FloatField(default=0.0, verbose_name='Fantasy Earned Run Average'),
        ),
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='fL',
            field=models.SmallIntegerField(default=0, verbose_name='Fantasy Losses'),
        ),
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='fW',
            field=models.SmallIntegerField(default=0, verbose_name='Fantasy Wins'),
        ),
    ]
