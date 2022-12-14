from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from .models import User, Post, Follow, Comment
from .forms import PostForm, EditPostForm, LikeForm, CommentForm, EditCommForm, FollowForm
from datetime import datetime


def index(request):
    add_post_form = PostForm()
    add_comm_form = CommentForm()
    edit_post_form = EditPostForm()
    handle_like_form = LikeForm()

    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "add_post_form": add_post_form,
        "add_comm_form": add_comm_form,
        "edit_post_form": edit_post_form,
        "handle_like_form": handle_like_form,
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required()
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = User.objects.get(username=request.user.username)
            new_post.timestamp = datetime.now(tz=timezone.utc)
            new_post.save()

            return JsonResponse({"message": "Post added successfully."}, status=201)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)             
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def user_page(request, username):
    edit_post_form = EditPostForm()
    handle_like_form = LikeForm()
    add_comm_form = CommentForm()
    handle_follow_form = FollowForm()
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist."}, status=400)
        # user = None
    posts = Post.objects.filter(author=user)
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/user.html", {
        "page_obj": page_obj,
        "username": username,
        "edit_post_form": edit_post_form,
        "handle_like_form": handle_like_form,
        "add_comm_form": add_comm_form,
        "handle_follow_form": handle_follow_form
    })


@login_required()
def follow_user(request):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            followed_user = User.objects.get(username=data["id"])
            following_user = request.user

            if len(Follow.objects.filter(followed=followed_user, follower=following_user)) == 0:
                new_follow = Follow(followed=followed_user, follower=following_user)
                new_follow.save()
            else:
                delete_follow = Follow.objects.get(followed=followed_user, follower=following_user)
                delete_follow.delete()

            return JsonResponse({"message": "Followed successfully."}, status=201)        
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@login_required()
def following_page(request):
    handle_like_form = LikeForm()
    add_comm_form = CommentForm()

    following_list = Follow.objects.filter(follower=request.user)
    followed_names = []
    for follow in following_list:
        followed_names.append(follow.followed)

    posts_lists = []
    for name in followed_names:
        posts_lists.append(Post.objects.filter(author=name))

    posts = []
    for list_ in posts_lists:
        for post in list_:
            posts.append(post)
    posts = sorted(posts, key=lambda instance: instance.timestamp, reverse=True)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "add_comm_form": add_comm_form,
        "handle_like_form": handle_like_form,
    })


@login_required()
def edit_post(request):
    if request.method == 'POST':
        form = EditPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_to_update = Post.objects.get(pk=data["id"])
            if post_to_update.author == request.user:
                post_to_update.text = data["text"]
                post_to_update.save()
            else:
                return JsonResponse({"error": "Unauthorized."}, status=401)

            return JsonResponse({"message": "Post updated successfully."}, status=200)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@login_required()
def edit_comment(request):
    if request.method != 'POST':
        form = EditCommForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Post.objects.get(pk=data["post_id"])
            comment_to_update = Comment.objects.get(pk=data["comment_id"], related_post=post)
            if comment_to_update.author == request.user:
                comment_to_update.text = data["text"]
                comment_to_update.save()
            else:
                return JsonResponse({"error": "Unauthorized."}, status=401)

            return JsonResponse({"message": "Comment updated successfully."}, status=200)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@login_required()
def likes(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Post.objects.get(pk=data["id"])
            user = User.objects.get(username=request.user)
            if Post.objects.filter(pk=data["id"], likes__username=request.user):
                post.likes.remove(user)
            else:
                post.likes.add(user)
            post.save()

            return JsonResponse({"message": "Like updated successfully."}, status=200)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def count_likes(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        likes_count = len(post.likes.all())
        data = {
            "likes": likes_count
        }
        return JsonResponse(data, safe=False)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=400)
    

def count_follows(request, username):
    try:
        user = User.objects.get(username=username)

        followers_sum = Follow.objects.filter(followed=user).count()
        following_sum = Follow.objects.filter(follower=user).count()

        follow_btn = ""
        if request.user.is_authenticated and user != request.user:
            follow_btn = '<input type="submit" class="btn btn-primary" value="Follow">'
            if len(Follow.objects.filter(followed=user, follower=request.user)) == 1:
                follow_btn = '<input type="submit" class="btn btn-danger" value="Unfollow">'

        data = {
            "followers_sum": followers_sum,
            "following_sum": following_sum,
            "follow_btn": follow_btn
        }

        return JsonResponse(data, safe=False)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=400)


@login_required()
def delete_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        if request.user == post.author:
            post.delete()
            return JsonResponse({'success': 'Post is deleted successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'You dont have permission.'}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@login_required()
def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = User.objects.get(username=request.user.username)
            new_comment.timestamp = datetime.now(tz=timezone.utc)
            new_comment.related_post = Post.objects.get(pk=post_id)
            new_comment.save()
            return JsonResponse({"message": "Comment added successfully."}, status=201)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def count_comments(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        comm = Comment.objects.filter(related_post=post)
        comm_count = comm.count()

        data = {
            "comm_count": comm_count
        }

        return JsonResponse(data, safe=False)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=400)


def show_comments(request, post_id):
    add_comm_form = CommentForm()
    edit_post_form = EditPostForm()
    edit_comm_form = EditCommForm()
    handle_like_form = LikeForm()

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=400)

    comments = Comment.objects.filter(related_post=post_id).order_by("-timestamp")

    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/comments.html", {
        "page_obj": page_obj,
        "post": post,
        "add_comm_form": add_comm_form,
        "edit_post_form": edit_post_form,
        "handle_like_form": handle_like_form,
        "edit_comm_form": edit_comm_form
    })


@login_required()
def delete_comment(request, post_id, comment_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.get(pk=comment_id, related_post=post)
        if request.user == comment.author:
            comment.delete()
            return JsonResponse({'success': 'Comment is deleted successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'You dont have permission.'}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
