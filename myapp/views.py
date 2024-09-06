# myapp/views.py
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from .models import Profile
from .forms import CustomUserCreationForm
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.core.files.storage import FileSystemStorage
from .models import VerificationRequest

FACE_API_KEY = 'LaS4yjF5zKNEz_ColwERkOLvvHCrN0E1'
FACE_API_SECRET = 'l6OYofWBC3RM_JCDe_fjM_jzQqB4Hr4n'
# Function to verify age using Face++ API
def verify_age_with_faceplusplus(image_base64):
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    params = {
        'api_key': FACE_API_KEY,
        'api_secret': FACE_API_SECRET,
        'image_base64': image_base64.split(',')[1],  # Remove 'data:image/jpeg;base64,'
        'return_attributes': 'age',
    }
    response = requests.post(url, data=params)
    data = response.json()
    if data and 'faces' in data and len(data['faces']) > 0:
        age = data['faces'][0]['attributes']['age']['value']
        return age > 18
    return False

@csrf_exempt
def verify_age(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_base64 = data.get('image_base64')
            if image_base64:
                is_verified = verify_age_with_faceplusplus(image_base64)
                return JsonResponse({'is_verified': is_verified})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'is_verified': False})

@csrf_exempt
def request_verification(request):
    if request.method == 'POST' and request.FILES.get('verification_file'):
        verification_file = request.FILES['verification_file']
        fs = FileSystemStorage()
        filename = fs.save(verification_file.name, verification_file)
        file_url = fs.url(filename)

        # Save verification request to the database
        VerificationRequest.objects.create(user=request.user, file_url=file_url)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# View for superuser to manage verification requests
@user_passes_test(lambda u: u.is_superuser)
def manage_verification_requests(request):
    if request.method == 'POST':
        verification_id = request.POST.get('verification_id')
        action = request.POST.get('action')
        verification_request = VerificationRequest.objects.get(id=verification_id)
        
        if action == 'approve':
            # Approve the verification request
            verification_request.user.is_verified = True
            verification_request.user.save()
            verification_request.delete()  # Remove the request after approval
            return redirect('login_successful')
        elif action == 'reject':
            # Reject the verification request
            verification_request.delete()
            return redirect('waiting_for_verification')

    # Fetch all verification requests to show to the superuser
    requests = VerificationRequest.objects.all()
    return render(request, 'myapp/manage_verification_requests.html', {'requests': requests})

def waiting_for_verification(request):
    return render(request, 'myapp/waiting_for_verification.html')
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the form and create a new user
            form.save()
            # Retrieve username and password from cleaned data
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Authenticate the user
            user = authenticate(username=username, password=raw_password)
            # Log in the user
            if user is not None:
                login(request, user)
                # Redirect to a success page after login
                return redirect('login_successful')
    else:
        # Instantiate the form for a GET request
        form = CustomUserCreationForm()

    # Render the signup page with the form
    return render(request, 'myapp/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        image_base64 = request.POST.get('image_base64')  # Get the base64 image from the frontend
        if form.is_valid() and verify_age(image_base64):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login_successful')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})

def login_successful(request):
    return render(request, 'myapp/login_successful.html')
