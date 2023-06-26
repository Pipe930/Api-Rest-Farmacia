from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from apps.ventas.models import Carrito
from .serializer import UsuarioSerializer
from rest_framework.parsers import JSONParser
from datetime import datetime

class RegisterUserView(generics.CreateAPIView):

    serializer_class = UsuarioSerializer
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "status": "Created",
                "message": "Se registro el usuario correctamente",
                "data": serializer.data
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
                            "id_carrito": carrito.id_carrito,
                        }

                        return Response({"status": "OK", "message": "Se inicio sesion correctamente. Bienvenido " + user.username, "data": userJson}, status.HTTP_200_OK)

                    token.delete()
                    token = Token.objects.create(user=user)
                    login(request=request, user=user)

                    userJson = {
                        "token": token.key,
                        "username": user.username,
                        "user_id": user.id,
                        "activate": user.is_active,
                        "staff": user.is_staff,
                        "id_carrito": carrito.id_carrito
                    }

                    return Response({"status": "OK", "message": "Se inicio sesion correctamente. Bienvenido " + user.username, "data": userJson}, status.HTTP_200_OK)

                return Response({"message": "El usuario no esta activo"},  status.HTTP_401_UNAUTHORIZED)

            return Response({"message": "Credenciales Invalidas"}, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:

            tokenUrl = request.GET.get("token")
            token = Token.objects.filter(key=tokenUrl).first()

            if token: 
                usuario = token.user
                sesiones_todas = Session.objects.filter(expire_date__gte = datetime.now())

                if sesiones_todas.exists():

                    for session in sesiones_todas:
                        session_data = session.get_decoded()

                        if usuario.id == int(session_data.get("_auth_user_id")):
                            session.delete()

                token.delete()
                logout(request=request)

                mensaje_session = "Session de usuario terminada"
                mensaje_token = "Token Eliminado"

                message = {
                    "sesion_message": mensaje_session,
                    "token_message": mensaje_token
                }

                return Response(
                    {
                        "status": "OK", 
                        "message": "Se cerro la sesion con exito", 
                        "messages": message
                        }, status.HTTP_200_OK)

            return Response({"error": "Usuario no encontrado con esas credenciales"},
                            status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"errors": "El token no se a encontrado en la cabecera"}, status.HTTP_409_CONFLICT)