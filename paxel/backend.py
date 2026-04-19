"""
Je gère ici le backend de Paxel.
Je détecte automatiquement la langue (FR, EN, ES) et je route chaque message
vers la bonne commande. J'utilise le Mock Backend pour des réponses riches
et cohérentes dans les trois langues.
"""

import re
from paxel.core.lang import detect_language, Lang
from paxel.core.mock_backend import (
    get_greeting, get_unknown, get_thanks, get_help, get_joke, get_linux_fact,
    format_cpu, format_ram, format_disk, format_uptime, format_system_summary,
    format_weather_label, format_search_label, format_files_label, get_clear_message,
)
from paxel.core.system import get_uptime, get_cpu_usage, get_ram_usage, get_disk_usage
from paxel.core.weather import get_weather
from paxel.core.web import search_duckduckgo
from paxel.core.files import list_files
from paxel.core.memory import get_preference, set_preference, clear_history


# ---------------------------------------------------------------------------
# Mots-clés de commandes regroupés par catégorie et par langue
# ---------------------------------------------------------------------------

_CMD_UPTIME = {
    "uptime", "depuis quand", "allumé", "démarré", "how long", "boot time",
    "desde cuando", "encendido", "arrancado",
}

_CMD_CPU = {
    "cpu", "processeur", "processor", "procesador",
    "charge cpu", "cpu load", "carga cpu",
}

_CMD_RAM = {
    "ram", "mémoire", "memoire", "memory", "memoria",
}

_CMD_DISK = {
    "disque", "disk", "disco", "stockage", "storage", "almacenamiento",
    "espace", "space", "espacio",
}

_CMD_SYSTEM = {
    "système", "systeme", "system", "sistema",
    "résumé", "resume", "resumen", "bilan", "overview",
}

_CMD_WEATHER = {
    "météo", "meteo", "weather", "clima", "tiempo",
    "température", "temperature", "temperatura",
}

_CMD_SEARCH = {
    "cherche", "recherche", "search", "busca", "buscar", "busco", "find",
    "google", "duckduckgo", "ddg",
}

_CMD_FILES = {
    "liste", "list", "lista", "fichiers", "files", "archivos",
    "dossier", "folder", "carpeta", "ls", "dir",
}

_CMD_JOKE = {
    "blague", "joke", "chiste", "humour", "humor",
    "fais moi rire", "make me laugh", "hazme reír",
}

_CMD_LINUX_FACT = {
    "info linux", "linux fact", "dato linux", "fait linux",
    "histoire linux", "linux history", "anecdote linux",
}

_CMD_GREET = {
    "bonjour", "salut", "bonsoir", "hello", "hi", "hey",
    "hola", "buenos días", "buenas tardes", "buenas noches",
    "coucou", "yo", "good morning", "good evening",
}

_CMD_THANKS = {
    "merci", "thanks", "thank you", "gracias", "thx", "ty",
    "parfait", "super", "great", "genial", "génial",
}

_CMD_HELP = {
    "aide", "help", "ayuda", "?", "commandes", "commands", "comandos",
    "que sais-tu", "what can you do", "qué puedes hacer",
}

_CMD_CLEAR = {
    "effacer", "clear", "borrar", "reset", "recommencer",
    "nouvelle conversation", "new conversation", "nueva conversación",
    "vider", "flush",
}


# ---------------------------------------------------------------------------
# Fonction principale de traitement
# ---------------------------------------------------------------------------

