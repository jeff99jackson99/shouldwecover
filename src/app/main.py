import streamlit as st
import os
from pathlib import Path
import tempfile
from typing import List, Dict, Any
import json
import pandas as pd

from pdf_processor import PDFProcessor
from ai_analyzer import AIAnalyzer
from claim_evaluator import ClaimEvaluator
from utils import setup_page_config, create_sidebar

def main():
    """Main Streamlit application for insurance claim analysis."""
    
    # Setup page configuration
    setup_page_config()
    
    # Create sidebar
    create_sidebar()
    
    # Main header
    st.title("🚗 Insurance Claim Coverage Analyzer")
    st.markdown("""
    **AI-Powered Analysis**: Upload your documents and get instant coverage recommendations based on contract terms.
    
    **Required Documents:**
    - 📋 Insurance Contract (PDF)
    - 🔍 Vehicle Inspection Report (PDF)
    - 💰 ACV Value Document (PDF)
    - 📊 Vehicle History Report (PDF)
    - 📝 Adjuster Assessment Form (PDF)
    """)
    
    # File upload section
    st.header("📁 Document Upload")
    
    # Contract upload (required)
    contract_file = st.file_uploader(
        "Upload Insurance Contract (Required)",
        type=['pdf'],
        help="This is the primary document that defines coverage terms and exclusions"
    )
    
    # Other documents upload
    col1, col2 = st.columns(2)
    
    with col1:
        inspection_file = st.file_uploader(
            "Vehicle Inspection Report",
            type=['pdf'],
            help="Detailed inspection findings and photos"
        )
        
        acv_file = st.file_uploader(
            "ACV Value Document",
            type=['pdf'],
            help="Actual Cash Value assessment"
        )
    
    with col2:
        history_file = st.file_uploader(
            "Vehicle History Report",
            type=['pdf'],
            help="Carfax or similar vehicle history report"
        )
        
        adjuster_file = st.file_uploader(
            "Adjuster Assessment Form",
            type=['pdf'],
            help="Adjuster's evaluation and recommendations"
        )
    
    # Analysis button
    if st.button("🔍 Analyze Coverage Eligibility", type="primary", use_container_width=True):
        if not contract_file:
            st.error("❌ Insurance Contract is required for analysis!")
            return
        
        # Show progress
        with st.spinner("Processing documents and analyzing coverage..."):
            try:
                # Process all uploaded documents
                documents = process_uploaded_files(
                    contract_file, inspection_file, acv_file, 
                    history_file, adjuster_file
                )
                
                # Analyze with AI
                analysis_results = analyze_documents(documents)
                
                # Evaluate claim coverage
                coverage_decision = evaluate_claim_coverage(analysis_results)
                
                # Display results
                display_results(coverage_decision, analysis_results)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.exception(e)
    
    # Show sample analysis if no files uploaded
    if not any([contract_file, inspection_file, acv_file, history_file, adjuster_file]):
        st.info("💡 **Tip**: Upload your documents above to begin analysis. The AI will scan each document for red flags and provide coverage recommendations.")

def process_uploaded_files(contract_file, inspection_file, acv_file, history_file, adjuster_file):
    """Process all uploaded PDF files and extract text content."""
    processor = PDFProcessor()
    documents = {}
    
    # Process contract first (required)
    if contract_file:
        documents['contract'] = {
            'filename': contract_file.name,
            'content': processor.extract_text(contract_file),
            'type': 'contract'
        }
    
    # Process other documents
    file_mappings = {
        'inspection': inspection_file,
        'acv': acv_file,
        'history': history_file,
        'adjuster': adjuster_file
    }
    
    for doc_type, file in file_mappings.items():
        if file:
            documents[doc_type] = {
                'filename': file.name,
                'content': processor.extract_text(file),
                'type': doc_type
            }
    
    return documents

def analyze_documents(documents: Dict[str, Any]):
    """Analyze all documents using AI to identify red flags and key information."""
    analyzer = AIAnalyzer()
    results = {}
    
    for doc_type, doc_data in documents.items():
        st.write(f"📄 Analyzing {doc_type} document...")
        
        if doc_type == 'contract':
            results[doc_type] = analyzer.analyze_contract(doc_data['content'])
        elif doc_type == 'inspection':
            results[doc_type] = analyzer.analyze_inspection(doc_data['content'])
        elif doc_type == 'acv':
            results[doc_type] = analyzer.analyze_acv(doc_data['content'])
        elif doc_type == 'history':
            results[doc_type] = analyzer.analyze_history(doc_data['content'])
        elif doc_type == 'adjuster':
            results[doc_type] = analyzer.analyze_adjuster(doc_data['content'])
    
    return results

def evaluate_claim_coverage(analysis_results: Dict[str, Any]):
    """Evaluate overall claim coverage based on all analysis results."""
    evaluator = ClaimEvaluator()
    return evaluator.evaluate_coverage(analysis_results)

def display_results(coverage_decision: Dict[str, Any], analysis_results: Dict[str, Any]):
    """Display comprehensive analysis results."""
    
    st.header("📊 Coverage Analysis Results")
    
    # Overall decision
    if coverage_decision['recommendation'] == 'COVER':
        st.success("✅ **RECOMMENDATION: COVER THIS CLAIM**")
    else:
        st.error("❌ **RECOMMENDATION: DO NOT COVER THIS CLAIM**")
    
    # Decision summary
    st.subheader("🎯 Decision Summary")
    st.write(coverage_decision['summary'])
    
    # Red flags section
    if coverage_decision['red_flags']:
        st.subheader("🚨 Red Flags Identified")
        for flag in coverage_decision['red_flags']:
            st.error(f"• **{flag['category']}**: {flag['description']}")
            if flag.get('contract_reference'):
                st.info(f"  📋 Contract Reference: {flag['contract_reference']}")
    
    # Document analysis details
    st.subheader("📋 Document Analysis Details")
    
    for doc_type, analysis in analysis_results.items():
        with st.expander(f"📄 {doc_type.title()} Analysis"):
            if 'key_findings' in analysis:
                st.write("**Key Findings:**")
                for finding in analysis['key_findings']:
                    st.write(f"• {finding}")
            
            if 'red_flags' in analysis:
                st.write("**Red Flags:**")
                for flag in analysis['red_flags']:
                    st.write(f"• ⚠️ {flag}")
            
            if 'recommendations' in analysis:
                st.write("**Recommendations:**")
                for rec in analysis['recommendations']:
                    st.write(f"• 💡 {rec}")
    
    # Coverage details
    st.subheader("📋 Coverage Details")
    st.json(coverage_decision['coverage_details'])
    
    # Export results
    st.subheader("💾 Export Results")
    
    # Create downloadable report
    report_data = {
        'coverage_decision': coverage_decision,
        'analysis_results': analysis_results,
        'timestamp': str(pd.Timestamp.now())
    }
    
    st.download_button(
        label="📥 Download Analysis Report (JSON)",
        data=json.dumps(report_data, indent=2),
        file_name=f"coverage_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main()
