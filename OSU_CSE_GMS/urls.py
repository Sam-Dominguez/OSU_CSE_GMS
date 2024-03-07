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
from .views import administrator, course_detail, student, sign_up, student_intake
from .algo.algo import algoTest
from django.views.generic import RedirectView
import logging

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('administrator/', RedirectView.as_view(url='/administrator/courses/')),
    path('administrator/courses/', administrator, name='administrator'),
    path('administrator/courses/<str:course_number>/', course_detail, name='course_detail'),
    path('sign_up/', sign_up, name='signup'),
    path('student/', student, name="student"),
    path('algo/', algoTest, name="algoTest"),
    path('student/', student, name="student"),
    path('application/', student_intake, name="application"),
    path('thanks/', TemplateView.as_view(template_name="thanks.html"), name="thanks"),
]

logger = logging.getLogger('django')

# Code to only run on server restart, allows logs to identify sessions
logger.info("\nSTARTING SERVER\n")