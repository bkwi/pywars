# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0007_challenge_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionComment',
            fields=[
                ('id', models.CharField(default=main.utils._gen_id, max_length=16, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('solution', models.ForeignKey(related_name='comments', to='challenges.Solution')),
            ],
        ),
    ]
