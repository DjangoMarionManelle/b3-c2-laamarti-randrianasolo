# Create your views here.
from django.shortcuts import render, redirect
from .models import User, SchoolCourse, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_authenticated:
        context = {}
        username = request.user.username
        shcool_course_list = SchoolCourse.objects.all()
        if shcool_course_list:
            context["username"] = username
            return render(request, 'myapp/home.html', locals())
        else:
            context["error"] = "Sorry no course availiable"
            return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findcourse(request):
    context = {}
    if request.method == 'POST':
        course_name_r = request.POST.get('course_name')
        date_r = request.POST.get('date')
        shcool_course_list = SchoolCourse.objects.filter(Q(course_name=course_name_r))
        if shcool_course_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "Sorry no course availiable"
            return render(request, 'myapp/findcourse.html', context)
    else:
        return render(request, 'myapp/findcourse.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('school_course_id')
        if id_r == "":
            context["error"] = "Please provide a valid course ID."
            return render(request, 'myapp/error.html', context)
        try:
            school_course = SchoolCourse.objects.get(id=id_r)
            if school_course:
                name_r = school_course.course_name
                schoolname_r = school_course.school_name
                date_r = school_course.date
                time_r = school_course.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                book = Book.objects.create(name=username_r, email=email_r, user_id=userid_r, course_name=name_r,
                                           school_course_id=id_r, date=date_r, time=time_r, school_name=schoolname_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry there is no course available"
                return render(request, 'myapp/findcourse.html', context)
        except SchoolCourse.DoesNotExist:
            context["error"] = "Sorry this course does not exist"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findcourse.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('school_course_id')
        if id_r == "":
            context["error"] = "Please provide a valid course ID."
            return render(request, 'myapp/error.html', context)
        try:
            book = Book.objects.get(id=id_r)
            if book.status == 'CANCELLED':
                context["error"] = "This course has already been cancelled."
                return render(request, 'myapp/error.html', context)
            else:
                book.status = 'CANCELLED'
                book.save()
                return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry, you have not booked that course."
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/home.html')

@login_required(login_url='signin')
def seebookings(request):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(user_id=id_r).order_by('-id')
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no course booked"
        return render(request, 'myapp/booklist.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
