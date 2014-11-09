from django.http import JsonResponse,HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST
import html
from . import models

try:
    import simplejson as json
except:
    import json


@require_GET
def musicList(request):
    '''
    get music list and background music playing settings
    :param request:
    :return:
    '''
    # TODO: write for music list
    return JsonResponse({})


@require_GET
def commentList(request):
    '''
    拉取某博文的评论列表
    querystring:
        articleId：博文id
    '''
    try:
        articleId=request.GET["articleId"]
    except:
        return HttpResponseBadRequest()
    try:
        tryIfArticleExist=models.article.objects.get(id=articleId)
    except:
        return HttpResponseNotFound()
    comments={"comments":[]}
    for i in models.comment.objects.list(articleId).page(1).object_list:
        if i.shown:comments["comments"].append(i.toDict())
    return JsonResponse(comments)


@require_POST
def postComment(request):
    '''
    write comment
    :param request:
    :return:
    '''
    config=models.config.objects.get(enabled=True)
    formData=json.loads(request.body)

    try:
        nickname=formData["nickname"]
        message=formData["message"]
        article=models.article.objects.get(id=int(formData["articleId"]))
    except:
        return JsonResponse({"error":1},status=400)
    try:
        email=formData["email"]
    except:
        email=""
    try:
        website=formData["website"]
    except:
        website=""
    try:
        replyCommentId=int(formData["replyCommentId"])
        parent=models.comment.objects.get(id=replyCommentId)
    except:
        parent=None
    newComment=models.comment(
        nickname=html.escape(nickname),
        email=html.escape(email),
        website=html.escape(website),
        message=html.escape(message),
        parent=parent,
        article=article,
        ipAddress=request.META["REMOTE_ADDR"],
        shown=not config.commentVerify
    )
    newComment.save()
    return JsonResponse({"error":0})
