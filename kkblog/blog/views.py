from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
import cgi  # for xml escaping

import simplejson as json

from . import models
from django.conf import settings
from djangomako import render_to_response


def common_view(navbarActive):
    '''
    for public view rendering(title bar and sidebar)
    return:
        dict()
    '''
    freqs = []
    for i in models.article.list(items_per_result=6, sort_by_frequence=True):
        freqs.append(models.article.article_obj_to_dict(i))
    return {
        "staticPrefix":settings.STATIC_URL,
        "config":models.config.objects.get(enabled=1),

        "navbarActive":navbarActive,
        "categoryList":models.category.objects.all(),
        "tagList":models.tag.objects.list(),
        "hotList":models.article.objects.list(sort_by_frequency=True),
        "friendList":{},
    }


def index(request, offset=""):
    '''
for showing index page

note:
    the url configuration for index view must be put after all the others' in url.py
arguments:
    request:
    offset:pagination of index page
'''
    try:
        if offset.strip() == "":
            offset = "1"
        offset = int(offset)
        if offset <= 0:
            raise Exception
    except:
        return render_to_response("404.html", status=404)
    # quick search
    if request.method == "GET" and len(request.GET) == 1:
        return HttpResponseRedirect("/search/" + request.GET["qsearch"])
    ls = []
    for i in models.list_articles(items_per_result=settings.articles_per_page, page=offset):
        ls.append(models.article_obj_to_dict(i))
    if len(models.article.objects.all()) % settings.articles_per_page != 0:
        pages = len(
            models.article.objects.all()) // settings.articles_per_page + 1
    else:
        pages = len(models.article.objects.all()) // settings.articles_per_page
    dic = {
        # featured
        "featured_title": "",
        "featured_content": settings.featured_content,
        "featured_img": settings.featured_img,

        # index
        "display_list": ls,

        # pagination
        "url_template": "/%s#latest",
        "pages": pages,
        "current": offset,
    }
    dic.update(common_view(navbar_active=0))  # common view
    return render_to_response("index.html", dic)


#=======================================================
'''
list.html interface
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
list_description:(string)description to the category,which will be shown at the top of all lists
list_type:(list)0archives 1categories 2tags
pagi:(boolean)wheather show the pagination bar
lists:(differ from list_type)
	0:[year,month,full,[]]
	1:[category,category_id,full,[]]
	2:[tag,None,full,[]]
	3:[None,None,False,[]]
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
'''


def archive(request, *offsets):
    '''
show archives
arguments:
    request:
    offsets:(tuple)year and month specified,both of them are optional(==ofsets can be empty)
'''
    ar = []
    if offsets == ("", "") or offsets == ("",) or offsets == ():
        for i in models.list_archives():
            atcls = []
            for a in models.list_articles(items_per_result=3, archive_obj=i):
                atcls.append(models.article_obj_to_dict(a))
            ar.append([i.year, i.month, False, atcls])
        list_descr = ""

    elif int(offsets[0]) >= 2012 and len(offsets) == 1:
        for i in models.list_archives(year=int(offsets[0])):
            atcls = []
            for a in models.list_articles(items_per_result=3, archive_obj=i):
                atcls.append(models.article_obj_to_dict(a))
            ar.append([i.year, i.month, False, atcls])
        list_descr = "%s年的归档" % (offsets[0],)

    elif int(offsets[0]) >= 2012 and 1 <= int(offsets[1]) <= 12:
        i = models.archive.objects.get(
            year=int(offsets[0]), month=int(offsets[1]))
        atcls = []
        for a in models.list_articles(items_per_result=999, archive_obj=i):
            atcls.append(models.article_obj_to_dict(a))
        ar.append([i.year, i.month, True, atcls])
        list_descr = "%s年%s月的归档" % (offsets[0], offsets[1])
    else:
        return render_to_response("404.html", status=404)

    dic = {
        "lists": ar,
        "list_type": 0,
        "list_description": list_descr,
        "pagi": False,
    }
    dic.update(common_view(navbar_active=2))  # common view
    return render_to_response("list.html", dic)


