from datetime import datetime
from django.utils import timezone
from django.contrib import admin
import django.db.models
import django.forms
from django.utils.timezone import template_localtime

from . import models


@admin.register(models.config)
class configAdmin(admin.ModelAdmin):
    list_display = ("enabled","domainName","articlesPerPage","commentVerify","musicAutoPlay")
    ordering = ("enabled",)


@admin.register(models.flatPage)
class flatPageAdmin(admin.ModelAdmin):
    list_display = ("title","createDatetime","modifyDatetime","shown")
    list_filter = ("shown",)
    readonly_fields = ("createDatetime","modifyDatetime")
    actions = ("hide","show")

    view_on_site = True # need a get_absolute_url method in model

    def hide(self,request,querystring):
        querystring.update(shown=False)
    hide.short_description="隐藏"

    def show(self,request,querystring):
        querystring.update(shown=True)
    show.short_description="显示"

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            "/static/js/tinymce_setup.js",
        ]


@admin.register(models.music)
class musicListAdmin(admin.ModelAdmin):
    list_display = ("title","musician","music","enabled")
    list_filter = ("enabled",)
    actions = ("disable","enable")

    def disable(self,request,querystring):
        querystring.update(enabled=False)
    disable.short_description="禁用"

    def enable(self,request,querystring):
        querystring.update(enabled=True)
    enable.short_description="启用"


@admin.register(models.comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ("nickname", "message", "datetime", "email",
                    "website", "ipAddress", "shown", "read","article","parent")
    ordering = ("-datetime",)
    list_filter = ("read", "shown")
    readonly_fields = ("parent","article")
    actions = ("markReadShown","markRead","show","hide")

    def markReadShown(self,request,queryset):
        queryset.update(read=True,shown=True)
    markReadShown.short_description="标记已读并显示"

    def markRead(self,request,queryset):
        queryset.update(read=True)
    markRead.short_description = "标记已读"

    def show(self,request,queryset):
        queryset.update(shown=True)
    show.short_description = "显示"

    def hide(self,request,queryset):
        queryset.update(shown=False)
    hide.short_description = "隐藏"



@admin.register(models.article)
class articleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "createDatetime","editDatetime",
                    "thumbnailLength","accessFrequency","shown","sticky",
                    "archive")
    ordering = ("-createDatetime",)
    list_filter = ("shown","sticky")
    readonly_fields = ("editDatetime",)
    view_on_site = True # need a get_absolute_url method in model
    actions = ("markSticky","unmarkSticky","hide","show")

    def markSticky(self,request,querystring):
        querystring.update(sticky=True)
    markSticky.short_description = "置顶"

    def unmarkSticky(self,request,querystring):
        querystring.update(sticky=False)
    unmarkSticky.short_description = "取消置顶"

    def hide(self,request,querystring):
        querystring.update(shown=False)
    hide.short_description="隐藏"

    def show(self,request,querystring):
        querystring.update(shown=True)
    show.short_description="显示"

    def save_model(self, request, obj, form, change):
        # auto add or select archive for this article
        if obj.archive_id is not None and \
            obj.createDatetime is not None:
            # if an article object is not being fresh saved,
            # DO NOT change it's archive since archive record the
            # create datetime of an article
            # 为了判断博文对象是否有archive，不能直接测obj.archive
            # 需要判断obj.archive_id是否为None。
            obj.save()
            return
        now=datetime.now()
        try:
            theArchive=models.archive.objects.get(year=now.year,month=now.month)
        except:
            theArchive=models.archive(year=now.year,month=now.month)
            theArchive.save()
        obj.archive=theArchive

        if obj.createDatetime is None:
            obj.createDatetime=timezone.now()
        obj.save()


    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            "/static/js/tinymce_setup.js",
        ]


@admin.register(models.category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("articles",)


@admin.register(models.tag)
class tagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.friend)
class friendAdmin(admin.ModelAdmin):
    list_display = ("name","url")


admin.site.register(models.archive)