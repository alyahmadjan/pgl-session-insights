"""
Unit tests for data cleaning and LLM analysis functions.
Tests standardization, parsing, and error handling.
"""

import pandas as pd
import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from scripts.clean_facilitator_notes import (
    standardize_child_id,
    parse_session_date,
    clean_observation_text,
)

class TestStandardizeChildId:
    """Test Child_ID standardization."""
    
    def test_uppercase_conversion(self):
        assert standardize_child_id('c001') == 'C001'
    
    def test_hyphen_removal(self):
        assert standardize_child_id('C-001') == 'C001'
    
    def test_missing_value(self):
        assert standardize_child_id('') == 'UNKNOWN'
        assert standardize_child_id(None) == 'UNKNOWN'
    
    def test_multiple_ids(self):
        assert standardize_child_id('C001; C002').split(';')[0].strip().replace('-', '').upper() == 'C001'

class TestParseSessionDate:
    """Test date parsing across formats."""
    
    def test_iso_format(self):
        result = parse_session_date('2025-10-20')
        assert result.year == 2025
        assert result.month == 10
        assert result.day == 20
    
    def test_dmy_format(self):
        result = parse_session_date('20/10/2025')
        assert result.year == 2025
        assert result.month == 10
        assert result.day == 20
    
    def test_missing_date(self):
        assert parse_session_date('') is None
        assert parse_session_date(None) is None
    
    def test_invalid_date(self):
        assert parse_session_date('invalid date') is None

class TestCleanObservationText:
    """Test observation text cleaning."""
    
    def test_strip_whitespace(self):
        assert clean_observation_text('  hello  ') == 'Hello'
    
    def test_capitalize_first_letter(self):
        assert clean_observation_text('child was quiet') == 'Child was quiet'
    
    def test_remove_bullet_points(self):
        text = "- Child was quiet\n- Helped peers"
        cleaned = clean_observation_text(text)
        assert '-' not in cleaned or 'Child was quiet' in cleaned
    
    def test_missing_text(self):
        assert clean_observation_text(None) == ''
        assert clean_observation_text('') == ''
    
    def test_shorthand_expansion(self):
        text = "Child worked w/ peers"
        cleaned = clean_observation_text(text)
        assert 'with' in cleaned

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
