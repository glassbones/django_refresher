from django.urls import path
from apps.profiles.views import (
    my_profile_view,
    invites_received_view,
    ProfileListView,
    profiles_list_view,
    invite_profiles_list_view, 
)

app_name ='profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
    # path('all-profiles/', profiles_list_view, name='all-profiles-view'), #function path
    path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'), #Class path
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
]
