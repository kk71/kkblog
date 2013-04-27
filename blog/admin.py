# -*- coding: utf-8 -*-
'''
kkblog admin views


author:kK(fkfkbill@gmail.com)
'''


#python import
import cgi

#django import
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django import forms
from django.contrib import admin

#third-part import
from djangomako import render_to_response,render_to_string

#project import
from blog.models import *
from simple_smtp import simple_smtp_send

#for datetime
from django.utils.timezone import template_localtime
from datetime import datetime
from django.utils.timezone import utc



#====================================================================
def AdminError(info):
	'''
return admin error info with status code 404
'''
	return HttpResponse(info,status=404)


#====================================================================
class commentAdmin(admin.ModelAdmin):
	list_display=("nickname","message","datetime","email","website","ip_address","shown","read")
	ordering=("-datetime",)
	list_filter=("read","shown")
	readonly_fields=("read",)


	#================================================================
	#manually add comment obj from admin management is not allowed
	def add_view(self, request, form_url="",extra_context=None):
		return HttpResponseRedirect("/admin/blog/comment/")
	
	def save_model(self,request,obj,form,change):
		pass
	
	
	#================================================================
	def change_view(self,request,form_url="",extra_context=None):
		'''
	redesigned admin page: change comment(used for reply and send email)
	'''
		#reply==============================
		if request.method=="POST":
			try:
				cmt_id=int(form_url)
				cmt_obj=comment.objects.get(id=cmt_id)
				cmt_dic=comment_obj_to_dict(cmt_obj)
			except:
				return AdminError("找不到该评论。")
			#wheather just simply change the display state
			try:
				if request.POST["mark_read"]=="隐藏":
					cmt_obj.shown=False
					cmt_obj.save()
					return HttpResponseRedirect("/admin/blog/comment/%s/"%cmt_id)
				elif request.POST["mark_read"]=="显示":
					cmt_obj.shown=True
					cmt_obj.save()
					return HttpResponseRedirect("/admin/blog/comment/%s/"%cmt_id)
			except:
				pass

			#otherwise,reply the comment and send an email
			reply_comment(request.POST["message"],cmt_obj)
			dic={
					"blog_name":settings.brand,
					"blog_url":settings.domain_name,
					"blog_owner":settings.author_name,
					"reply_content":request.POST["message"],
					"reply_refered":cmt_dic["message"],
					"datetime":str(cmt_dic["datetime"].date())+" "+str(cmt_dic["datetime"].time()),
			}
			#render the tmpl for email
			send_status=simple_smtp_send(settings.email,
						settings.email_p,
						settings.email_server,
						[request.POST["mail_to"],],
						"评论回复",
						render_to_string("reply_email",dic))
			if send_status==2:
				return AdminError("登录邮件服务器时出错。")
			elif send_status==3:
				return AdminError("发送邮件时出错。")
			return HttpResponseRedirect("/admin/blog/comment/")
		
		#show the reply page================================
		else:
			try:
				cmt_id=int(form_url)
				cmt_obj=comment.objects.get(id=cmt_id)
				cmt_dic=comment_obj_to_dict(cmt_obj)
			except:
				return AdminError("找不到该评论。")
			if cmt_obj.read==False:
				cmt_obj.read=True
				cmt_obj.save()
			dic=dict(
					csrf_token="",
					title="回复评论",
					cmt=cmt_dic,
					mail_from=settings.email,
					blog_owner_name=settings.author_name,
			)
			return render_to_response("redesigned_admin/reply_comment.html",dic,request=request)




