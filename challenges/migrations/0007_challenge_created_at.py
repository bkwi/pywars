# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0006_solution_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 10, 30, 0, 0), auto_now_add=True),
            preserve_default=False,
        ),
    ]
