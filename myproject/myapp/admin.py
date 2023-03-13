from django.contrib import admin
from .models import SchoolCourse, User, Book

# Register your models here.

admin.site.register(SchoolCourse)
admin.site.register(User)
admin.site.register(Book)
