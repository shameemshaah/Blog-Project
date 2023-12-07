from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Blog(models.Model):
    gener_choices = (
        ('education','Education'),
        ('movie','Movie'),
        ('politics','Politics'),
        ('others','Others')
    )
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,null=True)
    genre = models.CharField(max_length=20,choices=gener_choices,default='education')
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='image/',null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,related_name='comments',on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)


class UserOTP(models.Model):
    otp = models.CharField(max_length=5)
    user = models.OneToOneField(User, on_delete = models.CASCADE)


        