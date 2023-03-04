from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
# post model


class Category(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('posts', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    thumbnail = models.FileField(upload_to='./static/uploads')
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        'blog_app.Category', related_name='category', default=None, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

# Comments Model


class Comment(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'blog_app.Post', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username