# image_upload/models.py
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
import os
# ORIENTATION_CHOICES = [
#     ('portrait', 'Portrait'),
#     ('landscape', 'Landscape'),
# ]

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uplaods/')
    orientation = models.CharField(max_length=255, choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')],null=True)
    # orientation = models.CharField(max_length=100, choices=ORIENTATION_CHOICES,default='portrait')
    upload_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.user.username}'s {self.orientation} image uploaded at {self.upload_time}"

    # Overrides the default delete method
    def delete(self, *args, **kwargs):
        # Delete the image file when the model instance is deleted
        self.image.delete()
        super().delete(*args, **kwargs)


# Connect post_delete signal to automatically delete associated file
@receiver(models.signals.post_delete, sender=UploadedImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
