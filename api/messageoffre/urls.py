from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
#/api/messages

urlpatterns =[
    path('create/',views.CreateMessageAPIView.as_view()),
    path('updatelist/',views.UpdateBoiteMessageAPIView.as_view()),
    path('infosadministrateur/',views.AdministratorDataAPIView.as_view()),
]