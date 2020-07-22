from django.db import models


#TODO
# Create your models here.
class Questionnaire:
    max_question_length=100 #characters
    max_answer_characters=100 #characters
    max_answers=4

    question_id=models.SmallAutoField(primary_key=True)
    question=models.models.CharField(max_length=max_question_length)
    #answers=
    answer_count=models.PositiveSmallIntegerField()
    correct_answer_index=models.PositiveSmallIntegerField()