from django.db import models
from django.contrib.auth import get_user_model

#TODO
# Create your models here.
class Chapter(models.Model):
    max_name_length=100 #characters
    max_description_length=200 #characters
    
    chapter_id=models.SmallAutoField(primary_key=True)
    name=models.CharField(max_length=max_name_length,default="")
    order_number=models.PositiveSmallIntegerField(unique=True)
    description=models.CharField(max_length=max_description_length,default="")

    @classmethod
    def create(cls, name, order_number,description):
        chapter = cls(
            name=name, 
            order_number=order_number,
            description=description,
            )
        chapter.save()
        return chapter
    
    class Meta:
        ordering=['order_number',]


class Exercise(models.Model):
    class Meta:
        abstract = True
    max_question_length=100 #characters

    question_id=models.SmallAutoField(primary_key=True)
    question=models.CharField(max_length=max_question_length)
    chapter=models.ForeignKey("Chapter", on_delete=models.CASCADE)
    author=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_number=models.SmallIntegerField()
    answer_count=models.SmallIntegerField()


class TwoAnswerExercise(Exercise):
    max_answer_length=100 #characters
    answer1=models.CharField(max_length=max_answer_length)
    answer2=models.CharField(max_length=max_answer_length)
    
    correct_answer_index=models.PositiveSmallIntegerField(choices=(
        (1,"1"),
        (2,"2"),
    ))

class FourAnswerExercise(Exercise):
    max_answer_length=100 #characters
    answer1=models.CharField(max_length=max_answer_length, null=True, blank=True)
    answer2=models.CharField(max_length=max_answer_length, null=True, blank=True)
    answer3=models.CharField(max_length=max_answer_length, null=True, blank=True)
    answer4=models.CharField(max_length=max_answer_length, null=True, blank=True)
    
    correct_answer_index=models.PositiveSmallIntegerField(choices=(
        (1,"1"),
        (2,"2"),
        (3,"3"),
        (4,"4"),
    ))

    class Meta:
        ordering=['order_number',]

class Course(models.Model):
    max_content_length=300 #characters

    course_id=models.SmallAutoField(primary_key=True)
    name=models.CharField(max_length=100) #characters
    author=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content=models.CharField(max_length=max_content_length)
    order_number=models.PositiveSmallIntegerField()
    chapter=models.ForeignKey("Chapter", on_delete=models.CASCADE)
    
    class Meta:
        ordering=['order_number',]