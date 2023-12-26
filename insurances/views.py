from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import create_access_token
from .permissions import *
from .serializers import *
from .models import *

access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


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
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_driver(request):
    """
    Добавляет новый водителя
    """
    Driver.objects.create()

    drivers = Driver.objects.all()
    serializer = DriverSerializer(drivers, many=True)

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
    user_id = payload['user_id']

    if not Driver.objects.filter(pk=driver_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    driver = Driver.objects.get(pk=driver_id)

    insurance = Insurance.objects.filter(status=1).last()

    if insurance is None:
        insurance = Insurance.objects.create(date_created=datetime.now(timezone.utc), date_of_formation=None,
                                             date_complete=None)

    insurance.drivers.add(driver)
    insurance.user = CustomUser.objects.get(pk=user_id)
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

    status_id = int(request.GET.get("status", -1))
    user_id = int(request.GET.get("user", -1))

    date_form_after = request.GET.get("date_form_after")
    date_form_before = request.GET.get("date_form_before")
    insurances = Insurance.objects.exclude(status__in=[2, 5]) if user.is_moderator else Insurance.objects.filter(user_id=user.pk)

    if status_id != -1:
        insurances = insurances.filter(status=status_id)

    if user_id != -1:
        insurances = insurances.filter(user_id=user_id)

    if date_form_after:
        insurances = insurances.filter(date_of_formation__gte=datetime.strptime(date_form_after, "%Y-%m-%d").date())

    if date_form_before:
        insurances = insurances.filter(date_of_formation__lte=datetime.strptime(date_form_before, "%Y-%m-%d").date())

    serializer = InsuranceSerializer(insurances, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

    # insurance.status = 1
    # insurance.save()

    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsRemoteService])
def calc_amount(request, insurance_id):
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)
    serializer = InsuranceSerializer(insurance, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsModerator])
def update_status_admin(request, insurance_id):
    """
    Модератор обновляет информацию о страховке
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload['user_id']

    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance = Insurance.objects.get(pk=insurance_id)

    insurance_status = insurance.status

    if insurance_status in [3, 4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance.status = request_status
    insurance.date_complete = datetime.now()
    insurance.moderator = CustomUser.objects.get(pk=user_id)
    insurance.save()

    serializer = InsuranceSerializer(insurance, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_insurance(request, insurance_id):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]
    """
    Удаляет страховку
    """
    if not Insurance.objects.filter(pk=insurance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    insurance = Insurance.objects.get(pk=insurance_id)

    insurance_status = insurance.status
    if insurance_status not in [1]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    insurance.status = 5
    insurance.date_complete = datetime.now()
    insurance.save()

    insurances = Insurance.objects.filter(user_id=user_id).exclude(status__in=[5])
    serializer = InsuranceSerializer(insurances, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


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

    serializer = DriverSerializer(insurance.drivers, many=True)

    return Response(serializer.data)


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
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check credentials
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
    cache.set(access_token, user_data, access_token_lifetime)

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
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
