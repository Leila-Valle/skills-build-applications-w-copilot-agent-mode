from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from octofit_tracker.models import Team, UserProfile, Activity, Workout, LeaderboardEntry

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize and populate octofit tracker sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample teams...')
        team1, _ = Team.objects.get_or_create(name='Alpha')
        team2, _ = Team.objects.get_or_create(name='Beta')

        self.stdout.write('Creating sample activities...')
        run, _ = Activity.objects.get_or_create(name='Running', metric='km')
        steps, _ = Activity.objects.get_or_create(name='Steps', metric='steps')

        self.stdout.write('Creating sample users and profiles...')
        u1, _ = User.objects.get_or_create(username='alice')
        u2, _ = User.objects.get_or_create(username='bob')

        UserProfile.objects.get_or_create(user=u1, display_name='Alice', team=team1)
        UserProfile.objects.get_or_create(user=u2, display_name='Bob', team=team2)

        self.stdout.write('Creating sample workouts...')
        Workout.objects.create(user=u1, activity=run, value=5.0, units='km')
        Workout.objects.create(user=u2, activity=steps, value=10000, units='steps')

        self.stdout.write('Updating leaderboard...')
        LeaderboardEntry.objects.update_or_create(team=team1, period='all_time', defaults={'score': 100})
        LeaderboardEntry.objects.update_or_create(team=team2, period='all_time', defaults={'score': 90})

        self.stdout.write(self.style.SUCCESS('Sample data created.'))
