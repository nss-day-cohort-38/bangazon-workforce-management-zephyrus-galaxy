from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('training_programs/', training_program_list, name='training_programs'),
    path('training_programs/form', training_program_form, name='training_program_form'),
    path('employees/form', employee_form, name='employee_form'),
    path('employees/<int:employee_id>/', employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/form/', employee_edit_form, name='employee_edit_form'),
]
