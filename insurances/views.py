import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import create_access_token
from .utils import identity_user
from .permissions import *
from .serializers import *
from .models import *

access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


def get_draft_insurance_id(request):
    user = identity_user(request)

    if user is None:
        return None

    insurance = Insurance.objects.filter(employer_id=user.pk).filter(status=1).first()

    if insurance is None:
        return None

    return insurance


@api_view(["GET"])
def search_driver(request):
    """
    Возвращает список водителей
    """

    # Получим параметры запроса из URL
    name = request.GET.get('query')

    # Получение данные после запроса с БД (через ORM)
    driver = Driver.objects.filter(status=1)

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if name:
        driver = driver.filter(name__icontains=name)

    serializer = DriverSerializer(driver, many=True)

    draft_insurance = get_draft_insurance_id(request)

    resp = {
        "draft_insurance_id": draft_insurance.pk if draft_insurance else None,
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
@permission_classes([IsModerator])
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_driver(request):
    """
    Добавляет новый водитель
    """
    driver = Driver.objects.create()

    serializer = DriverSerializer(driver)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
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
@permission_classes([IsAuthenticated])
def add_driver_to_insurance(request, driver_id):
    """
    Добавляет водителя в страховку
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)

    insurance = Insurance.objects.filter(status=1).last()

    # Increment insurance ID if the insurance is already occupied
    while insurance is not None and insurance.drivers.filter(pk=driver_id).exists():
        new_insurance_id = insurance.pk + 1
        insurance = Insurance.objects.filter(pk=new_insurance_id, status=1).last()

    if insurance is None:
        insurance = Insurance.objects.create(date_created=timezone.now(), date_formation=None, date_complete=None)

    insurance.name = "Страховка №" + str(insurance.pk)
    insurance.employer = CustomUser.objects.get(pk=user_id)

    if insurance.drivers.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance.drivers.add(driver)
    insurance.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_driver_image(request, driver_id):
    """
    Возвращает фото водителя
    """
    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)

    return HttpResponse(driver.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
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
@permission_classes([IsAuthenticated])
def get_insurances(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user = CustomUser.objects.get(pk=payload["user_id"])

    status= int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    insurances = Insurance.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        insurances = insurances.filter(employer_id=user.pk)

    if status > 0:
        insurances = insurances.filter(status=status)

    if date_start:
        # insurances = insurances.filter(date_formation__gte=datetime.strptime(date_start, "%Y-%m-%d").date())
        insurances = insurances.filter(date_formation__gte=parse_datetime(date_start))

    if date_end:
        # insurances = insurances.filter(date_formation__lte=datetime.strptime(date_end, "%Y-%m-%d").date())
        insurances = insurances.filter(date_formation__lte=parse_datetime(date_end))

    serializer = InsuranceSerializer(insurances, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_insurance_by_id(request, insurance_id):
    """
    Возвращает информацию о конкретном водителе
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)
    serializer = InsuranceSerializer(insurance)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_insurance(request, insurance_id):
    """
    Обновляет информацию о водителе
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)

    serializer = InsuranceSerializer(insurance, data=request.data, many=False, partial=True)

    if serializer.is_valid():

        serializer.save()

    return Response(serializer.data)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])

def update_user(request):
    """
    Обновляет информацию о пользователе
    """
    user = identity_user(request)

    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        # Get the user instance
        user_instance = CustomUser.objects.get(pk=user.pk)

        # Update user data based on the request data
        user_instance.name = request.data.get('name', user_instance.name)
        user_instance.email = request.data.get('email', user_instance.email)

        # Save the updated user data
        user_instance.save()

        # Serialize and return the updated user data
        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(["POST"])
@permission_classes([IsRemoteService])
def update_insurance_amount(request, insurance_id):
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)
    serializer = InsuranceSerializer(insurance, data=request.data, many=False, partial=True)
    print(insurance.premium_amount)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def calc_amount(insurance_id):
    data = {
        "insurance_id": insurance_id
    }
    print(insurance_id)
    requests.post("http://127.0.0.1:8080/calc_amount/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, insurance_id):
    """
    Пользователь обновляет информацию о водителе
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
            insurance.date_formation = datetime.now()
            insurance.save()

    calc_amount(insurance_id)

    serializer = InsuranceSerializer(insurance)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, insurance_id):
    """
    Модератор обновляет информацию о водителе
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])
    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance = Insurance.objects.get(pk=insurance_id)

    if insurance.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # insurance.status = request_status
    # insurance.date_complete = datetime.now()
    # insurance.moderator = CustomUser.objects.get(pk=user_id)
    # insurance.save()

    if request_status == 4:
        insurance.date_complete = None
    else:
        insurance.date_complete = datetime.now()

    insurance.status = request_status
    insurance.moderator = CustomUser.objects.get(pk=user_id)
    insurance.save()

    serializer = InsuranceSerializer(insurance, many=False)
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

    if insurance.drivers.count() == 0:
        insurance.delete()
        return Response(status=status.HTTP_201_CREATED)

    serializer = DriverSerializer(insurance.drivers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check(request):
    user = identity_user(request)

    user = CustomUser.objects.get(pk=user.pk)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, access_token_lifetime)

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response
