from __future__ import annotations

from pathlib import Path

APP_NAME = "Project Portfolio Dashboard"
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

PROJECTS_CSV = DATA_DIR / "projects.csv"
PERCENT_NOT_COMPLETED_CSV = DATA_DIR / "percentage_not_completed.csv"
EXAM_DATA_CSV = DATA_DIR / "exam_data.csv"

CACHE_DIR = ROOT_DIR / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

GEOCODE_CACHE_CSV = CACHE_DIR / "geocode_cache.csv"
