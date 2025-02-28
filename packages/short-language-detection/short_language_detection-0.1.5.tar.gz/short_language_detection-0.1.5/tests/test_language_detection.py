import random

import pytest

from src.short_language_detection import Detector


@pytest.fixture
def detector():
    return Detector()


def test_detect_english(detector):
    text = "This is a test sentence."
    result = detector.detect(text)
    assert result[0]["language"] == "ENGLISH"
    assert result[0]["code"] == "EN"
    assert result[0]["reliable"]


def test_detect_portuguese(detector):
    text = "Esta é uma frase de teste."
    result = detector.detect(text)
    assert result[0]["language"] == "PORTUGUESE"
    assert result[0]["code"] == "PT"
    assert result[0]["reliable"]


def test_detect_french(detector):
    text = "Ceci est une phrase de test."
    result = detector.detect(text)
    assert result[0]["language"] == "FRENCH"
    assert result[0]["code"] == "FR"
    assert result[0]["reliable"]


def test_detect_spanish(detector):
    text = "Esta es una frase de prueba."
    result = detector.detect(text)
    assert result[0]["language"] == "SPANISH"
    assert result[0]["code"] == "ES"
    assert result[0]["reliable"]


def test_empty_text(detector):
    text = ""
    result = detector.detect(text)
    assert result == []


def test_space_text(detector):
    text = " "
    result = detector.detect(text)
    assert result == []


@pytest.mark.timeout(1)
def test_long_text(detector):
    # random text
    text = "".join(random.choices("abcdefghijklmnopqrstuvwxyz '!:.", k=1000000))
    detector.detect(text)


def test_invalid_text(detector):
    text = "123"
    result = detector.detect(text)
    assert result == []


def test_languages_list(detector):
    languages = detector.supported_languages
    assert languages["en"] == "ENGLISH"
    assert languages["fr"] == "FRENCH"
    assert languages["es"] == "SPANISH"
    assert languages["pt"] == "PORTUGUESE"
    assert languages["ro"] == "ROMANIAN"
    assert languages["ru"] == "RUSSIAN"
    assert languages["nl"] == "DUTCH"
    assert languages["it"] == "ITALIAN"
    assert languages["de"] == "GERMAN"
    assert len(languages) == 132
