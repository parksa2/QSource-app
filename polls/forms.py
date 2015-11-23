from django import forms
from django.core.validators import RegexValidator

# Form that generates the HTML required for a user to input their question and
# answer options.
class QuestionForm(forms.Form):
    alphanumeric = RegexValidator(r'^[\x20-\x7E]*$',
                                  'Only ASCII characters are allowed.')
    question_text = forms.CharField(label='Question', max_length=100, 
                                    validators=[alphanumeric])
    option1 = forms.CharField(label='Option 1', max_length=25, initial="Yes",
                              validators=[alphanumeric])
    option2 = forms.CharField(label='Option 2', max_length=25, initial="No",
                              validators=[alphanumeric])
