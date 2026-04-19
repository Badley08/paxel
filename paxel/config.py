import os
from pathlib import Path

APP_NAME = "Paxel"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Badley08"

# Je définis ici les chemins importants de l'application
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "paxel"
MEMORY_FILE = DATA_DIR / "memory.json"
CONFIG_FILE = DATA_DIR / "config.json"

# Je crée le dossier de données s'il n'existe pas encore
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Je configure le nom du bot et ses options par défaut
BOT_NAME = "Paxel"
DEFAULT_THEME = "dark"

# Je liste les dossiers auxquels Paxel est autorisé à accéder
ALLOWED_DIRS = [
    Path.home(),
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Pictures",
    Path.home() / "Music",
    Path.home() / "Videos",
    Path.home() / "Desktop",
]
