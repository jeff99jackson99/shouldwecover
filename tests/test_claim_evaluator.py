import pytest
from src.app.claim_evaluator import ClaimEvaluator

class TestClaimEvaluator:
    """Test cases for ClaimEvaluator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.evaluator = ClaimEvaluator()
    
    def test_evaluate_coverage_no_red_flags(self):
        """Test coverage evaluation with no red flags."""
        analysis_results = {
            'contract': {
                'red_flags': [],
                'key_findings': ['Clean contract']
            },
            'inspection': {
                'red_flags': [],
                'key_findings': ['No damage found']
            }
        }
        
        result = self.evaluator.evaluate_coverage(analysis_results)
        
        assert result['recommendation'] == 'COVER'
        assert 'No red flags identified' in result['summary']
        assert result['risk_score'] == 0.0
        assert result['confidence_level'] == 'HIGH'
    
    def test_evaluate_coverage_critical_red_flag(self):
        """Test coverage evaluation with critical red flag."""
        analysis_results = {
            'contract': {
                'red_flags': ['Fraud detected in claim'],
                'key_findings': ['Suspicious activity']
            },
            'history': {
                'red_flags': [],
                'key_findings': ['Clean history']
            }
        }
        
        result = self.evaluator.evaluate_coverage(analysis_results)
        
        assert result['recommendation'] == 'DENY'
        assert 'critical red flag' in result['summary'].lower()
        assert result['risk_score'] > 0.0
    
    def test_evaluate_coverage_multiple_high_flags(self):
        """Test coverage evaluation with multiple high-severity flags."""
        analysis_results = {
            'contract': {
                'red_flags': ['Title issue detected'],
                'key_findings': ['Ownership problem']
            },
            'inspection': {
                'red_flags': ['Previous total loss'],
                'key_findings': ['Major damage history']
            }
        }
        
        result = self.evaluator.evaluate_coverage(analysis_results)
        
        assert result['recommendation'] == 'DENY'
        assert 'Multiple high-risk issues' in result['summary']
    
    def test_evaluate_coverage_threshold_exceeded(self):
        """Test coverage evaluation when red flag threshold is exceeded."""
        analysis_results = {
            'contract': {
                'red_flags': ['Minor exclusion'],
                'key_findings': ['Standard terms']
            },
            'inspection': {
                'red_flags': ['Wear and tear'],
                'key_findings': ['Normal condition']
            },
            'acv': {
                'red_flags': ['Slight overvaluation'],
                'key_findings': ['Reasonable estimate']
            },
            'history': {
                'red_flags': ['Minor accident'],
                'key_findings': ['Repaired properly']
            }
        }
        
        result = self.evaluator.evaluate_coverage(analysis_results)
        
        assert result['recommendation'] == 'DENY'
        assert 'Excessive red flags' in result['summary']
    
    def test_evaluate_coverage_with_caution(self):
        """Test coverage evaluation with minor red flags."""
        analysis_results = {
            'contract': {
                'red_flags': ['Minor limitation'],
                'key_findings': ['Standard coverage']
            },
            'inspection': {
                'red_flags': [],
                'key_findings': ['No damage']
            }
        }
        
        result = self.evaluator.evaluate_coverage(analysis_results)
        
        assert result['recommendation'] == 'COVER_WITH_CAUTION'
        assert 'caution' in result['summary'].lower()
    
    def test_assess_flag_severity_critical(self):
        """Test severity assessment for critical flags."""
        critical_flags = [
            'Fraud detected in claim',
            'Salvage title found',
            'Policy violation confirmed'
        ]
        
        for flag in critical_flags:
            severity = self.evaluator._assess_flag_severity(flag, 'contract')
            assert severity == 'CRITICAL'
    
    def test_assess_flag_severity_high(self):
        """Test severity assessment for high-risk flags."""
        high_flags = [
            'Title issue detected',
            'Odometer rollback suspected',
            'Previous total loss found'
        ]
        
        for flag in high_flags:
            severity = self.evaluator._assess_flag_severity(flag, 'history')
            assert severity == 'HIGH'
    
    def test_assess_flag_severity_medium(self):
        """Test severity assessment for medium-risk flags."""
        medium_flags = [
            'Wear and tear issues',
            'Maintenance problems',
            'Pre-existing conditions'
        ]
        
        for flag in medium_flags:
            severity = self.evaluator._assess_flag_severity(flag, 'inspection')
            assert severity == 'MEDIUM'
    
    def test_determine_flag_category(self):
        """Test flag categorization."""
        categories = {
            'Title issue found': 'Title & Ownership Issues',
            'Fraud detected': 'Fraud & Misrepresentation',
            'Coverage exclusion': 'Coverage & Policy Issues',
            'Damage assessment': 'Damage & Accident Issues',
            'Valuation problem': 'Valuation Issues',
            'Maintenance issue': 'Maintenance & Condition Issues'
        }
        
        for flag, expected_category in categories.items():
            category = self.evaluator._determine_flag_category(flag)
            assert category == expected_category
    
    def test_calculate_risk_score(self):
        """Test risk score calculation."""
        # No flags
        no_flags = []
        score = self.evaluator._calculate_risk_score(no_flags)
        assert score == 0.0
        
        # Critical flag
        critical_flags = [{'severity': 'CRITICAL'}]
        score = self.evaluator._calculate_risk_score(critical_flags)
        assert score == 40.0
        
        # High flag
        high_flags = [{'severity': 'HIGH'}]
        score = self.evaluator._calculate_risk_score(high_flags)
        assert score == 25.0
        
        # Medium flag
        medium_flags = [{'severity': 'MEDIUM'}]
        score = self.evaluator._calculate_risk_score(medium_flags)
        assert score == 10.0
        
        # Multiple flags
        multiple_flags = [
            {'severity': 'CRITICAL'},
            {'severity': 'HIGH'},
            {'severity': 'MEDIUM'}
        ]
        score = self.evaluator._calculate_risk_score(multiple_flags)
        assert score == 75.0
        
        # Cap at 100
        many_flags = [{'severity': 'CRITICAL'} for _ in range(10)]
        score = self.evaluator._calculate_risk_score(many_flags)
        assert score == 100.0
    
    def test_calculate_confidence_level(self):
        """Test confidence level calculation."""
        # All documents analyzed successfully
        all_good = {
            'contract': {'key_findings': ['Good']},
            'inspection': {'key_findings': ['Good']}
        }
        confidence = self.evaluator._calculate_confidence_level(all_good)
        assert confidence == 'HIGH'
        
        # Some documents failed
        some_failed = {
            'contract': {'key_findings': ['Good']},
            'inspection': {'error': 'Failed'}
        }
        confidence = self.evaluator._calculate_confidence_level(some_failed)
        assert confidence == 'MEDIUM'
        
        # All documents failed
        all_failed = {
            'contract': {'error': 'Failed'},
            'inspection': {'error': 'Failed'}
        }
        confidence = self.evaluator._calculate_confidence_level(all_failed)
        assert confidence == 'LOW'
    
    def test_error_handling(self):
        """Test error handling in evaluation."""
        # Mock an error by passing invalid data
        with pytest.raises(Exception):
            # This should trigger an error in the evaluation process
            self.evaluator._collect_all_red_flags(None)
    
    def test_get_error_response(self):
        """Test error response generation."""
        error_response = self.evaluator._get_error_response()
        
        assert error_response['recommendation'] == 'ERROR'
        assert 'Unable to evaluate coverage' in error_response['summary']
        assert error_response['risk_score'] == 0.0
        assert error_response['confidence_level'] == 'LOW'
