# Generated by Django 4.0.5 on 2022-08-20 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]