# 🚗 Insurance Claim Coverage Analyzer

**AI-Powered Analysis**: Upload your documents and get instant coverage recommendations based on contract terms.

## 🎯 Overview

This Streamlit application uses advanced AI (OpenAI GPT-4) to analyze multiple insurance-related documents and determine claim coverage eligibility. It scans for red flags, cross-references contract terms, and provides clear recommendations with detailed reasoning.

## ✨ Features

- **Multi-Document Analysis**: Process insurance contracts, inspection reports, ACV values, vehicle history, and adjuster assessments
- **AI-Powered Red Flag Detection**: Identifies coverage issues, fraud indicators, and policy violations
- **Smart Coverage Evaluation**: Cross-references all documents against contract terms
- **Risk Scoring**: Calculates numerical risk scores and confidence levels
- **Exportable Reports**: Download detailed analysis results in JSON format
- **User-Friendly Interface**: Clean, intuitive Streamlit interface with helpful sidebar

## 📋 Required Documents

1. **📋 Insurance Contract** (Required) - Defines coverage terms and exclusions
2. **🔍 Vehicle Inspection Report** - Detailed damage assessment and photos
3. **💰 ACV Value Document** - Actual Cash Value assessment
4. **📊 Vehicle History Report** - Title status and accident history
5. **📝 Adjuster Assessment Form** - Professional evaluation and recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- PDF documents to analyze

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd insurance-claim-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   streamlit run src/app/main.py
   ```

### Usage

1. **Upload Documents**: Start with the insurance contract (required)
2. **Add Supporting Docs**: Upload inspection, ACV, history, and adjuster reports
3. **Run Analysis**: Click "Analyze Coverage Eligibility" to process all documents
4. **Review Results**: Check red flags and coverage recommendations
5. **Export Report**: Download detailed analysis for your records

## 🔍 How It Works

### 1. Document Processing
- **PDF Text Extraction**: Uses PyPDF2 to extract text content from uploaded PDFs
- **Content Validation**: Ensures documents are readable and contain relevant information

### 2. AI Analysis
- **Specialized Prompts**: Each document type has tailored analysis prompts
- **Red Flag Detection**: Identifies coverage issues, fraud indicators, and policy violations
- **Structured Output**: Returns analysis in consistent JSON format

### 3. Coverage Evaluation
- **Risk Assessment**: Categorizes red flags by severity (Critical, High, Medium)
- **Decision Logic**: Applies business rules to determine coverage recommendations
- **Comprehensive Analysis**: Cross-references all findings for final decision

### 4. Results Presentation
- **Clear Recommendations**: COVER, COVER_WITH_CAUTION, or DENY
- **Detailed Reasoning**: Explains why each decision was made
- **Risk Scoring**: Numerical risk assessment (0-100)
- **Exportable Reports**: Download complete analysis for record-keeping

## 🏗️ Architecture

```
src/
├── app/
│   ├── main.py              # Main Streamlit application
│   ├── pdf_processor.py     # PDF text extraction
│   ├── ai_analyzer.py       # OpenAI GPT-4 analysis
│   ├── claim_evaluator.py   # Coverage decision logic
│   └── utils.py             # Utility functions
└── config/
    └── settings.py          # Configuration management
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
DEBUG=False
LOG_LEVEL=INFO
RED_FLAG_THRESHOLD=3
CONFIDENCE_THRESHOLD=0.7
MAX_ANALYSIS_TIME=300
```

### Analysis Settings

- **Red Flag Threshold**: Number of flags before automatic denial (default: 3)
- **Confidence Threshold**: Minimum AI confidence level (default: 0.7)
- **Analysis Timeout**: Maximum time for AI analysis (default: 300 seconds)

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage
pytest tests/ --cov=src/ --cov-report=html
```

## 🐳 Docker Support

### Build and Run

```bash
# Build the Docker image
docker build -t insurance-claim-analyzer .

# Run the container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key insurance-claim-analyzer
```

### Docker Compose

```bash
# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📊 Red Flag Categories

### 🚨 Critical (Immediate Denial)
- Fraud or forgery indicators
- Salvage or rebuilt titles
- Policy violations
- Coverage exclusions

### ⚠️ High (Significant Risk)
- Title issues
- Odometer discrepancies
- Previous total loss
- Unreported damage

### 🔶 Medium (Requires Attention)
- Wear and tear issues
- Maintenance problems
- Pre-existing conditions
- Delayed reporting

## 🔒 Security Features

- **API Key Protection**: Secure input fields for sensitive credentials
- **File Validation**: PDF format and size restrictions
- **Error Handling**: Graceful failure with informative messages
- **Logging**: Comprehensive audit trail for analysis activities

## 📈 Performance

- **Processing Speed**: Typical analysis completes in 30-60 seconds
- **Document Size**: Supports PDFs up to 50MB
- **Concurrent Users**: Streamlit handles multiple simultaneous users
- **Memory Usage**: Efficient text processing with minimal memory footprint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**"Analysis failed" error**
- Check your OpenAI API key is valid
- Ensure PDFs are readable and not corrupted
- Verify document size is under 50MB

**"No red flags identified"**
- This is normal for clean claims
- Review the detailed analysis for insights
- Check confidence levels in results

**Slow processing**
- Large PDFs take longer to process
- AI analysis depends on OpenAI API response time
- Consider breaking large documents into smaller sections

### Getting Help

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs or feature requests via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas

## 🚀 Roadmap

### Upcoming Features
- [ ] Batch processing for multiple claims
- [ ] Integration with insurance databases
- [ ] Advanced fraud detection algorithms
- [ ] Mobile-responsive interface
- [ ] API endpoints for programmatic access

### Version History
- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Enhanced red flag detection
- **v1.2.0** - Improved AI analysis accuracy
- **v1.3.0** - Advanced reporting features

---

**Built with ❤️ for insurance professionals who need fast, accurate claim analysis.**
