from django import forms
from data_management.models import Chapter,FourAnswerExercise,Course
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input is-rounded is-primary is-medium', 'placeholder':'Nume de utilizator'}))
    password=forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={'class': 'input is-rounded is-primary is-medium', 'placeholder':'Parolă'}))


class ChapterCreationForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input is-medium', 'placeholder':'Numele capitolului'}),
            'order_number': forms.NumberInput(attrs={'class': 'input is-medium', 'placeholder':'Numarul de ordine'}),
            'description': forms.Textarea(attrs={'class': 'input is-medium', 'placeholder':'Descriere'}),
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
            'name': forms.TextInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Numele lecției'}),
            'content': forms.Textarea(attrs={'class': 'input is-medium mb-3', 'placeholder':'Conținut'}),
            'order_number': forms.NumberInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Numărul de ordine'}),
        }

class ExerciseCreationForm(forms.ModelForm):
    chapter = NameModelChoiceField(queryset=Chapter.objects.all())
    author=FullNameModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = FourAnswerExercise
        fields = ('question','chapter','author','answer1','answer2','answer3','answer4','correct_answer_index')

        widgets = {
            'question': forms.Textarea(attrs={'class': 'input is-medium mb-3', 'placeholder':'Întrebarea'}),
            'order_number': forms.NumberInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Numărul de ordine'}),
            'answer1': forms.TextInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Opțiunea 1'}),
            'answer2': forms.TextInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Opțiunea 2'}),
            'answer3': forms.TextInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Opțiunea 3'}),
            'answer4': forms.TextInput(attrs={'class': 'input is-medium mb-3', 'placeholder':'Opțiunea 4'}),
            'correct_answer_index': forms.Select(attrs={'class': 'is-medium mb-3'},choices=FourAnswerExercise.correct_answer_index.choices)
        }
