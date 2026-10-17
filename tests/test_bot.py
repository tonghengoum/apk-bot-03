import pytest
from unittest.mock import Mock, patch
from bot.research_engine import ResearchEngine

def test_research_engine_init():
    """Test ResearchEngine initialization"""
    engine = ResearchEngine()
    assert engine is not None

def test_research_engine_search_wikipedia_success():
    """Test successful Wikipedia search"""
    engine = ResearchEngine()

    # Mock wikipedia module
    with patch('bot.research_engine.wikipedia') as mock_wiki:
        mock_wiki.search.return_value = ["Test Page"]
        mock_wiki.page.return_value.summary = "Test summary"

        result = engine.search_wikipedia("test query")
        assert result == "Test summary"

def test_research_engine_search_wikipedia_not_found():
    """Test Wikipedia search when nothing is found"""
    engine = ResearchEngine()

    # Mock wikipedia module
    with patch('bot.research_engine.wikipedia') as mock_wiki:
        mock_wiki.search.return_value = []  # No results

        result = engine.search_wikipedia("test query")
        assert result is None

def test_research_engine_research_method():
    """Test the research method of ResearchEngine"""
    engine = ResearchEngine()

    # Mock the search_wikipedia method
    with patch.object(engine, 'search_wikipedia') as mock_search:
        mock_search.return_value = "Test summary"

        result = engine.research("test query")
        assert "According to Wikipedia:" in result
        assert "Test summary" in result

        # Test when search returns None
        mock_search.return_value = None
        result = engine.research("unknown query")
        assert "I couldn't find detailed information" in result