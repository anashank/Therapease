from django.contrib import admin
from score.models import UserProfile,QuestionResponse,UserType
# Register your models here.


class QuestionResponseAdmin(admin.ModelAdmin):
	list_display = ['question','response','created_at']


admin.site.register(UserProfile)
admin.site.register(QuestionResponse, QuestionResponseAdmin)
admin.site.register(UserType)