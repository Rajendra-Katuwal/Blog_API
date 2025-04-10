from django.urls import path
from .views import create_blog, update_blog, get_all_blogs, delete_blog, get_by_id, post_comment, get_blog_comments, delete_comment
from .views import BlogListCreate, BlogDetails, CommentListCreate, CommentDetail

urlpatterns = [
    # URLs for Blog CRUD operations
    path('create', create_blog, name="create_blog"),
    path('get_all', get_all_blogs, name="get_all_blogs"),
    path('<int:id>', get_by_id, name="get_by_id"),
    path('update/<int:id>', update_blog, name="update_blog"),
    path('delete/<int:id>', delete_blog, name="delete_blog"),

    # URLs for comment 
    path('comment/post', post_comment, name='post_comment'),
    path('<int:blog_id>/comment', get_blog_comments, name='get_blog_comments'),
    path('comment/delete/<int:comment_id>', delete_comment, name='delete_comment'),


    # Class Based views urls
    # path('', BlogListCreate.as_view(), name="blog_create_list"),
    # path('<int:id>', BlogDetails.as_view(), name="blog_create_list"),

    # # Class and Mixin based urls
    # path('comment/<int:blog_id>', CommentListCreate.as_view(), name="comment_create_list"),
    # path('comment/<int:comment_id>', CommentDetail.as_view(), name="comment_detail"),
]