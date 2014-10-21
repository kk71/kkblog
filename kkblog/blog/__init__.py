from django.apps import AppConfig

class app_config(AppConfig):
    name="blog"
    verbose_name="博客"


default_app_config="blog.app_config"
