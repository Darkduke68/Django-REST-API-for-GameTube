from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse

# =============================
# section for video models
# =============================


class VideoQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def has_embed(self):
        return self.filter(embed_code__isnull=False).exclude(embed_code__exact="")


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def get_featured(self):
        return self.get_queryset().featured()

    def all(self):
        return self.get_queryset().has_embed()


class Video(models.Model):
    """Model stores information of a single video item. """

    title = models.CharField(max_length=120)
    embed_code = models.CharField(max_length=500, null=True, blank=True)
    genres = GenericRelation("Genre", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey("Category", default=1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    image = models.ImageField(upload_to='images/')

    objects = VideoManager()

    class Meta:
        unique_together = ('slug', 'category')
        ordering = ['-created']

    def __str__(self):
        return self.slug


def video_post_save_receiver(sender, instance, created, *args, **kwargs):
    """Create unique slug each time after instance is saved. """

    if created:
        slug_title = slugify(instance.title)
        new_slug = "{0} {1} {2}".format(instance.title, instance.category.slug, instance.id)
        try:
            Video.objects.get(slug=slug_title, category=instance.category)
            instance.slug = slugify(new_slug)
            instance.save()
        except Video.DoesNotExist:
            instance.slug = slug_title
            instance.save()
        except Video.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            instance.save()


# register post save method
post_save.connect(video_post_save_receiver, sender=Video)


# =============================
# section for Category models
# =============================


class CategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_featured(self):
        return self.get_queryset().featured()


class Category(models.Model):
    """Model stores information about video game genre. """

    title = models.CharField(max_length=120)
    description = models.TextField(max_length=5000, null=True, blank=True)
    genres = GenericRelation("Genre", null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(default='', unique=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = CategoryManager()

    class Meta:
        ordering = ['title', 'created']

    def __str__(self):
        return self.title

    def absolute_url(self):
        return reverse('api_detail', kwargs={'category_slug': self.slug})

# =============================
# section for Category models
# =============================


GENRE_CHOICES = (
    ("RPG", "Role-playing"),
    ("ACT", "Action"),
    ('FPS', 'First Person Shooter'),
    ('TPS', 'Third Person Shooter'),
    ('Strategy', 'Strategy'),
    ('MMO', 'Massively Multiplayer Online'),
    ('Racing', 'Racing')
)


class Genre(models.Model):
    genre = models.SlugField(choices=GENRE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.genre













