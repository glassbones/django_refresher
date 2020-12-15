from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver #decorator these are cool!
from .models import Profile, Relationship


# creates a profile everytime a new user is created assigned to that user
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # print('sender = ', sender)
    # print('instance = ', instance)
    if created:
        Profile.objects.create(user=instance)

# creating friend friend requests and expanding friendslist when they are 'accepted'
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver

    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user) # adding receiver to senders 'Profile.friends' (manyToMany field)
        receiver_.friends.add(sender_.user) # adding sender to receivers 'Profile.friends' (manyToMany field)
        sender_.save()
        receiver_.save()