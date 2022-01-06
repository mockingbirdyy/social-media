from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    def get_absolute_url(self):
        return reverse('posts:each_post', args=[self.created.year, self.created.month, self.created.day, self.slug])

    def like_count(self):
        return self.post_vote.count()

    def can_like(self, user):
        user_vote = user.user_vote.all()
        query = user_vote.filter(post=self)
        if query.exists():
            return True
        return False

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    body = models.TextField(max_length=500)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comment_reply', null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.body[:30]}'

    class Meta:
        ordering = ('-created',)


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_vote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_vote')

    def __str__(self):
        return f'{self.user}-{self.post}'
