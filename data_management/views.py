from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm,ChapterCreationForm,CourseCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
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
        context = {
            "form":LoginForm,
        }
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
        "course_count": Course.objects.count(),
        'disable_column':True,
    }
    return render(request, "dashboard.html", context)
    

#View pages

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_view(request):
    return redirect('login')

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_view(request):
    breadcrumbs = [
        {"name":"Pagina principală", "link":"/"},
        {"name":"Capitole", "link":"#", "current_page":True}
    ]
    context = {
        "page_title": "Capitole",
        "breadcrumbs":breadcrumbs,
        "chapters":Chapter.objects.all(),
    }
    return render(request, "view_chapters.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_general_view(request):
    chapters={}
    for chapter in Chapter.objects.all():
        count=Course.objects.filter(chapter__chapter_id=chapter.chapter_id).count()
        chapters[chapter]=count
        
    breadcrumbs = [
        {"name":"Pagina principală", "link":"/"},
        {"name":"Lecții", "link":"#", "current_page":True}
    ]
    context = {
        "page_title": "Lecții",
        "breadcrumbs":breadcrumbs,
        "chapters":chapters,
    }
    return render(request, "view_courses_general.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_detailed_view(request):
    source_id = request.GET.get("id", None)
    if source_id is not None:
        chapter=Chapter.objects.get(chapter_id=source_id)
        courses=Course.objects.filter(chapter__chapter_id=chapter.chapter_id)
        
        breadcrumbs = [
            {"name":"Pagina principală", "link":"/"},
            {"name":"Lecții", "link":"/view/courses/general"},
            {"name":chapter.name, "link":"#", "current_page":True},
        ]

        processed_courses=[]

        for course in courses:
            processed_courses.append({
                "name":course.name, 
                "author":course.author.get_full_name(),
                "id":course.course_id,
                })

        context={
            "page_title":chapter.name,
            "breadcrumbs":breadcrumbs,
            "courses":processed_courses,
            "source_id":source_id,
        }
        return render(request, "view_courses_detail.html", context)
    else:
        return redirect('dashboard')


#Add pages

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_add_view(request):

    context = {
        "page_title": "Adaugă o întrebare",
    }
            
    return render(request, "add_question.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_add_view(request):
    target_chapter_id=request.GET.get("source_id", None)
    target_chapter=Chapter.objects.get(chapter_id=target_chapter_id)
    context = {
        "page_title": "Adaugă o lecție",
        "form":CourseCreationForm(initial={'chapter':target_chapter, 'author':request.user}),
    }
    return render(request, "add_course.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_add_view(request):
    context = {
        "page_title": "Adaugă un capitol",
        "form":ChapterCreationForm(initial={
            "name":request.GET.get("name",None),
            "order_number":request.GET.get("on",None),
            "description":request.GET.get("desc",None),
        }),
        "status":request.GET.get("status", None),
    }
    return render(request, "add_chapter.html", context)


#Edit pages
@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_edit_view(request):
    #TODO
    return render(request, "edit_course.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_edit_view(request):
    course_id=request.GET.get("id", None)
    course=Course.objects.get(course_id=course_id)
    name=course.name
    author=course.author
    content=course.content
    chapter=course.chapter

    context = {
        "page_title": "Modifică o lecție",
        "form":CourseCreationForm(initial={
            'name':name,
            'author':author,
            'content':content,
            'chapter':chapter}),
        'course_id':course_id
    }
    return render(request, "edit_course.html", context)

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_edit_view(request):
    chapter_id=request.GET.get("id",None)
    chapter=Chapter.objects.get(pk=chapter_id)
    name=chapter.name
    order_number=chapter.order_number
    description=chapter.description
    context = {
        "page_title": "Modifică un capitol",
        "form":ChapterCreationForm(initial={
            "name":request.GET.get("name",name),
            "order_number":request.GET.get("on",order_number),
            "description":request.GET.get("desc",description),
        }),
        "status":request.GET.get("status", None),
        "id":chapter_id,
    }
    return render(request, "edit_chapter.html", context)






################################## API #########################################


# Add API

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_questions_add(request):
    return redirect('view_chapters')

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_courses_add(request):
    name=request.POST.get("name", None)
    author_id=request.POST.get("author", None)
    author=User.objects.get(id=author_id)
    content=request.POST.get("content", None)
    chapter_id=request.POST.get("chapter", None)
    chapter=Chapter.objects.get(chapter_id=chapter_id)
    course=Course(
        name=name,
        author=author,
        content=content,
        chapter=chapter,
    )
    course.save()
    return redirect('/view/courses/detailed?id={}'.format(chapter_id))

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_chapters_add(request):
    name = request.POST.get("name", None)
    order_number = request.POST.get("order_number",None)
    description = request.POST.get("description",None)
    if Chapter.objects.filter(order_number=order_number).count() > 0:
        return redirect('/view/chapters/add?status=1&name={}&on={}&desc={}'.format(name,order_number,description))
    Chapter.create(
        name=name,
        order_number=order_number,
        description=description,
    )
    return redirect('view_chapters')


# Edit API

@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_questions_edit(request):
    #TODO
    return redirect('view_chapters')


@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_courses_edit(request):
    course_id=request.POST.get("course_id", None)
    course=Course.objects.get(pk=course_id)
    name=request.POST.get("name", None)
    author_id=request.POST.get("author", None)
    author=User.objects.get(id=author_id)
    content=request.POST.get("content", None)
    chapter_id=request.POST.get("chapter", None)
    chapter=Chapter.objects.get(chapter_id=chapter_id)

    course.name=name
    course.author=author
    course.content=content
    course.chapter=chapter
    course.save()
    return redirect('/view/courses/detailed?id={}'.format(chapter_id))


@require_http_methods(["POST"])
@login_required(login_url='login')
def manage_chapters_edit(request):
    name = request.POST.get("name", None)
    order_number = request.POST.get("order_number",None)
    description = request.POST.get("description",None)
    chapter_id = request.POST.get("id",None)
    if Chapter.objects.filter(order_number=order_number).count() > 0:
        return redirect('/view/chapters/edit?status=1&name={}&on={}&desc={}&id={}'.format(name,order_number,description,chapter_id))
    chapter=Chapter.objects.get(pk=chapter_id)
    chapter.name=name
    chapter.order_number=order_number
    chapter.description=description
    chapter.save()
    return redirect('view_chapters')
# Remove API
    
@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_questions_remove(request):
    target_id = request.GET.get("id", None)
    Exercise.objects.filter(exercise_id=target_id).delete()
    return redirect('view_chapters')

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_courses_remove(request):
    target_id = request.GET.get("id", None)
    source_id = request.GET.get("source_id", None)
    Course.objects.filter(course_id=target_id).delete()
    return redirect('/view/courses/detailed?id={}'.format(source_id))

@require_http_methods(["GET"])
@login_required(login_url='login')
def manage_chapters_remove(request):
    target_id = request.GET["id"]
    Chapter.objects.filter(chapter_id=target_id).delete()
    return redirect('view_chapters')

#TODO EDIT PAGES

#TODO ADD FISIERE (poate imagini?)