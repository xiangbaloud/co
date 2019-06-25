from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.http import AsgiHandler

from . import consumers

import django_eventstream

urlpatterns = [
    url(r'^events/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['test']}),
    url(r'', AsgiHandler),
]