# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.CharField(default=main.utils._gen_id, max_length=16, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('about', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
                ('url_params', models.TextField()),
                ('notified_user', models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
