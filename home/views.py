from django.shortcuts import render, redirect
from .models import Employee


def home_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')

        Employee.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            department=department
        )

        return redirect('home')

    employees = Employee.objects.all()
    return render(request, 'home/index.html', {'employees': employees})


def edit_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        employee.full_name = request.POST.get('full_name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.department = request.POST.get('department')

        employee.save()

        return redirect('home')

    return render(request, 'home/edit_employee.html', {'employee': employee})
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = Employee.objects.get(id=employee_id)
        employee.delete()

    return redirect('home')