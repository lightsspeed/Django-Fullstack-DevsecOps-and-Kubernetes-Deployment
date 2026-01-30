import requests
from bs4 import BeautifulSoup
import random
import time
import string

BASE_URL = "http://127.0.0.1:63371"


class MockUser:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.session = requests.Session()
        self.csrf_token = None

    def get_csrf(self, url):
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            token = soup.find("input", {"name": "csrfmiddlewaretoken"})
            if token:
                self.csrf_token = token["value"]
            return self.csrf_token
        except Exception as e:
            print(f"Error getting CSRF: {e}")
            return None

    def register(self):
        url = f"{BASE_URL}/users/register/"
        if not self.get_csrf(url):
            return False
        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        try:
            response = self.session.post(url, data=data, timeout=10)
            if response.status_code == 200 and "login" in response.url:
                print(f"User {self.username} registered.")
                return True
        except Exception as e:
            print(f"Registration error for {self.username}: {e}")
        return False

    def login(self):
        url = f"{BASE_URL}/users/login/"
        if not self.get_csrf(url):
            return False
        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "username": self.username,
            "password": self.password,
        }
        try:
            response = self.session.post(url, data=data, timeout=10)
            if response.status_code == 200 and (
                "polls" in response.url
                or response.url.rstrip("/") == BASE_URL.rstrip("/")
            ):
                print(f"User {self.username} logged in.")
                return True
        except Exception as e:
            print(f"Login error for {self.username}: {e}")
        return False

    def create_poll(self, title, choices):
        url = f"{BASE_URL}/create/"
        if not self.get_csrf(url):
            return None
        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "title": title,
            "description": f"Large scale poll: {title}",
            "is_public": "on",
            "start_date": time.strftime("%Y-%m-%dT%H:%M"),
            "choices-TOTAL_FORMS": len(choices),
            "choices-INITIAL_FORMS": 0,
            "choices-MIN_NUM_FORMS": 2,
            "choices-MAX_NUM_FORMS": 10,
        }
        for i, choice in enumerate(choices):
            data[f"choices-{i}-choice_text"] = choice

        try:
            response = self.session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                print(f"Poll '{title}' created.")
                return response.url
        except Exception as e:
            print(f"Poll creation error '{title}': {e}")
        return None

    def vote(self, poll_url):
        try:
            response = self.session.get(poll_url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            csrf_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
            if not csrf_input:
                return False
            self.csrf_token = csrf_input["value"]

            choices = soup.find_all("input", {"name": "choice"})
            if not choices:
                return False

            selected_choice = random.choice(choices)["value"]
            vote_url = poll_url.rstrip("/") + "/vote/"
            data = {"csrfmiddlewaretoken": self.csrf_token, "choice": selected_choice}
            response = self.session.post(vote_url, data=data, timeout=10)
            if response.status_code == 200:
                return True
        except Exception as e:
            # print(f"Voting error on {poll_url}: {e}")
            pass
        return False


def get_random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def setup_polls():
    print("Setting up 15 reference polls...")
    ts = int(time.time())
    admin = MockUser(f"setup_user_{ts}", "SetupPass123!", f"setup_{ts}@example.com")
    if not admin.register() or not admin.login():
        print("Failed to setup admin user for polls.")
        return []

    poll_data = [
        ("Cloud Infrastructure", ["AWS", "Azure", "GCP", "On-Prem"]),
        ("Database Backend", ["Postgres", "MySQL", "MongoDB", "Redis"]),
        ("DevSecOps Tools", ["Trivy", "Snyk", "SonarQube", "Prisma"]),
        ("Programming Language", ["Python", "Go", "Rust", "JavaScript"]),
        ("Container Orchestrator", ["Kubernetes", "Nomad", "Docker Swarm", "ECS"]),
        ("CI/CD Platform", ["Actions", "GitLab CI", "Jenkins", "CircleCI"]),
        (
            "Monitoring Stack",
            ["Prometheus/Grafana", "Datadog", "New Relic", "Dynatrace"],
        ),
        ("IaC Framework", ["Terraform", "Pulumi", "Ansible", "CloudFormation"]),
        ("Frontend Framework", ["React", "Vue", "Angular", "Svelte"]),
        ("Version Control", ["GitHub", "GitLab", "Bitbucket", "Azure DevOps"]),
        ("AI Assistant", ["ChatGPT", "Claude", "Gemini", "Github Copilot"]),
        ("OS for Server", ["Ubuntu", "Debian", "CentOS/Rocky", "Alpine"]),
        ("Messaging Queue", ["RabbitMQ", "Kafka", "Redis Streams", "SQS"]),
        ("API Architecture", ["REST", "GraphQL", "gRPC", "WebSockets"]),
        ("Security Scanner", ["ZAP", "Burp Suite", "Nessus", "Checkmarx"]),
    ]

    poll_urls = []
    for title, choices in poll_data:
        url = admin.create_poll(title, choices)
        if url:
            poll_urls.append(url)

    return poll_urls


def run_enhanced_simulation():
    poll_urls = setup_polls()
    if len(poll_urls) < 15:
        print(f"Warning: Only {len(poll_urls)}/15 polls created. Proceeding anyway.")

    if not poll_urls:
        print("No polls available. Exit.")
        return

    print(
        f"Starting simulation with {len(poll_urls)} polls and continuous user creation."
    )
    user_count = 0
    while True:
        try:
            ts = int(time.time())
            username = f"mass_user_{user_count}_{get_random_string(4)}"
            user = MockUser(username, "MassPass123!", f"{username}@sim.local")

            if user.register() and user.login():
                print(f"User {username} starting to vote in all polls...")
                success_votes = 0
                for url in poll_urls:
                    if user.vote(url):
                        success_votes += 1
                    time.sleep(0.1)  # Small delay to not overwhelm
                print(
                    f"User {username} finished. Success votes: {success_votes}/{len(poll_urls)}"
                )
                user_count += 1

            # Short wait between users
            time.sleep(2)
        except KeyboardInterrupt:
            print("Simulation stopped by user.")
            break
        except Exception as e:
            print(f"Unexpected error in simulation loop: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run_enhanced_simulation()
