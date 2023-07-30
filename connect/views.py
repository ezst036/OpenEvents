from django.shortcuts import render, redirect
from .forms import ConnectForm
from django.contrib import messages

def connectview(request):
    if request.method == 'GET':
        #Pre-populate user information in the new form
        if request.user.is_authenticated:
            if len(request.user.first_name) < 1 or len(request.user.last_name) < 1:
                messages.success(request, f'Your user profile is incomplete.  Username and email were filled in.')
                form = ConnectForm(initial={
                    'first_name': request.user.username,
                    'last_name': request.user.email
                })
            else:
                form = ConnectForm(initial={
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name
                })
    if request.method == 'POST':
        #Receive filled out form from user
        form = ConnectForm(request.POST)
        if form.is_valid():
            messages.success(request, f'Your message has been received and will be reviewed by the Prayer Team.')
            form.save()
            return redirect('home')
    
    #Blank form for users who are not logged in
    if not request.user.is_authenticated:
        form = ConnectForm()
    
    return render(request, 'form.html', {'form': form})