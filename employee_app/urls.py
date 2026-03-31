from django.conf.urls import url,include

from employee_app import views

app_name = 'employee_app'

urlpatterns = [
    # Modern Django 'path' syntax
    path('register/', views.register, name='register'),
]
