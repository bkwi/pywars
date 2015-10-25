# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150926_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='password_reset_token',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
    ]
