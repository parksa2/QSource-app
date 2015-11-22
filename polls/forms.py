from django import forms

# Form that generates the HTML required for a user to input their question and
# answer options.
class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=100)
    option1 = forms.CharField(label='Option 1', max_length=25, initial="Yes")
    option2 = forms.CharField(label='Option 2', max_length=25, initial="No")
