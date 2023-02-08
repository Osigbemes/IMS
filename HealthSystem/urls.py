from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistration, Login, BookAppointment, GetPatientVitals, AcceptOrRejectAppointment, GetAllUsers

app_name = 'HealthSystem'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('get_vitals/', GetPatientVitals.as_view(), name='get_vitals'),
    path('get_users/', GetAllUsers.as_view(), name='get_users'),
    path('appointment/', BookAppointment.as_view(), name='appointment'),
    path('accept_or_reject/<str:pk>', AcceptOrRejectAppointment.as_view(), name='accept_or_reject'),
]