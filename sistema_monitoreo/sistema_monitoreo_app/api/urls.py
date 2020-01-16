from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sistema_monitoreo_app.api.views import (MedicionListAPIView,
                                    ReglasView,
                                    MedicionMinMaxDates,)

app_name = 'api'
urlpatterns = [
    path("mediciones/", MedicionListAPIView.as_view(), name="medicion-list"),
    path("reglas/", ReglasView.as_view(), name="regla-list"),
    path('data_mediciones/', MedicionListAPIView.as_view(), name='data-mediciones'),
    path('min_max_dates/', MedicionMinMaxDates.as_view(), name='dates-mediciones'),
]
