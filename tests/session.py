from api.imports import pytest
from utils.session import Session_Class

@pytest.fixture
def mock_signals():
    return {
        "signal_a": 0.8,
        "signal_b": 0.4,
        "signal_c": 0.6
    }

@pytest.fixture
def session(mock_signals):
    return Session_Class(
        _signals=mock_signals,
        _time="14:30",
        _session_length=90,
        _noise_score=3
    )


def test_initialization(session):
    assert session.signals_values is not None
    assert session.time_of_day == "14:30"
    assert session.session_length == 90
    assert session.noise_score == 3
    assert session.multiplier == 1.0
    assert session.exploit_modifier == 1.0


def test_calculate_weights(session):
    session.calculate_weights()
    assert isinstance(session.state_weights, dict)
    assert len(session.state_weights) > 0


def test_get_dominating_state(session):
    session.calculate_weights()
    session.get_dominating_state()
    assert session.state is not None


def test_calculate_multipliers(session):
    session.calculate_multipliers(environmental_factor="NORMAL")
    assert session.multiplier > 0
    assert session.t_factor > 0
    assert session.sl_factor > 0
    assert session.nev_factor > 0


def test_calculate_exploit_modifier(session):
    session.calculate_exploit_modifier(
        access_level="LOW",
        attacking_skill="MEDIUM",
        user_interaction="REQUIRED",
        company_resources_stake="MEDIUM",
        company_resources_public=True
    )
    assert session.exploit_modifier > 0


def test_calculate_score(session):
    session.calculate_weights()
    session.get_dominating_state()
    session.calculate_multipliers(environmental_factor="NORMAL")
    session.calculate_exploit_modifier(
        access_level="LOW",
        attacking_skill="LOW",
        user_interaction="NONE",
        company_resources_stake="LOW",
        company_resources_public=False
    )
    session.calculate_score()
    assert session.base_score >= 0
    assert session.score >= 0


def test_get_exploit_band(session):
    session.score = 10
    session.get_exploit_band()
    assert session.exploit_band == "LOW"

    session.score = 25
    session.get_exploit_band()
    assert session.exploit_band == "MEDIUM"

    session.score = 45
    session.get_exploit_band()
    assert session.exploit_band == "HIGH"

    session.score = 70
    session.get_exploit_band()
    assert session.exploit_band == "VERY_HIGH"

    session.score = 90
    session.get_exploit_band()
    assert session.exploit_band == "CRITICAL"
