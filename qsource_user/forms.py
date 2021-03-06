from django import forms

# Form for generating the HTML so that a user can input text into the input
# fields associated with the "Contact Us" page.
class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
    
# class SignUpForm(forms.ModelForm):
    # class Meta:
        # model = SignUp
        # fields = ['email', 'username']
        # exclude = ['username'] Not recommended
        
    # def clean_email(self):
        # email = self.cleaned_data.get('email')
        # return email
    
    # def clean_username(self):
        # username = self.cleaned_data.get('username')
        # write validation code here
        # return username
