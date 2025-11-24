#-------------------------------------------
# Program: Time Keeper v2
# Description:
#   Portable multi-user, multi-project time tracker.
#   Tracks dev sessions, saves logs to JSON, and generates reports.
#
# Features:
#   - Clock in/out with timestamps
#   - Multi-user support with user switching and summary totals
#   - Per-project JSON log files
#   - Daily / weekly / monthly time reports
#   - Portable paths (default “data” folder next to script)
#   - Automatic folder creation and safe file handling
#   - Optional custom folder for log storage
#-------------------------------------------

import json
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DEFAULT_NAME = "default_project"


# --------- Path helpers ---------

BASE_DIR = Path(__file__).parent  # folder where this script lives


def slugify(name: str) -> str:
    """Get safe file name from a string. -> formatting"""
    name = name.strip().lower().replace(" ", "_")
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    cleaned = "".join(ch for ch in name if ch in allowed)
    return cleaned or "silly_goose"


def get_log_file(project_name: str, custom_folder: str | None) -> Path:
    """Return the JSON log file path for a given project and folder. -> JSON location"""
    if custom_folder:
        base = Path(custom_folder).expanduser()
    else:
        base = BASE_DIR / "data"

    project_slug = slugify(project_name or PROJECT_DEFAULT_NAME)
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{project_slug}_time_log.json"
