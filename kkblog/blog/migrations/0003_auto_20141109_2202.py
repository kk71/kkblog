# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141109_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='archive',
            field=models.ForeignKey(blank=True, related_name='articles', null=True, verbose_name='归档', to='blog.archive'),
            preserve_default=True,
        ),
    ]
