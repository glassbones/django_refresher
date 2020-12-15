from django.urls import path
from apps.posts.views import post_comment_create_and_list_view, like_toggle_post

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('liked', like_toggle_post, name='like-toggle-post-view')
]
