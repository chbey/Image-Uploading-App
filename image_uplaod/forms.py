# image_upload/forms.py
from django import forms
from .models import UploadedImage
# from django.core.validators import FileExtensionValidator
from PIL import Image


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']


class ImageUploadForm(forms.Form):
    image_type = forms.ChoiceField(
        choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check if the file extension is allowed
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in self.ALLOWED_EXTENSIONS:
                raise forms.ValidationError("Only JPG, GIF, or PNG images are allowed.")

            # Check if the orientation of the image matches the selected image type
            expected_orientation = self.cleaned_data.get('image_type')
            actual_orientation = self.get_image_orientation(image)

            if expected_orientation != actual_orientation:
                raise forms.ValidationError(f"Please select a {expected_orientation.capitalize()} image.")

        return image

    def get_image_orientation(self, image):
        img = Image.open(image)
        width, height = img.size
        return 'portrait' if height > width else 'landscape'
