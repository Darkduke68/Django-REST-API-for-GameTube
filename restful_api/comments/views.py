from rest_framework import generics, mixins

from .models import Comment
from .serializers import CommentCreateSerializer, CommentUpdateSerializer, CommentSerializer


class CommentListAPIView(generics.ListAPIView):
    """Endpoint to represent a collection of Comment model instances."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    paginate_by = 10


class CommentCreateAPIView(generics.CreateAPIView):
    """create-only endpoint."""

    serializer_class = CommentCreateSerializer


class CommentDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    lookup_field = 'id'

    def put(self, request, *args,**kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
