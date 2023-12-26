from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/drivers/search/', search_driver),  # GET
    path('api/drivers/<int:driver_id>/', get_driver_by_id),  # GET
    path('api/drivers/<int:driver_id>/update/', update_driver),  # PUT
    path('api/drivers/<int:driver_id>/delete/', delete_driver),  # DELETE
    path('api/drivers/create/', create_driver),  # POST
    path('api/drivers/<int:driver_id>/add_to_insurance/', add_driver_to_insurance),  # POST
    path('api/drivers/<int:driver_id>/image/', get_driver_image),  # GET
    path('api/drivers/<int:driver_id>/update_image/', update_driver_image),  # PUT

    # Набор методов для заявок
    path('api/insurances/', get_insurances),  # GET
    path('api/insurances/<int:insurance_id>/', get_insurance_by_id),  # GET
    path('api/insurances/<int:insurance_id>/update/', update_insurance),  # PUT
    path('api/insurances/<int:insurance_id>/calc_amount/', calc_amount),  # POST
    path('api/insurances/<int:insurance_id>/update_status_user/', update_status_user),  # PUT
    path('api/insurances/<int:insurance_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/insurances/<int:insurance_id>/delete/', delete_insurance),  # DELETE
    path('api/insurances/<int:insurance_id>/delete_driver/<int:driver_id>/', delete_driver_from_insurance),  # DELETE

    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]