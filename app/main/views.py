import os
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import File
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
import json
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework.response import Response


@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'detail': 'Username already taken'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({'detail': 'User registered successfully'}, status=201)
    return JsonResponse({'detail': 'Method "GET" not allowed.'}, status=405)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_file_view(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'message': 'No file part in the request'}, status=400)

        uploaded_file = request.FILES['file']
        name, extension = os.path.splitext(uploaded_file.name)
        file_instance = File(
            user=request.user,
            file=uploaded_file,
            name=name,
            extension=extension,
            MIME_type=uploaded_file.content_type,
            size=uploaded_file.size
        )
        file_instance.save()
        return JsonResponse({'message': 'File uploaded successfully'})

    return JsonResponse({'message': 'Failed to upload file'})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_file(request):
    if request.method == 'GET':
        if 'file' not in request.FILES:
            return JsonResponse({'message': 'No file part in the request'}, status=400)

        uploaded_file = request.FILES['file']
        name, extension = os.path.splitext(uploaded_file.name)
        file_instance = File(
            user=request.user,
            file=uploaded_file,
            name=name,
            extension=extension,
            MIME_type=uploaded_file.content_type,
            size=uploaded_file.size
        )
        file_instance.save()
        return JsonResponse({'message': 'File uploaded successfully'})

    return JsonResponse({'message': 'Failed to upload file'})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_info_view(request):
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active
    }
    return Response(data)
