from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True)
    photo = models.ImageField(null=True, blank=True, upload_to='profile/photos/%Y/%m/%d/')
    bio = models.TextField(null=True, blank=True)
    monet = models.PositiveIntegerField(default=0)
    subprice = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user, allow_unicode=True)
        return super().save(*args, **kwargs)


class SubscripModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


class CoinsModel(models.Model):
    reciver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reciver')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order:{self.created_at.strftime("%b %d %I: %M %p")}'

    def get_absolute_url(self):
        return reverse('home')
