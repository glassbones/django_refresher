from django.urls import path
from django_refresher.src.apps.posts.views import post_comment_create_and_list_view, like_toggle_post, PostDeleteView, PostUpdateView

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('liked', like_toggle_post, name='like-toggle-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
