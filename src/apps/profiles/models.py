from django.db import models
from django.contrib.auth.models import User
from .._utils import get_random_eight_digit_id
from django.template.defaultfilters import slugify

# Create your models here.
class Profile(models.Model):

    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # models.CASCADE (evertime a user is deleted the profile is also deleted)
    bio = models.TextField(default="n/a", max_length='512')
    email = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='') 
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created= models.DateTimeField(auto_now_add=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts_count(self):
        return self.posts.all().count() # we have access to posts via the fk attr on the Post class in posts/models.py

    def get_all_authored_posts(self):
        return self.posts.all

    def get_given_likes_count(self):
        likes = self.like_set.all() # we are using a fk in the Like class @ posts/models.py but we aren't passing it a related_name arg. Thats why we have to use the funky syntax here
        total_likes = 0
        for like in likes:
            if like.value =='Like':
                total_likes += 1
        return total_likes

    def get_recieved_likes_count(self):
        posts = self.posts.all()
        total_likes = 0
        for post in posts:
            total_likes += post.liked.all().count()
        return total_likes

        
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def save(self, *args, **kwargs):
        slugExists = False
        if self.first_name and self.last_name:
            # if first and last name make the slug "firstname lastname"
            to_slug = slugify( str(self.first_name) + ' ' + str(self.last_name) )
            # check if that slug isn't unique
            slugExists = Profile.objects.filter(slug=to_slug).exists()
            while slugExists:
                # while the slug is not unique, append an eight digit id to it and then check if the modified slug is unique
                to_slug = slugify(to_slug + " " + str(get_random_eight_digit_id()))
                slugExists = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)
    
class Relationship(models.Model):
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='receiver')
    created= models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=(
        ('send', 'send'), 
        ('accepted', 'accepted')
    ))

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
