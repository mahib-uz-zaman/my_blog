from django.urls import path
from .views import home, create_post, post_detail, like_post, dislike_post, delete_post, delete_comment, SignUpView

urlpatterns = [
    path('', home, name='home'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('dislike/<int:post_id>/', dislike_post, name='dislike_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]