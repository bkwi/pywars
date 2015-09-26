# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_appuser_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 10, 0, 0, 0), auto_now_add=True),
            preserve_default=False,
        ),
    ]
