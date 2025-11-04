from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models as djongo_models
from django.db import models

# Define models for teams, activities, leaderboard, workouts
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (superheroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            user_objs.append(user)

        # Create activities
        Activity.objects.create(user='ironman', team='Marvel', type='run', duration=30)
        Activity.objects.create(user='batman', team='DC', type='cycle', duration=45)
        Activity.objects.create(user='spiderman', team='Marvel', type='swim', duration=25)
        Activity.objects.create(user='superman', team='DC', type='run', duration=60)

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=100)
        Leaderboard.objects.create(team='DC', points=90)

        # Create workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy')
        Workout.objects.create(name='Sprints', description='Sprint 100m x 5', difficulty='Medium')
        Workout.objects.create(name='Plank', description='Hold plank for 2 minutes', difficulty='Hard')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
