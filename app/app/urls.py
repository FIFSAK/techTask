from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from django.urls import path
from main.views import user_registration, upload_file_view, user_info_view, user_files_view, delete_file_view, \
    get_one_file, download_file_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin/new_token', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', user_registration, name='signup'),
    path('file/upload/', upload_file_view, name='upload_file'),
    path('api/user-info/', user_info_view, name='user-info'),
    path('file/list/', user_files_view, name='user-files'),
    path('file/delete/<int:id>/', delete_file_view, name='delete-file'),
    path('file/<int:id>/', get_one_file, name='get_file_id'),
    path('file/download/<int:id>/', download_file_view, name='download-file'),
]
