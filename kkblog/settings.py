# -*- coding: utf-8 -*-
'''
kkblog setting


author:kK(fkfkbill@gmail.com)
'''


import sys

DEBUG = True

TEMPLATE_DEBUG = DEBUG


ADMINS = (
     ("",""),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'blogdata.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

ALLOWED_HOSTS = ["*"]

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	sys.path[0]+"/static/",
)

#where uploaded images stored
uploaded_image_dir=STATICFILES_DIRS[0]+"image_uploaded/"
uploaded_image_url=STATIC_URL+"image_uploaded/"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8ycirmfoxt)_-jja2pm1&5rp()#p$_3*ypru=q8yr4m7^28^ho'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

FILE_UPLOAD_HANDLERS = (
	"django.core.files.uploadhandler.MemoryFileUploadHandler",
	"django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
	sys.path[0]+"/template/",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	"django.contrib.sitemaps",
	"grappelli",
    'django.contrib.admin',
	"blog",

    "south",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#==================================================
#kkblog配置

#生产环境的域名（形如：http://*****，末尾不加/）
domain_name=r""

#grappelli配置
GRAPPELLI_ADMIN_TITLE=r"kkblog管理"


#博主名
author_name="kk"


#博客标题
brand=r"呼呼"
blog_description="测试～。"


#博主电邮
email_server=r"smtp.xxx.com"
email=r"xxx@xxx.com"
email_p=r""#login password

#首页每页显示的博文数目
articles_per_page=8

#新评论默认隐藏
comment_verification=False

#好友列表
friend_list={
#    "显示名":"主页",
}

#背景音乐
bgmusic={
#    "显示名":"url",
}

#首页上显示置顶
show_featured=False
featured_content=r''''''
featured_img="/static/featured_img.jpg"

#博主简介（显示在页尾）
brief_selfintro=r"test~"
#博主图片
master_photo=r""
page_icon=r""


#博主介绍（显示在“关于”页中）
self_intro=r'''
'''

#博主微博
weibo=r""

#博主推特
twitter=r""

#博主微博展示台
weibo_box=''''''

#博主推特关注按钮
twitter_follow=r''''''
