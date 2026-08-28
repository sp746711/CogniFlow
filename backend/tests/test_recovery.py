"""Tests for CogniFlow recovery analytics."""

from app.services.recovery_analyzer import RecoveryAnalyzer


def test_recovery_analyzer_can_be_created(db_session):
    """Recovery analyzer must initialize correctly."""

    analyzer = RecoveryAnalyzer(db_session)

    assert analyzer is not None


def test_recovery_analysis_returns_result(db_session):
    """Recovery analysis should return a result."""

    analyzer = RecoveryAnalyzer(db_session)

    result = analyzer.analyze_all()

    assert result is not None