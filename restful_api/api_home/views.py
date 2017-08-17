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
                'count': Category.objects.all().count(),
            },
            'comments': {
                'url': reverse_lazy('comment_list_api', request=request),
                'count': Comment.objects.all().count(),
            }
        }
        return Response(data)
