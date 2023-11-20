from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.filter(author=self.pk)
        val = sum(item.rating for item in posts) * 3
        val += sum(item.rating for item in Comment.objects.filter(user=self.user))
        for post in posts:
            val += sum(item.rating for item in Comment.objects.filter(post=post))
        self.rating = val
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscribe')

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    post_type = models.CharField(max_length=3, choices=[('ART', 'Статья'), ('NEW', 'Новость')], default='NEW')
    datetime_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[0:124]}..."

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    datetime_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscribe(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
