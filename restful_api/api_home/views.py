from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from videos.models import Category
from comments.models import Comment


# Create your views here.
class HomeAPIView(APIView):
    """View to list all model information in the backend service."""

    def get(self, request, format=None):
        """Return all model summary."""
        data = {
            'categories': {
                'url': reverse_lazy('category_list_api', request=request),
                'inst_count': Category.objects.all().count(),
            },
            'video_comments': {
                'list_url': reverse_lazy('comment_list_api', request=request),
                'create_url': reverse_lazy('comment_create_api', request=request),
                'inst_count': Comment.objects.all().count(),
            },
            'jwt_auth_related': {
                'create_url': reverse_lazy('create_jwt_token', request=request),
                'refresh_url': reverse_lazy('refresh_jwt_token', request=request),
                'verify_url': reverse_lazy('verify_jwt_token', request=request),
            },

        }
        return Response(data)
