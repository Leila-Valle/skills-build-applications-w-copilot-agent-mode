from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=150, blank=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.display_name or self.user.username

class Activity(models.Model):
    name = models.CharField(max_length=150)
    metric = models.CharField(max_length=50, help_text='e.g., steps, km, minutes')

    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, related_name='workouts')
    value = models.FloatField()
    units = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.activity} - {self.value}"

class LeaderboardEntry(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboard_entries')
    score = models.FloatField(default=0)
    period = models.CharField(max_length=50, default='all_time')

    class Meta:
        unique_together = ('team', 'period')

    def __str__(self):
        return f"{self.team.name} ({self.period}) - {self.score}"
