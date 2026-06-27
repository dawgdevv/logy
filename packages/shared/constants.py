from enum import StrEnum


class Difficulty(StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


CATEGORIES = [
    "feature",
    "bugfix",
    "refactor",
    "research",
    "learning",
    "infrastructure",
    "documentation",
    "other",
]

APP_NAME = "logy"
APP_VERSION = "0.1.0"