#====================================================================
class articleAdmin(admin.ModelAdmin):
	list_display=("title","category_key","datetime","thumbnail_plain","thumbnail_length","shown")
	ordering=("-datetime",)
	list_filter=("shown",)


	#================================================================
	def add_view(self,request,form_url="",extra_context=None):
		'''
	redesigned write new article page
	'''
		utcnow=datetime.utcnow().replace(tzinfo=utc)#utc standard time for db storage
		#received a new article========================================
		if request.method=="POST":
			#verify the post form
			try:
				c=category.objects.get(id=int(request.POST["category_key"]))
			except:
					return AdminError("该分类不存在。")
			if request.POST["title"].strip()=="":
				return AdminError("标题不可为空（或全空格）。")
			if request.POST["content"].strip()=="" or request.POST["thumbnail_plain"].strip()=="":
				return AdminError("内容不可为空（或全空格）。")
			thumbnail_length=int(request.POST["thumbnail_length"].strip())
			if thumbnail_length<=0 or thumbnail_length>99999:
				return AdminError("缩略长度错误。")
			
			#try to write to db
			new_article=article(
				title=request.POST["title"],
				content=request.POST["content"],
				thumbnail_length=thumbnail_length,
				thumbnail_plain=request.POST["thumbnail_plain"],
				datetime=utcnow,
				category_key=c,
				shown=False
			)
			try:
				if request.POST["shown"]=="on":
					new_article.shown=True
			except:
				pass
			new_article.save()
			update_tag(new_article.id,request.POST["tags"])
			update_archive(new_article.id)
			c.articles.add(new_article)
			return HttpResponseRedirect("/admin/blog/article/")

		#represent a writing page===================================
		elif request.method=="GET":
			dic={
				"title":"写博文",
				"categories":category.objects.all(),
				"article":article_obj_to_dict(article()),
			}
			return render_to_response(template_name="redesigned_admin/edit_article.html",dictionary=dic,request=request)
	
	
	#================================================================
	def change_view(self,request,form_url="",extra_context=None):
		'''
	redesigned change article page
	'''
		#get an existed article
		if request.method=="POST":
			#verify the post form 
			try:
				c=category.objects.get(id=int(request.POST["category_key"]))
			except:
					return AdminError("该分类不存在。")
			try:
				a=article.objects.get(id=int(form_url))
				old_version=a#the old version is for update the category
			except:
					return AdminError("该文章不存在。")
			if request.POST["title"].strip()=="":
				return AdminError("标题不可为空（或全空格）。")
			if request.POST["content"].strip()=="" or request.POST["thumbnail_plain"].strip()=="":
				return AdminError("内容不可为空（或全空格）。")
			thumbnail_length=int(request.POST["thumbnail_length"].strip())
			if thumbnail_length<=0 or thumbnail_length>999999:
				return AdminError("缩略长度错误。")
			
			#try to write to db
			a.title=request.POST["title"]
			a.content=request.POST["content"]
			a.thumbnail_length=thumbnail_length
			a.thumbnail_plain=request.POST["thumbnail_plain"]
			try:
				if request.POST["shown"]=="on":
					a.shown=True
			except:
				a.shown=False
			update_tag(int(form_url),request.POST["tags"])
			#更新分类
			if old_version.category_key.id!=int(request.POST["category_key"]):
				old_version.category_key.articles.remove(old_version)
				c.articles.add(a)
				c.save()
				a.category_key=c
			a.save()
			return HttpResponseRedirect("/admin/blog/article/")

		#represent a writing page
		elif request.method=="GET":
			try:
				atcl=article.objects.get(id=int(form_url))
			except:
				return render_to_response(template_name="redesigned_admin/error.html",
						dictionary={
							"error_info":"该文章不存在。",
							"title":"错误",
						},status=404)
			dic={
				"title":"修改博文",
				"categories":category.objects.all(),
				"article":article_obj_to_dict(atcl),
			}
			return render_to_response(template_name="redesigned_admin/edit_article.html",dictionary=dic,request=request)
	

	def delete_model(self, request, obj):
		obj.delete()
		clear_empty_tags()


#====================================================================
class categoryAdmin(admin.ModelAdmin):
	list_display=("name",)
	exclude=("articles",)





#register to the admin
admin.site.register(comment,commentAdmin)
admin.site.register(article,articleAdmin)
admin.site.register(category,categoryAdmin)
