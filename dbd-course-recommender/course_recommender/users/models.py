from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
# name, email, last_login are in auth_user
class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    image = models.ImageField( upload_to='student/%Y/%m/%d',blank=True, null = True)
    gender = models.CharField(max_length=2,choices=GENDER_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=80, blank=True, null=True)
    occupation = models.CharField(max_length=80, blank=True, null=True)
    graduated_university = models.CharField(max_length=80, blank=True, null=True)
    # email = models.CharField(max_length=80, blank=True, null=True)
    account = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    stream = models.ForeignKey('course.Domain', on_delete=models.CASCADE, null = True, blank=True)
    # last_login = models.DateTimeField(blank=True, null=True)
    dob = models.DateField(max_length=8, null = True, blank=True)
    number=models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f'{self.account.username}'


