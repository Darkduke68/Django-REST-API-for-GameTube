from django.conf.urls import url
from .views import CommentCreateAPIView, CommentListAPIView, CommentDetailAPIView

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='comment_list_api'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='comment_create_api'),
    url(r'^(?P<id>\d+)/$', CommentDetailAPIView.as_view(), name='comment_detail_api'),
]
