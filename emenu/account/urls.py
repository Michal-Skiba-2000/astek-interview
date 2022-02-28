from django.urls import path
from rest_framework.authtoken import views


app_name = 'account'  # pylint: disable=invalid-name

urlpatterns = [
    path('auth/', views.obtain_auth_token)
]
