# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.IntegerField()),
                ('medhome', models.IntegerField()),
                ('sqfthome', models.IntegerField()),
                ('rent', models.IntegerField()),]
        ),
        migrations.CreateModel(
                name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.IntegerField(max_length=5)),
                ('type_of_residence', models.CharField(max_length=50)),
                ('type_of_occupancy', models.CharField(max_length=50)),
                ('type_of_disaster', models.CharField(max_length=50)),
                ('date_of_disaster', models.DateField()),
                ('insured', models.IntegerField(max_length=1)),
                ('mortgage', models.IntegerField(max_length=1)),
                ('owned_less_than_30_years', models.IntegerField(max_length=1)),
                ('predisaster_value', models.IntegerField(max_length=1)),
                ('normal_water', models.IntegerField(max_length=1)),
                ('normal_destroyed_0', models.IntegerField(max_length=1)),
                ('normal_destroyed_1', models.IntegerField(max_length=1)),
                ('normal_destroyed_2', models.IntegerField(max_length=1)),
                ('normal_destroyed_3', models.IntegerField(max_length=1)),
                ('normal_major_0', models.IntegerField(max_length=1)),
                ('normal_major_1', models.IntegerField(max_length=1)),
                ('normal_major_2', models.IntegerField(max_length=1)),
                ('normal_major_3', models.IntegerField(max_length=1)),
                ('normal_minor_0', models.IntegerField(max_length=1)),
                ('normal_minor_1', models.IntegerField(max_length=1)),
                ('normal_minor_2', models.IntegerField(max_length=1)),
                ('normal_minor_3', models.IntegerField(max_length=1)),
                ('manufactured_destroyed_0', models.IntegerField(max_length=1)),
                ('manufactured_destroyed_1', models.IntegerField(max_length=1)),
                ('manufactured_destroyed_2', models.IntegerField(max_length=1)),
                ('manufactured_destroyed_3', models.IntegerField(max_length=1)),
                ('manufactured_major_0', models.IntegerField(max_length=1)),
                ('manufactured_major_1', models.IntegerField(max_length=1)),
                ('manufactured_major_2', models.IntegerField(max_length=1)),
                ('manufactured_major_3', models.IntegerField(max_length=1)),
                ('manufactured_minor_0', models.IntegerField(max_length=1)),
                ('manufactured_minor_1', models.IntegerField(max_length=1)),
                ('manufactured_minor_2', models.IntegerField(max_length=1)),
                ('manufactured_minor_3', models.IntegerField(max_length=1)),],
        ),
            ]

