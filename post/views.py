import datetime
import sqlite3

from django.db import transaction
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, HttpResponse, Http404, redirect

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from post import models
from .forms import PostCreateForm

from .models import Posts
from faker import Faker


def fake_create_user(request):
    f = Faker('ru-RU')
    for i in range(10):
        print(i)
        p = f.profile()
        User.objects.create(
            username=p['username'],
            email=p['mail'],
            password=f.password(length=8)
        )

    return redirect('/')


def fake_create_posts(request):
    f = Faker('ru-RU')
    users = User.objects.all()
    for u in users:
        models.Posts.objects.bulk_create(
            [
                models.Posts(
                    title=f.sentence(nb_words=5),
                    content=f.sentence(nb_words=100),
                    date=f.date_time_between(),
                    user=u
                ) for _ in range(10)
            ]
        )
        print(u.username)
    return redirect('/')


# def profile(request, user_name):
#     try:
#         p = int(request.GET.get('p', 1))
#     except ValueError:
#         p = 1
#
#     try:
#         user_profile = models.Profile.objects.get(user__username=user_name)
#         posts = models.Posts.objects.filter(user__username=user_name).order_by('-date')
#         pages = Paginator(posts, 100)
#         return render(
#             request,
#             'registration/profile.html',
#             {
#                 'profile': user_profile,
#                 'posts': pages.page(p),
#                 'page': p,
#                 'num_pages': int(pages.num_pages)
#             }
#         )
#     except (User.DoesNotExist, models.Profile.DoesNotExist):
#         return redirect('home')

def profile(request, user_name):
    posts_limit = 20
    print(user_name)
    print('*0'*5)
    try:
        p = int(request.GET.get('p', 1))
    except ValueError:
        p = 1
    try:
        user_profile = models.Profile.objects.get(user__username=user_name)
        posts = models.Posts.objects.filter(user__username=user_name).order_by('-date')
        pages = Paginator(posts, posts_limit)
        if p > pages.num_pages:
            p = pages.num_pages
        if p < 1:
            p = 1
        return render(
            request,
            'registration/profile.html',
            {
                'profile': user_profile,
                'posts': pages.page(p),
                'page': p,
                'num_pages': int(pages.num_pages)
            }
        )
    except (User.DoesNotExist, models.Profile.DoesNotExist):
        return redirect('home')


# Create your views here.
def home(request):
    # print(request.method)
    # posts = Posts.objects.all()
    # # for po in posts:
    # #     print(po['title'])
    # data = {'posts': posts}
    return render(request, 'posts/index.html')


def show_posts(request):
    posts_limit = 50
    print(request.GET)
    try:
        p = int(request.GET.get('p', 1))
    except ValueError:
        p = 1

    # date
    if request.GET.get('d'):
        date = datetime.datetime.strptime(request.GET['d'], '%Y-%m-%d')
        date_to = date + datetime.timedelta(days=1)
        date_query = (Q(date__gte=date) & Q(date__lt=date_to))
    else:
        date_query = Q()
    # all query
    if request.GET.get('s'):
        s = request.GET['s']

        q1 = models.Posts.objects.filter(
            date_query & Q(title__contains=s) & ~Q(content__contains=s)
        ).order_by('-date')

        print(q1.query)

        # q2 = models.Posts.objects.filter(
        #     date_query & ~Q(title__contains=s) & ~Q(content__contains=s)
        # ).order_by('-date')
        #
        # print(q2.query)

        # pages = Paginator(list(q1) + list(q2), posts_limit)
        pages = Paginator(list(q1), posts_limit)


    else:
        q = models.Posts.objects.filter(date_query).order_by('-date').all()
        print(q.query)
        pages = Paginator(q, posts_limit)

    if p > pages.num_pages:
        p = pages.num_pages
    if p < 1:
        p = 1
    print(pages.count)
    return render(
        request, 'posts/posts.html',
        {
            'posts': pages.page(p),
            'search_str': request.GET.get('s', ''),
            'search_date': request.GET.get('d', ''),
            'page': p,
            'num_pages': int(pages.num_pages),
        }
    )


def show_post(request):
    posts_ = Posts.objects.all()
    return render(request, 'posts/index.html', {'posts': posts_})


