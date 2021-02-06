from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.db.models import Avg
import math

class Platform(models.Model):
    name = name = models.CharField(max_length=80, blank=True, null=True)
    image = models.ImageField(upload_to='platform/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'{self.name}'

class Domain(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    image = models.ImageField(upload_to='domain/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to='category/%Y/%m/%d', blank=True)


    def __str__(self):
        return f'{self.name} | {self.domain.name}'
        
class Course(models.Model):
    LEVEL_CHOICES = (
        ('A', 'Avanced'),
        ('B', 'Beginner'),
        ('I', 'Intermediate')
    )
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    course_describtion = models.TextField(blank=True, null=True)
    instructor = models.CharField(max_length=80, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null =True)
    image = models.ImageField(upload_to='course/%Y/%m/%d', blank=True, null =True)
    cost = models.BooleanField(default= False, null =True)
    link = models.URLField(null= True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null = True)
    language = models.CharField(max_length=80, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, blank= True, null=True)
    certificate = models.BooleanField(default= True, null =True)

    @property
    def ratings(self):
        rating_list = SubjectRating.objects.filter(subject = self)
        count = len(rating_list)
        if count == 0:
            return [True,False,False,False,False]
        s=0
        for i in range(count):
            s+=rating_list[i].rating
        arr=[False,False,False,False,False,]
        ceil = math.ceil(s/count)
        for i in range(ceil):
            arr[i]=True
        return arr
    @property
    def people(self):
        rating_list = SubjectRating.objects.filter(subject = self)
        count = len(rating_list)
        return count
    
    def __str__(self):
        return f'{self.name}'

class SubjectRating(models.Model):
    subject = models.ForeignKey(Course,on_delete=models.CASCADE, null = True)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, null = True)
    rating = models.IntegerField(default = 1)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    @property
    def ratings(self):
        arr=[False,False,False,False,False,]
        for i in range(self.rating):
            arr[i]=True
        return arr
    
    def __str__(self):
        return f'Course: {self.subject.name} | Student: {self.student.account.username} | Rating: {self.rating}'


class Enrollment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null =True)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, null = True)
    status = models.IntegerField(blank=True, null=True)
    #completed = models.BooleanField(default= False, blank=True, null=True)
    # lesson = models.ForeignKey('Lesson', models.DO_NOTHING, db_column='lesson', blank=True, null=True)

    def __str__(self):
        return f'Student {self.student.account.username} | Course: {self.course.name}'