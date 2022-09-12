from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class PostNews(models.Model):
    title = models.TextField(max_length=125)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to='post/photos/%Y/%m/%d/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    view = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=200, blank=True)
    free =models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
