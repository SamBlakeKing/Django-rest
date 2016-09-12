# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-12 12:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_auto_20160912_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuUser',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sex', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=-1)),
                ('month', models.IntegerField(default=-1)),
                ('school', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('major', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Student User',
            },
            bases=('snippets.myuser',),
        ),
        migrations.CreateModel(
            name='TeamUser',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('leader', models.CharField(default='', max_length=255)),
                ('logo_path', models.CharField(default='', max_length=255)),
                ('contact_tel', models.CharField(default='', max_length=255)),
                ('slogan', models.CharField(default='', max_length=255)),
                ('about', models.CharField(default='', max_length=255)),
                ('history', models.CharField(default='', max_length=255)),
                ('b_type', models.IntegerField(default=0)),
                ('man_cnt', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Team User',
            },
            bases=('snippets.myuser',),
        ),
    ]