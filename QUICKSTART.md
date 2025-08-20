# 🚀 Quick Start Guide

## Insurance Claim Coverage Analyzer

This guide will get you up and running with the AI-powered insurance claim analyzer in minutes!

## ⚡ Quick Start (5 minutes)

### 1. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 3. Run the Application
```bash
# Run the Streamlit app
streamlit run src/app/main.py
```

The application will open in your browser at `http://localhost:8501`

## 🧪 Test the System

### Run Demo Script
```bash
python demo.py
```

This will test all components without requiring the full Streamlit interface.

### Run Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/ --cov-report=html
```

## 📁 Project Structure

```
insurance-claim-analyzer/
├── src/app/                    # Main application code
│   ├── main.py                # Streamlit interface
│   ├── pdf_processor.py       # PDF text extraction
│   ├── ai_analyzer.py         # OpenAI GPT-4 analysis
│   ├── claim_evaluator.py     # Coverage decision logic
│   └── utils.py               # Utility functions
├── src/config/                 # Configuration
├── tests/                      # Test suite
├── .github/workflows/          # CI/CD pipelines
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-service setup
└── Makefile                   # Development commands
```

## 🔧 Development Commands

```bash
# Code formatting
make fmt

# Linting
make lint

# Testing
make test

# Clean up
make clean

# Full development cycle
make dev
```

## 🐳 Docker Deployment

### Build and Run
```bash
# Build image
docker build -t insurance-claim-analyzer .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key insurance-claim-analyzer
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📊 How It Works

1. **Upload Documents**: Insurance contract (required) + supporting documents
2. **AI Analysis**: GPT-4 analyzes each document for red flags
3. **Coverage Evaluation**: Cross-references findings against contract terms
4. **Decision Output**: Clear recommendation with detailed reasoning

## 🚨 Red Flag Categories

- **🚨 Critical**: Immediate denial (fraud, title issues)
- **⚠️ High**: Significant policy violations
- **🔶 Medium**: Minor issues requiring attention

## 🔑 Required Documents

1. **📋 Insurance Contract** - Coverage terms and exclusions
2. **🔍 Vehicle Inspection Report** - Damage assessment
3. **💰 ACV Value Document** - Vehicle valuation
4. **📊 Vehicle History Report** - Title and accident history
5. **📝 Adjuster Assessment** - Professional evaluation

## 🆘 Troubleshooting

### Common Issues

**"Analysis failed"**
- Check OpenAI API key is valid
- Ensure PDFs are readable and under 50MB
- Verify internet connection

**"No red flags identified"**
- This is normal for clean claims
- Review detailed analysis for insights

**Slow processing**
- Large PDFs take longer
- AI analysis depends on OpenAI response time

### Getting Help

- Check the comprehensive README.md
- Run `python demo.py` to test components
- Review test output for debugging info

## 🚀 Next Steps

1. **Customize Analysis**: Modify prompts in `ai_analyzer.py`
2. **Add Document Types**: Extend `pdf_processor.py` for new formats
3. **Enhance Logic**: Improve decision rules in `claim_evaluator.py`
4. **Deploy**: Use Docker or cloud platforms for production

## 📞 Support

- **Documentation**: README.md and inline code comments
- **Tests**: Comprehensive test suite in `tests/`
- **Demo**: Run `python demo.py` for component testing

---

**Happy analyzing! 🎉**

Your AI-powered insurance claim analyzer is ready to help make informed coverage decisions.
