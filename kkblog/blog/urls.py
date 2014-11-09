from django.conf.urls import patterns, include, url
from . import views
from . import feed


urlpatterns = patterns('',
    # rss feed
    url(r"^rss/$", feed.articleFeed()),

    # search
    url(r"^search/$", views.searchArticle),

    # article
    url(r"^article/(.*)/$", views.article),

    # flatpage
    url(r"^flatpage/$",views.flatPage),
    url(r"^flatpage/(.*)/$",views.flatPage),

    # tag
    url(r"^tag/(\S*)/$", views.tag),

    # category
    url(r"^category/$", views.category),
    url(r"^category/(\d*)/$", views.category),

    # archive
    url(r"^archive/$", views.archive),
    url(r"^archive/(\d*)/$", views.archive),
    url(r"^archive/(\d*)/(\d*)/$", views.archive),

    # comment list(ajax)
    url(r"^comment-list/$", views.commentList),

    # post comment(ajax)
    url(r"^post-comment/$", views.postComment),

    # music list(ajax)
    # TODO: write code for music list
    url(r"^music-list/$", views.musicList),

    # about
    url(r"^about/$", views.about),

    # index
    # any url can't be processed by re above will be dealt with
    # here
    url(r"^$", views.index),
)
