# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(max_length=100, verbose_name='Search for')),
                ('location', models.CharField(max_length=50, verbose_name='Location')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fs_id', models.CharField(max_length=24, unique=True, verbose_name='Foursquare ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Phone Number')),
                ('checkins_count', models.IntegerField(default=0, verbose_name='Checkin Count')),
            ],
        ),
        migrations.AddField(
            model_name='search',
            name='venues',
            field=models.ManyToManyField(related_name='in_searches', to='search.Venue', verbose_name='Venues'),
        ),
        migrations.AlterUniqueTogether(
            name='search',
            unique_together=set([('phrase', 'location')]),
        ),
    ]