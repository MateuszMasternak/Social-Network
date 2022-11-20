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
from .forms import PostForm, EditForm, LikeForm, CommentForm
from datetime import datetime


def index(request):
    form_post = PostForm()
    form_comment = CommentForm()
    form_edit = EditForm()
    form_like = LikeForm()
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "form": form_post,
        "form_comm": form_comment,
        "form_2": form_edit,
        "form_3": form_like,
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = User.objects.get(username=request.user.username)
            new_post.timestamp = datetime.now(tz=timezone.utc)
            new_post.save()

            return JsonResponse({"message": "Post added successfully."}, status=201)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)


def user_page(request, username):
    form_edit = EditForm()
    form_like = LikeForm()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    posts = Post.objects.filter(author=user)
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    followers = Follow.objects.filter(followed=user)
    following = Follow.objects.filter(follower=user)
    followers_sum = len(followers)
    following_sum = len(following)

    is_followed = "not logged in or is the same user"
    if request.user.is_authenticated and user != request.user:
        is_followed = False
        if len(Follow.objects.filter(followed=user, follower=request.user)) == 1:
            is_followed = True

    return render(request, "network/user.html", {
        "page_obj": page_obj,
        "username": username,
        "is_followed": is_followed,
        "followers_sum": followers_sum,
        "following_sum": following_sum,
        "form_2": form_edit,
        "form_3": form_like
    })


@login_required()
def follow_user(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        url = request.META.get('HTTP_REFERER')
        url = url.split("/")
        username = url[-1]
        followed_user = User.objects.get(username=username)
        following_user = request.user

        if len(Follow.objects.filter(followed=followed_user, follower=following_user)) == 0:
            new_follow = Follow(followed=followed_user, follower=following_user)
            new_follow.save()
        else:
            delete_follow = Follow.objects.get(followed=followed_user, follower=following_user)
            delete_follow.delete()

        return JsonResponse({"message": "Followed successfully."}, status=201)


@login_required()
def following_page(request):
    form_like = LikeForm()

    following_list = Follow.objects.filter(follower=request.user)
    followed_names = []
    for follow in following_list:
        followed_names.append(follow.followed)

    posts_lists = []
    for name in followed_names:
        posts_lists.append(Post.objects.filter(author=name))

    posts = []
    for list_ in posts_lists:
        for element in list_:
            posts.append(element)
    posts = sorted(posts, key=lambda instance: instance.timestamp, reverse=True)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "form_3": form_like
    })


def edit_post(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        form = EditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_to_update = Post.objects.get(id=data["id"])
            if post_to_update.author == request.user:
                post_to_update.text = data["text"]
                post_to_update.save()
            else:
                return JsonResponse({"error": "Unauthorized."}, status=401)

            return JsonResponse({"message": "Post updated successfully."}, status=200)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)


@login_required()
def likes(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        form = LikeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Post.objects.get(id=data["id"])
            user = User.objects.get(username=request.user)
            print(post.likes.all())
            if Post.objects.filter(id=data["id"], likes__username=request.user):
                post.likes.remove(user)
            else:
                post.likes.add(user)
            post.save()

            return JsonResponse({"message": "Like updated successfully."}, status=200)
        else:
            return JsonResponse({"error": "Form's data is invalid."}, status=400)


def show_likes(request, post_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    else:
        post = Post.objects.filter(id=post_id)
        if post.count() != 0:
            likes_count = len(post[0].likes.all())
        else:
            likes_count = 0

        data = {
            "likes": likes_count
        }

        return JsonResponse(data, safe=False)
    

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    
    if request.user == post.author:
        post.delete()
        return JsonResponse({'success': 'Post is deleted successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'You dont have permission.'}, status=400)


@login_required()
def add_comment(request, post_id):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
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


def count_comments(request, post_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    else:
        post = Post.objects.filter(pk=post_id)
        comm = Comment.objects.filter(related_post=post[0])

        comm_count = comm.count()

        data = {
            "comm_count": comm_count
        }

        return JsonResponse(data, safe=False)
