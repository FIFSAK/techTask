from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
# from .models import User
# from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login

def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        # return redirect('')  # или куда-либо ещё после регистрации
    return render(request, 'signup.html')



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signin(request):
#     if request.method == 'POST':
#         phone_or_email = User.objects.
#         password = request.data.get("password", None)
#         if serializer.is_valid():
#             user = User(**serializer.validated_data)
#             user.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)