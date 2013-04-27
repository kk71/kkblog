# -*- coding: utf-8 -*-
'''
kkblog models and methods


author:kK(fkfkbill@gmail.com)
'''



# python import
import cgi#for xml escaping

#django import
from django.db import models
from django.db.models import Count
from django.db.models import CharField,TextField,ManyToManyField,OneToOneField,ForeignKey,PositiveSmallIntegerField,EmailField,URLField,BooleanField,DateTimeField,ImageField,IPAddressField
'''if wish a IntegerField,DecimalField,FloatField;DateField,TimeField,DateTimeField to receive an empty value,
null=True and blank=True must be set at the same time.'''

#project import
import settings

#for datetime
from django.utils.timezone import template_localtime
from datetime import datetime
from django.utils.timezone import utc



#====================================================================
class comment(models.Model):
	shown=BooleanField(default=False,verbose_name="显示")
	read=BooleanField(default=False,verbose_name="已读")
	ip_address=IPAddressField(verbose_name="IP地址")
	
	nickname=CharField(max_length=39,verbose_name="昵称")
	website=URLField(blank=True,null=True,verbose_name="网站")
	email=EmailField(blank=True,null=True,verbose_name="Email")
	datetime=DateTimeField(verbose_name="时间")
	message=TextField(max_length=9999,verbose_name="留言")
	
	refered_comment=ForeignKey("comment",blank=True,null=True,verbose_name="所引用的留言")
	refered_article=ForeignKey("article",blank=True,null=True,verbose_name="所引用的博文")
	
	def __unicode__(self):
		return '''
shown:%s,
datetime:%s,
nickname:%s,
refered_comment:%s,
'''%(self.shown,self.datetime,self.nickname,self.refered_comment)



#====================================================================
class tag(models.Model):
	name=CharField(primary_key=True,max_length=19,unique=True,verbose_name="标签名")
	articles=ManyToManyField("article")

	def __unicode__(self):
		return '%s'%(self.name,)



#====================================================================
class article(models.Model):
	title=CharField(blank=False,null=False,max_length=29,verbose_name="标题")
	content=TextField(blank=False,verbose_name="正文")
	thumbnail_plain=TextField(blank=False,verbose_name="纯文本缩略")
	thumbnail_length=PositiveSmallIntegerField(default=399,verbose_name="首页显示长度")
	datetime=DateTimeField(blank=False,verbose_name="时间")
	tags=ManyToManyField("tag",blank=True,null=True,verbose_name="标签")
	category_key=ForeignKey("category",blank=False,verbose_name="分类")
	shown=BooleanField(blank=False,verbose_name="显示",default=True)
	comments=ManyToManyField("comment",blank=True)
	access_frequence=PositiveSmallIntegerField(default=0)

	def __unicode__(self):
		return '''
shown:%s,
title:%s,
category_name:%s,
'''%(self.shown,self.title,self.category_key)



#====================================================================
class category(models.Model):
	name=CharField(max_length=19,unique=True,verbose_name="分类")
	articles=ManyToManyField("article")

	def __unicode__(self):
		return '%s'%(self.name,)



#====================================================================
class archive(models.Model):
	year=PositiveSmallIntegerField(verbose_name="年份")
	month=PositiveSmallIntegerField(verbose_name="月份")
	articles=ManyToManyField("article")

	def __unicode__(self):
		return '''
year:%s,
month:%s,
'''%(self.year,self.month)



#====================================================================
def list_tags():
	'''
罗列所有标签(默认按照从大到小)。
return:
	序列，标签。
'''
	t=[]
	
	for i in tag.objects.annotate(article_count=Count("articles")).order_by("-article_count"):
		t.append(i)
	return t



