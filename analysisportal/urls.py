from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^analyze$', views.analyze, name='analyze'),
]