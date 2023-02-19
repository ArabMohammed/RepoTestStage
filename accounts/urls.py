from django.urls import path
from .views import RegisterView,RetrieveUserView,ImageProfileUpdateAPIView,GetImageProfileAPIView,ProfileUpdateAPIView
from django.conf import settings
from django.conf.urls.static import static
#accounts/
urlpatterns = [
    path('register',RegisterView.as_view()),
    path('me/', RetrieveUserView.as_view()),
    path('me/updateprofile/', ProfileUpdateAPIView.as_view()),
    path('<id>/profileimage/',GetImageProfileAPIView.as_view()),
    path('me/profilimage/update/',ImageProfileUpdateAPIView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
