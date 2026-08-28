"""Tests for CogniFlow context-switch analytics."""

from app.services.context_switch_analyzer import (
    ContextSwitchAnalyzer,
)


def test_context_switch_analyzer_can_be_created(db_session):
    """Context-switch analyzer must initialize correctly."""

    analyzer = ContextSwitchAnalyzer(db_session)

    assert analyzer is not None


def test_context_switch_analysis_returns_result(db_session):
    """Context-switch analysis should return a result."""

    analyzer = ContextSwitchAnalyzer(db_session)

    result = analyzer.analyze_all()

    assert result is not None