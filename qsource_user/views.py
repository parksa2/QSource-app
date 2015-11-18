from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm

# Create your views here.

def home(request):
    title = 'Sign Up to our Newsletter' 
    #if request.user.is_authenticated():
    #    title = "Welcome to QSource %s" %(request.user)
    
    #add a form
    
    #if request.method == "POST":
    #    print request.POST
    #form = SignUpForm(request.POST or None)
    
    context = {
        "title": title,
        #"form": form
    }
    return render(request, "home.html", context)
    
    if form.is_valid():
        #form.save()
        #print request.POST['email'] Not secured. Not recommended.
        instance = form.save(commit=False)
        
        username = form.cleaned_data.get("username")
        if not username:
            username = "New username"
        instance.username = username
        
        instance.save()
        context = {
            "title": "Thank you %s" %(request.user)
        }
    
    return render(request, "home.html", context)

def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'qsourceapp@gmail.com']
        contact_message = "%$: %$ via %$"%(
            form_full_name,
            form_message,
            form_email)
        some_html_message = """
        <h1>hello</h1>
        """
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  html_message=some_html_message,
                  fail_silently=True)
    
    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    
    return render(request, "forms.html", context)
    