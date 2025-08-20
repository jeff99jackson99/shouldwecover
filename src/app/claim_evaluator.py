from typing import Dict, List, Any
import logging

class ClaimEvaluator:
    """Evaluates overall claim coverage based on all document analysis results."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Coverage decision thresholds
        self.red_flag_threshold = 3  # Number of red flags before denying
        self.critical_red_flags = [
            'title_issues',
            'fraud_indication',
            'coverage_exclusion',
            'policy_violation'
        ]
    
    def evaluate_coverage(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate overall claim coverage based on all analysis results.
        
        Args:
            analysis_results: Results from AI analysis of all documents
            
        Returns:
            dict: Coverage decision with detailed reasoning
        """
        try:
            # Extract all red flags from all documents
            all_red_flags = self._collect_all_red_flags(analysis_results)
            
            # Categorize red flags by severity
            categorized_flags = self._categorize_red_flags(all_red_flags)
            
            # Determine coverage recommendation
            recommendation, reasoning = self._determine_recommendation(categorized_flags)
            
            # Generate detailed coverage analysis
            coverage_details = self._generate_coverage_details(analysis_results, categorized_flags)
            
            # Create summary
            summary = self._create_summary(recommendation, categorized_flags, analysis_results)
            
            return {
                'recommendation': recommendation,
                'summary': summary,
                'reasoning': reasoning,
                'red_flags': categorized_flags,
                'coverage_details': coverage_details,
                'risk_score': self._calculate_risk_score(categorized_flags),
                'confidence_level': self._calculate_confidence_level(analysis_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error evaluating coverage: {e}")
            return self._get_error_response()
    
    def _collect_all_red_flags(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect all red flags from all document analyses."""
        all_flags = []
        
        for doc_type, analysis in analysis_results.items():
            if 'red_flags' in analysis and analysis['red_flags']:
                for flag in analysis['red_flags']:
                    all_flags.append({
                        'document': doc_type,
                        'flag': flag,
                        'severity': self._assess_flag_severity(flag, doc_type)
                    })
        
        return all_flags
    
    def _assess_flag_severity(self, flag: str, doc_type: str) -> str:
        """Assess the severity of a red flag based on content and document type."""
        flag_lower = flag.lower()
        
        # Critical flags that immediately suggest denial
        if any(critical in flag_lower for critical in [
            'fraud', 'forgery', 'stolen', 'salvage title', 'rebuilt title',
            'policy violation', 'coverage exclusion', 'material misrepresentation'
        ]):
            return 'CRITICAL'
        
        # High severity flags
        if any(high in flag_lower for high in [
            'title issue', 'odometer rollback', 'previous total loss',
            'unreported damage', 'modification', 'racing'
        ]):
            return 'HIGH'
        
        # Medium severity flags
        if any(medium in flag_lower for medium in [
            'wear and tear', 'maintenance issue', 'pre-existing condition',
            'delayed reporting', 'minor damage'
        ]):
            return 'MEDIUM'
        
        # Default to medium if unclear
        return 'MEDIUM'
    
    def _categorize_red_flags(self, all_flags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Categorize red flags by type and severity."""
        categorized = []
        
        for flag_data in all_flags:
            category = self._determine_flag_category(flag_data['flag'])
            
            categorized.append({
                'category': category,
                'description': flag_data['flag'],
                'severity': flag_data['severity'],
                'document': flag_data['document'],
                'contract_reference': self._find_contract_reference(flag_data['flag'])
            })
        
        # Sort by severity (CRITICAL > HIGH > MEDIUM)
        severity_order = {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1}
        categorized.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        return categorized
    
    def _determine_flag_category(self, flag: str) -> str:
        """Determine the category of a red flag."""
        flag_lower = flag.lower()
        
        if any(word in flag_lower for word in ['title', 'ownership', 'registration']):
            return 'Title & Ownership Issues'
        elif any(word in flag_lower for word in ['fraud', 'forgery', 'misrepresentation']):
            return 'Fraud & Misrepresentation'
        elif any(word in flag_lower for word in ['coverage', 'policy', 'exclusion']):
            return 'Coverage & Policy Issues'
        elif any(word in flag_lower for word in ['damage', 'accident', 'repair']):
            return 'Damage & Accident Issues'
        elif any(word in flag_lower for word in ['valuation', 'acv', 'market']):
            return 'Valuation Issues'
        elif any(word in flag_lower for word in ['maintenance', 'wear', 'condition']):
            return 'Maintenance & Condition Issues'
        else:
            return 'Other Issues'
    
    def _find_contract_reference(self, flag: str) -> str:
        """Find relevant contract reference for a red flag."""
        # This would ideally cross-reference with contract analysis
        # For now, return a generic reference
        return "Refer to contract exclusions and limitations section"
    
    def _determine_recommendation(self, categorized_flags: List[Dict[str, Any]]) -> tuple:
        """Determine coverage recommendation based on red flags."""
        critical_count = sum(1 for flag in categorized_flags if flag['severity'] == 'CRITICAL')
        high_count = sum(1 for flag in categorized_flags if flag['severity'] == 'HIGH')
        total_flags = len(categorized_flags)
        
        # Immediate denial for critical flags
        if critical_count > 0:
            return 'DENY', f"Critical red flags identified: {critical_count} critical issue(s) found"
        
        # Deny if too many high-severity flags
        if high_count >= 2:
            return 'DENY', f"Multiple high-severity red flags: {high_count} high-risk issues found"
        
        # Deny if total flags exceed threshold
        if total_flags >= self.red_flag_threshold:
            return 'DENY', f"Excessive red flags: {total_flags} issues identified (threshold: {self.red_flag_threshold})"
        
        # Cover with caution if some flags exist
        if total_flags > 0:
            return 'COVER_WITH_CAUTION', f"Coverage recommended with caution: {total_flags} minor issues noted"
        
        # Full coverage if no flags
        return 'COVER', "No red flags identified - coverage recommended"
    
    def _generate_coverage_details(self, analysis_results: Dict[str, Any], 
                                 categorized_flags: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed coverage analysis."""
        coverage_details = {
            'document_analysis': {},
            'risk_assessment': {},
            'coverage_limitations': [],
            'required_actions': []
        }
        
        # Document analysis summary
        for doc_type, analysis in analysis_results.items():
            coverage_details['document_analysis'][doc_type] = {
                'status': 'analyzed',
                'red_flags_count': len(analysis.get('red_flags', [])),
                'key_findings': analysis.get('key_findings', [])[:3]  # Top 3 findings
            }
        
        # Risk assessment
        risk_level = 'LOW'
        if any(flag['severity'] == 'CRITICAL' for flag in categorized_flags):
            risk_level = 'CRITICAL'
        elif any(flag['severity'] == 'HIGH' for flag in categorized_flags):
            risk_level = 'HIGH'
        elif len(categorized_flags) > 0:
            risk_level = 'MEDIUM'
        
        coverage_details['risk_assessment'] = {
            'overall_risk': risk_level,
            'red_flags_count': len(categorized_flags),
            'critical_issues': sum(1 for flag in categorized_flags if flag['severity'] == 'CRITICAL'),
            'high_risk_issues': sum(1 for flag in categorized_flags if flag['severity'] == 'HIGH')
        }
        
        # Coverage limitations based on red flags
        for flag in categorized_flags:
            if flag['severity'] in ['CRITICAL', 'HIGH']:
                coverage_details['coverage_limitations'].append({
                    'issue': flag['description'],
                    'impact': f"May limit or exclude coverage for {flag['category'].lower()}"
                })
        
        # Required actions
        if categorized_flags:
            coverage_details['required_actions'].append("Review all identified red flags before processing claim")
            coverage_details['required_actions'].append("Consider additional investigation for high-risk issues")
        
        return coverage_details
    
    def _create_summary(self, recommendation: str, categorized_flags: List[Dict[str, Any]], 
                       analysis_results: Dict[str, Any]) -> str:
        """Create a human-readable summary of the coverage decision."""
        if recommendation == 'COVER':
            return f"✅ Coverage Recommended: No significant red flags identified. All {len(analysis_results)} documents analyzed successfully."
        
        elif recommendation == 'COVER_WITH_CAUTION':
            return f"⚠️ Coverage Recommended with Caution: {len(categorized_flags)} minor issues identified but none critical. Proceed with additional review."
        
        elif recommendation == 'DENY':
            critical_count = sum(1 for flag in categorized_flags if flag['severity'] == 'CRITICAL')
            high_count = sum(1 for flag in categorized_flags if flag['severity'] == 'HIGH')
            
            if critical_count > 0:
                return f"❌ Coverage Denied: {critical_count} critical red flag(s) identified that violate policy terms."
            elif high_count >= 2:
                return f"❌ Coverage Denied: Multiple high-risk issues ({high_count}) indicate policy violations."
            else:
                return f"❌ Coverage Denied: {len(categorized_flags)} red flags exceed acceptable risk threshold."
        
        return "Unable to determine coverage recommendation due to analysis errors."
    
    def _calculate_risk_score(self, categorized_flags: List[Dict[str, Any]]) -> float:
        """Calculate a numerical risk score (0-100)."""
        if not categorized_flags:
            return 0.0
        
        score = 0.0
        for flag in categorized_flags:
            if flag['severity'] == 'CRITICAL':
                score += 40
            elif flag['severity'] == 'HIGH':
                score += 25
            elif flag['severity'] == 'MEDIUM':
                score += 10
        
        return min(score, 100.0)
    
    def _calculate_confidence_level(self, analysis_results: Dict[str, Any]) -> str:
        """Calculate confidence level in the analysis."""
        total_docs = len(analysis_results)
        analyzed_docs = sum(1 for doc in analysis_results.values() if 'error' not in doc)
        
        if analyzed_docs == 0:
            return 'LOW'
        elif analyzed_docs == total_docs:
            return 'HIGH'
        elif analyzed_docs >= total_docs * 0.8:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Get error response when evaluation fails."""
        return {
            'recommendation': 'ERROR',
            'summary': 'Unable to evaluate coverage due to processing errors',
            'reasoning': 'Analysis failed - manual review required',
            'red_flags': [],
            'coverage_details': {},
            'risk_score': 0.0,
            'confidence_level': 'LOW'
        }
