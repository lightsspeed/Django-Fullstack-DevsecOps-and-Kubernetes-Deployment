import requests
from bs4 import BeautifulSoup
import random
import time

BASE_URL = "http://localhost:8000"

class MockUser:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.session = requests.Session()
        self.csrf_token = None

    def get_csrf(self, url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if token:
            self.csrf_token = token['value']
        return self.csrf_token

    def register(self):
        url = f"{BASE_URL}/users/register/"
        self.get_csrf(url)
        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }
        response = self.session.post(url, data=data)
        if response.status_code == 200 and "login" in response.url:
            print(f"User {self.username} registered.")
            return True
        print(f"Failed to register {self.username}")
        return False

    def login(self):
        url = f"{BASE_URL}/users/login/"
        self.get_csrf(url)
        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'username': self.username,
            'password': self.password
        }
        response = self.session.post(url, data=data)
        if response.status_code == 200 and "polls" in response.url:
            print(f"User {self.username} logged in.")
            return True
        print(f"Failed to login {self.username}")
        return False

    def create_poll(self, title, choices):
        url = f"{BASE_URL}/polls/create/"
        self.get_csrf(url)
        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'title': title,
            'description': f"Automated poll: {title}",
            'is_public': 'on',
            'choice_set-TOTAL_FORMS': len(choices),
            'choice_set-INITIAL_FORMS': 0,
            'choice_set-MIN_NUM_FORMS': 2,
            'choice_set-MAX_NUM_FORMS': 10,
        }
        for i, choice in enumerate(choices):
            data[f'choice_set-{i}-choice_text'] = choice

        response = self.session.post(url, data=data)
        if response.status_code == 200:
            print(f"Poll '{title}' created.")
            return response.url
        print(f"Failed to create poll '{title}'")
        return None

    def vote(self, poll_url):
        # Get poll page to find choice IDs
        response = self.session.get(poll_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        
        choices = soup.find_all('input', {'name': 'choice'})
        if not choices:
            print(f"No choices found for poll at {poll_url}")
            return False
        
        selected_choice = random.choice(choices)['value']
        vote_url = poll_url + "vote/"
        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'choice': selected_choice
        }
        response = self.session.post(vote_url, data=data)
        if response.status_code == 200:
            print(f"User {self.username} voted on {poll_url}")
            return True
        print(f"User {self.username} failed to vote on {poll_url}")
        return False

def simulate():
    users = []
    for i in range(5):
        u = MockUser(f"user_{i}_{int(time.time())}", "pass1234", f"user{i}@example.com")
        if u.register():
            u.login()
            users.append(u)

    if not users:
        print("No users created. Exit.")
        return

    creator = users[0]
    poll_titles = ["What is your favorite cloud?", "Best DB?", "DevSecOps tool of choice?"]
    poll_choices = [
        ["AWS", "Azure", "GCP", "DigitalOcean"],
        ["PostgreSQL", "MySQL", "MongoDB", "SQLite"],
        ["Trivy", "Snyk", "Bandit", "Checkov"]
    ]

    poll_urls = []
    for title, choices in zip(poll_titles, poll_choices):
        url = creator.create_poll(title, choices)
        if url:
            poll_urls.append(url)

    # Simulate random voting
    print("Simulating votes...")
    for _ in range(20):
        u = random.choice(users)
        p = random.choice(poll_urls)
        u.vote(p)
        time.sleep(1)

if __name__ == "__main__":
    simulate()
