from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer
from .authentication import BearerTokenAuthentication

class RegisterAPI(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # User create হবে

        # Token generate
        token, created = Token.objects.get_or_create(user=user)

        # Response এ User info + Token pathano
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })

# Login API
class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user) 
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response({"error": "Invalid Credentials"}, status=400)

# User Detail API


class UserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

