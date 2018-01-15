# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('count', models.IntegerField(default=1, verbose_name='数量')),
                ('price', models.DecimalField(max_digits=10, verbose_name='单价', decimal_places=2)),
                ('comment', models.TextField(default='', verbose_name='评价信息')),
            ],
            options={
                'db_table': 'df_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_id', models.CharField(serialize=False, verbose_name='订单号', max_length=64, primary_key=True)),
                ('total_count', models.IntegerField(default=1, verbose_name='商品总数')),
                ('total_amount', models.DecimalField(max_digits=10, verbose_name='商品总金额', decimal_places=2)),
                ('trans_cost', models.DecimalField(max_digits=10, verbose_name='运费', decimal_places=2)),
                ('pay_method', models.SmallIntegerField(default=1, choices=[(1, '货到付款'), (2, '支付宝')], verbose_name='支付方式')),
                ('status', models.SmallIntegerField(default=1, choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], verbose_name='订单状态')),
                ('trade_id', models.CharField(blank=True, unique=True, null=True, max_length=100, verbose_name='支付编号')),
            ],
            options={
                'db_table': 'df_order_info',
            },
        ),
    ]
