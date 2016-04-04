# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-03 00:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reports', '0011_auto_20160403_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='city',
        ),
        migrations.RemoveField(
            model_name='report',
            name='date_of_disaster',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed100_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed100_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed80_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed80_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed80_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed80_3',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed80_4',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed90_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='destroyed90_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='report',
            name='insured',
        ),
        migrations.RemoveField(
            model_name='report',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major20_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major20_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major20_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major20_3',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major30_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major30_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major30_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major30_3',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major40_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major40_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major40_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major50_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major50_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major50_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major60_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major60_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major74_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major74_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='major74_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='minor10_0',
        ),
        migrations.RemoveField(
            model_name='report',
            name='minor10_1',
        ),
        migrations.RemoveField(
            model_name='report',
            name='minor10_2',
        ),
        migrations.RemoveField(
            model_name='report',
            name='mortgage',
        ),
        migrations.RemoveField(
            model_name='report',
            name='owned_less_than_30_years',
        ),
        migrations.RemoveField(
            model_name='report',
            name='predisaster_value',
        ),
        migrations.RemoveField(
            model_name='report',
            name='sewage',
        ),
        migrations.RemoveField(
            model_name='report',
            name='state',
        ),
        migrations.RemoveField(
            model_name='report',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='report',
            name='type_of_disaster',
        ),
        migrations.RemoveField(
            model_name='report',
            name='type_of_occupancy',
        ),
        migrations.RemoveField(
            model_name='report',
            name='type_of_residence',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_conventionalhome_destroyed',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_conventionalhome_major',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_conventionalhome_minor',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_damage',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_mobilehome',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_mobilehome_destroyed',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_mobilehome_major_nonplywood',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_mobilehome_major_plywood',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_mobilehome_major_plywood_yes',
        ),
        migrations.RemoveField(
            model_name='report',
            name='water_mobilehome_minor',
        ),
        migrations.RemoveField(
            model_name='report',
            name='zipcode',
        ),
    ]
