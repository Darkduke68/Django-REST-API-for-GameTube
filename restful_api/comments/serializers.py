from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Comment


class CommentVideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """Customized API url field."""

    def get_url(self, instance, view_name, request, format):
        if instance.is_reply:
            video = instance.parent.video
        else:
            video = instance.video
        kwargs = {
            'category_slug': video.category.slug,
            "video_slug": video.slug
        }
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField("comment_detail_api", lookup_field='id')
    reply = serializers.SerializerMethodField(read_only=True)

    def get_reply(self, instance):
        queryset = Comment.objects.filter(root_comment__pk=instance.pk)
        serializer = ReplyCommentSerializer(queryset, context={"request": instance}, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = [
            "url",
            'id',
            "reply",
            'text',
        ]


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "id",
            'text'
        ]


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'video',
            'root_comment',
            ]


class ReplyCommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
        ]

