from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


# ================== SIGNUP ==================
@api_view(['POST'])
def signup_view(request):
    fullname = request.data.get("fullname")
    username = request.data.get("username")
    password = request.data.get("password")

    if not fullname or not username or not password:
        return Response({"detail": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"detail": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=fullname
    )

    return Response({
        "message": "Account created successfully"
    })


# ================== LOGIN ==================
@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "Username and password required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=401)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "username": user.username
    })


# ================== LOGOUT ==================
@api_view(['POST'])
def logout_view(request):
    if request.auth:
        request.auth.delete()

    return Response({"message": "Logged out successfully"})