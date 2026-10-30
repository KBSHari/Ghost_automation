import os

# The Ghostfolio dev server (nx serve) runs over HTTPS with a self-signed certificate
BASE_URL = os.getenv("GHOSTFOLIO_URL", "https://localhost:4200").rstrip("/")
API_URL = os.getenv("GHOSTFOLIO_API_URL", "http://localhost:3333").rstrip("/")
LOCALE = os.getenv("GHOSTFOLIO_LOCALE", "en")

JIRA_BASE_URL = "https://epam-team-v1cb1mzz.atlassian.net/browse"
TICKET = "SCRUM-64"
