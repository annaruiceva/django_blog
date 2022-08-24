from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
# Create your models here.
from faker import Faker


class Posts(models.Model):
    pass
    # id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    # для FAKER
    # date = models.DateTimeField(auto_now_add=True)

    title = models.TextField(max_length=100)
    image = models.ImageField(upload_to='posts_img/%Y/%m/%d/', null=True, blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        db_table = 'posts'
        indexes = [
            models.Index(
                name='posts_date_time_idx',
                fields=['date']
            )
        ]
        ordering = ['date']

    def __str__(self):
        return 'Post: ' + self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    hobby = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        db_table = 'profile'
        # indexes = [
        #     models.Index(
        #         name='',
        #         fields=['']
        #     )
        # ]
        # ordering = ['']

class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    obj = models.CharField('model', max_length=10)
    message = models.CharField(max_length=300)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('create profile, sender: ', sender)
    if created:
        print('created', instance)
        f = Faker('ru-RU')
        Profile.objects.create(
            user=instance,
            phone=f.phone_number(),
            address=f.address()
        )
    print('create_profile, **kwargs: ', kwargs)

    # @receiver(post_save, sender=User)
    # def create_post(sender, instance, created, **kwargs):
    #     print('create profile, sender: ', sender)
    #     if created:
    #         print('created', instance)
    #         Posts.objects.create(
    #             user=instance,
    #         )
    #     print('create_post, **kwargs: ', kwargs)


@receiver(post_save, sender=User)
def user_log(sender, instance, created, **kwargs):
    Log.objects.create(
        obj=sender.__class__.__name__,
        message=f'{instance.username} saved: {created}, with: {kwargs}'
    )


@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    Log.objects.create(
        obj=str(type(sender))[:10],
        message=f'{instance.username} has been deleted | {kwargs}'
    )
