# -*- coding: utf-8 -*-

from django import forms
import settings
from djangomako import render_to_string
import simplejson as json


class kindeditor():
	css=r"/static/kindeditor/"
	js=r"/static/kindeditor/kindeditor-min.js"
	attrs={}
	id_for_label=""

	def __init__(self,attrs={}):
		pass

	def render(self,id,name,style,default_text="",default_html="",attrs={}):
		return render_to_string("widget_kindeditor.html",{
			"id":id,
			"style":style,
			"name":name,
			"default_text":json.dumps(default_text),
			"default_html":json.dumps(default_html),
		})
