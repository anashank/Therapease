from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, QuestionResponse, UserType, Match, Message
import json
from .forms import UserRegistrationForm
from .utils import compare_responses


@login_required
def messenger(request):
    try:
        # Fetch the most recent match for the current user
        recent_match = Match.objects.filter(user=request.user).latest('matched_on')
        matched_user = recent_match.matched_with

        # Fetch messages between the current user and the matched user
        messages = Message.objects.filter(
            sender__in=[request.user, matched_user],
            receiver__in=[request.user, matched_user]
        ).order_by('created_at')

        context = {
            'matched_user': matched_user,
            'messages': messages,
        }
        return render(request, 'messenger.html', context)
    except Match.DoesNotExist:
        # Handle the case where no matches exist for the user
        return render(request, 'messenger.html', {'error': 'No match found'})


@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_content = data.get('message')
        matched_user_id = data.get('matched_user_id')

        # Get the matched user object
        matched_user = User.objects.get(id=matched_user_id)

        # Create a new message instance
        message = Message(sender=request.user, receiver=matched_user, content=message_content)
        message.save()

        return JsonResponse({'message': 'Message sent successfully!'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def run_python_code(request):
    # Call compare_responses and get the output
    best_match_profile = compare_responses(request)

    if best_match_profile is None:
        return JsonResponse({'output': 'Not enough users to compare'})

    # Return the results as JSON
    return JsonResponse({
        'output': best_match_profile.user.username
    })


@login_required
def get_recent_match(request):
    try:
        # Fetch the most recent match from the database
        recent_match = Match.objects.filter(user=request.user).latest('matched_on')

        # Prepare the data to be returned
        data = {
            'user': recent_match.user.username,  # Access the username from the user who initiated the match
            'matched_with': recent_match.matched_with.username,  # Access the username of the matched user
            'date': recent_match.matched_on.strftime('%B %d, %Y'),  # Format date as needed
            'score': recent_match.match_score,
        }

        return JsonResponse({'recentMatch': data})
    except Match.DoesNotExist:
        # Return empty response if no recent match is found
        return JsonResponse({'recentMatch': None})
    except Exception as e:
        # Handle any other errors
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def quiz(request):
    # Calling compare_responses and passing the request to get the best match
    best_match_profile = compare_responses(request)

    # Fetch the user's match history
    user_matches = Match.objects.filter(user=request.user)

    # If no best match found
    if not best_match_profile:
        context = {
            'matches': user_matches,
            'match_message': 'No match found or not enough data to compare.'
        }
    else:
        context = {
            'matches': user_matches,
            'match_message': f'You matched with {best_match_profile.user.username}.'
        }

    response = render(request, 'frontend.html', context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response


@login_required
def save_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usertype = data.get('usertype')  # Therapist or user

        usertype_short = 'User' if usertype == "Looking for a Therapist?" else 'Therapist'

        user_profile = request.user.userprofile

        # Use get_or_create to avoid duplication
        user_type_db, created = UserType.objects.get_or_create(
            user_profile=user_profile, defaults={'user_type': usertype_short}
        )

        # If the UserType already exists, update it
        if not created:
            user_type_db.user_type = usertype_short
            user_type_db.save()

        return JsonResponse({'message': 'User type saved successfully!'}, status=201)

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

        # Check if the question response already exists, then update it
        question_response, created = QuestionResponse.objects.get_or_create(
            user_profile=user_profile, question=question_text,
            defaults={'response': response_boolean}
        )

        if not created:
            question_response.response = response_boolean
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
