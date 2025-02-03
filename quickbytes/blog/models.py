# from django.db import models
# from django.contrib.auth.models import User

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     media = models.FileField(upload_to='post_media/', blank=True, null=True)

#     def __str__(self):
#         return self.title

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

#     def __str__(self):
#         return f"Comment by {self.author} on {self.post}"

# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_dislike = models.BooleanField(default=False)  # True for dislike, False for like

#     def __str__(self):
#         return f"{'Dislike' if self.is_dislike else 'Like'} by {self.user} on {self.post}"


from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='post_media/', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_dislike = models.BooleanField(default=False)  # True for dislike, False for like

    def __str__(self):
        return f"{'Dislike' if self.is_dislike else 'Like'} by {self.user} on {self.post}"