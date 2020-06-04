# Generated by Django 3.0.5 on 2020-05-21 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Envs',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('id', models.AutoField(help_text='id主键', primary_key=True, serialize=False, verbose_name='id主键')),
                ('name', models.CharField(help_text='环境名称', max_length=200, unique=True, verbose_name='环境名称')),
                ('base_url', models.URLField(help_text='请求base_url', verbose_name='请求base_url')),
                ('desc', models.CharField(help_text='简要描述', max_length=200, verbose_name='简要描述')),
            ],
            options={
                'verbose_name': '环境信息',
                'verbose_name_plural': '环境信息',
                'db_table': 'tb_envs',
            },
        ),
    ]
