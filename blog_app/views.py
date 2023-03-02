from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages


def profile(request):
    return render(request, "profile.html");

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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", 'email', "password"]


def test(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                return redirect('/test')
            except:
                pass

    else:
        form = UserForm()
    return render(request, 'test.html', {'form': form})


def register(request):
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
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def post(request, slug):
    post = Post.objects.filter(slug=slug)

    if post.exists():
        post = post.first()
    else:
        return HttpResponse("<h3>Page Not Found otherwise contact us</h3>")

    context = {'post': post}
    return render(request, "single.html", context)
