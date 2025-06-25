import pytest
from unittest.mock import patch, MagicMock
from http import HTTPStatus

from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker import exceptions


# Patch the cache decorator to call the function directly (no caching)
@pytest.fixture(autouse=True)
def patch_cache(monkeypatch):
    monkeypatch.setattr("eco_tracker.api_cache.execute_or_get_from_cache", lambda **kwargs: lambda f: f)
    yield


@pytest.fixture
def categorizer():
    return BreactCategorizer("fake_api_key")

@patch("eco_tracker.categorization.breact.breact_categorization.requests.post")
@patch("eco_tracker.categorization.breact.breact_categorization.requests.get")
def test_classify_success_and_post_failure(mock_get, mock_post, categorizer):
    # Mock POST success
    mock_post.return_value = MagicMock(
        status_code=HTTPStatus.OK,
        json=lambda: {"access_token": "token123", "process_id": "proc123"}
    )
    # Mock GET success with nested result
    mock_get.return_value = MagicMock(
        status_code=HTTPStatus.OK,
        json=lambda: {"result": {"result": {"class": "Haushaltsgeraete", "confidence": 0.9}}}
    )
    result = categorizer._classify("product")
    assert result["class"] == "Haushaltsgeraete"
    assert result["confidence"] == 0.9

    # Mock POST failure triggers HTTPException
    mock_post.return_value = MagicMock(status_code=500, text="Server Error")
    with pytest.raises(exceptions.HTTPException) as e:
        categorizer._classify("product")
    assert e.value.status_code == 500


@patch("eco_tracker.categorization.breact.breact_categorization.requests.get")
def test_poll_for_result_success_and_timeout(mock_get, categorizer):
    # Success case with nested 'result' key present
    mock_get.return_value = MagicMock(
        status_code=HTTPStatus.OK,
        json=lambda: {"result": {"result": {"class": "some_class"}}}
    )
    response = categorizer._poll_for_result("http://fake-url", timeout=5, interval=0)
    assert "result" in response

    # Timeout case: simulate repeated non-200 responses
    mock_get.return_value = MagicMock(status_code=404, json=lambda: {})
    import time

    start_time = time.time()

    with patch("time.time", side_effect=[start_time, start_time + 6]):
        with pytest.raises(exceptions.HTTPException) as e:
            categorizer._poll_for_result("http://fake-url", timeout=5, interval=0)
        assert e.value.status_code == 504


def test_generate_categorization_branch(monkeypatch, categorizer):
    # confidence < 0.7 returns ["others"]
    monkeypatch.setattr(categorizer, "_classify", lambda product: {"confidence": 0.6, "class": "ClassX"})
    assert categorizer.generate_categorization("product") == ["others"]

    # confidence >= 0.7 returns list with class
    monkeypatch.setattr(categorizer, "_classify", lambda product: {"confidence": 0.8, "class": "ClassY"})
    assert categorizer.generate_categorization("product") == ["ClassY"]


def test_get_confidence_for_class_branches(monkeypatch, categorizer):
    # result is None branch
    monkeypatch.setattr(categorizer, "_classify", lambda product, allowed_classes=None: None)
    assert categorizer.get_confidence_for_class("product", "ClassA") == 0.0

    # result.get("class") != category branch
    monkeypatch.setattr(categorizer, "_classify", lambda product, allowed_classes=None: {"class": "ClassB", "confidence": 0.9})
    assert categorizer.get_confidence_for_class("product", "ClassA") == 0.0

    # normal branch where class matches
    monkeypatch.setattr(categorizer, "_classify", lambda product, allowed_classes=None: {"class": "ClassA", "confidence": 0.8})
    assert categorizer.get_confidence_for_class("product", "ClassA") == 0.8


def test_generate_confidences_filter_and_no_filter(monkeypatch, categorizer):
    sample_result = {
        "classifications": [
            {"class": "ClassA", "confidence": 0.9},
            {"class": "ClassB", "confidence": 0.7},
            {"class": "ClassC", "confidence": 0.3},
        ]
    }

    monkeypatch.setattr(categorizer, "_classify", lambda *args, **kwargs: sample_result)

    # With allowed_classes filter
    filtered = categorizer.generate_confidences("product", allowed_classes=["ClassA", "ClassC"])
    assert filtered == {"ClassA": 0.9, "ClassC": 0.3}

    # Without allowed_classes filter (should include all)
    all_classes = categorizer.generate_confidences("product")
    assert all_classes == {"ClassA": 0.9, "ClassB": 0.7, "ClassC": 0.3}
