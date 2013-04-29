# -*- coding: utf-8 -*-


from glob import glob
from random import randint
import settings

'''
#取得随机图片url
icon_img_dir=settings.STATICFILES_DIRS[0]+"icon_img/"
if icon_img_dir[-1:]!="/":
	icon_img_dir+="/"
if settings.STATIC_URL[-1:]!="/":
	settings.STATIC_URL+="/"
imgs=glob(icon_img_dir+"*.png")
imgs.extend(glob(icon_img_dir+"*.jpg"))
'''


#tag colors list
color_styles=["success","warning","important","info","default","inverse"]



def random_tag_color():
	'''
随机返回一个标签颜色的class名
'''
	return color_styles[randint(0,len(color_styles)-1)]



def article_stable_url(id,bgmusic=True):
	'''
通过一个已知的博文id来获得其固定url
'''
	if bgmusic==True:
		return settings.domain_name+"/article/%s"%(id,)
	else:
		return settings.domain_name+"/article/%s?bgmusic=none"%(id,)



def article_stable_comment(article_id):
	return article_stable_url(article_id)+"#comment"



def category_url(category_id,pagination=None):
	if pagination==None:
		return settings.domain_name+"/category/%s"%(str(category_id),)
	else:
		return settings.domain_name+"/category/%s/%s"%(str(category_id),str(pagination))



def tag_url(tag_name,pagination=None):
	if pagination==None:
		return settings.domain_name+"/tag/%s"%(str(tag_name),)
	else:
		return settings.domain_name+"/tag/%s/%s"%(str(tag_name),str(pagination))



def archive_url(year,month=None):
	if month==None:
		return settings.domain_name+"/archive/%s"%(str(year,))
	else:
		return settings.domain_name+"/archive/%s/%s"%(str(year),str(month))

	

def list_to_tag(lists):
	'''
将一个列表转换成一个以逗号分开的标签列
'''
	s=""
	for i in lists:
		s+=i+","
	return s[:-1]
