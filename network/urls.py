from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-post", views.create_post, name="create_post"),
    path("add-comment/<int:post_id>", views.add_comment, name="add_comment"),
    path("count-comments/<int:post_id>", views.count_comments, name="count_comments"),
    path("user/<str:username>", views.user_page, name="user_page"),
    path("follow", views.follow_user, name="follow_user"),
    path("following", views.following_page, name="following_page"),
    path("edit-post", views.edit_post, name="edit_post"),
    path("edit-comment", views.edit_comment, name="edit_comment"),
    path("like", views.likes, name="likes"),
    path("count-likes/<int:post_id>", views.count_likes, name="count_likes"),
    path("delete-post/<int:post_id>", views.delete_post, name="delete_post"),
    path("comments/<int:post_id>", views.show_comments, name="show_comments"),
    path("delete-comment/<int:post_id>/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("count-follows/<str:username>", views.count_follows, name="count_follows")
]
