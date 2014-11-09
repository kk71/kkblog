# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='archive',
            field=models.ForeignKey(related_name='articles', blank=True, to='blog.archive', verbose_name='归档'),
            preserve_default=True,
        ),
    ]
