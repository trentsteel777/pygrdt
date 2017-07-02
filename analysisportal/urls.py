from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^analyze$', views.analyze, name='analyze'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)