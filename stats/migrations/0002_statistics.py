# Generated by Django 3.0.6 on 2020-05-11 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('G', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Games Played')),
                ('PA', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Plate Appearances')),
                ('HR', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Home Runs')),
                ('R', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Runs Scored')),
                ('RBI', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Runs Batted In')),
                ('BB', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Walks')),
                ('IBB', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Intentional Walks')),
                ('SO', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Strike Outs')),
                ('HBP', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Hits By Pitch')),
                ('SF', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Sacrifice Flies')),
                ('SH', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Sacrifice Hits')),
                ('GDP', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Grounded into Double Plays')),
                ('SB', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Stolen Bases')),
                ('CS', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Caught Stealing')),
                ('AVG', models.FloatField(blank=True, null=True, verbose_name='Batting Average')),
                ('OBP', models.FloatField(blank=True, null=True, verbose_name='On-Base Percentage')),
                ('SLG', models.FloatField(blank=True, null=True, verbose_name='Slugging Percentage')),
                ('OPS', models.FloatField(blank=True, null=True, verbose_name='On-Base Plus Slugging')),
                ('fAVG', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Fantasy Batting Average')),
                ('fOPS', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Fantasy On-Base Plus Slugging')),
                ('fHR', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Fantasy Home Runs')),
                ('fRBI', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Fantasy Runs Batted In')),
                ('fR', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Fantasy Runs Scored')),
                ('fSB', models.PositiveSmallIntegerField(verbose_name='Fantasy Stolen Bases')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Player')),
            ],
        ),
    ]