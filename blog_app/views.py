from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


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
