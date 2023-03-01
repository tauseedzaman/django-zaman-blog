from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = auth
        return redirect("/home")
    return render(request, "auth/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        if userame.is_valid():
            try:
                print("not valid")
                return redirect('/register')
            except:
                print("valid")
                pass
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("password_conformation")
        user = User.objects.create_user(username, email, password)
        user.save()

        return render(request, "home.html")
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
