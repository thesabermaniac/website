# Generated by Django 3.0.6 on 2020-05-12 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20200511_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='fAVG',
            field=models.FloatField(blank=True, null=True, verbose_name='Fantasy Batting Average'),
        ),
    ]