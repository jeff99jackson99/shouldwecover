import PyPDF2
import streamlit as st
from typing import Union, Optional
import io
import logging

class PDFProcessor:
    """Handles PDF file processing and text extraction."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text(self, pdf_file) -> str:
        """
        Extract text content from uploaded PDF file.
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text content
        """
        try:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            
            # Extract text from all pages
            text_content = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n"
                        text_content += page_text
                except Exception as e:
                    self.logger.warning(f"Could not extract text from page {page_num + 1}: {e}")
                    continue
            
            # Reset file pointer for potential reuse
            pdf_file.seek(0)
            
            if not text_content.strip():
                raise ValueError("No text content could be extracted from PDF")
            
            return text_content.strip()
            
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_file.name}: {e}")
            raise Exception(f"Failed to process PDF {pdf_file.name}: {str(e)}")
    
    def validate_pdf(self, pdf_file) -> bool:
        """
        Validate that uploaded file is a valid PDF.
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            # Check file extension
            if not pdf_file.name.lower().endswith('.pdf'):
                return False
            
            # Try to read PDF header
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            pdf_file.seek(0)  # Reset file pointer
            
            # Check if PDF has pages
            return len(pdf_reader.pages) > 0
            
        except Exception:
            return False
    
    def get_pdf_info(self, pdf_file) -> dict:
        """
        Get basic information about the PDF file.
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            dict: PDF metadata and information
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            pdf_file.seek(0)  # Reset file pointer
            
            info = {
                'filename': pdf_file.name,
                'file_size': f"{pdf_file.size / 1024:.1f} KB",
                'page_count': len(pdf_reader.pages),
                'is_encrypted': pdf_reader.is_encrypted,
                'metadata': {}
            }
            
            # Try to get metadata
            if pdf_reader.metadata:
                for key, value in pdf_reader.metadata.items():
                    if value:
                        info['metadata'][key] = str(value)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting PDF info: {e}")
            return {
                'filename': pdf_file.name,
                'error': str(e)
            }
