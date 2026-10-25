from django.contrib import admin
from django.urls import path, include
from home.views import home_page, edit_employee, delete_employee

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('edit/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('delete/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('chatbot/', include('chatbot.urls')),
]