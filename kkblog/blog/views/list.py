import html
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.db.models import Count

from datetime import datetime

from .. import models
from .pages import frame
from djangomako import render_to_response

'''
listDescription: (string)description to the category,which will be shown at the top of all lists
listType: (list)0=archives 1=categories 2=tags 3=search
showPaginator: (boolean)whether show the pagination bar
lists: (integer, differ from listType)
    0:[archiveObj,if-full,[]]
    1:[categoryObj,if-full,[]]
    2:[tagObj,True,[]]
    3:[None,False,[]]
'''


@require_GET
def archive(request, year=None,month=None):
    '''
    show archives
    '''
    config = models.config.objects.get(enabled=1)
    ar = []

    if year is None and month is None:
        # show archives of this year
        # 如果未指定需要显示哪一段时间的归档，
        # 显示当年的归档以及他们前三篇博文，
        # 然后显示往年各个年份（并不显示其下的归档）
        for i in models.archive.objects.list(year=datetime.now().year):
            atcls = []
            for a in models.article.objects.list(
                    itemsPerResult=3,
                    archiveObj=i,
                    stickyIncluded=True
            ).page(1).object_list:
                atcls.append(a)
            ar.append([i, False, atcls])
        # legacy archives show legacy years
        legacyYears=models.archive.objects.getYears()
        legacyYears.remove(datetime.now().year)
        listDescription = ""

    elif year and not month:
        for i in models.archive.objects.list(year=int(year)):
            atcls = []
            for a in models.article.objects.list(
                    itemsPerResult=3,
                    archiveObj=i,
                    stickyIncluded=True
            ).page(1).object_list:
                atcls.append(a)
            ar.append([i, False, atcls])
        legacyYears=[]
        listDescription = "%s年的归档" % year

    elif int(year) >= 2012 and 1 <= int(month) <= 12:
        i = models.archive.objects.get(
            year=int(year),
            month=int(month)
        )
        atcls = []
        for a in models.article.objects.list(
                itemsPerResult=999,
                archiveObj=i,
                stickyIncluded=True
        ).page(1).object_list:
            atcls.append(a)
        ar.append([i, True, atcls])
        legacyYears=[]
        listDescription = "%s年%s月的归档" % (year,month)

    else:
        return Http404

    dic = {
        "config":config, # when creating legacy archives list, domain prefix is needed
        "lists": ar,
        "legacyYears":legacyYears, # for display older year, in archive page only
        "listType": 0,
        "listDescription": listDescription,
        "showPaginator": False,
    }
    dic.update(frame(navbarActive=2,title="分类 - "+config.getBrand()))
    return render_to_response("list.html", dic)


@require_GET
def tag(request, name):
    '''
    show the tag list
    '''
    config = models.config.objects.get(enabled=1)
    try:
        theTag=models.tag.objects.get(name=name)
    except:
        return Http404
    theArticles=Paginator(theTag.articles.all(),20)
    try:
        page=request.GET["page"]
    except:
        page=1

    dic = {
        "lists": [[theTag,True,theArticles.page(page).object_list]],
        "listType": 2,
        "listDescription": "包含标签“%s”的博文" % name,
        "showPaginator": True,

        # pagination
        "url_template": "/tag/" + name + "/",
        "pages": theArticles.num_pages,
        "current": page,
    }

    dic.update(frame(navbarActive=-1,title="标签“%s” - "%name+config.getBrand()))
    return render_to_response("list.html", dic)


@require_GET
def category(request, categoryId=None):
    '''
    get all categories and their articles
    '''
    config = models.config.objects.get(enabled=1)

    try:
        page = int(request.GET["page"])
    except:
        page = 1

    ar = []
    if not categoryId:
        # show category list only
        c = models.category.objects.annotate(article_count=Count("articles")).order_by(
            "-article_count")  # sort by the count of articles combined to the category
        for i in c:
            ctgry = [i, False, []]
            for atcls in models.article.objects.list(
                    categoryId=i.id,
                    itemsPerResult=3,
                    stickyIncluded=True
            ).page(1):
                ctgry[2].append(atcls)
            ar.append(ctgry)
        dic = {
            "lists": ar,
            "listType": 1,
            "listDescription": "",
            "showPaginator": False,
        }

    else:
        # show articles behind the given category
        # show has a paginator
        try:
            c = models.category.objects.get(id=categoryId)
        except:
            return Http404
        categoryArticlePaginator = models.article.objects.list(
            categoryId=c.id,
            itemsPerResult=20,
            stickyIncluded=True
        )
        ctgry = [c, True, []]
        for atcls in categoryArticlePaginator.page(page):
            ctgry[2].append(atcls)
        ar.append(ctgry)
        dic = {
            "lists": ar,
            "listType": 1,
            "listDescription": "分类“%s”的博文" % c.name,
            "showPaginator": True,

            # pagination
            "url_template": "/category/" + str(categoryId) + "/%s/",
            "pages": categoryArticlePaginator.num_pages,
            "current":page,
        }

    dic.update(frame(navbarActive=1, title="分类 - " + config.getBrand()))
    return render_to_response("list.html", dic)


@require_GET
def searchArticle(request):
    '''
    search the title and content of articles.
    '''
    config = models.config.objects.get(enabled=1)
    try:
        toSearch=request.GET["keywords"]
    except:
        return HttpResponseBadRequest("")

    dic = {
        "lists": [[None, False, models.article.objects.search(toSearch)]],
        "listDescription": "搜索包含“%s”的结果" % html.escape(toSearch),
        "listType": 3,
        "showPaginator": False
    }
    dic.update(frame(navbarActive=-1,title="搜索结果 - "+config.getBrand()))
    return render_to_response("list.html", dic)