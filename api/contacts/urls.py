from django.urls import path
from . import views
urlpatterns =[

    path('list/',views.ContactListAPView.as_view()),
    path('create/',views.ContactCreateAPView.as_view()),


]