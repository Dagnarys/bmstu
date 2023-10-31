from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .database import Database
from .models import Driver


def GetDrivers(request):
    filter_keyword = request.GET.get('filter_keyword')

    if filter_keyword is None:
        drivers = Driver.objects.filter(status=True)
    else:
        drivers = Driver.objects.filter(name=filter_keyword, status=True)

    return render(request, 'drivers.html', {'data': {
        'current_date': date.today(),
        'drivers': drivers
    }})


def GetDriver(request, driver_id=None):
    driver = Driver.objects.get(id=id)
    return render(request, 'driver.html', {'data': {
        'driver': driver
    }})

def DeleteCityByID(request):
    if request.method == 'POST':
        # Получаем значение city_id из POST-запроса
        driver_id = int(request.POST.get('driver_id'))
        if (driver_id is not None):
            # Выполняем SQL запрос для редактирования статуса
            DB = Database()
            DB.connect()
            DB.update_status_delete_city(status=False, id_driver=driver_id)
            DB.close()
        # Перенаправим на предыдующую ссылку после успешного удаления
        return redirect('drivers')
# database = [
#     {
#         "driver_id": 1,
#         "driver_name": "Иванова Анна Александровна",
#         "driver_passport": 1234567890,
#         "driver_age": 18,
#         "driver_number": 9999999,
#         "driver_photo": "/imgs/img1.png"
#
#     },
#     {
#         "driver_id": 2,
#         "driver_name": "Петров Михаил Викторович",
#         "driver_passport": 1234567890,
#         "driver_age": 18,
#         "driver_number": 9999999,
#         "driver_photo": "/imgs/img2.png"
#
#     },
#     {
#         "driver_id": 3,
#         "driver_name": "Сидорова Елена Петровна",
#         "driver_passport": 1234567890,
#         "driver_age": 18,
#         "driver_number": 9999999,
#         "driver_photo": "/imgs/img3.png"
#
#     },
#     {
#         "driver_id": 4,
#         "driver_name": "Козлов Игорь Дмитриевич",
#         "driver_passport": 1234567890,
#         "driver_age": 18,
#         "driver_number": 9999999,
#         "driver_photo": "/imgs/img4.png"
#
#     },
#     {
#         "driver_id": 5,
#         "driver_name": "Григорьева Ольга Сергеевна",
#         "driver_passport": 1234567890,
#         "driver_age": 18,
#         "driver_number": 9999999,
#         "driver_photo": "/imgs/img5.png"
#
#     },
#     {
#         "driver_id": 6,
#         "driver_name": "Никитин Артем Валентинович",
#         "driver_passport": 1234567890,
#         "driver_age": 18,
#         "driver_number": 9999999,
#         "driver_photo": "/imgs/img6.png"
#
#     }
# ]
#

#
# def GetDriver(request, driver_id=None):
#     if (driver_id is not None) and (driver_id != 0):
#         # Обработка GET-запроса с параметром driver_id
#         if driver_id is not None:
#             order = None
#             for obj in database:
#                 if obj['driver_id'] == int(driver_id):
#                     order = obj
#                     break
#             if order is None:
#                 raise Http404("object not found")
#             filtered_services = [order]
#
#         return render(request, 'driver.html', {'filtered_services': filtered_services})

