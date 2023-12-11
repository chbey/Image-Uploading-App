from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage
from .forms import UploadImageForm
from django.shortcuts import get_object_or_404, redirect
from PIL import Image
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




# Create a global list to store the uploaded image URLs
# uploaded_images = []
# Create your views here.

# View for the homepage
@login_required
def HomePage(request):
    # Handle form submission
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data['image']
            image_type = form.cleaned_data['image_type']

            # Validate image type based on orientation
            orientation = get_image_orientation(uploaded_file)
            if (orientation == 'portrait' and image_type != 'portrait') or \
               (orientation == 'landscape' and image_type != 'landscape'):
                messages.error(request, f"Please select the correct image type ({orientation.capitalize()}) for the uploaded image.")
                return redirect('home')
            else:
                

                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)

                # Create UploadedImage associated with the current user
                uploaded_image = UploadedImage.objects.create(user=request.user, image=filename, orientation=orientation)

                # Update the upload_time field with the current timestamp
                uploaded_image.upload_time = timezone.now()
                uploaded_image.save()

                messages.success(request, 'Image uploaded successfully!')
                # Redirect to the display page after a successful upload
                return redirect('display_image')
            
        else:
            messages.error(request, 'Error uploading image. Please check the Image type and try again.')

    # Fetch user-specific images and order them by type and time of upload
    user_images = UploadedImage.objects.filter(user=request.user).order_by('orientation', '-upload_time')

    # Separate images based on orientation (portrait and landscape)
    user_portrait_images = user_images.filter(orientation='portrait')
    user_landscape_images = user_images.filter(orientation='landscape')

    # Rearrange images to display Landscape images first, followed by Portrait images
    ordered_user_images = list(user_landscape_images) + list(user_portrait_images)

    form = ImageUploadForm()

    return render(request, 'home.html', {'ordered_user_images': ordered_user_images, 'form': form})

# Add this function to determine image orientation
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
    return render(request, 'user_image.html', {'uploaded_images': uploaded_images})


# Sign up page view
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')



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
