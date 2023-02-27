from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
# post model


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    thumbnail = models.FileField(upload_to='./static/uploads')
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
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