#====================================================================
def list_tags_with_articles(articles_to_list=3):
	'''
罗列所有标签，并罗列标签下的文章（篇数可选）
argument:
	articles_to_list:返回的文章数目
return:
	dict()
	标签名:文章列表（其中的文章是dict）
'''
	dic={}
	for t in tag.objects.all():
		dic.update({t.name:[]})
		count=0
		for atcls in t.articles.order_by("-datetime"):
			dic[t.name].append(article_obj_to_dict(atcls))
			count+=1
			if count>=articles_to_list:break
	return dic


#====================================================================
def list_archives(year=None,month=None):
	'''
罗列所有归档(默认按照从新到旧)。
argument:
	注意，month仅当year指定后才能使用
return:
	序列。
'''
	ar=[]
	for i in archive.objects.order_by("-year","-month"):
		if year==None and month==None:
			ar.append(i)
		elif year!=None and month==None:
			if i.year==year:ar.append(i)
		elif year!=None and month!=None:
			if i.year==year and i.month==month:ar.append(i)
	return ar


#====================================================================
def clear_empty_tags():
	'''
清空无博文关联的空标签。
'''
	for t in tag.objects.all():
		if len(t.articles.all())==0:
			t.delete()


#====================================================================
def update_tag(article_id,tag_str):
		'''
更新标签与当前文章的关系。
此操作之前，article对象必须已存在于数据库中
标签是区分大小写的，前导后续空格自动忽略
arguments:
	tag_str:由逗号分开的标签字符串
return:
	boolean
'''
		new_tags_list=[]
		for i in tag_str.split(","):
			i=i.strip()
			if i=="" or i==",":continue
			if i not in new_tags_list:new_tags_list.append(i)
		try:
			a=article.objects.get(id=article_id)
		except:
			return False
		current_tags_obj_list=a.tags.all()
		for i in current_tags_obj_list:
			if i.name in new_tags_list:
				new_tags_list.remove(i.name)
			else:
				i.delete()
		for i in new_tags_list:
			try:
				t=tag.objects.get(name=i)
			except:
				t=tag(name=i)
				t.save()
			t.articles.add(a)
			t.save()
			a.tags.add(t)
			a.save()
		return True


#====================================================================
def update_archive(article_id):
	'''
在归档中更新文章。
argument:
	article_id:已存的博文id
return:
	boolean
'''
	try:
		a=article.objects.get(id=article_id)
	except:
		return False
	try:
		ar=archive.objects.get(year=a.datetime.year,month=a.datetime.month)
	except:
		ar=archive(year=a.datetime.year,month=a.datetime.month)
		ar.save()
	ar.articles.add(a)
	ar.save()
	return True
		


#====================================================================
def list_articles(items_per_result=9,
					page=1,
					sort_by_frequence=False,
					category_id=None,
					archive_obj=None,
					):
	'''
罗列博文（排除shown==False的博文）
argument:
	sort_by_frequence:按照点击次数排序（默认False），否则就按日期排序
	category_id:仅选取某个分类中的博文（None则为所有博文）
	items_per_result:每次结果返回的博文数，默认9
	page:哪一页。
	archive_obj:归档对象，用于筛选出某个时段的文章
return:
	由article obj组成的序列
	False:errors
'''
	if category_id==None:
		at=article.objects
	else:
		ctgry=category.objects.get(id=category_id)
		at=ctgry.articles
	if sort_by_frequence==False:
		atcls=at.filter(shown=True).order_by("-datetime")
	else:
		atcls=at.filter(shown=True).order_by("-access_frequence")
	atcls=list(atcls)
	if archive_obj!=None:
		for i in atcls:
			if i not in archive_obj.articles.all():
				atcls.remove(i)
	
	r_start=items_per_result*(page-1)
	return atcls[r_start:r_start+items_per_result]



#====================================================================
def search_for_article(text):
	'''
在标题和内容中搜索博文。
'''
	result=[]
	labels=[]
	for i in text.split(" "):
		if i.strip()!="":
			labels.append(i)
	for i in article.objects.all():
		for label in labels:
			if label in i.title or label in i.thumbnail_plain:
				result.append(i)
				break
	return result
	


