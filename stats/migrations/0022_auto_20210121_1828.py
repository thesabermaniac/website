# Generated by Django 3.0.6 on 2021-01-21 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0021_auto_20210121_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hittingstatistics',
            name='SO',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Strike Outs'),
        ),
    ]
