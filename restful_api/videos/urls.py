from django.conf.urls import url
from .views import VideoDetailAPIView
from .views import CategoryDetailAPIView, CategoryListAPIView


urlpatterns = [
    url(r'^$', CategoryListAPIView.as_view(), name='category_list_api'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<video_slug>[\w-]+)/$', VideoDetailAPIView.as_view(), name='video_detail_api'),
    url(r'^(?P<category_slug>[\w-]+)/$', CategoryDetailAPIView.as_view(), name='category_detail_api'),
]