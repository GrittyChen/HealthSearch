# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import webapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('tags', webapp.models.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='TagDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_ch', models.TextField()),
                ('tag_en', models.TextField()),
                ('tag_class', webapp.models.ListField()),
            ],
        ),
    ]
