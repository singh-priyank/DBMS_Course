from django.contrib import admin

from course.models import *

admin.site.register(Course)
admin.site.register(Domain)
admin.site.register(Category)
admin.site.register(Platform)
admin.site.register(Enrollment)
admin.site.register(SubjectRating)