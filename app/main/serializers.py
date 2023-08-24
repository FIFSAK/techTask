from rest_framework import serializers
from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'name', 'extension', 'MIME_type', 'size', 'upload_date')
