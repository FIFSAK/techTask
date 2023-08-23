from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from django.urls import path
from main.views import user_registration, upload_file_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin/new_token', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', user_registration, name='signup'),
    path('file/upload/', upload_file_view, name='upload_file'),
]
