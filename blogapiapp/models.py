from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title=models.CharField(max_length=10)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    # comment=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')  # Overall Blog table
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
