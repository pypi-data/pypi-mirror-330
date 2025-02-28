"""
The output formater of the language detection.
"""

from typing import List, Tuple

from .constants import LANGUAGES, TOP_LANGUAGES


class OutputFormater:
    """
    The output of the language detection.
    """

    def __init__(
        self,
        detections_per_language: dict[str, int],
        reliability_threshold: float,
        filter_threshold: float,
        equal_traitements: bool,
    ):
        """Initialize the output of the language detection.

        Args:
            detections_per_language (dict[str, int]): the number of detections per language.
            reliability_threshold (float): the threshold to consider a language as reliable.
            filter_threshold (float): the threshold to filter the languages.
            equal_traitements (bool): if True, all detectors are considered equally important.
        """
        self._detections_per_language = detections_per_language
        self._reliability_threshold = reliability_threshold
        self._filter_threshold = filter_threshold
        self._equal_traitements = equal_traitements

    def _score_threshold(
        self, scores: List[Tuple[str, float]], threshold: float = 0.0
    ) -> List[Tuple[str, float]]:
        """Removes the languages with a score below the threshold.

        Args:
            scores (List[Tuple[str, float]]): The list of languages and their scores.

        Returns:
            List[Tuple[str, float]]: The list of languages and their scores above the threshold.
        """
        return [(lang, score) for lang, score in scores if score >= threshold]

    def _sort_by_language_popularity(
        self, scores: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        """Sorts the languages by popularity.

        Args:
            scores (List[Tuple[str, float]]): The list of languages and their scores.

        Returns:
            List[Tuple[str, float]]: The list of languages and their scores sorted by popularity.
        """
        # sort equal scores by the top languages
        # [('fr', 1.0), ('ro', 0.5), ('en', 0.5), ('ca', 0.25), ('es', 0.25)]
        # becomes
        # [('fr', 1.0), ('en', 0.5), ('ro', 0.5), ('es', 0.25), ('ca', 0.25)]

        result = sorted(
            scores,
            key=lambda x: (
                x[1],
                (
                    -TOP_LANGUAGES.index(x[0])
                    if x[0] in TOP_LANGUAGES
                    else -len(TOP_LANGUAGES)
                ),
            ),
            reverse=True,
        )

        return result

    def _normalize_scores(
        self, scores: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        output = []
        for lang, score in scores:
            output.append((lang, score / self._detections_per_language[lang]))
        return output

    def _filter_unsupported_languages(
        self, predictions: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        return [
            (lang, score)
            for lang, score in predictions
            if lang in self._detections_per_language
        ]

    def format_predictions(
        self,
        predictions: List[Tuple[str, float]],
        apply_end_score_normalization: bool = True,
    ) -> List[dict[str, float, bool]]:
        """Formats the predictions of the language detection.

        Args:
            predictions (List[Tuple[str, float]]): The predictions of the language detection.
            apply_end_score_normalization (bool, optional): If True, the scores are normalized by the number of detections for each language. Defaults to True.

        Returns:
            List[dict[str, float, bool]]: The formatted predictions of the language detection.
        """

        # unify the predictions
        scores = {}
        for prediction in predictions:
            for lang, score in prediction:
                if lang not in scores:
                    scores[lang] = 0
                scores[lang] += score

        predictions = self._filter_unsupported_languages(list(scores.items()))

        # Normalize the predictions scores by the number of detections for each language before sorting
        # the order is important because each detector can have a different number of detections so scores can be more
        # hurt by the normalization
        if self._equal_traitements:
            scores = self._normalize_scores(scores)

        # Sort the predictions by score
        predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
        predictions = self._score_threshold(predictions, self._filter_threshold)

        predictions = self._sort_by_language_popularity(predictions)

        # if not equal traitements, normalize the scores after sorting
        # language with more detectors have advantage
        if (
            not self._equal_traitements and apply_end_score_normalization
        ):  # when only one detector, no need to normalize
            predictions = self._normalize_scores(predictions)

        results = []
        for i, (lang, score) in enumerate(predictions):
            results.append(
                {
                    "language": str(LANGUAGES.from_iso_code_639_1_str(lang)),
                    "code": str(LANGUAGES.from_iso_code_639_1_str(lang).iso_code_639_1),
                    "score": round(score, 2),
                    "prefered": i == 0 and score >= self._reliability_threshold,
                    "reliable": score >= self._reliability_threshold,
                }
            )

        return tuple(results)
