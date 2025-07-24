#!/bin/bash
# Local CI test script

echo "Testing CI configuration locally..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test Python version
echo -e "\n${GREEN}Testing with Python:${NC}"
python --version

# Install empyrical
echo -e "\n${GREEN}Installing empyrical...${NC}"
pip install git+https://github.com/cloudQuant/empyrical.git || {
    echo -e "${RED}Failed to install from GitHub, trying Gitee...${NC}"
    pip install git+https://gitee.com/yunjinqi/empyrical.git
}

# Install dependencies
echo -e "\n${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pyfolio
echo -e "\n${GREEN}Installing pyfolio...${NC}"
pip install -e .

# Run tests
echo -e "\n${GREEN}Running tests...${NC}"
pytest tests/ -v -x --tb=short

# Run linting
echo -e "\n${GREEN}Running linting...${NC}"
flake8 pyfolio --count --select=E9,F63,F7,F82 --show-source --statistics || echo "Linting issues found"

echo -e "\n${GREEN}Local CI test completed!${NC}"