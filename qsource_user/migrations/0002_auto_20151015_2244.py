# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qsource_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='username',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
