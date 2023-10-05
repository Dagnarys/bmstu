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
        "polis_number": 1,
        "polis_cost": 1000,
        "polis_start": "01.01.2024",
        "polis_end": "01.01.2025",
        "polis_ts": "Модель 1",
        "polis_number_ts": "AB123CD",
        "polis_drivers": [
            {
                "name": "Водитель 4",
                "passport": "1234567890",
                "id_driver": "AB123456",
                "age": 30
            },
            {
                "name": "Водитель 5",
                "passport": "0987654321",
                "id_driver": "CD789012",
                "age": 25
            }
        ]
    },
    {
        "polis_number": 2,
        "polis_cost": 1500,
        "polis_start": "02.01.2024",
        "polis_end": "02.01.2025",
        "polis_ts": "Модель 2",
        "polis_number_ts": "XY456YZ",
        "polis_drivers": [
            {
                "name": "Водитель 4",
                "passport": "1234567890",
                "id_driver": "AB123456",
                "age": 30
            },
            {
                "name": "Водитель 5",
                "passport": "0987654321",
                "id_driver": "CD789012",
                "age": 25
            }
        ]
    },
    {
        "polis_number": 3,
        "polis_cost": 800,
        "polis_start": "03.01.2024",
        "polis_end": "03.01.2025",
        "polis_ts": "Модель 3",
        "polis_number_ts": "PQ789RS",
        "polis_drivers": [
            {
                "name": "Водитель 4",
                "passport": "1234567890",
                "id_driver": "AB123456",
                "age": 30
            },
            {
                "name": "Водитель 5",
                "passport": "0987654321",
                "id_driver": "CD789012",
                "age": 25
            }
        ]
    },
    {
        "polis_number": 4,
        "polis_cost": 1500,
        "polis_start": "04.01.2024",
        "polis_end": "04.01.2025",
        "polis_ts": "Модель 4",
        "polis_number_ts": "UV101WZ",
        "polis_drivers": [
            {
                "name": "Водитель 4",
                "passport": "111122223333",
                "id_driver": "XY987654",
                "age": 35
            },
            {
                "name": "Водитель 5",
                "passport": "555566667777",
                "id_driver": "ZW123456",
                "age": 28
            }
        ]
    },
    {
        "polis_number": 5,
        "polis_cost": 900,
        "polis_start": "05.01.2024",
        "polis_end": "05.01.2025",
        "polis_ts": "Модель 5",
        "polis_number_ts": "MN222OP",
        "polis_drivers": [
            {
                "name": "Водитель 4",
                "passport": "111122223333",
                "id_driver": "XY987654",
                "age": 35
            },
            {
                "name": "Водитель 5",
                "passport": "555566667777",
                "id_driver": "ZW123456",
                "age": 28
            }
        ]
    },
    {
        "polis_number": 6,
        "polis_cost": 1100,
        "polis_start": "06.01.2024",
        "polis_end": "06.01.2025",
        "polis_ts": "Модель 6",
        "polis_number_ts": "KL333QR",
        "polis_drivers": [
            {
                "name": "Водитель 4",
                "passport": "1234567890",
                "id_driver": "AB123456",
                "age": 30
            },
            {
                "name": "Водитель 5",
                "passport": "555566667777",
                "id_driver": "ZW123456",
                "age": 28
            },
{
                "name": "Водитель 4",
                "passport": "1234567890",
                "id_driver": "AB123456",
                "age": 30
            },
            {
                "name": "Водитель 5",
                "passport": "555566667777",
                "id_driver": "ZW123456",
                "age": 28
            },
{
                "name": "Водитель 4",
                "passport": "1234567890",
                "id_driver": "AB123456",
                "age": 30
            },
            {
                "name": "Водитель 5",
                "passport": "555566667777",
                "id_driver": "ZW123456",
                "age": 28
            },
        ]
    }
]


def GetOrders(request):
    return render(request, 'orders.html', {'data': {
        'current_date': date.today(),
        'orders': database

    }})


# Create your views here.
def GetOrder(request, polis_number):
    order = None
    for obj in database:
        if obj['polis_number'] == polis_number:
            order = obj
            break
    if order is None:
        raise Http404("object not found")
    return render(request, 'order.html', {'data': {
        'current_date': date.today(),
        'order': order
    }})


def sendText(request):
    if request.method == 'POST':

        input_text = request.POST.get('text', '')
        response_text = f"Вы ввели: {input_text}"

        return HttpResponse(response_text)
    else:

        return render(request, 'base.html')


def services(request, polis_number):
    order = None
    for obj in database:
        if obj['polis_number'] == polis_number:
            order = obj
            break
    if order is None:
        raise Http404("object not found")
    return render(request, 'services.html', {
        'filtered_services': [order]  # Передаем только один элемент, а не весь список
    })



def filter(request):
    filter_keyword = request.GET.get('filter_keyword')
    filter_field = request.GET.get('filter_field')
    print(filter_keyword)
    print(filter_field)

    if not filter_keyword or not filter_field:
        return HttpResponseBadRequest("Укажите ключевое слово")

    filter_keyword = str(filter_keyword)
    filtered_services = []

    if filter_field == "polis_number":
        filtered_services = [service for service in database if filter_keyword == str(service["polis_number"])]
    elif filter_field == "polis_ts":
        filtered_services = [service for service in database if filter_keyword in service["polis_ts"]]
    elif filter_field == "polis_number_ts":
        filtered_services = [service for service in database if filter_keyword in service["polis_number_ts"]]
    elif filter_field == "id_driver":
        filtered_services = [service for service in database if any(
            "id_driver" in driver and filter_keyword == driver["id_driver"] for driver in
            service.get("polis_drivers", []))]

    else:
        pass

    return render(request, 'services.html', {'filtered_services': filtered_services})
