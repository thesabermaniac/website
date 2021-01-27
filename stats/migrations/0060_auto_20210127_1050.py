# Generated by Django 3.0.6 on 2021-01-27 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0059_auto_20210127_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hittingstatistics',
            name='AVG',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=4, verbose_name='Batting Average'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='OBP',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=4, verbose_name='On-Base Percentage'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='OPS',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=4, verbose_name='On-Base Plus Slugging'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='SLG',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=4, verbose_name='Slugging Percentage'),
        ),
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='K_BB',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Strikeouts per Walk'),
        ),
        migrations.AlterField(
            model_name='pitchingstatistics',
            name='WHIP',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Walks + Hits/IP'),
        ),
    ]
