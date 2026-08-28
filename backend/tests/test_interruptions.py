"""Tests for CogniFlow interruption analytics."""

from app.services.interruption_analyzer import (
    InterruptionAnalyzer,
)


def test_interruption_analyzer_can_be_created(db_session):
    """Interruption analyzer must initialize correctly."""

    analyzer = InterruptionAnalyzer(db_session)

    assert analyzer is not None


def test_interruption_analysis_returns_result(db_session):
    """Interruption analysis should return a result."""

    analyzer = InterruptionAnalyzer(db_session)

    result = analyzer.analyze_all()

    assert result is not None