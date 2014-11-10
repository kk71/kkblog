import random

from django.utils.timezone import template_localtime
from django.db import models
from filebrowser.fields import FileBrowseField
from mptt.models import MPTTModel, TreeForeignKey

from . import managers


class config(models.Model):
    ENABLED=(
        (1,"启用"),
    )
    enabled=models.IntegerField(unique=True,choices=ENABLED,blank=True,verbose_name="启用该设置")

    # 生产环境的域名（形如：http://*****，末尾不加/）
    domainName=models.CharField(max_length=99,verbose_name="域名")
    articlesPerPage=models.PositiveSmallIntegerField(verbose_name="首页每页显示的博客数",default=9)
    commentVerify=models.BooleanField(verbose_name="新评论是否默认隐藏",default=True)
    musicAutoPlay=models.BooleanField(default=False,verbose_name="背景音乐自动播放")
    qrCodeImage=FileBrowseField(max_length=99,blank=True,verbose_name="QR码URL")

    brand=models.CharField(max_length=19,blank=True,verbose_name="博客名")
    subBrand=models.CharField(max_length=99,blank=True,verbose_name="副博客名")

    ownerName=models.CharField(max_length=19,verbose_name="博主名")
    ownerBriefSelfIntro=models.CharField(max_length=999,blank=True,verbose_name="博主简介")
    ownerIcon=FileBrowseField(max_length=99,blank=True,verbose_name="博主头像")
    ownerSelfIntro=models.ForeignKey("flatPage",related_name="self_intro",verbose_name="自我介绍")

    ownerGithub=models.URLField(max_length=999,blank=True,verbose_name="GitHub")
    ownerGoogle=models.URLField(max_length=999,blank=True,verbose_name="Google")
    ownerTwitter=models.URLField(max_length=999,blank=True,verbose_name="Twitter")
    ownerWeibo=models.URLField(max_length=999,blank=True,verbose_name="微博")
    ownerWeiboBox=models.TextField(max_length=9999,blank=True,verbose_name="微博展示台")
    ownerEmail=models.EmailField(max_length=99,blank=True,verbose_name="邮箱")

    def __str__(self):
        return "【设置%s】"%(self.id,)

    def getOwnerIcon(self):
        '''
        get the owner's icon
        if there's an icon in config,use it; otherwise generate from gravatar
        '''
        import hashlib
        from urllib import parse
        if self.ownerIcon:return self.ownerIcon
        if self.ownerEmail:
            return "http://www.gravatar.com/avatar/"+ \
                   hashlib.md5(self.ownerEmail.lower().encode("utf-8")).hexdigest()+ \
                   "?"+ \
                   parse.urlencode({
                       "d":"http://www.gravatar.com/avatar/",
                       "size":"32"
                   })
        return ""

    def getSafeOwnerEmail(self):
        '''
        return a 'safe' email address
        '''
        if not self.ownerEmail:return ""
        return self.ownerEmail.replace("@",random.choice(["(#)","($)","(&)","(*)","(a)"]))

    def getBrand(self):
        '''获取正确的博客名'''
        if self.brand:return self.brand
        return self.ownerName+"的博客"

    class Meta:
        verbose_name="设置"
        verbose_name_plural=verbose_name


class flatPage(models.Model):
    slug=models.SlugField(max_length=99,unique=True,verbose_name="缩略")
    title=models.CharField(max_length=99,verbose_name="标题")
    text=models.TextField(max_length=999999,verbose_name="正文")
    createDatetime=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    modifyDatetime=models.DateTimeField(verbose_name="最后修改时间",auto_now=True)
    shown=models.BooleanField(default=True,verbose_name="可见")

    def __str__(self):
        return "【静态页面%s】%s"%(self.id,self.title)

    def getUrl(self,absolute=False):
        s="/flatpage/%s/"%self.slug
        if not absolute: return s
        # otherwise return absolute url
        return config.objects.get(enabled=1).domainName+s

    def get_absolute_url(self):
        '''used for displaying a 'show in site' button in admin'''
        return self.getUrl(absolute=True)

    class Meta:
        verbose_name="静态页面"
        verbose_name_plural=verbose_name


class music(models.Model):
    music=FileBrowseField(max_length=999,verbose_name="音乐文件")
    title=models.CharField(max_length=99,verbose_name="标题")
    musician=models.CharField(max_length=99,verbose_name="音乐人")
    enabled=models.BooleanField(default=True,verbose_name="启用")

    def __str__(self):
        return "【音乐%s】%s - %s" % (self.id,self.title,self.musician)

    class Meta:
        verbose_name="背景音乐"
        verbose_name_plural=verbose_name


