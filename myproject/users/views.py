from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegistrationForm
from django.views.decorators.csrf import csrf_exempt 


def is_admin(user):
    return user.is_admin if hasattr(user, 'is_admin') else False

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = False  # Default to regular user
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and not is_admin(user):
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid user credentials')
    
    return render(request, 'login.html')

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect

def admin_login_view(request):
    # Hardcoded admin credentials
    hardcoded_username = 'adminUser'
    hardcoded_password = 'admin@123'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check against hardcoded credentials
        if username == hardcoded_username and password == hardcoded_password:
            # Get the custom user model
            User = get_user_model()

            # Retrieve or create the admin user
            user, created = User.objects.get_or_create(
                username=hardcoded_username,
                defaults={'is_superuser': True, 'is_staff': True}
            )
            if created:
                user.set_password(hardcoded_password)
                user.save()

            # Authenticate the user
            user = authenticate(request, username=hardcoded_username, password=hardcoded_password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                messages.error(request, 'Authentication failed for admin user.')
        else:
            messages.error(request, 'Invalid admin credentials')

    return render(request, 'admin_login.html')

    # Hardcoded admin credentials
    hardcoded_username = 'adminUser'
    hardcoded_password = 'admin@123'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check against hardcoded credentials
        if username == hardcoded_username and password == hardcoded_password:
            # Get the custom user model
            User = get_user_model()

            # Try to retrieve the admin user, or create one if it doesn't exist
            user, created = User.objects.get_or_create(
                username=hardcoded_username,
                defaults={'is_superuser': True, 'is_staff': True}
            )
            if created:
                user.set_password(hardcoded_password)
                user.save()

            # Authenticate and log in the user
            user = authenticate(request, username=hardcoded_username, password=hardcoded_password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Authentication failed for admin user.')
        else:
            messages.error(request, 'Invalid admin credentials')

    return render(request, 'admin_login.html')

    # Hardcoded admin credentials
    hardcoded_username = 'adminUser'
    hardcoded_password = 'admin@123'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check against hardcoded credentials
        if username == hardcoded_username and password == hardcoded_password:
            # Log in the user
            user = authenticate(request, username=hardcoded_username, password=hardcoded_password)

            if user is None:  # If user doesn't exist, create a temporary admin user
                from django.contrib.auth.models import User
                user = User.objects.create_superuser(username=hardcoded_username, password=hardcoded_password)
                user.save()

            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials')

    return render(request, 'admin_login.html')

@login_required
@user_passes_test(lambda u: not is_admin(u))
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login') 


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import GasServiceRequest
from .forms import GasServiceRequestForm
from django.views.decorators.http import require_http_methods

@login_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def user_dashboard(request):
    if request.method == 'POST':
        # Print debug information
        print("POST data:", request.POST)
        print("CSRF token in session:", request.session.get('csrf_token'))
        
        form = GasServiceRequestForm(request.POST)
        if form.is_valid():
            gas_request = form.save(commit=False)
            gas_request.user = request.user
            gas_request.save()
            return redirect('user_dashboard')
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)
    else:
        form = GasServiceRequestForm()
    
    # Get user's recent requests
    recent_requests = GasServiceRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recent_requests': recent_requests
    }
    return render(request, 'user_dashboard.html', context)