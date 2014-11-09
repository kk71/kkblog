from glob import glob

from django.http import HttpResponse
from django.core.context_processors import csrf
from django.conf import settings

from mako.lookup import TemplateLookup
djlookup = TemplateLookup(
    directories=settings.TEMPLATE_DIRS, input_encoding="utf-8")


def render_to_string(template_name,
                     dictionary=None,
                     request=None):
    '''
    render a template to a string(like render_to_string django.template.loader)
    '''
    t = djlookup.get_template(template_name)
    if request != None:
        dictionary.update(csrf(request))
    page = t.render(**dictionary)
    return page


def render_to_response(template_name,
                       dictionary={},
                       content_type="text/html",
                       request=None,
                       status=200):
    '''
    a simple http response method just like django's
    for easier replacement
    '''
    page = render_to_string(template_name, dictionary, request)
    return HttpResponse(content=page, content_type=content_type, status=status)


def tmpldebug(request, tmpl=""):
    '''
    template debug tool
    argument:
    tmpl:specific template file name.
    '''
    if tmpl == "":
        t = '''
<!DOCTYPE html>
<html>
<head>
<title>djangomako template design mode</title>
</head>
<body>
'''
        for tmpldir in settings.TEMPLATE_DIRS:
            if tmpldir[-1] != "/":
                tmpldir += "/"
            t += "<h2>" + tmpldir + "</h2>"
            for s in glob(tmpldir + "*"):
                if s[-1:] == "~":
                    continue
                s = s[len(tmpldir):]
                t += '<a href=\"' + s + '\">' + s + "</p>"
            s += "<br>"
        t += '''
</body> 
</html>
'''
        return HttpResponse(t)

    else:
        return render_to_response(tmpl, {})
