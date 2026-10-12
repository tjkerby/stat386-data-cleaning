"""Illustrative STAT 386 cleaning pipelines and fixed reference values.

The reference statistics belong to the three raw talks in data/talks_reference.csv.
For a predictive model, estimate them on training data only and reuse them later.
"""

import pandas as pd

PIPELINE_V1 = "talks-v1"
PIPELINE_V2 = "talks-v2"
REFERENCE_ID = "reference-T01-T03"
MEAN_WORDS = 2000.0
STD_WORDS = 1000.0  # Population standard deviation (ddof=0).
MIN_WORDS = 1000.0
MAX_WORDS = 3000.0


def _check_raw(raw: pd.DataFrame) -> None:
    needed = {"talk_id", "speaker", "title", "word_count"}
    missing = needed.difference(raw.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if raw["talk_id"].isna().any() or not raw["talk_id"].is_unique:
        raise ValueError("Every talk needs a unique, nonmissing talk_id")


def clean_v1(raw: pd.DataFrame) -> pd.DataFrame:
    """Trim and lowercase speaker keys; z-score counts with saved values."""
    _check_raw(raw)
    result = raw.copy()
    result["speaker_key"] = result["speaker"].astype("string").str.strip().str.lower()
    result["word_count"] = pd.to_numeric(result["word_count"], errors="raise")
    result["word_scaled"] = (result["word_count"] - MEAN_WORDS) / STD_WORDS
    result["pipeline_version"] = PIPELINE_V1
    result["scaling_reference"] = REFERENCE_ID
    return result


def clean_v2(raw: pd.DataFrame) -> pd.DataFrame:
    """Also collapse internal spaces; min-max scale with saved values."""
    _check_raw(raw)
    result = raw.copy()
    result["speaker_key"] = (
        result["speaker"].astype("string").str.split().str.join(" ").str.lower()
    )
    result["word_count"] = pd.to_numeric(result["word_count"], errors="raise")
    result["word_scaled"] = (result["word_count"] - MIN_WORDS) / (MAX_WORDS - MIN_WORDS)
    result["pipeline_version"] = PIPELINE_V2
    result["scaling_reference"] = REFERENCE_ID
    return result


def check_cleaned(result: pd.DataFrame, expected_version: str) -> None:
    """Basic checks on claims the pipeline makes; unknown speakers remain missing."""
    if not result["talk_id"].is_unique or result["talk_id"].isna().any():
        raise ValueError("Talk identity changed")
    if result["word_count"].isna().any() or (result["word_count"] < 0).any():
        raise ValueError("Invalid word count")
    if not result["pipeline_version"].eq(expected_version).all():
        raise ValueError("Unexpected pipeline version")
    if not result["scaling_reference"].eq(REFERENCE_ID).all():
        raise ValueError("Unexpected scaling reference")
    if result["speaker_key"].dropna().eq("").any():
        raise ValueError("Blank speaker key")
