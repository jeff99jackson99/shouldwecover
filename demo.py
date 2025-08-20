#!/usr/bin/env python3
"""
Demo script for Insurance Claim Coverage Analyzer
This script demonstrates the core functionality without requiring Streamlit
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from app.pdf_processor import PDFProcessor
from app.ai_analyzer import AIAnalyzer
from app.claim_evaluator import ClaimEvaluator

def demo_pdf_processing():
    """Demonstrate PDF processing functionality."""
    print("🔍 Testing PDF Processing...")
    
    processor = PDFProcessor()
    
    # Create a mock PDF file for testing
    mock_pdf_content = """
    INSURANCE CONTRACT
    
    Coverage Terms:
    - Comprehensive coverage for vehicle damage
    - Excludes wear and tear
    - Excludes pre-existing conditions
    - Requires timely reporting within 30 days
    
    Exclusions:
    - Racing or competitive events
    - Unauthorized modifications
    - Salvage or rebuilt titles
    """
    
    # Mock file object
    class MockPDFFile:
        def __init__(self, content):
            self.content = content.encode()
            self.name = "demo_contract.pdf"
            self.size = len(self.content)
        
        def read(self):
            return self.content
        
        def seek(self, pos):
            pass
    
    mock_file = MockPDFFile(mock_pdf_content)
    
    try:
        # Test PDF validation
        is_valid = processor.validate_pdf(mock_file)
        print(f"✅ PDF Validation: {'Passed' if is_valid else 'Failed'}")
        
        # Test PDF info extraction
        info = processor.get_pdf_info(mock_file)
        print(f"✅ PDF Info: {info['filename']} - {info['file_size']}")
        
        print("✅ PDF Processing Demo Completed!")
        
    except Exception as e:
        print(f"❌ PDF Processing Demo Failed: {e}")

def demo_ai_analysis():
    """Demonstrate AI analysis functionality."""
    print("\n🤖 Testing AI Analysis...")
    
    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OpenAI API key not found. Skipping AI analysis demo.")
        print("   Set OPENAI_API_KEY environment variable to test AI features.")
        return
    
    try:
        analyzer = AIAnalyzer()
        
        # Test contract analysis
        sample_contract = """
        INSURANCE POLICY
        
        Coverage: Comprehensive auto insurance
        Exclusions: 
        - Racing events
        - Unauthorized modifications
        - Pre-existing damage
        
        Requirements:
        - Report claims within 30 days
        - Maintain vehicle in good condition
        """
        
        print("📋 Analyzing sample contract...")
        result = analyzer.analyze_contract(sample_contract)
        
        if 'error' not in result:
            print("✅ AI Analysis Demo Completed!")
            print(f"   Found {len(result.get('red_flags', []))} red flags")
            print(f"   Key findings: {len(result.get('key_findings', []))}")
        else:
            print(f"⚠️  AI Analysis had issues: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ AI Analysis Demo Failed: {e}")

def demo_claim_evaluation():
    """Demonstrate claim evaluation functionality."""
    print("\n⚖️  Testing Claim Evaluation...")
    
    evaluator = ClaimEvaluator()
    
    # Sample analysis results
    sample_analysis = {
        'contract': {
            'red_flags': ['Excludes racing events', 'Requires timely reporting'],
            'key_findings': ['Standard comprehensive coverage', '30-day reporting requirement']
        },
        'inspection': {
            'red_flags': ['Previous damage found', 'Wear and tear issues'],
            'key_findings': ['Vehicle in fair condition', 'Some pre-existing damage']
        },
        'history': {
            'red_flags': [],
            'key_findings': ['Clean title', 'No major accidents']
        }
    }
    
    try:
        result = evaluator.evaluate_coverage(sample_analysis)
        
        print("✅ Claim Evaluation Demo Completed!")
        print(f"   Recommendation: {result['recommendation']}")
        print(f"   Risk Score: {result['risk_score']}")
        print(f"   Confidence: {result['confidence_level']}")
        print(f"   Summary: {result['summary']}")
        
        if result['red_flags']:
            print(f"   Red Flags Found: {len(result['red_flags'])}")
            for flag in result['red_flags'][:3]:  # Show first 3
                print(f"     - {flag['category']}: {flag['description']}")
        
    except Exception as e:
        print(f"❌ Claim Evaluation Demo Failed: {e}")

def main():
    """Run all demo functions."""
    print("🚗 Insurance Claim Coverage Analyzer - Demo Mode")
    print("=" * 60)
    
    try:
        demo_pdf_processing()
        demo_ai_analysis()
        demo_claim_evaluation()
        
        print("\n" + "=" * 60)
        print("✅ All Demos Completed Successfully!")
        print("\nTo run the full application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your OpenAI API key: export OPENAI_API_KEY='your_key'")
        print("3. Run Streamlit: streamlit run src/app/main.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
