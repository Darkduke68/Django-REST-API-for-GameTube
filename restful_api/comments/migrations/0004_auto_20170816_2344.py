# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 23:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_remove_comment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent',
            new_name='root_comment',
        ),
    ]