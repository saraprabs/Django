from django.shortcuts import render, redirect
from django.urls import reverse
from employee_app.forms import UserForm, UserProfileInfoForm
from .services import storage_service
from .services.cosmos_service import cosmos_service

def index(request):
    return render(request, 'employee_app/index.html')

def register(request):
    registered = False
    image_url = "No URL Generated"
    if request.method == 'POST':
        print(f"FILES received: {request.FILES}")
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                try:
                    image_url = storage_service.upload_profile_picture(request.FILES['profile_pic'])
                    print(f"Azure returned URL: {image_url}")
                except Exception as e:
                    print(f"Blob Storage Error: {e}")
            else:
                print("Logic skipped: 'profile_pic' not found in request.FILES")
            user_data = {
                'id': user.username,
                'partitionKey': user.email, # Matches your "Anna" example
                'email': user.email,
                'password': user.password,
                'portfolio': profile_form.cleaned_data.get('portfolio_site'),
                'full_name': f"{user.first_name} {user.last_name}".strip(),
                'profile_pic_url': image_url, # <--- THIS MUST BE THE AZURE URL
                'type': 'employee'
            }
            # save to cosmos DB
            try:
                #cosmos_service.save_user_profile(user_data, image_url)
                cosmos_service.create_item(user_data)
                registered = True
                # 5. Redirect instead of hanging on the same page
                return redirect('index') 
            except Exception as e:
                print(f"Cosmos DB Error: {e}")
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    return render(request, 'employee_app/registration.html',{'user_form':user_form,
                                                           'profile_form': profile_form,
                                                           'registered':registered})
            
def employee_list(request):
    # Call the get_items method from your service layer
    employees = cosmos_service.get_items()
    
    return render(request, 'employee_app/employee_list.html', {
        'employees': employees
    })