#====================================================================
def article_obj_to_dict(article_obj):
	'''
article_obj转换为字典形式，方便渲染成模板
id若无，则为None
'''
	dic=dict(
			id=article_obj.id,
			title=article_obj.title,
			content=article_obj.content,
			thumbnail_length=article_obj.thumbnail_length,
			thumbnail_plain=article_obj.content[:article_obj.thumbnail_length],
			datetime=template_localtime(article_obj.datetime),
			tags=[],
			category_key={"id":None,"name":None},
			shown=article_obj.shown,
			comments=[],
			access_frequence=article_obj.access_frequence
	)
	try:
		for i in article_obj.tags.all():
			dic["tags"].append(i.name)
	except:
		pass
	try:
		c=article_obj.category_key
		dic["category_key"]={
				"id":c.id,
				"name":c.name,
		}
	except:
		pass
	return dic



#====================================================================
def comment_obj_to_dict(comment_obj):
	'''
comment_obj转换为字典形式，方便渲染成模板
若无，则为None
'''
	dic={
			"id":comment_obj.id,
			"nickname":comment_obj.nickname,
			"website":comment_obj.website,
			"email":comment_obj.email,
			"datetime":template_localtime(comment_obj.datetime),
			"message":comment_obj.message,
			"shown":comment_obj.shown,
			"ip_address":comment_obj.ip_address,
			"refered_comment":None,
			"refered_article":None,
	}
	if comment_obj.refered_comment!=None and comment_obj.refered_comment.shown==True:
		i=comment_obj.refered_comment
		dic["refered_comment"]={
				"nickname":i.nickname,
				"website":i.website,
				"email":i.email,
				"ip_address":i.ip_address,
				"datetime":template_localtime(i.datetime),
				"message":i.message,	
		}
	if comment_obj.refered_article!=None and comment_obj.refered_article.shown==True:
		dic["refered_article"]=article_obj_to_dict(comment_obj.refered_article)
	return dic



#====================================================================
def list_comments(isolated,
					article_id=None,
					include_hide=False,
					to_dict=True,
					comment_per_result=9,
					page=1):
	'''
列出评论
argument:
	isolated:是独立留言还是对某文章的评论
	article_id:当isolated=True时则此选项不需要，为对应博文的id
	to_dict:将queryset转换为list，将每条评论转换为dict
	include_hide:包含隐藏（未通过审核）的评论？
	comment_per_result:每次返回的条数
	page:返回第几页
return:
	返回一个列表包含每条评论
	注意，关联的评论仅包含最近的一条（当to_dict==True的时候才包含）
	关联的博文仅包含其id
'''
	if isolated==True:
		cmt=comment.objects.filter(refered_article=None).order_by("-datetime")
	else:
		atcle=article.objects.get(id=article_id)
		cmt=atcle.comments.order_by("-datetime")
	if include_hide==False:
		cmt=cmt.filter(shown=True)

	if len(cmt)%comment_per_result==0:
		pages=len(cmt)//comment_per_result
	else:
		pages=len(cmt)//comment_per_result+1
	n=(page-1)*comment_per_result
	result=cmt[n:n+comment_per_result]

	if to_dict==True:
		result_dict=[]
		for i in result:
			result_dict.append(comment_obj_to_dict(i))
		result=result_dict
	return result


#====================================================================
def reply_comment(message,refered_comment_obj):
	'''
在数据库中回复一条评论
'''
	utcnow=datetime.utcnow().replace(tzinfo=utc)#utc standard time for db storage
	r=comment(shown=True,read=True,nickname=settings.author_name,email=settings.email,website=settings.domain_name,datetime=utcnow,message=message,refered_comment=refered_comment_obj)
	try:
		r.refered_article=refered_comment_obj.refered_article
	except:
		pass
	r.save()
