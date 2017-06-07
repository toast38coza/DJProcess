from django.conf.urls import url, include
from .api import router
urlpatterns = [
    url(r'^', include(router.urls))
]