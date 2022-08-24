"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from post import views as post_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    #
    # path('', views.show_post, name='show_posts'),
    # path('home', views.home, name='home'),
    #
    path('', post_views.show_posts, name='show_posts'),
    path('create', post_views.create_post, name='create_post'),

    path('update/<int:post_id>', post_views.update_post, name='update_post'),
    path('delete/<int:post_id>', post_views.delete, name='delete_post'),

    path('<int:post_id>', post_views.post, name='get_post'),
    path('profile/<user_name>', post_views.profile, name='profile'),
    # # path('posts/<post_id>', views.post_str),
    # # path('posts/<int:other>/post_id', views.post_with_two)
    # # re_path(r'posts/\s+/(?P<post_id>)', views.post),
    # # re_path(r'posts|post/(?P<post_id>)')
    # path('about', post_views.about, name='url_to_about'),

    path('fake/posts', post_views.fake_create_posts, name='create_posts'),

]
