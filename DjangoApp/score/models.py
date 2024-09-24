from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class QuestionResponse(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    response = models.BooleanField()  # True for 'Yes', False for 'No'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username}:Question: {self.question}, Response: {'Yes' if self.response else 'No'}"

class UserType(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username}:User Type: {self.user_type}"
    
class Match(models.Model):
    user = models.ForeignKey(User, related_name="matches", on_delete=models.CASCADE)
    matched_with = models.ForeignKey(User, related_name="matched_by", on_delete=models.CASCADE)
    match_score = models.FloatField(default=0.0)  # If you have a matching score
    matched_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-matched_on']  # Order by most recent match first

    def __str__(self):
        return f"{self.user.username} matched with {self.matched_with.username} ({self.match_score})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating UserProfile for {instance.username}")
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(f"Saving UserProfile for {instance.username}")
    instance.userprofile.save()