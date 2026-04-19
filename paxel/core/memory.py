"""
Je gère ici la mémoire persistante de Paxel.
Je stocke les données dans un fichier JSON local pour rester simple et léger.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from paxel.config import MEMORY_FILE


def load_memory() -> Dict[str, Any]:
    """Je charge la mémoire depuis le fichier JSON local."""
    if not MEMORY_FILE.exists():
        return _default_memory()
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Je m'assure que les champs obligatoires sont présents
            default = _default_memory()
            for key, value in default.items():
                if key not in data:
                    data[key] = value
            return data
    except (json.JSONDecodeError, OSError):
        return _default_memory()


def save_memory(memory: Dict[str, Any]) -> bool:
    """Je sauvegarde la mémoire dans le fichier JSON local."""
    try:
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def add_message(role: str, content: str) -> None:
    """J'ajoute un message à l'historique de la conversation."""
    memory = load_memory()
    import time
    message = {
        "role": role,
        "content": content,
        "timestamp": time.time(),
    }
    memory["history"].append(message)

    # Je limite l'historique aux 100 derniers messages pour éviter que le fichier grossisse trop
    if len(memory["history"]) > 100:
        memory["history"] = memory["history"][-100:]

    save_memory(memory)


def get_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Je retourne les derniers messages de l'historique."""
    memory = load_memory()
    return memory["history"][-limit:]


def clear_history() -> None:
    """J'efface l'historique des conversations."""
    memory = load_memory()
    memory["history"] = []
    save_memory(memory)


def set_preference(key: str, value: Any) -> None:
    """J'enregistre une préférence utilisateur."""
    memory = load_memory()
    memory["preferences"][key] = value
    save_memory(memory)


def get_preference(key: str, default: Any = None) -> Any:
    """Je récupère une préférence utilisateur."""
    memory = load_memory()
    return memory["preferences"].get(key, default)


def _default_memory() -> Dict[str, Any]:
    """Je retourne la structure mémoire par défaut."""
    return {
        "history": [],
        "preferences": {
            "theme": "dark",
            "language": "fr",
        },
        "version": "0.1.0",
    }
