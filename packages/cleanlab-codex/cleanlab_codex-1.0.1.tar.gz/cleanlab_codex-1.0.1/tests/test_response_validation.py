"""Unit tests for validation module functions."""

from __future__ import annotations

from typing import Any, Dict, Sequence, Union
from unittest.mock import Mock, patch

import pytest

from cleanlab_codex.response_validation import (
    _DEFAULT_UNHELPFULNESS_CONFIDENCE_THRESHOLD,
    is_bad_response,
    is_fallback_response,
    is_unhelpful_response,
    is_untrustworthy_response,
)

# Mock responses for testing
GOOD_RESPONSE = "This is a helpful and specific response that answers the question completely."
BAD_RESPONSE = "Based on the available information, I cannot provide a complete answer."
QUERY = "What is the capital of France?"
CONTEXT = "Paris is the capital and largest city of France."


class MockTLM(Mock):
    _trustworthiness_score: float = 0.8
    _response: str = "No"

    @property
    def trustworthiness_score(self) -> float:
        return self._trustworthiness_score

    @trustworthiness_score.setter
    def trustworthiness_score(self, value: float) -> None:
        self._trustworthiness_score = value

    @property
    def response(self) -> str:
        return self._response

    @response.setter
    def response(self, value: str) -> None:
        self._response = value

    def get_trustworthiness_score(
        self,
        prompt: Union[str, Sequence[str]],  # noqa: ARG002
        response: Union[str, Sequence[str]],  # noqa: ARG002
        **kwargs: Any,  # noqa: ARG002
    ) -> Dict[str, Any]:
        return {"trustworthiness_score": self._trustworthiness_score}

    def prompt(
        self,
        prompt: Union[str, Sequence[str]],  # noqa: ARG002
        /,
        **kwargs: Any,  # noqa: ARG002
    ) -> Dict[str, Any]:
        return {"response": self._response, "trustworthiness_score": self._trustworthiness_score}


@pytest.fixture
def mock_tlm() -> MockTLM:
    return MockTLM()


@pytest.mark.parametrize(
    ("response", "threshold", "fallback_answer", "expected"),
    [
        # Test threshold variations
        (GOOD_RESPONSE, 30, None, True),
        (GOOD_RESPONSE, 55, None, False),
        # Test default behavior (BAD_RESPONSE should be flagged)
        (BAD_RESPONSE, None, None, True),
        # Test default behavior for different response (GOOD_RESPONSE should not be flagged)
        (GOOD_RESPONSE, None, None, False),
        # Test custom fallback answer
        (GOOD_RESPONSE, 80, "This is an unhelpful response", False),
    ],
)
def test_is_fallback_response(
    response: str,
    threshold: float | None,
    fallback_answer: str | None,
    *,
    expected: bool,
) -> None:
    """Test fallback response detection."""
    kwargs: dict[str, float | str] = {}
    if threshold is not None:
        kwargs["threshold"] = threshold
    if fallback_answer is not None:
        kwargs["fallback_answer"] = fallback_answer

    assert is_fallback_response(response, **kwargs) is expected  # type: ignore


def test_is_untrustworthy_response(mock_tlm: Mock) -> None:
    """Test untrustworthy response detection."""
    # Test trustworthy response
    mock_tlm.trustworthiness_score = 0.8
    assert is_untrustworthy_response(GOOD_RESPONSE, CONTEXT, QUERY, mock_tlm, trustworthiness_threshold=0.5) is False

    # Test untrustworthy response
    mock_tlm.trustworthiness_score = 0.3
    assert is_untrustworthy_response(BAD_RESPONSE, CONTEXT, QUERY, mock_tlm, trustworthiness_threshold=0.5) is True


