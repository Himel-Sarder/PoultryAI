from django.db import models
from accounts.models import User


class FarmPost(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.seller.full_name}"

    def get_like_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def get_comment_count(self):
        return self.comments.count()


class PostLike(models.Model):
    post = models.ForeignKey(FarmPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']


class PostComment(models.Model):
    post = models.ForeignKey(FarmPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.full_name}"