class comment(MPTTModel):
    objects=managers.commentManager()

    shown = models.BooleanField(default=False, verbose_name="显示")
    read = models.BooleanField(default=False, verbose_name="已读")
    ipAddress = models.IPAddressField(verbose_name="IP地址")
    byOwner = models.BooleanField(default=False,verbose_name="博主自己的评论")
    # TODO: 之后将加上判断是不是博主的回复。将特殊对待。
    # TODO: 另外还需在admin界面中加入回复页。

    nickname = models.CharField(max_length=39, verbose_name="昵称")
    website = models.URLField(blank=True, verbose_name="网站")
    email = models.EmailField(blank=True, verbose_name="Email")
    datetime = models.DateTimeField(verbose_name="时间")
    message = models.TextField(max_length=999999, verbose_name="内容")

    parent = TreeForeignKey(
        "self",related_name="children",null=True, blank=True, verbose_name="父评论")
    article = models.ForeignKey(
        "article", related_name="comments", verbose_name="引用博文")

    def __str__(self):
        return "【评论%s】%s" % (self.id,self.nickname)

    def reply(self,nickname,message,website="",email=""):
        '''
        回复该留言/评论
        '''
        return

    def toDict(self,withParent=True):
        '''
        将当前评论转换成字典，以便转换为json传输
        '''
        result={
            "id":self.id,
            "shown":self.shown,
            "read":self.read,
            "nickname":self.nickname,
            "website":self.website,
            "email":self.email,
            "datetime":template_localtime(self.datetime).strftime("%Y-%m-%d,%H-%M-%S"),
            "message":self.message,
            "byOwner":self.byOwner,
            "parent":None,
            "article":self.article.id
        }
        if self.parent_id is not None and withParent:
            result.update({
                "parent":self.parent.toDict(withParent=False)
            })
        return result

    class Meta:
        verbose_name="评论"
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

    def get_absolute_url(self):
        return self.getUrl(True)

    def randomTagColor(self):
        '''
        return a random tag color name
        '''
        colorStyles = ["success", "warning", "danger", "info", "default","primary"]
        return random.choice(colorStyles)

    class Meta:
        verbose_name="标签"
        verbose_name_plural=verbose_name


class article(models.Model):
    objects=managers.articleManager()

    slug=models.SlugField(max_length=255,unique=True,verbose_name="缩略")
    title = models.CharField(
        blank=False, max_length=29, verbose_name="标题")
    content = models.TextField(blank=False, verbose_name="正文")
    thumbnailLength = models.PositiveSmallIntegerField(
        default=399, verbose_name="展示长度")
    createDatetime = models.DateTimeField(verbose_name="创建时间",blank=True,help_text="如果不给出，将自动创建。")
    editDatetime=models.DateTimeField(verbose_name="最后修改时间",auto_now=True,help_text="自动生成。")
    tags = models.ManyToManyField("tag",related_name="articles",null=True, blank=True, verbose_name="标签")
    category = models.ForeignKey("category",related_name="articles", verbose_name="分类")
    archive = models.ForeignKey("archive",related_name="articles",blank=True,null=True,verbose_name="归档",
                                help_text="如果不给出，将自动创建。")
    shown = models.BooleanField(verbose_name="可见", default=True)
    sticky = models.BooleanField(default=False,verbose_name="置顶")
    accessFrequency = models.PositiveIntegerField(verbose_name="阅读次数",default=0)

    def __str__(self):
        return "【博文%s】%s" % (self.id, self.title)

    def getUrl(self,absolute=False):
        s="/article/%s/"%self.slug
        if not absolute: return s
        # otherwise return absolute url
        return config.objects.get(enabled=1).domainName+s

    def getThumbnail(self):
        return self.content[:self.thumbnailLength]

    def getCreateDate(self):
        return self.createDatetime.strftime("%Y-%m-%-%d")

    def get_absolute_url(self):
        '''used for displaying a 'show in site' button in admin'''
        return self.getUrl(absolute=True)

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

    def get_absolute_url(self):
        return self.getUrl(True)

    class Meta:
        verbose_name="分类"
        verbose_name_plural=verbose_name


class archive(models.Model):
    objects=managers.archiveManager()

    year = models.PositiveSmallIntegerField(verbose_name="年份")
    month = models.PositiveSmallIntegerField(verbose_name="月份")

    def __str__(self):
        return '''%s - %s''' % (self.year, self.month)

    def getUrl(self,absolute=False):
        s="/archive/%s/%s/" % (self.year,self.month)
        if not absolute: return s
        # otherwise return absolute url
        return config.objects.get(enabled=1).domainName+s

    def get_absolute_url(self):
        return self.getUrl(True)

    class Meta:
        verbose_name="归档"
        verbose_name_plural=verbose_name


class friend(models.Model):
    name=models.CharField(max_length=99,verbose_name="友链名")
    url=models.URLField(max_length=99,verbose_name="URL")

    def __str__(self):
        return "【友链%s】%s - %s"%(self.id,self.name,self.url)

    class Meta:
        verbose_name="友链"
        verbose_name_plural=verbose_name