def process_message(message: str) -> str:
    """
    Je traite le message de l'utilisateur :
    1. Je détecte la langue automatiquement
    2. Je sauvegarde la langue préférée en mémoire
    3. Je route vers la bonne commande
    4. Je retourne une réponse localisée
    """
    msg_lower = message.lower().strip()

    # Je détecte la langue — je réutilise la préférence mémorisée comme fallback
    stored_lang = get_preference("language", "fr")
    lang: Lang = detect_language(message, fallback=stored_lang)

    # Je mémorise la langue détectée pour les prochains messages ambigus
    if lang != stored_lang:
        set_preference("language", lang)

    # --- Salutations ---
    if _matches(msg_lower, _CMD_GREET):
        return get_greeting(lang)

    # --- Remerciements ---
    if _matches(msg_lower, _CMD_THANKS):
        return get_thanks(lang)

    # --- Aide ---
    if _matches(msg_lower, _CMD_HELP):
        return get_help(lang)

    # --- Effacer la conversation ---
    if _matches(msg_lower, _CMD_CLEAR):
        clear_history()
        return get_clear_message(lang)

    # --- Blague ---
    if _matches(msg_lower, _CMD_JOKE):
        return get_joke(lang)

    # --- Fait Linux ---
    if _matches(msg_lower, _CMD_LINUX_FACT):
        return get_linux_fact(lang)

    # --- Résumé système complet ---
    if _matches(msg_lower, _CMD_SYSTEM):
        uptime = get_uptime()
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        disk = get_disk_usage()
        return format_system_summary(lang, uptime, cpu, ram, disk)

    # --- Uptime ---
    if _matches(msg_lower, _CMD_UPTIME):
        uptime = get_uptime()
        return format_uptime(lang, uptime)

    # --- CPU ---
    if _matches(msg_lower, _CMD_CPU):
        cpu = get_cpu_usage()
        return format_cpu(lang, cpu)

    # --- RAM ---
    if _matches(msg_lower, _CMD_RAM):
        ram = get_ram_usage()
        return format_ram(lang, ram)

    # --- Disque ---
    if _matches(msg_lower, _CMD_DISK):
        disk = get_disk_usage()
        return format_disk(lang, disk)

    # --- Météo ---
    if _matches(msg_lower, _CMD_WEATHER):
        city = _extract_city(message, lang)
        weather = get_weather(city)
        label = format_weather_label(lang, city)
        return f"{label}\n{weather}"

    # --- Recherche web ---
    if _matches(msg_lower, _CMD_SEARCH):
        query = _extract_search_query(message, lang)
        if query:
            results = search_duckduckgo(query)
            label = format_search_label(lang, query)
            return f"{label}\n{results}"

    # --- Liste de fichiers ---
    if _matches(msg_lower, _CMD_FILES):
        path = _extract_path(message)
        result = list_files(path)
        label = format_files_label(lang, path)
        return f"{label}\n{result}"

    # --- Réponse par défaut du Mock Backend ---
    return get_unknown(lang)


# ---------------------------------------------------------------------------
# Utilitaires internes
# ---------------------------------------------------------------------------

def _matches(msg_lower: str, keywords: set) -> bool:
    """
    Je vérifie si le message contient l'un des mots-clés donnés.
    Je supporte les mots-clés simples et les expressions multi-mots.
    """
    for keyword in keywords:
        if keyword in msg_lower:
            return True
    return False


def _extract_city(message: str, lang: Lang) -> str:
    """
    J'extrais le nom de la ville depuis le message météo.
    Je cherche après les prépositions courantes dans chaque langue.
    """
    triggers_by_lang = {
        "fr": ["météo à", "météo de", "meteo à", "meteo de", "temps à", "temps de", "météo pour"],
        "en": ["weather in", "weather for", "weather at", "forecast for", "forecast in"],
        "es": ["clima en", "tiempo en", "clima de", "temperatura en"],
    }
    triggers = triggers_by_lang.get(lang, triggers_by_lang["fr"])
    msg_lower = message.lower()

    for trigger in triggers:
        if trigger in msg_lower:
            idx = msg_lower.find(trigger) + len(trigger)
            rest = message[idx:].strip()
            city = rest.split()[0].strip("?.,!") if rest.split() else ""
            if city and len(city) > 1:
                return city

    # Fallback : je cherche un mot capitalisé après les mots-clés météo
    words = message.split()
    weather_words = {"météo", "meteo", "weather", "clima", "tiempo", "forecast", "température"}
    for i, word in enumerate(words):
        if word.lower() in weather_words and i + 1 < len(words):
            candidate = words[i + 1].strip("?.,!")
            if candidate and candidate[0].isupper() and len(candidate) > 1:
                return candidate

    return ""


def _extract_search_query(message: str, lang: Lang) -> str:
    """J'extrais la requête de recherche depuis le message."""
    triggers_by_lang = {
        "fr": ["cherche", "recherche", "rechercher", "trouver", "googler"],
        "en": ["search", "find", "look for", "google"],
        "es": ["busca", "buscar", "busco", "encontrar"],
    }
    triggers = triggers_by_lang.get(lang, triggers_by_lang["fr"])
    msg_lower = message.lower()

    for trigger in sorted(triggers, key=len, reverse=True):
        if trigger in msg_lower:
            idx = msg_lower.find(trigger) + len(trigger)
            rest = message[idx:].strip()
            if rest:
                return rest

    return message.strip()


def _extract_path(message: str) -> str:
    """J'extrais un chemin de fichier depuis le message."""
    path_match = re.search(r"[~/][\w/.\-]+", message)
    if path_match:
        return path_match.group(0)
    return ""
