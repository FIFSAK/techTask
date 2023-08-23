import os

from django.contrib.auth.decorators import login_required

from .models import File
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import FileForm


def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        # return redirect('')  # или куда-либо ещё после регистрации
    return render(request, 'signup.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Determine file attributes
            file_name, file_extension = os.path.splitext(uploaded_file.name)
            file_size = uploaded_file.size
            mime_type = uploaded_file.content_type

            # Create a new File instance and save
            new_file = File(
                user=request.user,  # добавить эту строку
                name=file_name,
                extension=file_extension,
                MIME_type=mime_type,
                size=file_size,
                file=uploaded_file  # заменить uploaded_file на file, потому что в модели это поле называется file
            )
            new_file.save()

            # return redirect('success_url')  # replace 'success_url' with your desired redirect
    else:
        form = FileForm()
    return render(request, 'upload.html', {'form': form})


