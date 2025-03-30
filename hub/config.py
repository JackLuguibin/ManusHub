from pathlib import Path

DEFINE_PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFINE_LOGS_ROOT = DEFINE_PROJECT_ROOT.joinpath("logs")
DEFINE_DEFAULT_CONFIG_ROOT = DEFINE_PROJECT_ROOT.joinpath("configs")
DEFINE_MAIN_CONFIG_FILE = DEFINE_DEFAULT_CONFIG_ROOT.joinpath("main.config.yaml")