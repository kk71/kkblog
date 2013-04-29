# -*- coding: utf-8 -*-
'''
kkblog setting


author:kK(fkfkbill@gmail.com)
'''


import sys
from os import environ
local_path=sys.path[0]

#django调试模式
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

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
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
	local_path+"/static/",
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

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
	local_path+"/template/",
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
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
#kkblog静态配置

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

#留言、评论验证（即新评论默认隐藏）
comment_verification=False

#好友列表
friend_list={
		
}

#背景音乐
bgmusic={
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
