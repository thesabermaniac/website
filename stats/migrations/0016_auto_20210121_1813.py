# Generated by Django 3.0.6 on 2021-01-21 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0015_auto_20210121_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hittingstatistics',
            name='IBB',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Intentional Walks'),
        ),
    ]