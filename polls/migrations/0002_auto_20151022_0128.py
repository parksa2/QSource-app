# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='ans1_text',
            field=models.CharField(default='?', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='ans1_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='ans2_text',
            field=models.CharField(default='??', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='ans2_votes',
            field=models.IntegerField(default=0),
        ),
    ]
