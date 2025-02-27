""" 
Language detection using FastText
"""

import os

import fasttext

from .constants import LANGUAGES, WEIGHTS_PATH
from .detector import AbstractDetector

fasttext.FastText.eprint = lambda x: None


class FastTextDetector(AbstractDetector):
    """A language detector based on FastText"""

    def __init__(
        self,
        weight: str,
        weighted_reliability: float = 1.0,
    ) -> None:
        """Load the FastText model"""
        self._model = fasttext.load_model(os.path.join(WEIGHTS_PATH, weight))
        self._weighted_reliability = weighted_reliability

    def detect(self, text):
        preds = self._model.predict(text.lower(), k=5)

        predictions = []
        for i in range(len(preds[0])):
            predictions.append(
                (
                    preds[0][i][9:],  # Remove the "__label__" prefix
                    round(preds[1][i] * self._weighted_reliability, 2),
                )
            )

        return predictions

    @property
    def supported_languages(self):
        languages = [
            label[9:] for label in self._model.get_labels()
        ]  # Remove the "__label__" prefix

        # filter out unsupported languages
        return [
            lang
            for lang in languages
            if lang.upper() in LANGUAGES.all_iso_codes_639_1()
        ]
