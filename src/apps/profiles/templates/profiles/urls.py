from django.urls import path
from apps.profiles.views import my_profile_view

app_name ='profiles'

urlpatterns = [
    path('myprofile', my_profile_view, name='my-profile-view')
]
