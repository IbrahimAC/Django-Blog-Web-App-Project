 #djangos ones provides functions that query the data the the user inputs for us e.g. is password similar to username
from django.contrib import messages                    #however djangos control may be disadvantageous for our vision e.g. for a low level super user friendly site without all django's form rules
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST': # If the HTTP request is a POST request then...
        form = UserRegisterForm(request.POST) # Create a form containing the data payload inside the POST request
        if form.is_valid(): # Check if the data meets the forms requirments eg. Has this user been created previously? 
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in') 
            # The validated form will be stored in the cleaned_data dictionary  
            return redirect('login') # Where do you think is needs to go? 
            
    else:
        form = UserRegisterForm() 
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)