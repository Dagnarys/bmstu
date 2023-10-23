from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

# def hello(request):
#     return HttpResponse('Hello World!')

# def hello(request):
#     return render(request, 'index.html', {'data': {
#         'current_date': date.today(),
#         'list': ['python', 'django', 'html']
#     }})
database = [
    {
        "driver_id": 1,
        "driver_name": "Иванова Анна Александровна",
        "driver_passport": 1234567890,
        "driver_age": 18,
        "driver_number": 9999999,

    },
    {
        "driver_id": 2,
        "driver_name": "Петров Михаил Викторович",
        "driver_passport": 1234567890,
        "driver_age": 18,
        "driver_number": 9999999,

    },
    {
        "driver_id": 3,
        "driver_name": "Сидорова Елена Петровна",
        "driver_passport": 1234567890,
        "driver_age": 18,
        "driver_number": 9999999,

    },
    {
        "driver_id": 4,
        "driver_name": "Козлов Игорь Дмитриевич",
        "driver_passport": 1234567890,
        "driver_age": 18,
        "driver_number": 9999999,

    },
    {
        "driver_id": 5,
        "driver_name": "Григорьева Ольга Сергеевна",
        "driver_passport": 1234567890,
        "driver_age": 18,
        "driver_number": 9999999,

    },
    {
        "driver_id": 6,
        "driver_name": "Никитин Артем Валентинович",
        "driver_passport": 1234567890,
        "driver_age": 18,
        "driver_number": 9999999,

    }
]


def GetDrivers(request):
    return render(request, 'orders.html', {'data': {
        'current_date': date.today(),
        'orders': database
    }})

#
def GetDriver(request, driver_id=None):
    if (driver_id is not None) and (driver_id != 0):
        # Обработка GET-запроса с параметром driver_id
        if driver_id is not None:
            order = None
            for obj in database:
                if obj['driver_id'] == int(driver_id):
                    order = obj
                    break
            if order is None:
                raise Http404("object not found")
            filtered_services = [order]

        return render(request, 'services.html', {'filtered_services': filtered_services})


    else:
        filter_keyword = request.GET.get('FullName')
        filtered_services = []

        # Остальная логика фильтрации
        if filter_keyword:
            filtered_services = [service for service in database if
                                 filter_keyword.lower() in service["driver_name"].lower()]

        return render(request, 'orders.html', {'data': {'orders': filtered_services}})


# def filter(request):
#     filter_keyword = request.GET.get('filter_keyword')
#
#     print(filter_keyword)
#
#     if not filter_keyword:
#         return HttpResponseBadRequest("Укажите ключевое слово")
#     else:
#         filter_keyword = str(filter_keyword)
#         filtered_services = []
#         filtered_services = [service for service in database if
#                              filter_keyword.lower() in service["driver_name"].lower()]
#         return render(request, 'services.html', {'filtered_services': filtered_services})


