from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm

from django.shortcuts import render
from .models import Post, Like

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.like_count = post.likes.filter(is_dislike=False).count()  # Number of likes
        post.dislike_count = post.likes.filter(is_dislike=True).count()  # Number of dislikes
        # Check if the current user has liked or disliked the post
        if request.user.is_authenticated:
            user_like = post.likes.filter(user=request.user).first()
            post.user_has_liked = user_like and not user_like.is_dislike
            post.user_has_disliked = user_like and user_like.is_dislike
        else:
            post.user_has_liked = False
            post.user_has_disliked = False
    return render(request, 'blog/home.html', {'posts': posts})
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None)  # Only top-level comments
    if request.user.is_authenticated:
        user_like = post.likes.filter(user=request.user).first()
        post.user_has_liked = user_like and not user_like.is_dislike
        post.user_has_disliked = user_like and user_like.is_dislike
    else:
        post.user_has_liked = False
        post.user_has_disliked = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # Unlike/undislike if already liked/disliked
    return redirect('post_detail', post_id=post.id)

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    like.is_dislike = True  # Mark as dislike
    like.save()
    return redirect('post_detail', post_id=post.id)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'