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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('year', models.PositiveSmallIntegerField(verbose_name='年份')),
                ('month', models.PositiveSmallIntegerField(verbose_name='月份')),
            ],
            options={
                'verbose_name_plural': '归档',
                'verbose_name': '归档',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='缩略')),
                ('title', models.CharField(verbose_name='标题', max_length=29)),
                ('content', models.TextField(verbose_name='正文')),
                ('thumbnailLength', models.PositiveSmallIntegerField(verbose_name='展示长度', default=399)),
                ('createDatetime', models.DateTimeField(help_text='如果不给出，将自动创建。', verbose_name='创建时间', blank=True)),
                ('editDatetime', models.DateTimeField(help_text='自动生成。', auto_now=True, verbose_name='最后修改时间')),
                ('shown', models.BooleanField(verbose_name='可见', default=True)),
                ('sticky', models.BooleanField(verbose_name='置顶', default=False)),
                ('accessFrequency', models.PositiveIntegerField(verbose_name='阅读次数', default=0)),
                ('archive', models.ForeignKey(help_text='如果不给出，将自动创建。', to='blog.archive', null=True, related_name='articles', verbose_name='归档', blank=True)),
            ],
            options={
                'verbose_name_plural': '文章',
                'verbose_name': '文章',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='分类名', max_length=99)),
            ],
            options={
                'verbose_name_plural': '分类',
                'verbose_name': '分类',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('shown', models.BooleanField(verbose_name='显示', default=False)),
                ('read', models.BooleanField(verbose_name='已读', default=False)),
                ('ipAddress', models.IPAddressField(verbose_name='IP地址')),
                ('byOwner', models.BooleanField(verbose_name='博主自己的评论', default=False)),
                ('nickname', models.CharField(verbose_name='昵称', max_length=39)),
                ('website', models.URLField(verbose_name='网站', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='Email', blank=True)),
                ('datetime', models.DateTimeField(verbose_name='时间')),
                ('message', models.TextField(verbose_name='内容', max_length=999999)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('article', models.ForeignKey(to='blog.article', related_name='comments', verbose_name='引用博文')),
                ('parent', mptt.fields.TreeForeignKey(to='blog.comment', null=True, related_name='children', verbose_name='父评论', blank=True)),
            ],
            options={
                'verbose_name_plural': '评论',
                'verbose_name': '评论',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='config',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('enabled', models.IntegerField(choices=[(1, '启用')], unique=True, verbose_name='启用该设置', blank=True)),
                ('domainName', models.CharField(verbose_name='域名', max_length=99)),
                ('articlesPerPage', models.PositiveSmallIntegerField(verbose_name='首页每页显示的博客数', default=9)),
                ('commentVerify', models.BooleanField(verbose_name='新评论是否默认隐藏', default=True)),
                ('musicAutoPlay', models.BooleanField(verbose_name='背景音乐自动播放', default=False)),
                ('qrCodeImage', filebrowser.fields.FileBrowseField(max_length=99, verbose_name='QR码URL', blank=True)),
                ('brand', models.CharField(max_length=19, verbose_name='博客名', blank=True)),
                ('subBrand', models.CharField(max_length=99, verbose_name='副博客名', blank=True)),
                ('ownerName', models.CharField(verbose_name='博主名', max_length=19)),
                ('ownerBriefSelfIntro', models.CharField(max_length=999, verbose_name='博主简介', blank=True)),
                ('ownerIcon', filebrowser.fields.FileBrowseField(max_length=99, verbose_name='博主头像', blank=True)),
                ('ownerGithub', models.URLField(max_length=999, verbose_name='GitHub', blank=True)),
                ('ownerGoogle', models.URLField(max_length=999, verbose_name='Google', blank=True)),
                ('ownerTwitter', models.URLField(max_length=999, verbose_name='Twitter', blank=True)),
                ('ownerWeibo', models.URLField(max_length=999, verbose_name='微博', blank=True)),
                ('ownerWeiboBox', models.TextField(max_length=9999, verbose_name='微博展示台', blank=True)),
                ('ownerEmail', models.EmailField(max_length=99, verbose_name='邮箱', blank=True)),
            ],
            options={
                'verbose_name_plural': '设置',
                'verbose_name': '设置',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='flatPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slug', models.SlugField(unique=True, max_length=99, verbose_name='缩略')),
                ('title', models.CharField(verbose_name='标题', max_length=99)),
                ('text', models.TextField(verbose_name='正文', max_length=999999)),
                ('createDatetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modifyDatetime', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('shown', models.BooleanField(verbose_name='可见', default=True)),
            ],
            options={
                'verbose_name_plural': '静态页面',
                'verbose_name': '静态页面',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='friend',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='友链名', max_length=99)),
                ('url', models.URLField(verbose_name='URL', max_length=99)),
            ],
            options={
                'verbose_name_plural': '友链',
                'verbose_name': '友链',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='music',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('music', filebrowser.fields.FileBrowseField(verbose_name='音乐文件', max_length=999)),
                ('title', models.CharField(verbose_name='标题', max_length=99)),
                ('musician', models.CharField(verbose_name='音乐人', max_length=99)),
                ('enabled', models.BooleanField(verbose_name='启用', default=True)),
            ],
            options={
                'verbose_name_plural': '背景音乐',
                'verbose_name': '背景音乐',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tag',
            fields=[
                ('name', models.CharField(primary_key=True, unique=True, serialize=False, verbose_name='标签名', max_length=99)),
            ],
            options={
                'verbose_name_plural': '标签',
                'verbose_name': '标签',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='config',
            name='ownerSelfIntro',
            field=models.ForeignKey(to='blog.flatPage', related_name='self_intro', verbose_name='自我介绍'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='blog.category', related_name='articles', verbose_name='分类'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.tag', null=True, related_name='articles', verbose_name='标签', blank=True),
            preserve_default=True,
        ),
    ]
