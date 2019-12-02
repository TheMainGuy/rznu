from django.urls import path
from .api import list_create_posts, get_update_delete_post

urlpatterns = [
    path('posts', list_create_posts),
    path('posts/<post_id>', get_update_delete_post),

]
