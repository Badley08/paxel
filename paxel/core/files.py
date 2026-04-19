"""
Je gère ici les opérations sur les fichiers de manière sécurisée.
Je limite l'accès aux dossiers autorisés et j'évite toute action destructive non contrôlée.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional

from paxel.config import ALLOWED_DIRS


def _is_path_allowed(path: Path) -> bool:
    """Je vérifie que le chemin est dans la liste des dossiers autorisés."""
    try:
        resolved = path.resolve()
        for allowed in ALLOWED_DIRS:
            try:
                resolved.relative_to(allowed.resolve())
                return True
            except ValueError:
                continue
        return False
    except Exception:
        return False


def list_files(directory: Optional[str] = None) -> str:
    """
    Je liste les fichiers d'un dossier.
    Si aucun dossier n'est fourni, je liste le home de l'utilisateur.
    """
    if directory:
        target = Path(directory).expanduser()
    else:
        target = Path.home()

    if not target.exists():
        return f"❌ Le dossier '{target}' n'existe pas."

    if not target.is_dir():
        return f"❌ '{target}' n'est pas un dossier."

    if not _is_path_allowed(target):
        return f"🔒 Accès refusé : '{target}' n'est pas dans les dossiers autorisés."

    try:
        entries = sorted(target.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
        lines = []
        for entry in entries:
            if entry.is_dir():
                lines.append(f"📁 {entry.name}/")
            elif entry.is_file():
                size = entry.stat().st_size
                size_str = _format_size(size)
                lines.append(f"📄 {entry.name} ({size_str})")
            else:
                lines.append(f"🔗 {entry.name}")

        if not lines:
            return "📭 Dossier vide."

        return "\n".join(lines)
    except PermissionError:
        return f"🔒 Permission refusée pour '{target}'."
    except Exception as e:
        return f"❌ Erreur : {e}"


def delete_file(filepath: str) -> str:
    """
    Je supprime un fichier de manière sécurisée.
    Je vérifie toujours que le chemin est autorisé avant toute suppression.
    """
    target = Path(filepath).expanduser()

    if not target.exists():
        return f"❌ Le fichier '{target}' n'existe pas."

    if not _is_path_allowed(target):
        return f"🔒 Accès refusé : '{target}' n'est pas dans les dossiers autorisés."

    if target.is_dir():
        return f"⚠️ '{target}' est un dossier. Je ne supprime pas les dossiers via cette commande."

    try:
        target.unlink()
        return f"✅ Fichier '{target.name}' supprimé avec succès."
    except PermissionError:
        return f"🔒 Permission refusée pour supprimer '{target}'."
    except Exception as e:
        return f"❌ Erreur lors de la suppression : {e}"


def get_file_info(filepath: str) -> str:
    """Je retourne les informations détaillées d'un fichier."""
    target = Path(filepath).expanduser()

    if not target.exists():
        return f"❌ '{target}' n'existe pas."

    if not _is_path_allowed(target):
        return f"🔒 Accès refusé : '{target}' n'est pas dans les dossiers autorisés."

    try:
        stat = target.stat()
        size = _format_size(stat.st_size)
        import datetime
        modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M")
        return (
            f"📄 Informations sur '{target.name}' :\n"
            f"  • Chemin : {target}\n"
            f"  • Taille : {size}\n"
            f"  • Modifié : {modified}\n"
            f"  • Type : {'Dossier' if target.is_dir() else 'Fichier'}"
        )
    except Exception as e:
        return f"❌ Erreur : {e}"


def _format_size(size_bytes: int) -> str:
    """Je formate la taille d'un fichier de manière lisible."""
    if size_bytes < 1024:
        return f"{size_bytes} o"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} Ko"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} Mo"
    else:
        return f"{size_bytes / (1024 ** 3):.1f} Go"
