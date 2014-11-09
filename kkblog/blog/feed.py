from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from . import models


class articleFeed(Feed):
    try:
        config=models.config.objects.get(enabled=1)
        title=config.getBrand()+"的RSS博文订阅"
        link="/rss/"
        description=config.getBrand()+"的RSS订阅。"
    except:
        title="feeds from kkblog"
        link="/rss/"
        description="feeds from kkblog."

    def items(self):
        return models.article.objects.all()[:9]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.getThumbnail()
