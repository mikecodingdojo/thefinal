from django.db import models
import re 

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if len(postdata['first_name']) < 2 or len(postdata['last_name']) < 2:
            errors['name'] = "Your name must be at least 2 characters"
        if not email_checker.match(postdata['email']):
            errors['email'] = 'Email must be valid'
        if postdata['password'] != postdata['password_confirm']:
            errors['password'] = 'Password and Confirm Password do not match'
        return errors
    def login_validator(self, postdata):

        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_checker.match(postdata['email']):
            errors['email'] = 'Email must be valid'
        if len(postdata['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    objects = UserManager()
    # created_at = models.DateField(auto_now=True)
    # updated_at = models.DateField(auto_now_add=True)
    

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    #What I have added
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    # created_at = models.DateField(auto_now=True)
    # updated_at = models.DateField(auto_now_add=True)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
    # created_at = models.DateField(auto_now=True)
    # updated_at = models.DateField(auto_now_add=True)

class Upload(models.Model):
    file = models.FileField(upload_to="user_images")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None, related_name="upload")
    