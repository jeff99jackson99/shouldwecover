"""
AI-powered document analysis using OpenAI GPT models.
"""

import os
import logging
import json
import openai
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    """AI-powered document analysis using OpenAI GPT models."""
    
    def __init__(self):
        # Use the API key from environment variables only
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = openai.OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        
        # Analysis prompts for different document types
        self.prompts = {
            'contract': self._get_contract_prompt(),
            'inspection': self._get_inspection_prompt(),
            'acv': self._get_acv_prompt(),
            'history': self._get_history_prompt(),
            'adjuster': self._get_adjuster_prompt()
        }
    
    def analyze_contract(self, content: str) -> Dict[str, Any]:
        """Analyze insurance contract for coverage terms and exclusions."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.prompts['contract']},
                    {"role": "user", "content": f"Analyze this insurance contract:\n\n{content}"}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Error analyzing contract: {e}")
            return self._get_error_response("contract")
    
    def analyze_inspection(self, content: str) -> Dict[str, Any]:
        """Analyze vehicle inspection report for damage and condition issues."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.prompts['inspection']},
                    {"role": "user", "content": f"Analyze this inspection report:\n\n{content}"}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Error analyzing inspection: {e}")
            return self._get_error_response("inspection")
    
    def analyze_acv(self, content: str) -> Dict[str, Any]:
        """Analyze ACV value document for valuation accuracy."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.prompts['acv']},
                    {"role": "user", "content": f"Analyze this ACV document:\n\n{content}"}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Error analyzing ACV: {e}")
            return self._get_error_response("acv")
    
    def analyze_history(self, content: str) -> Dict[str, Any]:
        """Analyze vehicle history report for title issues and accidents."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.prompts['history']},
                    {"role": "user", "content": f"Analyze this vehicle history:\n\n{content}"}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Error analyzing history: {e}")
            return self._get_error_response("history")
    
    def analyze_adjuster(self, content: str) -> Dict[str, Any]:
        """Analyze adjuster assessment form for recommendations and concerns."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.prompts['adjuster']},
                    {"role": "user", "content": f"Analyze this adjuster assessment:\n\n{content}"}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            return self._parse_analysis_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Error analyzing adjuster assessment: {e}")
            return self._get_error_response("adjuster")
    
    def _get_contract_prompt(self) -> str:
        """Get the prompt for contract analysis."""
        return """You are an expert insurance claims analyst. Analyze the insurance contract and identify:

1. Coverage terms and conditions
2. Exclusions and limitations
3. Deductibles and policy limits
4. Special conditions or endorsements
5. Any red flags that could affect claim coverage

Return your analysis in this JSON format:
{
    "coverage_terms": ["list of key coverage terms"],
    "exclusions": ["list of exclusions"],
    "deductibles": "deductible amount and type",
    "policy_limits": "policy limits information",
    "red_flags": [
        {
            "issue": "description of the issue",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "impact": "how this affects coverage"
        }
    ],
    "key_findings": ["list of important findings"],
    "recommendations": ["list of recommendations"]
}"""

    def _get_inspection_prompt(self) -> str:
        """Get the prompt for inspection report analysis."""
        return """You are an expert vehicle inspector. Analyze the inspection report and identify:

1. Vehicle damage assessment
2. Pre-existing conditions
3. Safety concerns
4. Maintenance issues
5. Any red flags that could affect insurance coverage

Return your analysis in this JSON format:
{
    "damage_assessment": "overall damage assessment",
    "pre_existing_conditions": ["list of pre-existing conditions"],
    "safety_concerns": ["list of safety concerns"],
    "maintenance_issues": ["list of maintenance issues"],
    "red_flags": [
        {
            "issue": "description of the issue",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "impact": "how this affects coverage"
        }
    ],
    "key_findings": ["list of important findings"],
    "recommendations": ["list of recommendations"]
}"""

    def _get_acv_prompt(self) -> str:
        """Get the prompt for ACV document analysis."""
        return """You are an expert vehicle appraiser. Analyze the ACV document and identify:

1. Vehicle valuation accuracy
2. Market comparisons
3. Condition adjustments
4. Any discrepancies or concerns
5. Red flags that could affect claim value

Return your analysis in this JSON format:
{
    "valuation_accuracy": "assessment of valuation accuracy",
    "market_comparisons": ["list of market comparisons"],
    "condition_adjustments": ["list of condition adjustments"],
    "discrepancies": ["list of any discrepancies"],
    "red_flags": [
        {
            "issue": "description of the issue",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "impact": "how this affects claim value"
        }
    ],
    "key_findings": ["list of important findings"],
    "recommendations": ["list of recommendations"]
}"""

    def _get_history_prompt(self) -> str:
        """Get the prompt for vehicle history analysis."""
        return """You are an expert vehicle history analyst. Analyze the vehicle history report and identify:

1. Title issues or problems
2. Accident history
3. Odometer discrepancies
4. Salvage or rebuilt status
5. Any red flags that could affect insurance coverage

Return your analysis in this JSON format:
{
    "title_status": "current title status",
    "accident_history": ["list of accidents and severity"],
    "odometer_reading": "current odometer reading",
    "salvage_status": "salvage or rebuilt information",
    "red_flags": [
        {
            "issue": "description of the issue",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "impact": "how this affects coverage"
        }
    ],
    "key_findings": ["list of important findings"],
    "recommendations": ["list of recommendations"]
}"""

    def _get_adjuster_prompt(self) -> str:
        """Get the prompt for adjuster assessment analysis."""
        return """You are an expert insurance adjuster. Analyze the adjuster assessment form and identify:

1. Claim assessment details
2. Coverage recommendations
3. Concerns or reservations
4. Supporting documentation
5. Any red flags that could affect claim approval

Return your analysis in this JSON format:
{
    "claim_assessment": "overall claim assessment",
    "coverage_recommendation": "coverage recommendation",
    "concerns": ["list of concerns or reservations"],
    "supporting_docs": ["list of supporting documentation"],
    "red_flags": [
        {
            "issue": "description of the issue",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "impact": "how this affects claim approval"
        }
    ],
    "key_findings": ["list of important findings"],
    "recommendations": ["list of recommendations"]
}"""

    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response and extract structured data."""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback to structured text parsing
                return self._parse_fallback_response(response_text)
                
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse JSON response: {e}")
            return self._parse_fallback_response(response_text)
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
            return self._get_error_response("unknown")
    
    def _parse_fallback_response(self, response_text: str) -> Dict[str, Any]:
        """Parse response when JSON parsing fails."""
        return {
            "analysis": response_text,
            "red_flags": [],
            "key_findings": ["Analysis completed but structured parsing failed"],
            "recommendations": ["Review the analysis manually for complete details"]
        }
    
    def _get_error_response(self, document_type: str) -> Dict[str, Any]:
        """Get a fallback response when analysis fails."""
        return {
            "error": f"Failed to analyze {document_type} document",
            "red_flags": [],
            "key_findings": ["Analysis failed - manual review required"],
            "recommendations": ["Review document manually and contact support if needed"]
        }
