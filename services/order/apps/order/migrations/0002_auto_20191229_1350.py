# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-29 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='customer_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='product_id',
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('customer_id', 'product_id', 'quantity')]),
        ),
    ]