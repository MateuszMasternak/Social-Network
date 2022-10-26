from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-post", views.create_post, name="create_post"),
    path("user/<str:username>", views.user_page, name="user_page"),
    path("follow", views.follow_user, name="follow_user"),
    path("following", views.following_page, name="following_page"),
    path("edit-post", views.edit_post, name="edit_post"),
    path("like", views.likes, name="likes"),
    path("show-likes/<int:post_id>", views.show_likes, name="show_likes"),
    path("delete-post/<int:post_id>", views.delete_post, name="delete_post")
]
