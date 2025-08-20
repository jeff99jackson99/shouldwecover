import pytest
from unittest.mock import Mock, patch, mock_open
import io
from src.app.pdf_processor import PDFProcessor

class TestPDFProcessor:
    """Test cases for PDFProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = PDFProcessor()
        self.mock_pdf_file = Mock()
        self.mock_pdf_file.name = "test.pdf"
        self.mock_pdf_file.size = 1024
    
    def test_extract_text_success(self):
        """Test successful text extraction from PDF."""
        # Mock PDF content
        mock_content = "This is test PDF content"
        self.mock_pdf_file.read.return_value = b"mock_pdf_data"
        
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_page = Mock()
            mock_page.extract_text.return_value = mock_content
            mock_reader.return_value.pages = [mock_page]
            
            result = self.processor.extract_text(self.mock_pdf_file)
            
            assert result == "--- Page 1 ---\nThis is test PDF content"
            self.mock_pdf_file.seek.assert_called_with(0)
    
    def test_extract_text_no_content(self):
        """Test handling of PDF with no extractable text."""
        self.mock_pdf_file.read.return_value = b"mock_pdf_data"
        
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_page = Mock()
            mock_page.extract_text.return_value = ""
            mock_reader.return_value.pages = [mock_page]
            
            with pytest.raises(ValueError, match="No text content could be extracted"):
                self.processor.extract_text(self.mock_pdf_file)
    
    def test_extract_text_multiple_pages(self):
        """Test text extraction from multiple PDF pages."""
        self.mock_pdf_file.read.return_value = b"mock_pdf_data"
        
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_page1 = Mock()
            mock_page1.extract_text.return_value = "Page 1 content"
            mock_page2 = Mock()
            mock_page2.extract_text.return_value = "Page 2 content"
            mock_reader.return_value.pages = [mock_page1, mock_page2]
            
            result = self.processor.extract_text(self.mock_pdf_file)
            
            expected = "--- Page 1 ---\nPage 1 content\n--- Page 2 ---\nPage 2 content"
            assert result == expected
    
    def test_validate_pdf_valid(self):
        """Test validation of valid PDF file."""
        self.mock_pdf_file.read.return_value = b"mock_pdf_data"
        
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_reader.return_value.pages = [Mock()]
            
            result = self.processor.validate_pdf(self.mock_pdf_file)
            assert result is True
    
    def test_validate_pdf_invalid_extension(self):
        """Test validation of file with invalid extension."""
        self.mock_pdf_file.name = "test.txt"
        
        result = self.processor.validate_pdf(self.mock_pdf_file)
        assert result is False
    
    def test_validate_pdf_no_pages(self):
        """Test validation of PDF with no pages."""
        self.mock_pdf_file.read.return_value = b"mock_pdf_data"
        
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_reader.return_value.pages = []
            
            result = self.processor.validate_pdf(self.mock_pdf_file)
            assert result is False
    
    def test_get_pdf_info_success(self):
        """Test successful PDF info extraction."""
        self.mock_pdf_file.read.return_value = b"mock_pdf_data"
        
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_page = Mock()
            mock_reader.return_value.pages = [mock_page]
            mock_reader.return_value.is_encrypted = False
            mock_reader.return_value.metadata = {"Title": "Test Document"}
            
            result = self.processor.get_pdf_info(self.mock_pdf_file)
            
            assert result['filename'] == "test.pdf"
            assert result['page_count'] == 1
            assert result['is_encrypted'] is False
            assert result['metadata']['Title'] == "Test Document"
    
    def test_get_pdf_info_error(self):
        """Test PDF info extraction with error."""
        self.mock_pdf_file.read.side_effect = Exception("PDF read error")
        
        result = self.processor.get_pdf_info(self.mock_pdf_file)
        
        assert result['filename'] == "test.pdf"
        assert 'error' in result
        assert "PDF read error" in result['error']
