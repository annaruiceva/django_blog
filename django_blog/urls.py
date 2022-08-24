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
from django.urls import path, re_path, include
import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static

import post
from post import views, urls

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('fake/users', views.fake_create_user, name='create_users'),

                  path('', views.about, name='home'),
                  path('posts/', include('post.urls')),

                  # path('home', views.home, name='home'),
                  path('accounts/', include('django.contrib.auth.urls')),

                  path('__debug__/', include('debug_toolbar.urls')),
                  # path('creditor/', include('creditor_uploader.urls')),

                  # path('posts/<post_id>', views.post_str),
                  # path('posts/<int:other>/post_id', views.post_with_two)
                  # re_path(r'posts/\s+/(?P<post_id>)', views.post),
                  # re_path(r'posts|post/(?P<post_id>)')
                  # path('about', views.about, name='about'),
                  # path('post/create', views.create_post, name='create_post')

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
