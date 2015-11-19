# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('qsource_user', '0004_auto_20151118_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='user',
            field=models.OneToOneField(related_name='data', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
