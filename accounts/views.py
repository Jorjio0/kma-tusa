import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Реєстрація",
        responses={
            201: RegisterSerializer,
            400: OpenApiResponse(description="Дані не пройшли перевірку."),
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info("Зареєстровано користувача %s (id=%s)", user.username, user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Реєстрація не вдалася, помилки в полях: %s", list(serializer.errors)
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            logger.warning("Невдала спроба входу для користувача %s", username)
            raise
        logger.info("Користувач %s увійшов", username)
        return response


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        summary="Поточний користувач",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Немає токена або токен невалідний."),
        },
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
