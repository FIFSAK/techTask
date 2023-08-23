import os

from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated

from .models import File
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import FileForm
from django.http import JsonResponse
from .models import File


def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        # return redirect('')  # или куда-либо ещё после регистрации
    return render(request, 'signup.html')


from django.http import JsonResponse
from .models import File


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_file_view(request):
    if request.method == 'POST' and request.FILES['file']:
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