@pytest.mark.parametrize(
    ("tlm_score", "threshold", "expected_unhelpful"),
    [
        # Scores above threshold indicate unhelpful responses
        (0.9, 0.5, True),  # High score (0.9) > threshold (0.5) -> unhelpful
        (0.3, 0.5, False),  # Low score (0.3) < threshold (0.5) -> helpful
        (0.5, 0.5, False),  # Equal score (0.5) = threshold (0.5) -> helpful
        # Different threshold tests
        (0.8, 0.7, True),  # Score 0.8 > threshold 0.7 -> unhelpful
        (0.1, 0.3, False),  # Score 0.1 < threshold 0.3 -> helpful
        # Default threshold tests
        (0.4, None, False),  # Below default
        (_DEFAULT_UNHELPFULNESS_CONFIDENCE_THRESHOLD, None, False),  # At default
        (_DEFAULT_UNHELPFULNESS_CONFIDENCE_THRESHOLD + 0.01, None, True),  # Just above default
        (0.7, None, True),  # Above default
    ],
)
def test_is_unhelpful_response(
    mock_tlm: Mock,
    tlm_score: float,
    threshold: float | None,
    *,
    expected_unhelpful: bool,
) -> None:
    """Test unhelpful response detection.

    A response is considered unhelpful if its trustworthiness score is ABOVE the threshold.
    This may seem counter-intuitive, but higher scores indicate more similar responses to
    known unhelpful patterns.
    """
    mock_tlm.trustworthiness_score = tlm_score

    # The response content doesn't affect the result, only the score matters
    if threshold is not None:
        result = is_unhelpful_response(GOOD_RESPONSE, QUERY, mock_tlm, confidence_score_threshold=threshold)
    else:
        result = is_unhelpful_response(GOOD_RESPONSE, QUERY, mock_tlm)

    assert result is expected_unhelpful


@pytest.mark.parametrize(
    ("response", "trustworthiness_score", "prompt_score", "expected"),
    [
        # Good response passes all checks
        (GOOD_RESPONSE, 0.8, 0.2, False),
        # Bad response fails at least one check
        (BAD_RESPONSE, 0.3, 0.9, True),
    ],
)
def test_is_bad_response(
    mock_tlm: Mock,
    response: str,
    trustworthiness_score: float,
    prompt_score: float,
    *,
    expected: bool,
) -> None:
    """Test the main is_bad_response function."""
    # Create a new Mock object for get_trustworthiness_score
    mock_tlm.get_trustworthiness_score = Mock(return_value={"trustworthiness_score": trustworthiness_score})
    # Set up the second call to return prompt_score
    mock_tlm.get_trustworthiness_score.side_effect = [
        {"trustworthiness_score": trustworthiness_score},  # Should be called by is_untrustworthy_response
        {"trustworthiness_score": prompt_score},  # Should be called by is_unhelpful_response
    ]

    assert (
        is_bad_response(
            response,
            context=CONTEXT,
            query=QUERY,
            config={"tlm": mock_tlm},
        )
        is expected
    )


@pytest.mark.parametrize(
    ("response", "fuzz_ratio", "prompt_score", "query", "tlm", "expected"),
    [
        # Test with only fallback check (no context/query/tlm)
        (BAD_RESPONSE, 90, None, None, None, True),
        # Test with fallback and unhelpful checks (no context)
        (GOOD_RESPONSE, 30, 0.1, QUERY, "mock_tlm", False),
        # Test with fallback and unhelpful checks (with context) (prompt_score is above threshold)
        (GOOD_RESPONSE, 30, 0.6, QUERY, "mock_tlm", True),
    ],
)
def test_is_bad_response_partial_inputs(
    mock_tlm: Mock,
    response: str,
    fuzz_ratio: int,
    prompt_score: float,
    query: str,
    tlm: Mock,
    *,
    expected: bool,
) -> None:
    """Test is_bad_response with partial inputs (some checks disabled)."""
    mock_fuzz = Mock()
    mock_fuzz.partial_ratio.return_value = fuzz_ratio
    with patch.dict("sys.modules", {"thefuzz": Mock(fuzz=mock_fuzz)}):
        if prompt_score is not None:
            mock_tlm.trustworthiness_score = prompt_score
            tlm = mock_tlm

        assert (
            is_bad_response(
                response,
                query=query,
                config={"tlm": tlm},
            )
            is expected
        )
