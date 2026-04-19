"""
Je collecte ici les informations système de la machine Linux.
J'utilise psutil pour avoir des données fiables et cross-distro.
"""

import subprocess
from typing import Dict

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False


def get_uptime() -> str:
    """Je récupère le temps de fonctionnement du système."""
    try:
        if _PSUTIL_AVAILABLE:
            import time
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)

            parts = []
            if days > 0:
                parts.append(f"{days}j")
            if hours > 0:
                parts.append(f"{hours}h")
            parts.append(f"{minutes}min")
            return " ".join(parts)
        else:
            result = subprocess.run(["uptime", "-p"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
    except Exception as e:
        return f"Impossible de récupérer l'uptime : {e}"


def get_cpu_usage() -> float:
    """Je retourne le pourcentage d'utilisation du CPU."""
    try:
        if _PSUTIL_AVAILABLE:
            return psutil.cpu_percent(interval=1)
        else:
            result = subprocess.run(
                ["top", "-bn1"],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split("\n"):
                if "Cpu(s)" in line or "cpu" in line.lower():
                    import re
                    match = re.search(r"(\d+\.?\d*)\s*%?\s*us", line)
                    if match:
                        return float(match.group(1))
            return 0.0
    except Exception:
        return 0.0


def get_ram_usage() -> Dict[str, float]:
    """Je retourne les statistiques de mémoire RAM en gigaoctets."""
    try:
        if _PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            return {
                "total": mem.total / (1024 ** 3),
                "used": mem.used / (1024 ** 3),
                "available": mem.available / (1024 ** 3),
                "percent": mem.percent,
            }
        else:
            result = subprocess.run(["free", "-b"], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line.startswith("Mem:"):
                    parts = line.split()
                    total = int(parts[1]) / (1024 ** 3)
                    used = int(parts[2]) / (1024 ** 3)
                    available = int(parts[6]) / (1024 ** 3)
                    percent = (used / total) * 100
                    return {"total": total, "used": used, "available": available, "percent": percent}
    except Exception:
        pass
    return {"total": 0.0, "used": 0.0, "available": 0.0, "percent": 0.0}


def get_disk_usage(path: str = "/") -> Dict[str, float]:
    """Je retourne les statistiques d'utilisation du disque en gigaoctets."""
    try:
        if _PSUTIL_AVAILABLE:
            disk = psutil.disk_usage(path)
            return {
                "total": disk.total / (1024 ** 3),
                "used": disk.used / (1024 ** 3),
                "free": disk.free / (1024 ** 3),
                "percent": disk.percent,
            }
        else:
            result = subprocess.run(
                ["df", "-B1", path], capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                total = int(parts[1]) / (1024 ** 3)
                used = int(parts[2]) / (1024 ** 3)
                free = int(parts[3]) / (1024 ** 3)
                percent = float(parts[4].replace("%", ""))
                return {"total": total, "used": used, "free": free, "percent": percent}
    except Exception:
        pass
    return {"total": 0.0, "used": 0.0, "free": 0.0, "percent": 0.0}
