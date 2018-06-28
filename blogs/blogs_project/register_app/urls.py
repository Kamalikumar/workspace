# register_app/urls.py
from django.conf.urls import url

from .views import signup


urlpatterns = [
    url(r'^$', signup ,name='signup'),
]