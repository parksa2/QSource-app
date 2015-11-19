# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qsource_user', '0005_auto_20151118_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionsAnswered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionID', models.IntegerField()),
                ('user', models.ForeignKey(to='qsource_user.UserData')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsAsked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionID', models.IntegerField()),
                ('user', models.ForeignKey(to='qsource_user.UserData')),
            ],
        ),
    ]
