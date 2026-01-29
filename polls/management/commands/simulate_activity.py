from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from polls.models import Poll, Choice, Vote, Category
from django.utils import timezone
import random

# Import the Prometheus counter
from polls.views import votes_cast_total

User = get_user_model()

class Command(BaseCommand):
    help = 'Simulate user activity for testing Grafana dashboards'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting activity simulation...'))
        
        # Create categories
        categories = []
        for cat_name in ['Technology', 'Entertainment', 'Sports']:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            categories.append(cat)
        
        # Create users
        users = []
        for i in range(5):
            username = f'testuser_{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Test',
                    'last_name': f'User{i}'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)
        
        # Create polls
        poll_data = [
            {
                'title': 'What is your favorite cloud provider?',
                'description': 'Choose your preferred cloud platform',
                'choices': ['AWS', 'Azure', 'GCP', 'DigitalOcean']
            },
            {
                'title': 'Best database for production?',
                'description': 'Which database do you trust most?',
                'choices': ['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite']
            },
            {
                'title': 'DevSecOps tool of choice?',
                'description': 'Your favorite security scanning tool',
                'choices': ['Trivy', 'Snyk', 'Bandit', 'Checkov']
            },
            {
                'title': 'Preferred CI/CD platform?',
                'description': 'Which CI/CD do you use?',
                'choices': ['GitHub Actions', 'GitLab CI', 'Jenkins', 'CircleCI']
            },
            {
                'title': 'Container orchestration preference?',
                'description': 'How do you manage containers?',
                'choices': ['Kubernetes', 'Docker Swarm', 'Nomad', 'ECS']
            }
        ]
        
        polls = []
        # Use shorter random suffix to avoid slug length issues
        run_id = random.randint(1000, 9999)
        
        for i, data in enumerate(poll_data):
            creator = users[i % len(users)]
            # Add short random ID to make polls unique each run
            unique_title = f"{data['title']} #{run_id}"
            poll = Poll.objects.create(
                title=unique_title,
                description=data['description'],
                creator=creator,
                category=random.choice(categories),
                is_public=True,
                allow_multiple_votes=False
            )
            
            # Create choices
            for choice_text in data['choices']:
                Choice.objects.create(poll=poll, choice_text=choice_text)
            self.stdout.write(f'Created poll: {poll.title}')
            polls.append(poll)
        
        # Simulate voting
        self.stdout.write(self.style.WARNING('Simulating votes...'))
        vote_count = 0
        
        for _ in range(50):  # Create 50 random votes
            user = random.choice(users)
            poll = random.choice(polls)
            
            # Check if user already voted
            if Vote.objects.filter(poll=poll, user=user).exists():
                continue
            
            # Get random choice from poll
            choices = list(poll.choices.all())
            if not choices:
                continue
            
            choice = random.choice(choices)
            
            Vote.objects.create(
                poll=poll,
                choice=choice,
                user=user,
                ip_address='127.0.0.1'
            )
            # Increment the Prometheus counter just like the real VoteView does
            votes_cast_total.inc()
            vote_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(polls)} polls'))
        self.stdout.write(self.style.SUCCESS(f'✓ Simulated {vote_count} votes'))
        self.stdout.write(self.style.SUCCESS('Simulation complete! Check your Grafana dashboard.'))
