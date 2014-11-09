from django.db.models import Manager
from django.db.models import Count
from django.core.paginator import Paginator


class commentManager(Manager):
    def list(self,
             articleId,
             includeHide=False,
             commentPerResult=999,
             orphans=0):
        '''
        列出评论
        argument:
            articleId:为对应博文的id
            includeHide:包含隐藏（未通过审核）的评论
            commentPerResult:每次返回的条数
            orphans:paginator的孤立项。
        return:
        返回一个分页对象
        '''
        cmt = self.filter(article__id=articleId).order_by("-datetime")
        if not includeHide:
            cmt = cmt.filter(shown=True)
        return Paginator(
            object_list=cmt.all(),
            per_page=commentPerResult,
            orphans=orphans
        )


class tagManager(Manager):
    def list(self):
        '''罗列所有标签(默认按照从大到小)'''
        return [i for i in self.annotate(
            article_count=Count("articles")
        ).order_by("-article_count")]

    def listWithArticles(self,articlesToList=3):
        '''
        罗列所有标签，并罗列标签下的文章（篇数可选默认3）
        argument:
            articles_to_list:返回的文章数目
        return:
        标签名:文章列表（其中的文章是list）
        '''
        dic = []
        for t in self.list():
            dic.append((t.name,
                [the_article for the_article in t.articles.order_by("-datetime")[:articlesToList]]
            ))
        return dic


class articleManager(Manager):
    def list(self,
             itemsPerResult=9,
             orphans=0,
             sortByFrequency=False,
             categoryId=None,
             archiveObj=None,
             stickyIncluded=False):
        '''
        罗列博文（排除shown==False的博文）
        argument:
            itemsPerResult:每次结果返回的博文数，默认9
            orphans：最后一页允许的最少个数，默认为0
            sortByFrequency:按照点击次数排序（默认False），否则就按日期排序
            categoryId:仅选取某个分类中的博文（None则为所有博文）
            archiveObj:归档对象，用于筛选出某个时段的文章
            stickyIncluded:包含置顶的文章（默认不包含）
        return:
            Paginator object
        '''
        if categoryId is None:
            at = self
        else:
            at = self.filter(category_id=categoryId)
        if sortByFrequency == False:
            atcls = at.filter(shown=True).order_by("-createDatetime")
        else:
            atcls = at.filter(shown=True).order_by("-accessFrequency")
        if not stickyIncluded:
            atcls = atcls.filter(sticky=False)
        if archiveObj is not None:
            atcls=atcls.filter(archive=archiveObj)
        return Paginator(atcls,itemsPerResult, orphans)

    def listSticky(self):
        '''罗列置顶的博文'''
        return self.filter(sticky=True,shown=True).order_by("-createDatetime")

    def search(self,text):
        '''在标题和内容中搜索博文。'''
        result = []
        labels = []
        for i in text.split(" "):
            if i.strip() != "":
                labels.append(i)
        for i in self.all():
            for label in labels:
                if label in i.title or label in i.content:
                    result.append(i)
                    break
        return result


class archiveManager(Manager):
    def list(self,year=None, month=None):
        '''
        罗列所有归档(默认按照从新到旧)。
        argument:
            注意，month仅当year指定后才能使用
        return:
            list
        '''
        ar = []
        for i in self.order_by("-year", "-month"):
            if year == None and month == None:
                ar.append(i)
            elif year != None and month == None:
                if i.year == year:
                    ar.append(i)
            elif year != None and month != None:
                if i.year == year and i.month == month:
                    ar.append(i)
        return ar

    def getYears(self):
        '''return years range'''
        years=set()
        for i in self.all():
            years.add(i.year)
        years=list(years)
        years.reverse() # 取年份由近及远
        return years
