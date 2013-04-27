# -*- coding: utf-8 -*-
'''
kkblog url configuration


author:kK(fkfkbill@gmail.com)
'''

#django import
from django.conf.urls import patterns, include, url

#third-part import
import djangomako
import grappelli

#project import
import settings
from blog import views

#for admin
from django.contrib import admin
admin.autodiscover()


urlpatterns=patterns("",)

if settings.DEBUG==True:
	urlpatterns+=patterns("",
		url(r"^tmpldebug/?(.*)",djangomako.tmpldebug),#template debugging
	)

urlpatterns += patterns('',
		#admin management
		url(r'^admin/', include(admin.site.urls)),
		url(r'^grappelli/', include('grappelli.urls')),

		#search
		url(r"^search/(.*)$",views.search_article),
		
		#article
		url(r"^article/(.*)$",views.article),

		#tag
		url(r"^tag/(.*)/(.*)$",views.tag),
		url(r"^tag/(.*)$",views.tag),
		url(r"^tag",views.tag),

		#category
		url(r"^category/(.*)/(.*)$",views.category),
		url(r"^category/(.*)$",views.category),
		url(r"^category",views.category),

		#archive
		url(r"^archive/(.*)/(.*)$",views.archive),
		url(r"^archive/(.*)$",views.archive),
		url(r"^archive$",views.archive),

		#comment
		url(r"^commentbox/?(.*)$",views.commentbox),

		#comment list(ajax)
		url(r"^comment/?(.*)$",views.comment_list),

		#post comment(ajax)
		url(r"^postcomment$",views.post_comment),

		#upload image
		url(r"^uploadimage$",views.upload_image),

		#about
		url(r"^about$",views.about),

		#index
		url(r"^(.*)$",views.index),#any url can't be proccessed by re above will be dealt with here
)
