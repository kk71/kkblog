from django.contrib import admin
from . import models


@admin.register(models.config)
class configAdmin(admin.ModelAdmin):
    list_display = ("enabled","domainName","articlesPerPage","commentVerify","musicAutoPlay")
    ordering = ("enabled",)


@admin.register(models.flatPage)
class flatPageAdmin(admin.ModelAdmin):
    list_display = ("title","createDatetime","modifyDatetime","shown")
    list_filter = ("shown",)

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            "/static/js/tinymce_setup.js",
        ]


@admin.register(models.musicList)
class musicListAdmin(admin.ModelAdmin):
    list_display = ("title","musician","music","enabled")
    list_filter = ("enabled",)


@admin.register(models.comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ("nickname", "message", "datetime", "email",
                    "website", "ipAddress", "shown", "read")
    ordering = ("-datetime",)
    list_filter = ("read", "shown")
    readonly_fields = ("referredComment","referredArticle","nickname","website","email","message")
    exclude = ("ipAddress",)


@admin.register(models.article)
class articleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "createDatetime",
                    "thumbnailPlain", "thumbnailLength", "shown")
    ordering = ("-createDatetime",)
    list_filter = ("shown",)
    exclude = ("thumbnailPlain",)
    readonly_fields = ("accessFrequency",)

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