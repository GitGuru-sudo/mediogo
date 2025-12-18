from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient, Helper, Request
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Home Page
def home(request):
    return render(request, 'home.html')

# Patient Login
def patient_login(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        password = request.POST.get('password')
        
        try:
            patient = Patient.objects.get(patient_id=patient_id)
            user = authenticate(username=patient.user.username, password=password)
            
            if user:
                login(request, user)
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient not found')
    
    return render(request, 'patient_login.html')

# Patient Registration
def patient_register(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif Patient.objects.filter(patient_id=patient_id).exists():
            messages.error(request, 'Patient ID already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            Patient.objects.create(user=user, patient_id=patient_id, name=name)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('patient_login')
    
    return render(request, 'patient_register.html')

# Patient Dashboard
@login_required
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
        # Filter requests from last 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        requests = Request.objects.filter(
            patient=patient,
            created_at__gte=seven_days_ago
        ).order_by('-created_at')
        return render(request, 'patient_dashboard.html', {'patient': patient, 'requests': requests})
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please register as a patient.')
        logout(request)
        return redirect('patient_register')

# Create Request
@login_required
def create_request(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please register as a patient.')
        return redirect('patient_register')
    
    if request.method == 'POST':
        floor = request.POST.get('floor')
        time_to_reach = request.POST.get('time_to_reach')
        
        Request.objects.create(
            patient=patient,
            floor=floor,
            time_to_reach=time_to_reach
        )
        messages.success(request, 'Request created successfully!')
        return redirect('patient_dashboard')
    
    return render(request, 'create_request.html')

# Helper Login
def helper_login(request):
    if request.method == 'POST':
        helper_id = request.POST.get('helper_id')
        
        try:
            helper = Helper.objects.get(helper_id=helper_id)
            request.session['helper_id'] = helper_id
            return redirect('helper_dashboard')
        except Helper.DoesNotExist:
            messages.error(request, 'Helper not found')
    
    return render(request, 'helper_login.html')

# Helper Dashboard
def helper_dashboard(request):
    helper_id = request.session.get('helper_id')
    if not helper_id:
        return redirect('helper_login')
    
    helper = get_object_or_404(Helper, helper_id=helper_id)
    # Filter requests from last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    pending_requests = Request.objects.filter(
        is_accepted=False,
        created_at__gte=seven_days_ago
    ).order_by('-created_at')
    accepted_requests = Request.objects.filter(
        helper=helper,
        is_accepted=True,
        created_at__gte=seven_days_ago
    ).order_by('-created_at')
    
    total_requests = pending_requests.count() + accepted_requests.count()
    
    return render(request, 'helper_dashboard.html', {
        'helper': helper,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'total_requests': total_requests
    })

# Accept Request
def accept_request(request, request_id):
    helper_id = request.session.get('helper_id')
    if not helper_id:
        return redirect('helper_login')
    
    helper = get_object_or_404(Helper, helper_id=helper_id)
    req = get_object_or_404(Request, id=request_id)
    
    req.helper = helper
    req.is_accepted = True
    req.save()
    
    messages.success(request, 'Request accepted successfully!')
    return redirect('helper_dashboard')

# Logout
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('home')