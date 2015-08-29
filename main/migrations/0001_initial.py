# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.CharField(default=main.utils._gen_id, max_length=16, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('initial_code', models.TextField(blank=True)),
                ('solution', models.TextField(blank=True)),
                ('tests', models.TextField(blank=True)),
            ],
        ),
    ]
