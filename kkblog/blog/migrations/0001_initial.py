# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('year', models.PositiveSmallIntegerField(verbose_name='年份')),
                ('month', models.PositiveSmallIntegerField(verbose_name='月份')),
            ],
            options={
                'verbose_name': '归档',
                'verbose_name_plural': '归档',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('slug', models.SlugField(verbose_name='缩略', max_length=255, unique=True)),
                ('title', models.CharField(verbose_name='标题', max_length=29)),
                ('content', models.TextField(verbose_name='正文')),
                ('thumbnailLength', models.PositiveSmallIntegerField(default=399, verbose_name='展示长度')),
                ('createDatetime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('editDatetime', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('shown', models.BooleanField(default=True, verbose_name='可见')),
                ('sticky', models.BooleanField(default=False, verbose_name='置顶')),
                ('accessFrequency', models.PositiveIntegerField(default=0, verbose_name='阅读次数')),
                ('archive', models.ForeignKey(related_name='articles', to='blog.archive', verbose_name='归档')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='分类名', max_length=99, unique=True)),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('shown', models.BooleanField(default=False, verbose_name='显示')),
                ('read', models.BooleanField(default=False, verbose_name='已读')),
                ('ipAddress', models.IPAddressField(verbose_name='IP地址')),
                ('nickname', models.CharField(verbose_name='昵称', max_length=39)),
                ('website', models.URLField(blank=True, verbose_name='网站')),
                ('email', models.EmailField(blank=True, verbose_name='Email', max_length=75)),
                ('datetime', models.DateTimeField(verbose_name='时间', auto_now_add=True)),
                ('message', models.TextField(verbose_name='内容', max_length=999999)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('article', models.ForeignKey(blank=True, related_name='comments', to='blog.article', verbose_name='引用博文')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, related_name='children', to='blog.comment', verbose_name='父评论')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('enabled', models.IntegerField(blank=True, choices=[(1, '启用')], verbose_name='启用该设置', unique=True)),
                ('domainName', models.CharField(verbose_name='域名', max_length=99)),
                ('articlesPerPage', models.PositiveSmallIntegerField(default=9, verbose_name='首页每页显示的博客数')),
                ('commentVerify', models.BooleanField(default=True, verbose_name='新评论是否默认隐藏')),
                ('musicAutoPlay', models.BooleanField(default=False, verbose_name='背景音乐自动播放')),
                ('qrCodeImage', filebrowser.fields.FileBrowseField(blank=True, verbose_name='QR码URL', max_length=99)),
                ('brand', models.CharField(blank=True, verbose_name='博客名', max_length=19)),
                ('subBrand', models.CharField(blank=True, verbose_name='副博客名', max_length=99)),
                ('ownerName', models.CharField(verbose_name='博主名', max_length=19)),
                ('ownerBriefSelfIntro', models.CharField(blank=True, verbose_name='博主简介', max_length=999)),
                ('ownerPhoto', filebrowser.fields.FileBrowseField(blank=True, verbose_name='博主照片', max_length=99)),
                ('ownerIcon', filebrowser.fields.FileBrowseField(blank=True, verbose_name='博主头像', max_length=99)),
                ('ownerGithub', models.URLField(blank=True, verbose_name='GitHub', max_length=999)),
                ('ownerGoogle', models.URLField(blank=True, verbose_name='Google', max_length=999)),
                ('ownerTwitter', models.URLField(blank=True, verbose_name='Twitter', max_length=999)),
                ('ownerWeibo', models.URLField(blank=True, verbose_name='微博', max_length=999)),
                ('ownerWeiboBox', models.TextField(blank=True, verbose_name='微博展示台', max_length=9999)),
                ('ownerEmail', models.EmailField(blank=True, verbose_name='邮箱', max_length=99)),
            ],
            options={
                'verbose_name': '设置',
                'verbose_name_plural': '设置',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='flatPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('slug', models.SlugField(verbose_name='缩略', max_length=99, unique=True)),
                ('title', models.CharField(verbose_name='标题', max_length=99)),
                ('text', models.TextField(verbose_name='正文', max_length=999999)),
                ('createDatetime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('modifyDatetime', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('shown', models.BooleanField(default=True, verbose_name='可见')),
            ],
            options={
                'verbose_name': '静态页面',
                'verbose_name_plural': '静态页面',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='友链名', max_length=99)),
                ('url', models.URLField(verbose_name='URL', max_length=99)),
            ],
            options={
                'verbose_name': '友链',
                'verbose_name_plural': '友链',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('music', filebrowser.fields.FileBrowseField(verbose_name='音乐文件', max_length=999)),
                ('title', models.CharField(verbose_name='标题', max_length=99)),
                ('musician', models.CharField(verbose_name='音乐人', max_length=99)),
                ('enabled', models.BooleanField(default=True, verbose_name='启用')),
            ],
            options={
                'verbose_name': '背景音乐',
                'verbose_name_plural': '背景音乐',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tag',
            fields=[
                ('name', models.CharField(verbose_name='标签名', primary_key=True, max_length=99, unique=True, serialize=False)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='config',
            name='ownerSelfIntro',
            field=models.ForeignKey(related_name='self_intro', to='blog.flatPage', verbose_name='自我介绍'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(related_name='articles', to='blog.category', verbose_name='分类'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.tag', verbose_name='标签', related_name='articles'),
            preserve_default=True,
        ),
    ]
