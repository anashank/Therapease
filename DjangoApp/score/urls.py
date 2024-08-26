from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
	path('', views.quiz,name='frontend'),
	path('save-response/', views.save_question_response, name='save_question_response'),
	path('save-type/', views.save_type, name='save_type'),
	path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]
