from django.db import models
import os


# class User(models.Model):
#     phone_or_email = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=50)


class File(models.Model):
    name = models.CharField(max_length=100)
    extension = models.CharField(max_length=10, blank=True)
    MIME_type = models.CharField(max_length=50)
    size = models.PositiveIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Определение расширения файла
        self.extension = os.path.splitext(self.name)[1].lower().strip('.')
        super(File, self).save(*args, **kwargs)
