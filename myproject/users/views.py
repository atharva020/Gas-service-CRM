from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .forms import RegistrationForm, GasServiceRequestForm
from .models import GasServiceRequest, CustomUser

def is_admin(user):
    return user.is_admin if hasattr(user, 'is_admin') else False

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = False
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_protect
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

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('admin_dashboard')

    hardcoded_username = 'adminUser'
    hardcoded_password = 'admin@123'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == hardcoded_username and password == hardcoded_password:
            try:
                admin_user = CustomUser.objects.get(username=hardcoded_username)
            except CustomUser.DoesNotExist:
                admin_user = CustomUser.objects.create_user(
                    username=hardcoded_username,
                    email='admin@example.com',
                    password=hardcoded_password,
                    is_staff=True,
                    is_superuser=True,
                    is_admin=True
                )

            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                messages.success(request, 'Successfully logged in as admin')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid admin credentials')
        else:
            messages.error(request, 'Invalid admin credentials')
    return render(request, 'admin_login.html')

@login_required
@user_passes_test(lambda u: not is_admin(u))
def user_dashboard(request):
    if request.method == 'POST':
        form = GasServiceRequestForm(request.POST)
        if form.is_valid():
            gas_request = form.save(commit=False)
            gas_request.user = request.user
            gas_request.save()
            messages.success(request, 'Service request submitted successfully')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Error in form submission')
    else:
        form = GasServiceRequestForm()
    
    recent_requests = GasServiceRequest.objects.filter(
        user=request.user
    ).order_by('-updated_at')
    
    context = {
        'form': form,
        'recent_requests': recent_requests,
        'user': request.user
    }
    return render(request, 'user_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    status_filter = request.GET.get('status', None)
    service_requests = GasServiceRequest.objects.all()
    
    if status_filter:
        service_requests = service_requests.filter(status=status_filter)
    
    service_requests = service_requests.order_by('-created_at')
    
    context = {
        'service_requests': service_requests,
        'user': request.user,
        'status_choices': GasServiceRequest.STATUS_CHOICES,
        'current_filter': status_filter
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
@require_POST
def update_request_status(request, request_id):
    try:
        service_request = get_object_or_404(GasServiceRequest, id=request_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(GasServiceRequest.STATUS_CHOICES):
            service_request.status = new_status
            service_request.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Status updated successfully',
                'new_status': service_request.get_status_display(),
                'updated_at': service_request.updated_at.strftime("%d %b %Y %H:%M")
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid status value'
            }, status=400)
    except Exception:
        return JsonResponse({
            'success': False,
            'message': 'Request not found'
        }, status=404)

def get_user_requests(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=403)
    
    requests = GasServiceRequest.objects.filter(user=request.user).order_by('-updated_at')
    data = [{
        'id': req.id,
        'status': req.status,
        'status_display': req.get_status_display(),
        'updated_at': req.updated_at.strftime("%M d, Y H:i")
    } for req in requests]
    
    return JsonResponse({'requests': data})

def logout_view(request):
    logout(request)
    return redirect('login')