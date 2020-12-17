from django.urls import path
from apps.profiles.views import (
    my_profile_view,
    invites_received_view,
    ProfileListView,
    profiles_list_view,
    invite_profiles_list_view,
    send_invitation,
    remove_friend,
    accept_invitation,
    reject_invitation
)

app_name ='profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('my-invites/accept/', accept_invitation, name='accept-invitation'),
    path('my-invites/reject/', reject_invitation, name='reject-invitation'),
    # path('all-profiles/', profiles_list_view, name='all-profiles-view'), #function path
    path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'), #Class path
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend/', remove_friend, name='remove-friend'),
    
]
