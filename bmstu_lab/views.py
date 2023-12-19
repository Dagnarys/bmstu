from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *
from datetime import datetime, timezone

@api_view(["GET"])
def search_driver(request):
    """
    Возвращает список страховок
    """
    def get_draft_insurance_id():
        insurance = Insurance.objects.filter(status=1).first()
        if insurance is None:
            return None
        return insurance.pk

    # Получим параметры запроса из URL
    full_name = request.GET.get('full_name')


    # Получение данные после запроса с БД (через ORM)
    driver = Driver.objects.filter(status=1)

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if full_name:
        driver = driver.filter(full_name__icontains=full_name)


    serializer = DriverSerializer(driver, many=True)
    # для работы с лаб4
    # return Response(serializer.data)

    resp = {
        "draft_insurance": get_draft_insurance_id(),
        "drivers": serializer.data
    }
    return Response(resp)


@api_view(['GET'])
def get_driver_by_id(request, driver_id):
    """
    Возвращает информацию о конкретном водителе
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Получение данные после запроса с БД (через ORM)
    driver = Driver.objects.get(pk=driver_id)

    serializer = DriverSerializer(driver, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_driver(request, driver_id):
    """
    Обновляет информацию о водителе
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)
    serializer = DriverSerializer(driver, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_driver(request):
    """
    Добавляет новый водителя
    """
    Driver.objects.create()

    drivers = Driver.objects.all()
    serializer = DriverSerializer(drivers, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_driver(request, driver_id):
    """
    Удаляет водителя
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)
    driver.status = 2
    driver.save()

    drivers = Driver.objects.filter(status=1)
    serializer = DriverSerializer(drivers, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_driver_to_insurance(request, driver_id):
    """
    Добавляет водителя в страховку
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)

    insurance = Insurance.objects.filter(status=1).last()

    if insurance is None:
        insurance = Insurance.objects.create(date_created=datetime.now(timezone.utc), date_of_formation=None, date_complete=None)

    insurance.drivers.add(driver)
    insurance.save()

    serializer = InsuranceSerializer(insurance.drivers, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_driver_image(request, driver_id):
    """
    Возвращает фото водителя
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Driver.objects.get(pk=driver_id)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_driver_image(request, driver_id):
    """
    Обновляет фото водителя
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)
    serializer = DriverSerializer(driver, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)




@api_view(["GET"])
def get_insurances(request):
    """
    Возвращает список страховок
    """
    insurances = Insurance.objects.all()

    # Получим параметры запроса из URL
    status = request.GET.get('status')
    date_created = request.GET.get('date_created')
    date_complete = request.GET.get('date_complete')
    date_form_after = request.GET.get('date_form_after')
    date_form_before = request.GET.get('date_form_before')

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if status:
        insurances = insurances.filter(status=status)
    if date_created:
        insurances = insurances.filter(date_created=date_created)
    if date_complete:
        insurances = insurances.filter(date_complete=date_complete)

    # Дата формирования ПОСЛЕ
    if date_form_after and date_form_before is None:
        insurances = insurances.filter(date_of_formation__gte=date_form_after)
    # Дата формирования ДО
    if date_form_after is None and date_form_before:
        insurances = insurances.filter(date_of_formation__lte=date_form_before)

    # Дата формирования ПОСЛЕ и ДО
    if date_form_after and date_form_before:
        if date_form_after > date_form_before:
            return Response('Mistake! It is impossible to sort when "BEFORE" exceeds "AFTER"!')
        insurances = insurances.filter(date_of_formation__gte=date_form_after, date_of_formation__lte=date_form_before)

    serializer = InsuranceSerializer(insurances, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_insurance_by_id(request, insurance_id):
    """
    Возвращает информацию о конкретной страховке
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)
    serializer = InsuranceSerializer(insurance, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_insurance(request, insurance_id):
    """
    Обновляет информацию о страховке
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)
    serializer = InsuranceSerializer(insurance, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    insurance.status = 1
    # if insurance.status == 1:
    #     insurance.date_created = datetime.now()
    insurance.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, insurance_id):
    """
    Пользователь обновляет информацию о страховке
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)

    if insurance.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        insurance.status = 2
        insurance.save()
        if insurance.status == 2:
            insurance.date_of_formation = datetime.now()

            insurance.save()

    serializer = InsuranceSerializer(insurance, many=False)
    return Response(serializer.data)

@api_view(["PUT"])
def update_status_admin(request, insurance_id):
    """
    Модератор обновляет информацию о страховке
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance = Insurance.objects.get(pk=insurance_id)

    insurance_status = insurance.status

    if insurance_status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance.status = request_status
    insurance.save()

    serializer = InsuranceSerializer(insurance, many=False)
    return Response(serializer.data)

@api_view(["DELETE"])
def delete_insurance(request, insurance_id):
    """
    Удаляет страховку
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)

    if insurance.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance.status = 5
    insurance.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_driver_from_insurance(request, insurance_id, driver_id):
    """
    Удаляет водителя из страховки
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)
    insurance.drivers.remove(Driver.objects.get(pk=driver_id))
    insurance.save()

    serializer = DriverSerializer(insurance.drivers, many=True)

    return Response(serializer.data)