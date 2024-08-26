from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile,QuestionResponse,UserType
import json
import json
from .forms import UserRegistrationForm



@login_required
def quiz(request):
	return render(request, 'frontend.html')

@login_required
def save_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usertype = data.get('usertype') #Therapist or user

        usertype_short = 'User' if usertype == "Looking for a Therapist?" else 'Therapist'

        print(usertype_short)

        user_profile = request.user.userprofile 

        user_type_db = UserType(user_profile=user_profile,user_type=usertype_short)
        user_type_db.save()

        return JsonResponse({'message': 'Response saved successfully!'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def save_question_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_text = data.get('question')
        response_value = data.get('response')  # Expecting 'yes' or 'no'

        # Convert the response to a boolean
        response_boolean = True if response_value == 'A' else False

        user_profile = request.user.userprofile 

        # Save the question and response to the database
        question_response = QuestionResponse(user_profile=user_profile,question=question_text, response=response_boolean)
        question_response.save()

        return JsonResponse({'message': 'Response saved successfully!'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('frontend')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})