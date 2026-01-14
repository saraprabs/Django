from django.conf.urls import url,include

from employee_app import views

app_name = 'employee_app'

urlpatterns = [
    
    url(r'^register/', views.register, name='register'),
]