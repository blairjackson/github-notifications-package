#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Setting up GitHub Notifications Checker...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is required but not installed. Please install Python3 first."
    exit 1
fi

# Install Poetry if not present
if ! command -v poetry &> /dev/null; then
    echo -e "${BLUE}Installing Poetry...${NC}"
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
poetry install

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    echo "GITHUB_TOKEN=" > .env
    echo "GITHUB_USERNAME=" >> .env
    echo -e "${GREEN}Created .env file. Please add your GitHub token and username.${NC}"
fi

if [ ! -f repos.py ]; then
    echo -e "${BLUE}Creating repos.py file...${NC}"
    echo "REPOS = []" > repos.py
    echo -e "${GREEN}Created repos.py file. Please add your repositories.${NC}"
fi

echo -e "${GREEN}Setup complete! Next steps:${NC}"
echo "1. Add your GitHub token to .env"
echo "2. Add your GitHub username to .env"
echo "3. Add your repositories to repos.py"
echo "4. Create alias in .zshrc or .bashrc"
echo "alias ghpr='(cd $PWD/github-notifications && poetry run python get_notifications.py && cd - > /dev/null)'"
echo "5. Run: poetry run python get_notifications.py" 

