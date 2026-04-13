from django.shortcuts import render
from employee_app import views
from employee_app.forms import UserForm, UserProfileInfoForm
from .services import storage_service, cosmos_service

def index(request):
    return render(request, 'employee_app/index.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                image_url = storage_service.upload_profile_picture(request.FILES['profile_pic'])

            user_data = {
                'username': user.username,
                'email': user.email,
                'password': user.password, # This is now the hashed string
                'portfolio': profile_form.cleaned_data.get('portfolio_site'),
                'name': f"{user.first_name} {user.last_name}".strip()
            }
            cosmos_service.save_user_profile(user_data, image_url)
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    return render(request, 'employee_app/registration.html',{'user_form':user_form,
                                                           'profile_form': profile_form,
                                                           'registered':registered})
            
