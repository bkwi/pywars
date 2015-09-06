# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0002_challenge_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.CharField(default=main.utils._gen_id, max_length=16, serialize=False, primary_key=True)),
                ('challenge_id', models.CharField(max_length=16)),
                ('code', models.TextField()),
                ('author', models.ForeignKey(related_name='solutions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
