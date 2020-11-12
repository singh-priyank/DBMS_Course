from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to = 'assets/images',
        default = 'no-img.jpg',
        blank=True
    )
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='none@email.com')
    birth_date = models.DateField(default='1999-12-31')
    bio = models.TextField(default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    favorite_animal = models.CharField(max_length=255, default='')
     = models.CharField(max_length=255, default='')
	university = models.CharField(max_length=255, default='')


    def __str__(self):
        return self.user.username
