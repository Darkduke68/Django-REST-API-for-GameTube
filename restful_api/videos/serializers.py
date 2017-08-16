from rest_framework import serializers
from rest_framework.reverse import reverse

from comments.serializers import CommentSerializer
from .models import Category, Video


# =============================
# Video Model Serializer
# =============================


class VideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """Return customized API link rather than default."""

    def get_url(self, instance, view_name, request, format):
        kwargs = {
            'category_slug': instance.category.slug,
            "video_slug": instance.slug
        }
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    """Video instance serializer.

    Also flatten the nested foreign keys relationship such as Category, and Comments.
    """

    url = VideoUrlHyperlinkedIdentityField("video_detail_api")
    # category = CategorySerializer(many=False, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    category_url = serializers.CharField(source='category.absolute_url', read_only=True)

    class Meta:
        model = Video
        fields = [
            "url",
            'id',
            'slug',
            'title',
            'embed_code',
            'created',
            'category',
            "category_url",
            "comment_set",
        ]


# =============================
# Category Model Serializer
# =============================


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """Category Instance serializer.

    Flatten one-to-many relationship with model Video, and return customized url.
    """

    url = serializers.HyperlinkedIdentityField('category_detail_api', lookup_field='slug')
    video_set = VideoSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            "url",
            'id',
            'slug',
            'title',
            'description',
            'image',
            'video_set',
        ]


