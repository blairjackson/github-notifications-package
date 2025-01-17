## Setup

1. **Run the bootstrap script**

Run: ./bootstrap.sh

2. **Configure GitHub Token**
- Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
- Create a token with `repo` and `notifications` scopes
- Add your token to `.env`:
- Add your username to `.env`:

GITHUB_TOKEN=your_token_here
GITGITHUB_USERNAME=your_username

3. **Configure Repositories**
- Open `repos.py`
- Add the repositories you want to monitor

This will show:
- PRs where you're requested as a reviewer (excluding approved PRs)
- Recent mentions in issues/PRs
- "All clear" message if nothing needs attention

NOTE: There are API limits to GitHub so only add repos you care about
