# Generated by Django 3.0.6 on 2020-05-17 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20200515_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fAVG',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy Batting Average'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fHR',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy Home Runs'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fOPS',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy On-Base Plus Slugging'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fR',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy Runs Scored'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fRBI',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy Runs Batted In'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fSB',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy Stolen Bases'),
        ),
        migrations.AlterField(
            model_name='hittingstatistics',
            name='fTotal',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Fantasy Total'),
        ),
    ]
