from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'blog/index.html')


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    account = post.author.account
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'account': account
    }
    return render(request, 'blog/detail.html', context)


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {"form": form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'forms/comment.html', context)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = Post.published.annotate(similarity=TrigramSimilarity("title", query)).filter(similarity__gt=0.1)
            results2 = Post.published.annotate(similarity=TrigramSimilarity("description", query)).filter(
                similarity__gt=0.1)
            results = results1 | results2.order_by('-similarity')
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    return render(request, "blog/profile.html", {"posts": posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create-post.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile")
    return render(request, 'forms/delete-post.html', {"post": post})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create-post.html', {"form": form, "post": post})


def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')


# def user_login(request):
#   if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            cd = form.cleaned_data
#            user = authenticate(request, username=cd['username'], password=cd['password'])
#            if user is not None:
#                if user.is_active:
#                    login(request, user)
#                    return redirect('blog:profile')
#                else:
#                    return HttpResponse('your account is disabled!')
#            else:
#                return HttpResponse('your account does not exist!')
#    else:
#       form = LoginForm()
#    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        account_form = EditAccountForm(request.POST, files=request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
    else:
        user_form = EditUserForm(instance=request.user)
        account_form = EditAccountForm(instance=request.user.account)
    context = {'user_form': user_form, 'account_form': account_form}
    return render(request, 'registration/edit_account.html', context)


def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    return render(request, 'blog/account_detail.html', {'account': account})


def user_comments(request):
    user = request.user
    comments = []
    for post in user.user_posts.all().filter(status=Post.Status.PUBLISHED):
        comments.append(post.comments.all().filter(active=True))
    return render(request, 'blog/user_comments.html', {'comments': comments})
