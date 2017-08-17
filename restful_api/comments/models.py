from django.conf import settings
from django.db import models

from videos.models import Video


class CommentManager(models.Manager):
    def all(self):
        """Get all parent comments."""
        return super(CommentManager, self).filter(root_comment=None)

    def recent(self):
        """Retrieve limited number of comments.

        This method works because Comment instance is sorted by created time.
        """
        try:
            limit_to = settings.RECENT_COMMENT_NUMBER
        except:
            limit_to = 4
        return self.get_queryset().filter(root_comment=None)[:limit_to]

    def create_comment(self, user=None, text=None, video=None, root_comment=None):
        if not user:
            raise ValueError("Must include a user when adding a Comment")

        comment = self.model(user=user, text=text)
        if video is not None:
            comment.video = video
        if root_comment is not None:
            comment.root_comment = root_comment
        comment.save(using=self._db)
        return comment


class Comment(models.Model):
    """Model stores user comment related to a particular video."""

    root_comment = models.ForeignKey("self", null=True, blank=True)
    video = models.ForeignKey(Video, null=True, blank=True)
    text = models.TextField()
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text

    @property
    def content(self):
        return self.text

    @property
    def is_reply(self):
        if self.root_comment is not None:
            return True
        return False

    @property
    def reply(self):
        """Only support one-level parent-child relationship."""
        if self.is_reply:
            return None
        else:
            return Comment.objects.filter(root_comment=self)
