from django.conf import settings
from django.db import models
from filebrowser.fields import FileBrowseField
import mptt

from . import managers


class config(models.Model):
    ENABLED=(
        (1,"启用"),
    )
    enabled=models.IntegerField(unique=True,choices=ENABLED,blank=True,null=True,verbose_name="启用该设置")

    # 生产环境的域名（形如：http://*****，末尾不加/）
    domainName=models.CharField(max_length=99,verbose_name="域名")
    articlesPerPage=models.IntegerField(verbose_name="首页每页显示的博客数",default=9)
    commentVerify=models.BooleanField(verbose_name="新评论是否默认隐藏",default=True)
    musicAutoPlay=models.BooleanField(default=False,verbose_name="背景音乐自动播放")
    qrCodeImage=FileBrowseField(max_length=99,blank=True,null=True,verbose_name="QR码URL")

    brand=models.CharField(max_length=19,verbose_name="博客名")
    subBrand=models.CharField(max_length=99,verbose_name="副博客名")

    ownerName=models.CharField(max_length=19,verbose_name="博主名")
    ownerBriefSelfIntro=models.CharField(max_length=999,blank=True,null=True,verbose_name="博主简介")
    ownerPhoto=FileBrowseField(max_length=99,verbose_name="博主照片")
    ownerIcon=FileBrowseField(max_length=99,verbose_name="博主头像")
    ownerSelfIntro=models.ForeignKey("flatPage",related_name="self_intro",verbose_name="自我介绍")
    ownerGithub=models.CharField(max_length=999,blank=True,null=True,verbose_name="GitHub")
    ownerGoogle=models.CharField(max_length=999,blank=True,null=True,verbose_name="Google")
    ownerTwitter=models.CharField(max_length=999,blank=True,null=True,verbose_name="Twitter")
    ownerWeibo=models.CharField(max_length=999,blank=True,null=True,verbose_name="微博")
    ownerWeiboBox=models.TextField(max_length=9999,blank=True,null=True,verbose_name="微博展示台")

    def __str__(self):
        return "【设置%s】%s"%(self.id,self.enabled)

    class Meta:
        verbose_name="设置"
        verbose_name_plural=verbose_name


class flatPage(models.Model):
    title=models.CharField(max_length=99,verbose_name="标题")
    text=models.TextField(max_length=999999,verbose_name="正文")
    createDatetime=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    modifyDatetime=models.DateTimeField(verbose_name="修改时间",auto_now=True)
    shown=models.BooleanField(default=True,verbose_name="可见")

    def __str__(self):
        return "【静态页面%s】%s"%(self.id,self.title)

    class Meta:
        verbose_name="静态页面"
        verbose_name_plural=verbose_name


class musicList(models.Model):
    objects=managers.music_list_manager()

    music=FileBrowseField(max_length=999,verbose_name="音乐文件")
    title=models.CharField(max_length=99,verbose_name="标题")
    musician=models.CharField(max_length=99,verbose_name="音乐人")
    enabled=models.BooleanField(default=True,verbose_name="启用")

    def __str__(self):
        return "%s - %s" % (self.title,self.musician)

    class Meta:
        verbose_name="背景音乐"
        verbose_name_plural=verbose_name


class comment(models.Model):
    objects=managers.comment_manager()

    shown = models.BooleanField(default=False, verbose_name="显示")
    read = models.BooleanField(default=False, verbose_name="已读")
    ipAddress = models.IPAddressField(verbose_name="IP地址")

    nickname = models.CharField(max_length=39, verbose_name="昵称")
    website = models.URLField(blank=True, null=True, verbose_name="网站")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    datetime = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    message = models.TextField(max_length=999999, verbose_name="留言内容")

    referredComment = models.ForeignKey(
        "comment", blank=True, null=True, verbose_name="所引用的留言")
    referredArticle = models.ForeignKey(
        "article", blank=True, null=True, verbose_name="所引用的博文")

    def __str__(self):
        return '''
shown:%s,
datetime:%s,
nickname:%s,
refered_comment:%s,
''' % (self.shown, self.datetime, self.nickname, self.refered_comment)

    def reply(self,nickname,message,website="",email=""):
        '''
        回复该留言/评论
        '''
        return

    class Meta:
        verbose_name="评论和留言"
        verbose_name_plural=verbose_name


class tag(models.Model):
    name = models.CharField(
        primary_key=True, max_length=99, unique=True, verbose_name="标签名")

    def __str__(self):
        return self.name

    def getUrl(self,absolute=False):
        s="/tag/%s/"%self.name
        if not absolute: return s
        # otherwise return absolute url
        return config.objects.get(enabled=1).domainName+s

    class Meta:
        verbose_name="标签"
        verbose_name_plural=verbose_name


class article(models.Model):
    objects=managers.article_manager()

    slug=models.SlugField(max_length=999,verbose_name="缩略")
    title = models.CharField(
        blank=False, null=False, max_length=29, verbose_name="标题")
    content = models.TextField(blank=False, verbose_name="正文")
    thumbnailPlain = models.TextField(blank=False, verbose_name="纯文本缩略")
    thumbnailLength = models.PositiveSmallIntegerField(
        default=399, verbose_name="展示长度")
    createDatetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    editDatetime=models.DateTimeField(verbose_name="最后修改时间",auto_now=True)
    tags = models.ManyToManyField("tag",related_name="articles", blank=True, null=True, verbose_name="标签")
    category = models.ForeignKey("category",related_name="articles",blank=False,null=False, verbose_name="分类")
    shown = models.BooleanField(verbose_name="可见", default=True)
    accessFrequency = models.PositiveIntegerField(verbose_name="阅读次数",default=0)

    def __str__(self):
        return '''
shown:%s,
title:%s,
category_name:%s,
''' % (self.shown, self.title, self.category_key)

    def getUrl(self,absolute=True):
        s="/article/%s/"%self.slug
        if not absolute: return s
        # otherwise return absolute url
        return config.objects.get(enabled=1).domainName+s

    class Meta:
        verbose_name="文章"
        verbose_name_plural=verbose_name


class category(models.Model):
    name = models.CharField(max_length=99, unique=True, verbose_name="分类名")

    def __str__(self):
        return self.name

    def getUrl(self,absolute=False):
        s="/category/%s/"%self.id
        if not absolute: return s
        # otherwise return absolute url
        return config.objects.get(enabled=1).domainName+s

    class Meta:
        verbose_name="分类"
        verbose_name_plural=verbose_name


class archive(models.Model):
    objects=managers.article_manager()

    year = models.PositiveSmallIntegerField(verbose_name="年份")
    month = models.PositiveSmallIntegerField(verbose_name="月份")

    def __str__(self):
        return '''
year:%s,
month:%s,
''' % (self.year, self.month)

    class Meta:
        verbose_name="归档"
        verbose_name_plural=verbose_name
