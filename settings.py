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

#djangomako模板调试
TEMPLATE_DEBUG = False


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
ALLOWED_HOSTS = []

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
brand=r"軒簫榭雨"
blog_description="陌不相识时，你我是天空中的云；相识后，你我是溪中的水。你看，下雨了。"


#博主电邮
email_server=r"smtp.gmail.com"
email=r"fkfkbill@gmail.com"
email_p=r"zlgwxlztljaddviy"#login password

#首页每页显示的博文数目
articles_per_page=8

#留言、评论验证（即新评论默认隐藏）
comment_verification=False

#好友列表
friend_list={
		
}

#背景音乐
bgmusic={
		"夏夕空 - 中孝介":"/static/music/nyz.mp3",
		"夏の終わり - 森山直太朗":"/static/music/nnowr.mp3",
		"夢想歌 - Suara":"/static/music/msu.mp3",
		"The Sound of the Sea - 遠Tone音":"/static/music/TheSoundoftheSea.mp3",
		"雪の音 - き乃はち":"/static/music/YukiNoNe.mp3",
		"三个人的晚餐 - 王若琳":"/static/music/sgrdwc.mp3",
}







#首页上显示置顶
show_featured=True
featured_content=r'''我不知道人为何要为无聊所苦。<br>
不要用心于外物，最好的办法是一个人独处；<br>
一旦把心放在世俗，就免不了被它迷惑，失去自主。<br>
比如和人交谈，总想博得别人的好感，就做不到言为心声了。<br>
又不免有和人嬉闹的时候，有和人争执的时候，以至于喜怒不定，妄念丛生，得失之心就再难放下。
<p style="text-align:right;">—— 《徒然草》</p>'''
featured_img="/static/featured_img.jpg"

#博主简介（显示在页尾）
brief_selfintro=r"kK，堕落在校野生程序猿一枚。初识编程于小学，大学认识Python、Linux；现用笔记本单系统Ubuntu。编程之余曾热爱写作，鼓捣过小说，弹过吉他，装过伪文艺；现热爱尺八箫、日语、轻音乐，伪汉服复兴者（没穿过汉服），极品宅男+路痴，羡慕丰沛的人生，向往简单平实的生活。"
#博主图片
master_photo=r"/static/author.jpg"
page_icon=r"/static/author_small.jpg"


#博主介绍（显示在“关于”页中）
self_intro=r'''
<h3>自我介绍</h3>
<p>kK，堕落在校的野生程序猿一枚，一路自学成长而来，热爱开源与Python，实用主义喜欢ubuntu，不打游戏，爱咖啡爱咖喱爱烹饪。生活中是个极品宅男+路痴，编程之余喜欢尺八、日语、轻音乐，兴趣甚广，然而不少都散落在成长的道路上，比如写小说弹吉他、比如装伪文艺。曾经希望活出一片生机盎然的岁月，一不小心就宅到了现今，于是还是淡淡的继续简单平实的生活吧。</p>
<p>使用的语言：Python, HTML+CSS+JS(jQuery), Java, C(++), PHP, Haskell, 曾经还有VB（那是我入门的语言）</p>
<p>人语：英语、日语、韩语入门、西班牙语……（已经放弃了- -）</p>
<p></p>

<h3>关于博客</h3>
<p>一直想设计一个从前端到后端全是自己设计的博客，鼓捣了一段时间才发现，对于我这个没什么设计天赋的木讷码农，这种想法终究还是显得太过于滑稽。于是懂一点前端的我借用了别人开源（确切说是Creative Commons Attribution 3.0 License）的html模板，加以修改，才有今天博客的样子。</p>
<p>前几天jQuery2出来了（不支持IE678）于是果断换用。只是建一个个人博客，而且还是偏于技术的，相信浏览的人不会用这些坑跌的浏览器了吧。</p>
<p>所使用的项目都在博客页脚写清楚了。Python3.3+Django1.5，个人比较有代码洁癖，所以喜欢追新。枯燥的博客设计更加让人觉得疲惫了（部分库仍然不支持Python3，比如PIL，这致使我无法使用filebrowser）。</p>
<p></p>

<h3>联系方式</h3>
<p>E-Mail:fkfkbill@gmail.com</p>
<p></p>
<p>
<iframe width="100%" height="24" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0" scrolling="no" border="0" src="http://widget.weibo.com/relationship/followbutton.php?language=zh_cn&width=100%&height=24&uid=1603705420&style=3&btn=red&dpc=1"></iframe>
<iframe allowtransparency="true" frameborder="0" scrolling="no"
  src="//platform.twitter.com/widgets/follow_button.html?screen_name=fkfkbill&lang=zh"
  style="width:300px; height:20px;"></iframe>
</p>
<p>呵呵如果你看到上面出现一块空白区域说明你没有翻墙（具体请参考<a href="https://code.google.com/p/goagent/" target="_blank">goagent</a>）</p>
'''

#博主微博
weibo=r"http://weibo.com/billfk"

#博主推特
twitter=r"http://twitter.com/fkfkbill"

#博主微博展示台
weibo_box='''<iframe width="100%" height="330" class="share_self"  frameborder="0" scrolling="no" src="http://widget.weibo.com/weiboshow/index.php?language=zh_tw&width=0&height=330&fansRow=2&ptype=1&speed=0&skin=10&isTitle=0&noborder=0&isWeibo=1&isFans=0&uid=1603705420&verifier=a1171a80&dpc=1"></iframe>'''

#博主推特关注按钮
twitter_follow=r'''<iframe allowtransparency="true" frameborder="0" scrolling="no" src="//platform.twitter.com/widgets/follow_button.html?screen_name=fkfkbill&amp;lang=zh" style="width:300px; height:20px;"></iframe>'''
