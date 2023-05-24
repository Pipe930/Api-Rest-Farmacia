from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from apps.ventas.models import Carrito
from .serializer import UsuarioSerializer
from rest_framework.parsers import JSONParser

class RegisterUserView(generics.CreateAPIView):

    serializer_class = UsuarioSerializer
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "data": serializer.data,
                "message": "Se Registro Correctamente"
                }, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):

    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():

            user_found = authenticate(
                username = request.data["username"],
                password = request.data["password"]
            )

            if user_found is not None:

                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data["user"]

                if user.is_active:

                    token, created = Token.objects.get_or_create(user=user)
                    carrito, carritoCreado = Carrito.objects.get_or_create(id_usuario=user)

                    if created:

                        login(request=request, user=user)

                        userJson = {
                            "token": token.key,
                            "username": user.username,
                            "id_usuario": user.id,
                            "activate": user.is_active,
                            "staff": user.is_staff,
                            "id_carrito": carrito.id_carrito
                        }

                        return Response(userJson, status.HTTP_200_OK)

                    token.delete()
                    token = Token.objects.create(user=user)

                    userJson = {
                        "token": token.key,
                        "username": user.username,
                        "user_id": user.id,
                        "activate": user.is_active,
                        "staff": user.is_staff,
                        "id_carrito": carrito.id_carrito
                    }

                    return Response(userJson, status.HTTP_200_OK)

                return Response({"message": "El usuario no esta activo"},  status.HTTP_401_UNAUTHORIZED)

            return Response({"message": "Credenciales Invalidas"}, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
