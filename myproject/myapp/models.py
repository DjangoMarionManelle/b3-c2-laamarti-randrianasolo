# Create your models here.
from django.db import models


# Create your models here.

class SchoolCourse(models.Model):
    course_name = models.CharField(max_length=30)
    school_name = models.CharField(max_length=30)
    address = models.CharField(max_length=80)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.course_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    BOOKING_STATUS = ((BOOKED, 'Booked'),
                      (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    user_id = models.DecimalField(decimal_places=0, max_digits=2)
    school_course_id = models.DecimalField(decimal_places=0, max_digits=2)
    course_name = models.CharField(max_length=30)
    school_name = models.CharField(max_length=30, null=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=BOOKING_STATUS,
                              default=BOOKED, max_length=2)

    def __str__(self):
        return self.email
