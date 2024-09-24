import os
import django
from score.models import Match

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')
django.setup()

from score.models import UserProfile, QuestionResponse, UserType

def compare_responses(request):

    # Fetch therapist and user profiles based on their user type
    therapist_profiles = [t.user_profile for t in UserType.objects.filter(user_type='Therapist')]
    user_profiles = [u.user_profile for u in UserType.objects.filter(user_type='User')]

    # Check if there are enough profiles for comparison
    if len(therapist_profiles) == 0 or len(user_profiles) == 0:
        print("Not enough users to compare")
        return None  # Return None if not enough users

    question_map_dict = {}

    # Get the responses of the first therapist and user profiles
    therapist_response = QuestionResponse.objects.filter(user_profile=therapist_profiles[0])
    user_response = QuestionResponse.objects.filter(user_profile=user_profiles[0])

    # Map therapist questions to user questions
    for i, r in enumerate(therapist_response):
        if i < len(user_response):
            question_map_dict[r.question] = user_response[i].question
        else:
            print(f"No corresponding user response for therapist question: {r.question}")
            return None

    # Get the logged-in user's profile and their user type
    profile = UserProfile.objects.get(user=request.user)
    current_user_type_obj = UserType.objects.filter(user_profile=profile).first()

    # If the user doesn't have a user type, return None
    if not current_user_type_obj:
        print("User does not have a user type assigned.")
        return None

    score_dict = {}

    # Loop through all user and therapist profiles and calculate match scores
    for user_profile in set(user_profiles):
        for therapist_profile in set(therapist_profiles):

            therapist_responses = QuestionResponse.objects.filter(user_profile=therapist_profile)
            user_responses = QuestionResponse.objects.filter(user_profile=user_profile)

            therapist_responses_dict = {response.question: response.response for response in therapist_responses}
            user_responses_dict = {response.question: response.response for response in user_responses}

            matches = 0
            total_questions = len(therapist_responses_dict)

            # Compare responses between user and therapist
            for question, therapist_answer in therapist_responses_dict.items():
                if question_map_dict.get(question) is None:
                    return None
                else:
                    user_answer = user_responses_dict.get(question_map_dict[question])
                    if user_answer is not None and therapist_answer == user_answer:
                        matches += 1

            # Calculate match percentage
            if total_questions > 0:
                match_percentage = (matches / total_questions) * 100
            else:
                match_percentage = 0

            score_dict[(user_profile, therapist_profile)] = match_percentage

    # Determine the best match for the current user based on their user type
    if current_user_type_obj.user_type == "User":
        max_score = -float('inf')
        therapist_profile_match = None
        for k, v in score_dict.items():
            if k[0].user.username == request.user.username:
                print(k[0].user.username, k[1].user.username, v)
                if v > max_score:
                    max_score = v
                    therapist_profile_match = k[1]

        if therapist_profile_match:
            # Create a new match in the database
            Match.objects.create(
                user=request.user,
                matched_with=therapist_profile_match.user,
                match_score=max_score
            )
        return therapist_profile_match
    else:
        max_score = -float('inf')
        user_profile_match = None
        for k, v in score_dict.items():
            if k[1].user.username == request.user.username:
                print(k[1].user.username, k[0].user.username, v)
                if v > max_score:
                    max_score = v
                    user_profile_match = k[0]

        if user_profile_match:
            # Create a new match in the database
            Match.objects.create(
                user=request.user,
                matched_with=user_profile_match.user,
                match_score=max_score
            )
        return user_profile_match
