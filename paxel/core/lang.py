"""
Je gère ici la détection automatique de la langue des messages.
Je supporte le Français, l'Anglais et l'Espagnol.
"""

from typing import Literal

Lang = Literal["fr", "en", "es"]

# Je regroupe ici les mots-clés caractéristiques de chaque langue
_FR_MARKERS = {
    "bonjour", "salut", "bonsoir", "merci", "aide", "liste", "fichier",
    "dossier", "disque", "mémoire", "memoire", "processeur", "depuis",
    "allumé", "espace", "stockage", "cherche", "recherche", "météo",
    "meteo", "temps", "comment", "quoi", "pourquoi", "quand", "où",
    "oui", "non", "voici", "voilà", "affiche", "montre", "donne",
    "quelle", "quel", "je", "tu", "il", "nous", "vous",
}

_EN_MARKERS = {
    "hello", "hi", "hey", "thanks", "thank", "help", "list", "file",
    "folder", "directory", "disk", "memory", "cpu", "processor", "uptime",
    "space", "storage", "search", "find", "weather", "forecast", "show",
    "display", "give", "what", "when", "where", "why", "how", "yes",
    "no", "please", "can", "could", "would", "do", "does", "is", "are",
    "get", "open", "run", "check",
}

_ES_MARKERS = {
    "hola", "buenos", "buenas", "gracias", "ayuda", "lista", "archivo",
    "carpeta", "disco", "memoria", "procesador", "desde", "encendido",
    "espacio", "almacenamiento", "busca", "buscar", "busco", "tiempo",
    "clima", "muestra", "ver", "mostrar", "dame", "qué", "que", "cuando",
    "dónde", "donde", "cómo", "como", "por", "para", "sí", "no", "favor",
    "puedes", "puede", "quiero", "tengo", "sistema",
}


def detect_language(message: str, fallback: Lang = "fr") -> Lang:
    """
    Je détecte la langue du message en comptant les mots-clés caractéristiques.
    Je retourne 'fr', 'en' ou 'es'. En cas d'ambiguïté, j'utilise le fallback.
    """
    words = set(message.lower().split())

    scores = {
        "fr": len(words & _FR_MARKERS),
        "en": len(words & _EN_MARKERS),
        "es": len(words & _ES_MARKERS),
    }

    best_lang = max(scores, key=lambda k: scores[k])
    best_score = scores[best_lang]

    # Si aucun mot-clé reconnu, je retourne le fallback
    if best_score == 0:
        return fallback

    return best_lang


def get_lang_label(lang: Lang) -> str:
    """Je retourne le nom lisible de la langue détectée."""
    return {"fr": "Français", "en": "English", "es": "Español"}.get(lang, "Français")
