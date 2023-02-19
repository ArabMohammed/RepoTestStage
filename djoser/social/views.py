from rest_framework import generics, permissions, status
from rest_framework.response import Response
from social_django.utils import load_backend, load_strategy

from djoser.conf import settings
from djoser.social.serializers import ProviderAuthSerializer


class ProviderAuthView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProviderAuthSerializer

    def get(self, request, *args, **kwargs):
        print("welcome in redirect_uri confirmation ")
        redirect_uri = request.GET.get("redirect_uri")
        print(f'redirect_uri : {redirect_uri}')
        if redirect_uri not in settings.SOCIAL_AUTH_ALLOWED_REDIRECT_URIS:
            print("error redirect_uri not in allowed uris")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print("\n")
        print("success")
        strategy = load_strategy(request)
        print("success1")
        strategy.session_set("redirect_uri", redirect_uri)
        print("success2")
        backend_name = self.kwargs["provider"]
        backend = load_backend(strategy, backend_name, redirect_uri=redirect_uri)
        print("success3")
        authorization_url = backend.auth_url()
        print(f"success4 : {authorization_url}")
        print("\n")
        return Response(data={"authorization_url": authorization_url})
