from django.shortcuts import get_object_or_404

from rest_framework import generics

from .models import Video, Category
from .serializers import CategorySerializer, VideoSerializer


# =============================
# Video model API views
# =============================


class VideoDetailAPIView(generics.RetrieveAPIView):
    """Provide read-only endpoints for single Video model instance.

    Only 'GET' request is allowed.
    """

    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_object(self):
        """Look up instance using both category slug and video slug."""
        category_slug = self.kwargs["category_slug"]
        video_slug = self.kwargs["video_slug"]
        category = get_object_or_404(Category, slug=category_slug)
        return get_object_or_404(Video, category=category, slug=video_slug)


# =============================
# Category model API views
# =============================


class CategoryListAPIView(generics.ListAPIView):
    """Provides endpoints of a collection of all Category model instances."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    paginate_by = 10


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """Provide endpoints for a single Category model instance."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self):
        slug = self.kwargs["slug"]
        return get_object_or_404(Category, slug=slug)
