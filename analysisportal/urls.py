from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^analyze$', views.analyze, name='analyze'),
    url(r'^grdt$', views.grdt, name='grdt'),
    url(r'^ajax/dispatcher/$', views.dispatcher, name='dispatcher'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)