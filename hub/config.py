from pathlib import Path

DEFINE_PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFINE_LOGS_ROOT = DEFINE_PROJECT_ROOT.joinpath("logs")