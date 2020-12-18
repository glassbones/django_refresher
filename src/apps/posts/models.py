from django.db import models
from django.core.validators import FileExtensionValidator
from django_refresher.src.apps.profiles.models import Profile

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, related_name='likes', blank=True) # default=None did not make this an unrequired field
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_of_comments(self):
        return self.comment_set.all().count() #weird syntax

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=512)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=8, choices=(('Like','Like'),('Unlike','Unlike')))
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"