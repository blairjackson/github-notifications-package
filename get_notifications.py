#!/usr/bin/env python3
import os
import requests
import sys
import warnings
from datetime import datetime, timezone
from dotenv import load_dotenv
from repos import REPOS

# Suppress urllib3 warnings about LibreSSL
warnings.filterwarnings('ignore', category=Warning)

# GitHub Personal Access Token (create one at https://github.com/settings/tokens)
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

if not GITHUB_TOKEN:
    print("Error: Please set GITHUB_TOKEN environment variable")
    sys.exit(1)

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


def check_pull_requests(repo):
    url = f"https://api.github.com/repos/{repo}/pulls?state=open"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return

    prs = response.json()
    found_prs = False
    for pr in prs:

        if not any(reviewer.get('login') == GITHUB_USERNAME for reviewer in pr.get('requested_reviewers', [])):
            continue

        reviews_url = f"https://api.github.com/repos/{repo}/pulls/{pr['number']}/reviews"
        reviews_response = requests.get(reviews_url, headers=headers)

        if reviews_response.status_code == 200:
            reviews = reviews_response.json()

            if any(review.get('state') == 'APPROVED' for review in reviews):
                continue

        found_prs = True
        print(f"\n🔍 Review requested: {repo}")
        print(f"PR: {pr['title']}")
        print(f"URL: {pr['html_url']}")
    return found_prs


def check_mentions(repo):
    url = f"https://api.github.com/search/issues?q=mentions:{GITHUB_USERNAME}+repo:{repo}+state:open"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return False

    found_mentions = False
    items = response.json().get('items', [])
    for item in items:
        updated_at = datetime.strptime(item['updated_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        if (datetime.now(timezone.utc) - updated_at).days <= 7:
            print(f"\n@ Mentioned in: {repo}")
            print(f"Title: {item['title']}")
            print(f"URL: {item['html_url']}")
            found_mentions = True
    return found_mentions


def main():
    print("🔎 Checking GitHub notifications...\n")    
    found_anything = False

    if not REPOS:
        print("No repositories found in repos.py. Please add your repositories.")
        return

    for repo in REPOS:
        if check_pull_requests(repo) or check_mentions(repo):
            found_anything = True

    if not found_anything:
        print("✨ All clear! No pending reviews or mentions.")


if __name__ == "__main__":
    main()
