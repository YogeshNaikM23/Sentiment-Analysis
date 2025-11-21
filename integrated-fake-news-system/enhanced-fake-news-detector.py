"""
Enhanced Fake News Detector with Temporal Awareness
This version includes proper date context and improved logic
"""

import re
from datetime import datetime
import random
import numpy as np

class ImprovedFakeNewsDetector:
    """
    Enhanced fake news detector with temporal context and better logic
    """
    
    def __init__(self):
        self.current_year = 2025  # Set current context
        self.current_date = datetime(2025, 8, 23)
        
    def enhanced_prediction(self, text, source=None):
        """
        Enhanced prediction with temporal context and better heuristics
        """
        text_lower = text.lower().strip()
        
        # Handle temporal statements
        if self._is_temporal_statement(text_lower):
            return self._evaluate_temporal_claim(text_lower)
        
        # Handle factual vs speculative language
        confidence_score = self._calculate_confidence(text_lower, source)
        
        # Determine classification
        if confidence_score > 0.6:
            classification = "Real"
        else:
            classification = "Fake"
            
        return {
            'classification': classification,
            'confidence': confidence_score,
            'reasoning': self._explain_decision(text_lower, confidence_score),
            'temporal_context': self._check_temporal_context(text_lower)
        }
    
    def _is_temporal_statement(self, text):
        """Check if this is a temporal/date-related statement"""
        temporal_patterns = [
            r'we are in \d{4}',
            r'the year is \d{4}',
            r'it is \d{4}',
            r'current year.*\d{4}',
            r'today is.*\d{4}'
        ]
        
        return any(re.search(pattern, text) for pattern in temporal_patterns)
    
    def _evaluate_temporal_claim(self, text):
        """Evaluate temporal claims against known current date"""
        # Extract year mentions
        years = re.findall(r'\d{4}', text)
        
        if not years:
            return {'classification': 'Real', 'confidence': 0.5, 'reasoning': 'No specific year mentioned'}
        
        mentioned_year = int(years[0])
        
        if mentioned_year == self.current_year:
            return {
                'classification': 'Real',
                'confidence': 0.95,
                'reasoning': f'Correctly states current year ({self.current_year})',
                'temporal_accuracy': 'Accurate'
            }
        elif mentioned_year < self.current_year:
            return {
                'classification': 'Fake',
                'confidence': 0.85,
                'reasoning': f'Claims we are in {mentioned_year}, but current year is {self.current_year}',
                'temporal_accuracy': 'Outdated'
            }
        else:  # future year
            return {
                'classification': 'Fake',
                'confidence': 0.90,
                'reasoning': f'Claims we are in future year {mentioned_year}, current year is {self.current_year}',
                'temporal_accuracy': 'Future prediction'
            }
    
    def _calculate_confidence(self, text, source):
        """Calculate confidence based on multiple factors"""
        confidence = 0.5  # baseline
        
        # Source credibility
        if source:
            source_lower = source.lower()
            if any(credible in source_lower for credible in ['bbc', 'cnn', 'reuters', 'nytimes']):
                confidence += 0.2
            elif any(suspicious in source_lower for suspicious in ['fake', 'conspiracy', 'hoax']):
                confidence -= 0.3
        
        # Language analysis
        suspicious_words = ['shocking', 'unbelievable', 'secret', 'exposed', 'miracle cure']
        suspicious_count = sum(1 for word in suspicious_words if word in text)
        confidence -= (suspicious_count * 0.1)
        
        # Excessive punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 2:
            confidence -= 0.15
        
        # Proper attribution
        if any(phrase in text for phrase in ['according to', 'sources say', 'study shows']):
            confidence += 0.15
        
        # Ensure confidence stays in valid range
        return max(0.1, min(0.95, confidence))
    
    def _explain_decision(self, text, confidence):
        """Provide explanation for the decision"""
        reasons = []
        
        if confidence > 0.7:
            reasons.append("High confidence due to factual language and credible patterns")
        elif confidence < 0.4:
            reasons.append("Low confidence due to suspicious patterns or unreliable indicators")
        else:
            reasons.append("Moderate confidence - requires additional verification")
            
        return reasons
    
    def _check_temporal_context(self, text):
        """Check temporal context of claims"""
        context = {
            'has_dates': bool(re.search(r'\d{4}', text)),
            'current_year_mentioned': str(self.current_year) in text,
            'temporal_accuracy': 'unknown'
        }
        
        if context['current_year_mentioned']:
            context['temporal_accuracy'] = 'accurate'
        
        return context

# Example usage and testing
def test_enhanced_detector():
    """Test the enhanced detector with various inputs"""
    detector = ImprovedFakeNewsDetector()
    
    test_cases = [
        "we are in 2025",
        "we are in 2023", 
        "we are in 2026",
        "SHOCKING: Scientists discover aliens!",
        "According to Reuters, the stock market closed higher today",
        "Unbelievable miracle cure discovered by researchers",
        "The weather forecast shows rain tomorrow"
    ]
    
    print("Enhanced Fake News Detection Results:")
    print("=" * 50)
    
    for i, text in enumerate(test_cases, 1):
        result = detector.enhanced_prediction(text, "Test Source")
        
        print(f"\n{i}. Text: '{text}'")
        print(f"   Classification: {result['classification']}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Reasoning: {result['reasoning']}")
        
        if 'temporal_accuracy' in result:
            print(f"   Temporal Accuracy: {result['temporal_accuracy']}")

if __name__ == "__main__":
    test_enhanced_detector()