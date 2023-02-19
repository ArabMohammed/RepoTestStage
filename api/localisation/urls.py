from django.urls import path
from . import views
urlpatterns =[
    #path('list/',views.LocalisationListCreateAPView.as_view()),
    #path('create/',views.LocalisationCreateAPView.as_view()),
    #path('<int:pk>/update/',views.LocalisationUpdateAPIView.as_view()),
    path('dict_wilayas_communes/',views.WilayasCommunesListAPIView.as_view()),
]