from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm,ChapterCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from data_management.models import TwoAnswerExercise,FourAnswerExercise,Course,Chapter
from django.views.decorators.http import require_http_methods
import logging



# Create your views here.
logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        context = {}
        context["form"] = LoginForm
        return render(request, "login.html", context=context)

#TODO Session timeout
@require_http_methods(["POST"])
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


@require_http_methods(["GET"])
@login_required(login_url='login')
def logout_redirect_view(request):
    logout(request)
    return redirect('login')

@require_http_methods(["GET"])
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        "chapters_count": Chapter.objects.count(), 
        "question_count":  TwoAnswerExercise.objects.count() + FourAnswerExercise.objects.count(),
        "course_count": Course.objects.count()
    }
    return render(request, "dashboard.html", context)
    

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_view(request):
    return redirect('login')

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_view(request):
    return redirect('login')

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_view(request):
    context = {
        "chapters":Chapter.objects.all()
    }
    return render(request, "view_chapters.html", context)



#Add pages

    
@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_add_view(request):
    context = {

    }
    return render(request, "add_question.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_add_view(request):
    context = {

    }
    return render(request, "add_course.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_add_view(request):
    context = {
        "form":ChapterCreationForm()
    }
    return render(request, "add_chapter.html", context)


# Add API

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_questions_add(request):
    return redirect('view_chapters')

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_courses_add(request):
    return redirect('view_chapters')

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_chapters_add(request):
    name=request.POST["name"]
    Chapter.create(name)
    return redirect('view_chapters')

# Remove API
    
@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_remove(request):
    target_id = request.GET["id"]
    Exercise.objects.filter(chapter_id=target_id).delete()
    return redirect('view_chapters')

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_remove(request):
    target_id = request.GET["id"]
    Course.objects.filter(chapter_id=target_id).delete()
    return redirect('view_chapters')

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_remove(request):
    target_id = request.GET["id"]
    Chapter.objects.filter(chapter_id=target_id).delete()
    return redirect('view_chapters')
