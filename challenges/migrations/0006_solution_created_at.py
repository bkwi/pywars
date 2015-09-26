# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_auto_20150909_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 11, 0, 0, 0), auto_now_add=True),
            preserve_default=False,
        ),
    ]
