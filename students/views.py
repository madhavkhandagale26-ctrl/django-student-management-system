from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Student
from .forms import StudentForm

def register(request):

    if request.method == 'POST':

        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not username or not email or not password:
            return render(
                request,
                'students/register.html',
                {'error': 'All fields are required.'}
            )

        if password != confirm_password:
            return render(
                request,
                'students/register.html',
                {'error': 'Passwords do not match.'}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'students/register.html',
                {'error': 'Username already exists.'}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                'students/register.html',
                {'error': 'Email is already registered.'}
            )

        try:
            validate_password(password)

        except ValidationError as e:
            return render(
                request,
                'students/register.html',
                {'error': ' '.join(e.messages)}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'students/register.html')

@login_required
def home(request):

    total_students = Student.objects.count()

    total_courses = (
        Student.objects
        .values('course')
        .distinct()
        .count()
    )

    recent_students = Student.objects.order_by('-id')[:5]

    course_counts = (
        Student.objects
        .values('course')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    return render(
        request,
        'students/home.html',
        {
            'total_students': total_students,
            'total_courses': total_courses,
            'recent_students': recent_students,
            'course_counts': course_counts,
        }
    )


@login_required
def add_student(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('students')

    else:
        form = StudentForm()

    return render(
        request,
        'students/add_student.html',
        {'form': form}
    )

@login_required
def students(request):

    query = request.GET.get('search', '')
    course = request.GET.get('course', '')
    sort = request.GET.get('sort', '')

    # Get all students first
    student_list = Student.objects.all()

    # Search by name
    if query:
        student_list = student_list.filter(
            name__icontains=query
        )

    # Filter by course
    if course:
        student_list = student_list.filter(
            course__iexact=course
        )

    # Sorting
    if sort == 'name':
        student_list = student_list.order_by('name')

    elif sort == '-name':
        student_list = student_list.order_by('-name')

    elif sort == 'oldest':
        student_list = student_list.order_by('id')

    else:
        student_list = student_list.order_by('-id')

    # Pagination
    paginator = Paginator(student_list, 5)

    page_number = request.GET.get('page')

    student_list = paginator.get_page(page_number)

    # Get available courses
    courses = (
        Student.objects
        .values_list('course', flat=True)
        .distinct()
        .order_by('course')
    )

    return render(
        request,
        'students/students.html',
        {
            'students': student_list,
            'query': query,
            'course': course,
            'courses': courses,
            'sort': sort,
        }
    )

@login_required
def edit_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect('students')

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'students/edit_student.html',
        {'form': form}
    )

@login_required
def delete_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('students')

    return render(
        request,
        'students/delete_student.html',
        {'student': student}
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'students/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'students/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def student_detail(request, id):
    student = Student.objects.get(id=id)

    return render(
        request,
        'students/student_detail.html',
        {'student': student}
    )