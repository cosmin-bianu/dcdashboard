from django import forms
from data_management.models import Chapter,TwoAnswerExercise,FourAnswerExercise,Course
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input is-rounded is-primary is-medium', 'placeholder':'Nume de utilizator'}))
    password=forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={'class': 'input is-rounded is-primary is-medium', 'placeholder':'Parolă'}))


class ChapterCreationForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ["name","order_number"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input is-medium', 'placeholder':'Numele capitolului'}),
            'order_number': forms.NumberInput(attrs={'class': 'input is-medium', 'placeholder':'Numarul de ordine'}),
        }

class NameModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return obj.name

class FullNameModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return obj.get_full_name()

class CourseCreationForm(forms.ModelForm):
    chapter = NameModelChoiceField(queryset=Chapter.objects.all())
    author=FullNameModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Numele lecției'}), #Textarea
            'content': forms.Textarea(attrs={'class': 'input is-medium mb-3', 'placeholder':'Conținut'}),

        }
