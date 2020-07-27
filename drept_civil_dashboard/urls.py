"""drept_civil_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from data_management import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('authenticate/', views.authenticate_redirect_view, name='authentication'),
    path('logout/', views.logout_redirect_view, name='logout'),
    path('view/courses/general', views.manage_courses_general_view, name='view_courses_general'),
    path('view/courses/detailed', views.manage_courses_detailed_view, name='view_courses_detailed'),
    path('view/questions/general', views.manage_questions_view_general, name='view_questions_general'),
    path('view/questions/detailed', views.manage_questions_view_detailed, name='view_questions_detailed'),
    path('view/chapters', views.manage_chapters_view, name='view_chapters'),
    path('view/courses/add', views.manage_courses_add_view, name='add_courses'),
    path('view/questions/add', views.manage_questions_add_view, name='add_questions'),
    path('view/chapters/add', views.manage_chapters_add_view, name='add_chapters'),
    path('view/courses/edit', views.manage_courses_edit_view, name='edit_courses'),
    path('view/questions/edit', views.manage_questions_edit_view, name='edit_questions'),
    path('view/chapters/edit', views.manage_chapters_edit_view, name='edit_chapters'),
    path('manage/courses/add', views.manage_courses_add),
    path('manage/questions/add', views.manage_questions_add),
    path('manage/chapters/add', views.manage_chapters_add),
    path('manage/courses/edit', views.manage_courses_edit),
    path('manage/questions/edit', views.manage_questions_edit),
    path('manage/chapters/edit', views.manage_chapters_edit),
    path('manage/courses/remove', views.manage_courses_remove),
    path('manage/questions/remove', views.manage_questions_remove),
    path('manage/chapters/remove', views.manage_chapters_remove),
    path('', views.dashboard_view, name='dashboard')
]
