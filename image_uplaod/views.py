from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage
from .forms import UploadImageForm
from django.shortcuts import get_object_or_404, redirect
from PIL import Image,ImageOps 
from django.http import HttpResponseBadRequest
from io import BytesIO
from .forms import ImageUploadForm
from django.views import View
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.utils import timezone
from .forms import ImageUploadForm
from django.contrib import messages
from django.core.files.base import ContentFile
import io



# Create a global list to store the uploaded image URLs
# uploaded_images = []
# Create your views here.


@login_required
def HomePage(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['image']
            image_type = form.cleaned_data['image_type']

            orientation = get_image_orientation(uploaded_file)
            img = Image.open(uploaded_file)

            # Resize and crop based on orientation
            if orientation == 'portrait':
                img = ImageOps.exif_transpose(img)
                img.thumbnail((1080, 608))
                img = ImageOps.fit(img, (1080, 608), method=0, bleed=0.0, centering=(0.5, 0.5))
            elif orientation == 'landscape':
                img.thumbnail((1080, 1350))
                img = ImageOps.fit(img, (680,1070), method=0, bleed=0.0, centering=(0.5, 0.5))

            # Save the original image
            fs = FileSystemStorage()
            filename_original = fs.save(uploaded_file.name, uploaded_file)

            # Save the resized image
            output = io.BytesIO()
            img.save(output, format='JPEG')
            filename_resized = fs.save(f"resized_{uploaded_file.name}", ContentFile(output.getvalue()))

            # Create UploadedImage instances associated with the current user
            uploaded_image_original = UploadedImage.objects.create(user=request.user, image=filename_original, orientation=orientation)
            uploaded_image_resized = UploadedImage.objects.create(user=request.user, image=filename_resized, orientation=orientation)

            # Update the upload_time fields with the current timestamp
            uploaded_image_original.upload_time = timezone.now()
            uploaded_image_resized.upload_time = timezone.now()
            uploaded_image_original.save()
            uploaded_image_resized.save()

            messages.success(request, 'Image uploaded and processed successfully!')
            return redirect('display_image')
        else:
            messages.error(request, 'Error uploading image. Please check the Image type and try again.')

    user_images = UploadedImage.objects.filter(user=request.user).order_by('orientation', '-upload_time')
    form = ImageUploadForm()
    username = request.user.username

    return render(request, 'home.html', {'user_images': user_images, 'form': form, 'username': username})


def get_image_orientation(image):
    img = Image.open(image)
    width, height = img.size
    return 'portrait' if height > width else 'landscape'




# Delete page function
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)
    image.delete()
    return redirect('display_image')


# Display page view
def display_image(request):
    uploaded_images = UploadedImage.objects.all()
    return render(request, {'uploaded_images': uploaded_images})


# Sign up page view
# def SignupPage(request):
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')

#         if pass1!=pass2:
#             return HttpResponse("Your password and confrom password are not Same!!")
#         else:

#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#             return redirect('login')
        



#     return render (request,'signup.html'
def SignupPage(request):
    error_message = None

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
            except Exception as e:
                error_message = f"Error:This account already exists."

    return render(request, 'signup.html', {'error_message': error_message})



# Login page View
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')


# View for the logout page
def LogoutPage(request):
    logout(request)
    return redirect('login')



# View class displaying user-associated images, requiring user authentication.
# @method_decorator(login_required, name='dispatch')
# class UserImageView(View):
#     template_name = 'user_image.html'

#     def get(self, request, user_id, *args, **kwargs):
#         user_images = UploadedImage.objects.filter(user__id=user_id)
#         print("User image>>>",user_images)  # Add a print statement to check if user_images is empty
#         return render(request, self.template_name, {'user_images': user_images})




# View class displaying user-specific images, requiring user authentication.
@method_decorator(login_required, name='dispatch')
class DisplayImageView(View):
    template_name = 'display.html'

    def get(self, request, *args, **kwargs):
        # Retrieve user-specific images for display, ordered by upload_time in descending order
        user_images = UploadedImage.objects.filter(user=request.user).order_by('-upload_time')
        return render(request, self.template_name, {'user_images': user_images})

    def post(self, request, *args, **kwargs):
        # Handle form submission
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['image']
            orientation = get_image_orientation(uploaded_file)

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)

            # Create UploadedImage associated with the current user
            UploadedImage.objects.create(user=request.user, image=filename, orientation=orientation)

            return redirect('display_image')  # Redirect to the display_image view

        # If form is not valid, re-render the page with the form and existing images
        user_images = UploadedImage.objects.filter(user=request.user).order_by('-upload_time')
        return render(request, self.template_name, {'user_images': user_images, 'form': form})
