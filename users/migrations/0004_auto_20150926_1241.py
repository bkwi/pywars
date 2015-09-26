# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_appuser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
