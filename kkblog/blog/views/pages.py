from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponseNotFound
import html # for html escaping

from .. import models
from django.conf import settings
from djangomako import render_to_response
from .list import *


def frame(navbarActive,title):
    '''
    return
    '''
    return {
        "config":models.config.objects.get(enabled=1),
        "staticPrefix":settings.STATIC_URL,
        "title":title,
        "navbarActive":navbarActive,
        "categoryList":models.category.objects.all(),
        "tagList":models.tag.objects.all(),
        "hotList":models.article.objects.list(sortByFrequency=True,stickyIncluded=True).page(1).object_list,
        "friendList":models.friend.objects.all(),
    }


@require_GET
def index(request):
    '''
    for showing index page
    '''
    config=models.config.objects.get(enabled=1)

    try:
        page=int(request.GET["page"])
    except:
        page=1
    ls = models.article.objects.list(itemsPerResult=config.articlesPerPage)
    if page>ls.num_pages:
        return HttpResponseRedirect("/")
    dic = {
        # index
        "displayList": ls.page(page).object_list,

        # pagination
        "url_template": "?page=%s",
        "pages": ls.num_pages,
        "current": page,
    }
    if page==1:
        dic.update(stickyList=models.article.objects.listSticky())
    dic.update(frame(0,config.getBrand()))
    return render_to_response("index.html", dic)


@require_GET
def flatPage(request,slug=""):
    '''
    展示静态页
    '''
    config=models.config.objects.get(enabled=1)
    try:
        page=int(request.GET["page"])
    except:
        page=1

    print(slug)
    if slug:
        # show one flatpage
        showLinkToOriginal=False
        try:
            ls=Paginator([models.flatPage.objects.get(slug=slug)],per_page=1)
        except:
            return HttpResponseNotFound()
    else:
        # display a flatpages list
        showLinkToOriginal=True
        ls = Paginator(models.flatPage.objects.filter(shown=True),config.articlesPerPage,0)
        if page>ls.num_pages:
            return HttpResponseRedirect("/flatpage/")
    dic = {
        # flatpage
        "displayList": ls.page(page).object_list,
        "showLinkToOriginal":showLinkToOriginal,

        # pagination
        "url_template": "?page=%s",
        "pages": ls.num_pages,
        "current": page,
    }
    dic.update(frame(3,"静态页 - "+config.getBrand()))
    return render_to_response("flatpage.html",dic)


@require_GET
def about(request):
    '''
    show about page
    '''
    config=models.config.objects.get(enabled=1)
    dic = {
        # about
        "about": config.ownerSelfIntro
    }
    dic.update(frame(4,"关于 - "+config.getBrand()))
    return render_to_response("about.html",dic)


def article(request, slug):
    '''
    show an article
    '''
    config=models.config.objects.get(enabled=1)
    try:
        atcle = models.article.objects.get(slug=slug)
        if not atcle.shown:
            return render_to_response("404.html", status=404)
        atcle.accessFrequency = F("accessFrequency")+1
        atcle.save()
        # F函数使得原本的AccessFrequency过期且无法使用
        # 故须要重新读取
        atcle = models.article.objects.get(slug=slug)
    except:
        return render_to_response("404.html", status=404)
    dic = {
        "article": atcle,
    }
    dic.update(frame(navbarActive=-1,title=atcle.title+" - "+config.getBrand()))
    return render_to_response("article.html", dic, request=request)
