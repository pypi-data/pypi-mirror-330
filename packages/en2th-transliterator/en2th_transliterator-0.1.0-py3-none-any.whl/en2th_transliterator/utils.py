"""Utility functions for English-to-Thai transliteration."""

import pandas as pd
import editdistance


def clean_text(text):
    """Clean and validate text input."""
    if pd.isna(text):
        return ""
    try:
        cleaned = str(text).strip()
        return cleaned
    except Exception:
        return ""


def word_accuracy(predictions, references):
    """Calculate word-level accuracy."""
    correct = sum(1 for p, r in zip(predictions, references) if p == r)
    return correct / len(references) if len(references) > 0 else 0


def character_error_rate(predictions, references):
    """Calculate character error rate."""
    total_chars = sum(len(r) for r in references)
    total_edits = sum(
        editdistance.eval(p, r) for p, r in zip(predictions, references))
    return total_edits / total_chars if total_chars > 0 else 0


def mean_levenshtein_distance(predictions, references):
    """Calculate mean Levenshtein distance."""
    distances = [
        editdistance.eval(p, r) for p, r in zip(predictions, references)
    ]
    return sum(distances) / len(distances) if distances else 0


def evaluate_predictions(predictions, references):
    """Evaluate predictions against references."""
    metrics = {
        'accuracy':
        word_accuracy(predictions, references),
        'character_error_rate':
        character_error_rate(predictions, references),
        'mean_levenshtein_distance':
        mean_levenshtein_distance(predictions, references),
    }
    return metrics
