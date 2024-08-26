import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')
django.setup()

from score.models import UserProfile, QuestionResponse, UserType

def compare_responses():
    therapist_profiles = [t.user_profile for t in UserType.objects.filter(user_type='Therapist')]
    user_profiles = [u.user_profile for u in UserType.objects.filter(user_type='User')]

    
    question_map_dict = {}

    therapist_response = QuestionResponse.objects.filter(user_profile=therapist_profiles[0])
    user_response = QuestionResponse.objects.filter(user_profile=user_profiles[0])

    for i,r in enumerate(therapist_response):
        question_map_dict[r.question] = user_response[i].question

    for user_profile in user_profiles:
        for therapist_profile in therapist_profiles:
    
            therapist_responses = QuestionResponse.objects.filter(user_profile=therapist_profile)
            user_responses = QuestionResponse.objects.filter(user_profile=user_profile)

            therapist_responses_dict = {response.question: response.response for response in therapist_responses}
            user_responses_dict = {response.question: response.response for response in user_responses}

            matches = 0
            total_questions = len(therapist_responses_dict)

            for question, therapist_answer in therapist_responses_dict.items():
                user_answer = user_responses_dict.get(question_map_dict[question])
                if user_answer is not None and therapist_answer == user_answer:
                    matches += 1
            
            if total_questions > 0:
                match_percentage = (matches / total_questions) * 100
            else:
                match_percentage = 0

            print(user_profile,therapist_profile)
            print(f"Therapist and User match score: {matches}/{total_questions} ({match_percentage:.2f}%)")

if __name__ == "__main__":
    compare_responses()
