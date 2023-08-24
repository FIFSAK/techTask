import os
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import FileSerializer
from .models import File
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
import json
from rest_framework.response import Response
from django.http import FileResponse, Http404


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
def user_files_view(request):
    user = request.user
    user_files = File.objects.filter(user=user)

    # Serialize the user's files
    serializer = FileSerializer(user_files, many=True)

    return Response(serializer.data)


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


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_file_view(request, id):  # Notice the 'id' parameter here
    try:
        file_instance = File.objects.get(id=id)
    except File.DoesNotExist:
        raise Http404("File not found.")

    # Check if the authenticated user is the owner of the file or is an admin
    if request.user == file_instance.user or request.user.is_staff:
        file_instance.delete()
        return Response({'message': 'File deleted successfully.'}, status=200)
    else:
        return Response({'message': 'Permission denied.'}, status=403)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_one_file(request, id):
    try:
        user_file = File.objects.get(id=id)
    except File.DoesNotExist:
        return Response({'message': 'File not found.'}, status=404)

    # Check if the authenticated user is the owner of the file or is an admin
    if request.user != user_file.user and not request.user.is_staff:
        return Response({'message': 'Permission denied.'}, status=403)

    # Serialize the user's file
    serializer = FileSerializer(user_file)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def download_file_view(request, id):
    try:
        file_instance = File.objects.get(id=id)
    except File.DoesNotExist:
        raise Http404("File not found.")

    # Check if the authenticated user is the owner of the file, an admin, or if you want to allow everyone to download
    if request.user != file_instance.user and not request.user.is_staff:
        return Response({'message': 'Permission denied.'}, status=403)

    # Serve the file for download
    response = FileResponse(file_instance.file)
    response['Content-Disposition'] = f'attachment; filename="{file_instance.name}{file_instance.extension}"'
    return response


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_file_view(request, id):
    try:
        file_instance = File.objects.get(id=id)
    except File.DoesNotExist:
        return JsonResponse({'message': 'File not found.'}, status=404)

    # Check if the authenticated user is the owner of the file or an admin
    if request.user != file_instance.user and not request.user.is_staff:
        return JsonResponse({'message': 'Permission denied.'}, status=403)

    # Handle file update
    if 'file' in request.FILES:
        file_instance.file.delete()  # Delete the old file
        uploaded_file = request.FILES['file']
        name, extension = os.path.splitext(uploaded_file.name)
        file_instance.file = uploaded_file
        file_instance.name = name
        file_instance.extension = extension
        file_instance.MIME_type = uploaded_file.content_type
        file_instance.size = uploaded_file.size
        file_instance.save()
        return JsonResponse({'message': 'File updated successfully'})
    else:
        return JsonResponse({'message': 'No file part in the request'}, status=400)
