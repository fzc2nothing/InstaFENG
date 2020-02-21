from django.db import models

from django.urls import reverse

from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField

class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True,
        )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='my_posts', # we can use author.posts to get all posts belong to this user
        )
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
    upload_to='static/images/posts',
    format = 'JPEG',
    options={'quality':100},
    blank=True,
    null = True
    )

     

    def get_like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail',args = [str(self.id)])



class PostTwo(models.Model):
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
    upload_to='static/images/posts',
    format = 'JPEG',
    options={'quality':100},
    blank=True,
    null = True
    )



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title

