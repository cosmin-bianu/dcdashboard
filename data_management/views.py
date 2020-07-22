from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login
import logging


# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
logger = logging.getLogger(__name__)

def login_view(request):
    context = {}
    context["form"] = LoginForm
    return render(request, "login.html", context=context)

def authenticate_redirect_view(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            logger.error('Invalid credentials.')
            return redirect('login')
    else:    
        logger.error('Not a POST request. Request method: ' + request.method)
        return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    context = {}
    context["username"] = request.user.username
    return render(request, "dashboard.html", context)
    
