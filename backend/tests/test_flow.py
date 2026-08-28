"""Tests for CogniFlow flow analytics."""

from app.services.flow_analyzer import FlowAnalyzer


def test_flow_analyzer_can_be_created(db_session):
    """Flow analysis service must initialize with a database."""

    analyzer = FlowAnalyzer(db_session)

    assert analyzer is not None


def test_flow_analysis_returns_result(db_session):
    """Flow analysis should return a result."""

    analyzer = FlowAnalyzer(db_session)

    result = analyzer.analyze_all()

    assert result is not None