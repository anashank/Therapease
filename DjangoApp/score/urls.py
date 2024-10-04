from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.quiz, name='frontend'),  # Main quiz view
    path('messenger/<int:matched_user_id>/', views.messenger, name='messenger'),
    path('messenger/', views.messenger, name='messenger'),  
    path('send-message/', views.send_message, name='send_message'),  # Endpoint for sending messages
    path('save-response/', views.save_question_response, name='save_question_response'),  # Save user responses to questions
    path('save-type/', views.save_type, name='save_type'),  # Save user type (Therapist/User)
    path('register/', views.register, name='register'),  # User registration view
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Login view
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),  # Logout view
    path('run-python/', views.run_python_code, name='run_python_code'),  # Endpoint to run Python code
    path('get-recent-match/', views.get_recent_match, name='get_recent_match'),  # Fetch the most recent match
]
