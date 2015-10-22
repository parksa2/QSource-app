# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20151022_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ans1_text',
            field=models.CharField(default=b'Yes', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='ans2_text',
            field=models.CharField(default=b'No', max_length=200),
        ),
    ]
