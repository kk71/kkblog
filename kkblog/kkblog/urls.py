from django.conf.urls import patterns, include, url

import djangomako
from django.conf import settings

# for admin
from django.contrib import admin
admin.autodiscover()


from filebrowser import sites


urlpatterns = patterns("",)

if settings.DEBUG == True:
    urlpatterns += patterns("",
        # template debugging
        url(r"^tmpldebug/?(.*)", djangomako.tmpldebug),
    )

urlpatterns += patterns('',
    # admin management
    url(r'^admin/filebrowser/', include(sites.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^",include("blog.urls"))
)
