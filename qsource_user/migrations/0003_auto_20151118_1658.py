# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qsource_user', '0002_auto_20151015_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('showMyQuestions', models.BooleanField(default=False)),
                ('showLocal', models.BooleanField(default=False)),
                ('showRecent', models.BooleanField(default=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='SignUp',
        ),
    ]
