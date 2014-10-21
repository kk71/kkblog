from django.db.models import Manager
from django.db.models import Count


class music_list_manager(Manager):
    def list(self):
        '''
        list all enabled music
        '''
        return


class comment_manager(Manager):
    def list(self,
             isolated,
             article_id=None,
             include_hide=False,
             comment_per_result=9,
             page=1
    ):
        '''
        列出评论
        argument:
            isolated:是独立留言还是对某文章的评论
            article_id:当isolated=True时则此选项不需要，为对应博文的id
            include_hide:包含隐藏（未通过审核）的评论？
            comment_per_result:每次返回的条数
            page:返回第几页
        return:
        返回一个列表包含每条评论
        关联的博文仅包含其id
        '''
        if isolated == True:
            cmt = self.objects.filter(
                refered_article=None).order_by("-datetime")
        else:
            atcle = self.objects.get(id=article_id)
            cmt = atcle.comments.order_by("-datetime")
        if include_hide == False:
            cmt = cmt.filter(shown=True)

        if len(cmt) % comment_per_result == 0:
            pages = len(cmt) // comment_per_result
        else:
            pages = len(cmt) // comment_per_result + 1
        n = (page - 1) * comment_per_result
        result = cmt[n:n + comment_per_result]

        return result


class tag_manager(Manager):
    def list(self):
        '''
        罗列所有标签(默认按照从大到小)。
        '''
        return [i for i in self.objects.annotate(
            article_count=Count("articles")
        ).order_by("-article_count")]

    def list_with_articles(self,articles_to_list=3):
        '''
        罗列所有标签，并罗列标签下的文章（篇数可选默认3）
        argument:
            articles_to_list:返回的文章数目
        return:
        标签名:文章列表（其中的文章是list）
        '''
        dic = []
        for t in self.objects.list():
            dic.append((t.name,
                [the_article for the_article in t.articles.order_by("-datetime")[:articles_to_list]]
            ))
        return dic


class article_manager(Manager):
    def list(self,
             items_per_result=9,
             page=1,
             sort_by_frequency=False,
             category_id=None,
             archive_obj=None,
             ):
        '''
        罗列博文（排除shown==False的博文）
        argument:
            sort_by_frequency:按照点击次数排序（默认False），否则就按日期排序
            category_id:仅选取某个分类中的博文（None则为所有博文）
            items_per_result:每次结果返回的博文数，默认9
            page:哪一页。
            archive_obj:归档对象，用于筛选出某个时段的文章
        return:
            由article obj组成的序列
            False:errors
        '''
        if category_id == None:
            at = self.objects
        else:
            ctgry = self.objects.get(id=category_id)
            at = ctgry.articles
        if sort_by_frequency == False:
            atcls = at.filter(shown=True).order_by("-datetime")
        else:
            atcls = at.filter(shown=True).order_by("-access_frequency")
        atcls = list(atcls)
        if archive_obj != None:
            for i in atcls:
                if i not in archive_obj.articles.all():
                    atcls.remove(i)

        r_start = items_per_result * (page - 1)
        return atcls[r_start:r_start + items_per_result]

    def search(self,text):
        '''
        在标题和内容中搜索博文。
        '''
        result = []
        labels = []
        for i in text.split(" "):
            if i.strip() != "":
                labels.append(i)
        for i in self.objects.all():
            for label in labels:
                if label in i.title or label in i.thumbnail_plain:
                    result.append(i)
                    break
        return result


class archive_manager(Manager):
    def list(self,year=None, month=None):
        '''
        罗列所有归档(默认按照从新到旧)。
        argument:
            注意，month仅当year指定后才能使用
        return:
            list
        '''
        ar = []
        for i in self.objects.order_by("-year", "-month"):
            if year == None and month == None:
                ar.append(i)
            elif year != None and month == None:
                if i.year == year:
                    ar.append(i)
            elif year != None and month != None:
                if i.year == year and i.month == month:
                    ar.append(i)
        return ar