#=======================================================
def tag(request, *offsets):
    '''
show the tag list
arguments:
    request:
    offsets(optional):(tuple)tag name and pagination specified,both of them are optional(==it can be empty)
'''
    if len(offsets) == 1:  # if not specified,turn to the first page
        offsets = [offsets[0], "1"]
    ar = []

    if offsets == ("", "") or offsets == ("",) or offsets == ():
        all_tags = list(models.tag.objects.all())
        # items are tagname:articles_list
        tags_atcls = models.list_tags_with_articles()
        for i in tags_atcls:
            ar.append([i, None, False, tags_atcls[i]])
        dic = {
            "lists": ar,
            "list_type": 2,
            "list_description": "所有标签",
            "pagi": False,
        }

    elif len(offsets) == 2 and 0 < int(offsets[1]) < 999:
        try:
            article_objs = models.tag.objects.get(
                name=offsets[0]).articles.order_by("-datetime")
            ar = []
            for i in article_objs:
                ar.append(models.article_obj_to_dict(i))
        except:
            return render_to_response("404.html", status=404)
        if len(ar) % 16 != 0:
            pages = len(ar) // 16 + 1
        else:
            pages = len(ar) // 16
        page = int(offsets[1])
        r_start = 16 * (page - 1)
        ar = ar[r_start:r_start + 16]
        ar = [["", None, True, ar]]  # pack the list
        dic = {
            "lists": ar,
            "list_type": 2,
            "list_description": "包含标签“%s”的博文" % offsets[0],
            "pagi": True,

            # pagination
            "url_template": "/tag/" + offsets[0] + "/%s",
            "pages": pages,
            "current": int(offsets[1]),
        }

    dic.update(common_view(navbar_active=-1))  # common view
    return render_to_response("list.html", dic)


#=======================================================
def article(request, offset):
    '''
show an article
arguments:
    offset:the id to the article
'''
    try:
        a_id = int(offset)
        atcle = models.article.objects.get(id=a_id)
        if atcle.shown == False:
            raise Exception
        article_dict = models.article_obj_to_dict(atcle)
        atcle.access_frequence += 1
        atcle.save()
    except:
        return render_to_response("404.html", status=404)
    dic = {
        "article": article_dict,
        "atcle_id": a_id,
        "comment_brand": "评论 %s" % (article_dict["title"],),
    }
    dic.update(common_view(navbar_active=-1))  # common view
    return render_to_response("article.html", dic, request=request)


#=======================================================
def search_article(request, offset):
    '''
search the title and content of articles.
argument:
    offset:something to search for
'''
    if offset == "" or offset == None:
        return HttpResponseRedirect("/")
    dic = {
        "lists": [[None, None, False, []]],
        "list_description": "搜索包含“%s”的结果" % offset,
        "list_type": 3,
        "pagi": False
    }
    for i in models.search_for_article(offset):
        dic["lists"][0][3].append(models.article_obj_to_dict(i))
    dic.update(common_view(navbar_active=-1))  # common view
    return render_to_response("list.html", dic)


#=======================================================
def category(request, *offsets):
    '''
show categories
argument:
    offsets:(tuple)the id to the category and the pagination,both are optional
'''
    if len(offsets) == 1:  # if the id is given but the pagination not,show the first page by default
        offsets = [offsets[0], "1"]
    ar = []
    if offsets == ("", "") or offsets == ("",) or offsets == ():
        c = models.category.objects.annotate(article_count=Count("articles")).order_by(
            "-article_count")  # sort by the count of articles combined to the category
        for i in c:
            ctgry = [i.name, i.id, False, []]
            for atcls in models.list_articles(category_id=i.id, items_per_result=3, page=1):
                ctgry[3].append(models.article_obj_to_dict(atcls))
            ar.append(ctgry)
        dic = {
            "lists": ar,
            "list_type": 1,
            "list_description": "",
            "pagi": False,
        }

    elif len(offsets) == 2:
        c = models.category.objects.get(id=offsets[0])
        ar = [[c.name, c.id, True, []]]
        for i in models.list_articles(category_id=int(offsets[0]), items_per_result=16, page=int(offsets[1])):
            ar[0][3].append(models.article_obj_to_dict(i))
        if c.articles.count() % 16 != 0:
            pages = c.articles.count() // 16 + 1
        else:
            pages = c.articles.count() // 16
        dic = {
            "lists": ar,
            "list_type": 1,
            "list_description": "分类为“%s”下的博文" % c.name,
            "pagi": True,

            # pagination
            "url_template": "/category/" + offsets[0] + "/%s",
            "pages": pages,
            "current": int(offsets[1]),
        }

    dic.update(common_view(navbar_active=1))  # common view
    return render_to_response("list.html", dic)