@transaction.atomic
def update_post(request, post_id):
    print('UPDATE FUNC')

    try:
        user_post = models.Posts.objects.get(id=post_id)

        if request.user != user_post.user and not request.user.is_superuser:
            return HttpResponseNotAllowed(request)

    except models.Posts.DoesNotExist:
        return HttpResponseNotFound(request)

    if request.method == 'GET':
        return render(request, 'posts/create.html',
                      {'title': user_post.title,
                       'content': user_post.content,
                       'delete': True,
                       'post_id': post_id})
    elif request.method == 'POST':
        print(request.POST)

        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''

        if title and content:
            update_fields = []

            if user_post.title != title:
                update_fields.append('title')
                user_post.title = title

            if user_post.content != content:
                update_fields.append('content')
                user_post.content = content

            # user_post.save(update_fields=update_fields or None)

            return redirect('/posts')

        else:
            error = 'Укажите все поля!'
            return render(request, 'posts/create.html',
                          {'title': title,
                           'content': content,
                           'error': error,
                           'delete': True,
                           'post_id': post_id}
                          )


def delete(request, post_id):
    if request.method == 'POST':
        try:
            models.Posts.objects.get(id=post_id).delete()
            return redirect('/posts/')
        except models.Posts.DoesNotExist:
            return HttpResponseNotFound(request)
    else:
        return HttpResponseNotAllowed(request)


# def post(request, post_id):
#     print("POST")
#     print(type(post_id), post_id)
#
#     if request.method == 'GET':
#         print("param: ", request.GET)
#     query_to_bd = (request.GET.get('prise_min'), request.GET.get('prise_max'))
#     return render(request, 'posts/post.html', {'content': request.GET})
#
#     # try:
#     #     user_post = Posts.objects.get(id=post_id)
#     #     return render(request, 'posts/post.html', {'content': request.GET})
#     # except:
#     #     return 1

def post(request, post_id):
    try:
        user_post = models.Posts.objects.get(id=post_id)
        print('***', user_post.user, '***')
        author = user_post.user.username

        return render(request,
                      'posts/user_post.html',
                      {
                          'post': user_post,
                          'user': author})
    except models.Posts.DoesNotExist:
        return HttpResponseNotFound(request)


# def post_with_two(request, other: int, post_id: int):
#     print(post_id)
#     if request.method == 'GET':
#         print("param: ", request.GET)
#     query_to_bd = (request.GET.get('prise_min'), request.GET.get('prise_max'))
#     return render(request, 'posts/post.html', {'content': request.GET})
#
#
# def post_str(request, post_id: str):
#     print(post_id)
#     post_content = request.headers
#     return render(request, 'posts/post.html', {'content': post_content})
#

# return render(request, 'posts/post.html')


def about(request):
    return render(request, 'posts/about.html', {'content': 'Начальная страница'})
    # return HttpResponse('<h1>hello</h1>', status=404)


# def create_post(request):
#     form = PostCreateForm()
#     data = {
#         'form': form
#     }
#     # user_form = PostCreateForm()
#     print("create FUNC")
#     print(request.method)
#     # user_form = CreateForm()
#     if request.method == 'GET':
#         return render(request, 'posts/create.html', data)
#     elif request.method == 'POST':
#         form = PostCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             error = "error"
#         print(request.POST)
#         title = request.POST['title'] or ''
#         content = request.POST['content'] or ''
#         user = request.user
#         if title and content:
#             user_post = Posts(title=title, content=content, user=user)
#             user_post.save()
#             return redirect('/posts')
#         else:
#             error = 'Укажите все поля'
#             return render(request, 'posts/create.html', {'title': title, 'content': content, 'error': error})

def create_post(request):
    # user_form = PostCreateForm()
    print("create FUNC")
    print(request.method)
    # user_form = CreateForm()
    if request.method == 'GET':
        return render(request, 'posts/create.html')
    elif request.method == 'POST':
        print(request.POST)
        title = request.POST['title'] or ''
        content = request.POST['content'] or ''
        if title and content:
            user_post = Posts(title=title, content=content, user=request.user)
            user_post.save()
            return redirect('/posts')
        else:
            error = 'Укажите все поля'
            return render(request, 'posts/create.html', {'title': title, 'content': content, 'error': error, 'form':form})
