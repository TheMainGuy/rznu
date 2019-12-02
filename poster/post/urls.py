from django.urls import path
from .api import list_create_posts, get_update_delete_post, list_create_comment, get_update_delete_comment, \
    list_create_post_comment, get_update_delete_post_comment

urlpatterns = [
    path('posts', list_create_posts),
    path('posts/<post_id>', get_update_delete_post),
    path('comments', list_create_comment),
    path('comments/<comment_id>', get_update_delete_comment),
    path('posts/<post_id>/comments', list_create_post_comment),
    path('posts/<post_id>/comments/<comment_id>', get_update_delete_post_comment),
]
