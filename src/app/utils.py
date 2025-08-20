import streamlit as st
import os
from typing import Optional
import logging

def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="Insurance Claim Analyzer",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def create_sidebar():
    """Create the application sidebar."""
    with st.sidebar:
        st.title("🚗 Claim Analyzer")
        st.markdown("---")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable AI analysis",
            value=os.getenv('OPENAI_API_KEY', '')
        )
        
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ API Key required for AI analysis")
        
        st.markdown("---")
        
        # Analysis settings
        st.subheader("⚙️ Analysis Settings")
        
        # Confidence threshold
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Minimum confidence level for AI analysis"
        )
        
        # Red flag sensitivity
        red_flag_sensitivity = st.selectbox(
            "Red Flag Sensitivity",
            options=["Low", "Medium", "High"],
            index=1,
            help="How sensitive the system should be to potential red flags"
        )
        
        st.markdown("---")
        
        # Help and information
        st.subheader("ℹ️ Help")
        
        with st.expander("How to Use"):
            st.markdown("""
            1. **Upload Documents**: Start with the insurance contract (required)
            2. **Add Supporting Docs**: Upload inspection, ACV, history, and adjuster reports
            3. **Run Analysis**: Click analyze to process all documents
            4. **Review Results**: Check red flags and coverage recommendations
            5. **Export Report**: Download detailed analysis for your records
            """)
        
        with st.expander("Document Requirements"):
            st.markdown("""
            **Contract**: Must be clear, readable PDF with coverage terms
            **Inspection**: Should include photos and detailed damage assessment
            **ACV**: Must show valuation methodology and market comparison
            **History**: Should be recent and from reputable source
            **Adjuster**: Must include professional assessment and recommendations
            """)
        
        with st.expander("Red Flag Categories"):
            st.markdown("""
            🚨 **Critical**: Immediate denial reasons (fraud, title issues)
            ⚠️ **High**: Significant policy violations
            🔶 **Medium**: Minor issues requiring attention
            ✅ **Low**: Informational items only
            """)

def validate_environment():
    """Validate that required environment variables are set."""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        st.info("Please set these variables in your .env file or environment")
        return False
    
    return True

def setup_logging():
    """Setup application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )

def create_temp_directory():
    """Create temporary directory for file processing."""
    import tempfile
    temp_dir = tempfile.mkdtemp()
    return temp_dir

def cleanup_temp_files(temp_dir: str):
    """Clean up temporary files and directories."""
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        logging.warning(f"Could not cleanup temp directory {temp_dir}: {e}")

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_pdf_file(file) -> tuple[bool, str]:
    """Validate uploaded PDF file."""
    if file is None:
        return False, "No file uploaded"
    
    if not file.name.lower().endswith('.pdf'):
        return False, "File must be a PDF"
    
    if file.size > 50 * 1024 * 1024:  # 50MB limit
        return False, "File size must be less than 50MB"
    
    return True, "File is valid"

def show_upload_progress(file_name: str, progress: float):
    """Show file upload progress."""
    st.progress(progress)
    st.write(f"Processing {file_name}... {progress:.1%}")

def create_download_link(data: str, filename: str, text: str):
    """Create a download link for data."""
    import base64
    
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
