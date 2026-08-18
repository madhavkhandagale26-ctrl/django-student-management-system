from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='students/password_reset.html'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='students/password_reset_done.html'
    ),
    name='password_reset_done'
),

    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', views.logout_view, name='logout'),

    path('', views.home, name='home'),

    path('add/', views.add_student, name='add_student'),

    path('students/', views.students, name='students'),

    path('student/<int:id>/', views.student_detail, name='student_detail'),

    path('edit/<int:id>/', views.edit_student, name='edit_student'),

    path('delete/<int:id>/', views.delete_student, name='delete_student'),
]