from django.contrib import admin
from score.models import UserProfile,QuestionResponse,UserType,Match,Message
# Register your models here.


class QuestionResponseAdmin(admin.ModelAdmin):
	list_display = ['question','response','created_at']


admin.site.register(UserProfile)
admin.site.register(QuestionResponse, QuestionResponseAdmin)
admin.site.register(UserType)
admin.site.register(Match)
admin.site.register(Message)