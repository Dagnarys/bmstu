from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .database import Database
from .models import Driver


def GetDrivers(request):
    filter_keyword = request.GET.get('full_name')

    if filter_keyword is None:
        drivers = Driver.objects.filter(status=True)
    else:
        drivers = Driver.objects.filter(full_name__icontains=filter_keyword, status=True)

    return render(request, 'drivers.html', {'data': {
        'current_date': date.today(),
        'drivers': drivers
    }})


def GetDriver(request, id):
    try:
        driver = Driver.objects.get(id=id, status=True)
        return render(request, 'driver.html', {'data': {'driver': driver}})
    except Driver.DoesNotExist:
        return render(request, 'driver.html', {'data': {'driver': None}})


def DeleteDriverByID(request):
    if request.method == 'POST':

        id_driver = int(request.POST.get('id_driver'))
        if (id_driver is not None):
            # Выполняем SQL запрос для редактирования статуса
            DB = Database()
            DB.connect()
            DB.update_status_delete_driver(status=False, id_driver=id_driver)
            DB.close()
        # Перенаправим на предыдующую ссылку после успешного удаления
        return redirect('drivers')
