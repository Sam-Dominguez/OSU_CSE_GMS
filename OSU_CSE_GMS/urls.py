"""
URL configuration for OSU_CSE_GMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import administrator, course_detail, student_dashboard, sign_up, student_intake, create_admin, create_instructor, make_assignments, dashboard, instructor_grader_request, instructor_dashboard,instructor_course_detail
from .algo.algo import algoTest
from django.views.generic import RedirectView
import logging

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

    path('algo/', algoTest, name="algoTest"),

    path('thanks/', TemplateView.as_view(template_name="thanks.html"), name="thanks"),
    path('dashboard/',dashboard , name="dashboard"),

    path('sign_up/', sign_up, name='signup'),

    path('administrator/', RedirectView.as_view(url='/administrator/courses/'), name='administrator'),
    path('administrator/courses/', RedirectView.as_view(url='/administrator/dashboard/')),
    path('administrator/dashboard/', administrator, name='administrator_dashboard'),
    path('administrator/courses/<str:course_number>/', course_detail, name='course_detail'),
    path('administrator/create_admin/', create_admin, name='create_admin'),
    path('administrator/create_instructor/', create_instructor, name='create_instructor'),
    path('administrator/make_assignments/', make_assignments, name='make_assignments'),

    path('student/', RedirectView.as_view(url='/student/dashboard/'), name='student'),
    path('student/dashboard/', student_dashboard, name="student_dashboard"),
    path('student/application/', student_intake, name="application"),

    path('instructor/', RedirectView.as_view(url='/instructor/dashboard/'), name='instructor'),
    path('instructor/courses/', RedirectView.as_view(url='/instructor/dashboard/')),
    path('instructor/dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('instructor/courses/<str:course_number>/', instructor_course_detail , name='instructor_course_detail'),
    path('instructor/grader_request/', instructor_grader_request, name='instructor_grader_request')
]   

logger = logging.getLogger('django')

# Code to only run on server restart, allows logs to identify sessions
logger.info("\nSTARTING SERVER\n")