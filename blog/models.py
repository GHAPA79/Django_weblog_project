from django.db import models
from django.shortcuts import reverse


class Post(models.Model):
    STATUS_CHOICES = (
        ('pub', 'Published'),
        ('drf', 'Draft'),
    )

    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=5)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Baraye redirect() kardan dar views estefade mishe.
        return reverse('post_details', args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

