#!/bin/bash

# Insurance Claim Coverage Analyzer - GitHub Setup Script

echo "🚗 Setting up GitHub repository for Insurance Claim Coverage Analyzer"
echo "=================================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run 'git init' first."
    exit 1
fi

echo ""
echo "📋 Current repository status:"
git status --short

echo ""
echo "🔑 To create a GitHub repository and push your code:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'insurance-claim-analyzer'"
echo "3. Make it public or private as you prefer"
echo "4. Don't initialize with README, .gitignore, or license (we already have them)"
echo ""
echo "5. After creating the repository, run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/insurance-claim-analyzer.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "6. To enable GitHub Actions:"
echo "   - Go to your repository Settings > Actions > General"
echo "   - Enable 'Allow all actions and reusable workflows'"
echo "   - Set 'Workflow permissions' to 'Read and write permissions'"
echo ""
echo "7. To set up environment variables for CI/CD:"
echo "   - Go to Settings > Secrets and variables > Actions"
echo "   - Add OPENAI_API_KEY with your API key"
echo ""

# Check if remote origin is already set
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote origin is already set to:"
    git remote get-url origin
    echo ""
    echo "To push to GitHub:"
    echo "   git push -u origin main"
else
    echo "⚠️  No remote origin set yet."
    echo "Follow the steps above to add your GitHub repository."
fi

echo ""
echo "🎯 Quick Start Commands:"
echo "========================"
echo "Install dependencies:  pip install -r requirements.txt"
echo "Run demo:             python demo.py"
echo "Run Streamlit app:    streamlit run src/app/main.py"
echo "Run tests:            pytest tests/"
echo "Format code:          black src/ tests/"
echo "Lint code:            ruff check src/ tests/"
echo ""

echo "🐳 Docker Commands:"
echo "==================="
echo "Build image:          docker build -t insurance-claim-analyzer ."
echo "Run container:        docker run -p 8501:8501 -e OPENAI_API_KEY=your_key insurance-claim-analyzer"
echo "Docker Compose:       docker-compose up -d"
echo ""

echo "📚 Documentation:"
echo "================="
echo "README:               README.md"
echo "API Documentation:    https://docs.streamlit.io/"
echo "OpenAI API:           https://platform.openai.com/docs"
echo ""

echo "🚀 Your Insurance Claim Coverage Analyzer is ready!"
echo "Happy coding! 🎉"
