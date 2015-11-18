from django import forms

class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=100)
    option1 = forms.CharField(label='Option 1', max_length=25)
    option2 = forms.CharField(label='Option 2', max_length=25)
