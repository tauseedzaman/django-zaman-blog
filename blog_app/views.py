from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from .models import Post, Comment, Category, Subscribe, Contact
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.db import models


def view_404(request, exception):
    return HttpResponseNotFound(render(request, '404.html'))


def categories(request):
    categories = Category.objects.annotate(post_count=models.Count('category'))
    return render(request, 'categories.html', {'categories': categories})


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        subscribe = Subscribe(email=email)
        subscribe.save()
        messages.success(
            request, "Thank you for subscribing to our newsletter! You'll now receive updates on the latest news from our community.")
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseNotFound(render(request, '404.html'))


def profile(request):
    if request.method == 'POST':
        # Update user data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.username = username
        request.user.email = email

        his_error = False
        if first_name == "" or last_name == "" or username == "" or email == "":
            messages.error(request, "⚠ All fields are required.")
            his_error = True

        if his_error:
            return render(request, "registration/profile.html", form_data)

        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.userprofile)
        if form.is_valid():
            form.save()
        # Check if user has uploaded a new image
        # if request.FILES.get('profile'):
            # Delete old image if it exists
            if request.user.UserProfile.profile_image:
                request.user.UserProfile.profile_image.delete()

            # Save new image
            request.user.UserProfile.profile_image = request.FILES['profile']
            request.user.UserProfile.save()

        # Save user data
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

        messages.success(request, "Profile Updated Successfully.")
        return render(request, "profile.html")

    return render(request, "profile.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        form_data = {}
        form_data["username"] = username
        his_error = False

        # validation
        if username == "" or password == "":
            messages.error(request, "⚠ All fields are required.")
            his_error = True

        if his_error:
            return render(request, "registration/register.html", form_data)

        return redirect("/home")
    return render(request, "auth/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        form_data = {}
        form_data["username"] = username
        form_data["email"] = email
        his_error = False

        if request.POST.get("terms") == None:
            his_error = True
            messages.error(
                request, "⚠ You Should accept our terms and conditions.")

        # validation
        if username == "" or email == "" or password == "" or password_confirmation == "":
            messages.error(request, "⚠ All fields are required.")
            his_error = True

        if password != password_confirmation:
            messages.error(
                request, "⚠ Password Confirmation does not matched.")
            his_error = True

        # if User.objects.get(username=username) != None:
        #     messages.error(
        #         request, "⚠ The username you entered has already been taken. try another username..")

        # if User.objects.get(email=email) != None:
        #     messages.error(
        #         request, "⚠ The email you entered has already been taken. try another email..")

        if his_error:
            return render(request, "registration/register.html", form_data)

        user = User.objects.create_user(username, email, password)
        user.save()
        messages.success(
            request, "Account Registered Successfully. login to Continue.")
        return redirect("accounts/login/")
    else:
        return render(request, "registration/register.html")


# home page . load all posts
def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    posts = Post.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "index.html", {'posts': posts})


def gallery(request):
    return render(request, "gallery.html")


@login_required
def home(request):
    posts = Post.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "home.html", {'posts': posts})


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        if name == "" or email == "" or subject == "" or message == "":
            messages.error(request, "All Fields are required.")
            return render(request, "contact.html")
        contact = Contact(name=name, email=email,
                          subject=subject, message=message)
        if contact:
            contact.save()
            messages.success(
                request, "Thanks for your message our team will reply shortly.")
            return render(request, "contact.html")
    return render(request, "contact.html")


@login_required
def post(request, slug):
    post = Post.objects.filter(slug=slug)
    categories = Category.objects.annotate(post_count=models.Count('category'))
    comments = ""

    if post.exists():
        post = post.first()
        comments = Comment.objects.filter(post=post.id)

    else:
        return HttpResponse("<h3>Page Not Found otherwise contact us</h3>")

    context = {'post': post, 'comments': comments,
               'comments_count': comments.count(), 'categories': categories}
    if request.method == "POST":
        # save comment and redirect back
        comment = request.POST.get("comment")
        comment = Comment(
            content=comment, auther=request.user, post=post)
        comment.save()
        messages.success(request, "Thanks for your comment.")
        return render(request, "single.html", context)

    return render(request, "single.html", context)


@login_required
def category_posts(request, category):
    category = Category.objects.filter(title=category)
    if category.exists():
        category = category.first()
    posts = Post.objects.filter(category=category)

    if not posts.exists():
        return HttpResponseNotFound(render(request, '404.html'))

    context = {'posts': posts, 'posts_count': posts.count(),
               'category': category}
    return render(request, "category-posts.html", context)


@login_required
def tag_posts(request, tag):
    posts = Post.objects.filter(tags=tag)

    if not posts.exists():
        return HttpResponseNotFound(render(request, '404.html'))

    context = {'posts': posts, 'posts_count': posts.count(),
               'tag': tag}
    return render(request, "tag-posts.html", context)
