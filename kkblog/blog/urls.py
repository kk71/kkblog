from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',

    # search
    url(r"^search/(.*)$", views.search_article),

    # article
    url(r"^article/(.*)$", views.article),

    # tag
    url(r"^tag/(.*)/(.*)$", views.tag),
    url(r"^tag/(.*)$", views.tag),
    url(r"^tag", views.tag),

    # category
    url(r"^category/(.*)/(.*)$", views.category),
    url(r"^category/(.*)$", views.category),
    url(r"^category", views.category),

    # archive
    url(r"^archive/(.*)/(.*)$", views.archive),
    url(r"^archive/(.*)$", views.archive),
    url(r"^archive$", views.archive),

    # comment
    url(r"^commentbox/?(.*)$", views.commentbox),

    # comment list(ajax)
    url(r"^comment/?(.*)$", views.comment_list),

    # post comment(ajax)
    url(r"^postcomment$", views.post_comment),

    # about
    url(r"^about$", views.about),

    # index
    # any url can't be processed by re above will be dealt with
    # here
    url(r"^(.*)$", views.index),
)
