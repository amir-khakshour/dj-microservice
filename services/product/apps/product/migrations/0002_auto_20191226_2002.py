# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-26 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, validators=[product.models.validate_product_name], verbose_name='name'),
        ),
    ]