#=======================================================
def commentbox(request, offset="1"):
    '''
show comment box(used for common message leaving)
arguments:
    request:pagination
'''
    if offset == "":
        offset = "1"
    try:
        page = int(offset)
    except:
        return render_to_response("404.html", status=404)
    cmt_list = models.list_comments(True, comment_per_result=12, page=page)
    cmts = len(models.comment.objects.filter(refered_article=None))
    if cmts % 12 == 0:
        pages = cmts // 12
    else:
        pages = cmts // 12 + 1
    dic = {
        "csrf_token": None,
        "comment_brand": "给博主留言",
        "atcle_id": None,

        "comment_list": cmt_list,
        "pagi": True,

        # pagination
        "url_template": "/commentbox/%s",
        "pages": pages,
        "current": page,
    }
    dic.update(common_view(navbar_active=3))  # common view
    return render_to_response("commentbox.html", dic, request=request)


#=======================================================
def comment_list(request, offset):
    '''
show the comment list to some article(ajax)
argument:
    offset:the id to the article(required)
return:
    note this view function only return the html of the comment list
'''
    try:
        atcle_id = int(offset)
    except:
        return render_to_response("404.html", status=404)
    cmt_list = models.list_comments(
        isolated=False, article_id=atcle_id, comment_per_result=999)
    dic = {
        "comment_list": cmt_list,
        "pagi": False,
    }
    return render_to_response("comment_list.html", dic)


#=======================================================
def post_comment(request):
    '''
post comment through ajax
request.method should be POST
POST:
    nickname
    email
    website
    message
    refered_article
    refered_comment
return:
    return empty with status code;succeeded with 200,failed with 400
'''
    utcnow = datetime.utcnow().replace(
        tzinfo=utc)  # utc standard time for db storage
    if request.method != "POST":
        return HttpResponse("", status=400)
    cmt = models.comment(read=False, shown=False, datetime=utcnow)
    # verify the form
    if request.POST["nickname"].strip() == "" or request.POST["message"].strip() == "":
        return render_to_response("", status=400)
    try:
        cmt.nickname = cgi.escape(request.POST["nickname"])
        cmt.message = cgi.escape(request.POST["message"])
        cmt.email = cgi.escape(request.POST["email"])
        cmt.website = cgi.escape(request.POST["website"])
        cmt.ip_address = str(request.META["REMOTE_ADDR"])
        cmt.shown = not settings.comment_verification
    except:
        return HttpResponse("", status=400)
    if len(cmt.nickname) > 19 or len(cmt.email) > 39 or len(cmt.website) > 59 or len(cmt.message) > 9999:
        return HttpResponse("", status=400)

    # write
    try:
        ra_id = int(request.POST["refered_article"])
        cmt.refered_article = models.article.objects.get(id=ra_id)
    except:
        pass
    try:
        rc_id = int(request.POST["refered_comment"])
        cmt.refered_comment = models.comment.objects.get(id=rc_id)
    except:
        pass
    cmt.save()
    try:
        ra = models.article.objects.get(id=ra_id)
        ra.comments.add(cmt)
        ra.save()
    except:
        pass
    return HttpResponse("")


#=======================================================
def about(request):
    '''
show about page
'''
    dic = {
        "about_img": settings.master_photo,
        "about_content": settings.self_intro,
    }
    dic.update(common_view(navbar_active=4))  # common view
    return render_to_response("about.html", dic)


#========================================================
def upload_image(request):
    '''
upload picture through ajax(method:POST)
'''
    if request.user.is_authenticated == False or request.method != "POST":
        return HttpResponse("", status=403)
    # utc standard time for db storage
    utcnow = datetime.utcnow().replace(tzinfo=utc)
    try:
        img = request.FILES["imgFile"].read()
        img_name = request.FILES["imgFile"].name
        new_imgname = utcnow.strftime("%Y%m%d%H%M%S-") + img_name
        f = open(settings.uploaded_image_dir + new_imgname, "wb")
        f.write(img)
        f.close()
        result = json.dumps({
            "error": 0,
            "url": settings.uploaded_image_url + new_imgname,
        })
    except:
        result = json.dumps({
            "error": 1,
            "message": "%s：传输、储存错误" % img_name,
        })
    return HttpResponse(result)
