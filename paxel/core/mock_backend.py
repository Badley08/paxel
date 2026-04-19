"""
Je suis le Mock Backend de Paxel.
Je fournis des réponses simulées riches et cohérentes en Français, Anglais et Espagnol,
sans dépendre d'un vrai modèle de langage. Je suis conçu pour être facilement remplaçable
par un vrai backend IA dans une version future.
"""

import random
from typing import Dict, List
from paxel.core.lang import Lang


# ---------------------------------------------------------------------------
# Je définis ici les réponses mock par catégorie et par langue
# ---------------------------------------------------------------------------

_GREETINGS: Dict[Lang, List[str]] = {
    "fr": [
        "👋 Bonjour ! Je suis Paxel, ton assistant Linux. Tape **aide** pour voir mes commandes.",
        "🤖 Salut ! Content de te voir. Comment puis-je t'aider aujourd'hui ?",
        "👋 Bonsoir ! Paxel est là. Qu'est-ce que je peux faire pour toi ?",
    ],
    "en": [
        "👋 Hello! I'm Paxel, your Linux assistant. Type **help** to see what I can do.",
        "🤖 Hey there! Happy to assist. What can I do for you today?",
        "👋 Hi! Paxel here. How can I help you?",
    ],
    "es": [
        "👋 ¡Hola! Soy Paxel, tu asistente Linux. Escribe **ayuda** para ver mis comandos.",
        "🤖 ¡Buenas! Encantado de ayudarte. ¿En qué puedo servirte?",
        "👋 ¡Hola! Paxel a tu servicio. ¿Qué necesitas?",
    ],
}

_UNKNOWN: Dict[Lang, List[str]] = {
    "fr": [
        "🤔 Je ne suis pas sûr de comprendre. Essaie de reformuler ou tape **aide** pour voir mes commandes.",
        "💬 Hmm, je n'ai pas de réponse précise pour ça. Je suis encore en apprentissage ! Tape **aide** pour mes fonctionnalités.",
        "🙃 Cette requête me dépasse un peu… Voici ce que je sais faire : tape **aide**.",
    ],
    "en": [
        "🤔 I'm not sure I understand. Try rephrasing or type **help** to see my commands.",
        "💬 Hmm, I don't have a precise answer for that. I'm still learning! Type **help** for my features.",
        "🙃 That's a bit beyond me… Here's what I can do: type **help**.",
    ],
    "es": [
        "🤔 No estoy seguro de entender. Intenta reformular o escribe **ayuda** para ver mis comandos.",
        "💬 Hmm, no tengo una respuesta precisa para eso. ¡Sigo aprendiendo! Escribe **ayuda** para mis funciones.",
        "🙃 Eso me supera un poco… Esto es lo que puedo hacer: escribe **ayuda**.",
    ],
}

_THANKS: Dict[Lang, List[str]] = {
    "fr": [
        "😊 Avec plaisir ! N'hésite pas si tu as besoin d'autre chose.",
        "🙌 De rien ! Je suis là si tu as d'autres questions.",
        "✨ Tout le plaisir est pour moi !",
    ],
    "en": [
        "😊 You're welcome! Don't hesitate if you need anything else.",
        "🙌 No problem! I'm here if you have more questions.",
        "✨ My pleasure!",
    ],
    "es": [
        "😊 ¡De nada! No dudes en preguntar si necesitas algo más.",
        "🙌 ¡Con gusto! Aquí estoy si tienes más preguntas.",
        "✨ ¡El placer es mío!",
    ],
}

_HELP: Dict[Lang, str] = {
    "fr": (
        "📖 **Commandes disponibles :**\n\n"
        "  🖥️  **Système :**\n"
        "     • `uptime` — temps de fonctionnement du système\n"
        "     • `cpu` — utilisation du processeur\n"
        "     • `ram` / `mémoire` — utilisation de la mémoire\n"
        "     • `disque` / `espace` — espace de stockage\n"
        "     • `système` — résumé complet\n\n"
        "  📁 **Fichiers :**\n"
        "     • `liste [chemin]` — lister les fichiers d'un dossier\n\n"
        "  🌤️  **Météo :**\n"
        "     • `météo [ville]` — conditions météo actuelles\n\n"
        "  🔍 **Recherche :**\n"
        "     • `cherche [requête]` — recherche DuckDuckGo\n\n"
        "  💬 **Conversation :**\n"
        "     • `blague` — une blague aléatoire\n"
        "     • `info linux` — un fait sur Linux\n"
        "     • `effacer` — effacer la conversation\n\n"
        "  🌐 **Langues supportées :** Français · English · Español\n"
        "  ℹ️  `aide` / `help` / `ayuda` — afficher ce message"
    ),
    "en": (
        "📖 **Available commands:**\n\n"
        "  🖥️  **System:**\n"
        "     • `uptime` — system uptime\n"
        "     • `cpu` — processor usage\n"
        "     • `ram` / `memory` — memory usage\n"
        "     • `disk` / `space` — storage space\n"
        "     • `system` — full summary\n\n"
        "  📁 **Files:**\n"
        "     • `list [path]` — list files in a folder\n\n"
        "  🌤️  **Weather:**\n"
        "     • `weather [city]` — current weather conditions\n\n"
        "  🔍 **Search:**\n"
        "     • `search [query]` — DuckDuckGo search\n\n"
        "  💬 **Chat:**\n"
        "     • `joke` — a random joke\n"
        "     • `linux fact` — a Linux fun fact\n"
        "     • `clear` — clear the conversation\n\n"
        "  🌐 **Supported languages:** Français · English · Español\n"
        "  ℹ️  `help` / `aide` / `ayuda` — show this message"
    ),
    "es": (
        "📖 **Comandos disponibles:**\n\n"
        "  🖥️  **Sistema:**\n"
        "     • `uptime` — tiempo de funcionamiento\n"
        "     • `cpu` — uso del procesador\n"
        "     • `ram` / `memoria` — uso de memoria\n"
        "     • `disco` / `espacio` — espacio de almacenamiento\n"
        "     • `sistema` — resumen completo\n\n"
        "  📁 **Archivos:**\n"
        "     • `lista [ruta]` — listar archivos de una carpeta\n\n"
        "  🌤️  **Clima:**\n"
        "     • `clima [ciudad]` — condiciones climáticas actuales\n\n"
        "  🔍 **Búsqueda:**\n"
        "     • `busca [consulta]` — búsqueda en DuckDuckGo\n\n"
        "  💬 **Conversación:**\n"
        "     • `chiste` — un chiste aleatorio\n"
        "     • `dato linux` — un dato sobre Linux\n"
        "     • `borrar` — borrar la conversación\n\n"
        "  🌐 **Idiomas soportados:** Français · English · Español\n"
        "  ℹ️  `ayuda` / `help` / `aide` — mostrar este mensaje"
    ),
}

_JOKES: Dict[Lang, List[str]] = {
    "fr": [
        "😄 Pourquoi les programmeurs confondent-ils Halloween et Noël ? Parce que Oct 31 == Dec 25 !",
        "🤣 Un administrateur système entre dans un bar. Personne ne remarque — le serveur est tombé.",
        "😂 Comment appelle-t-on un pingouin sous Windows ? Un virus.",
        "😆 Un bug, c'est une feature non documentée.",
        "🙃 Pourquoi Linux ne tombe jamais malade ? Parce qu'il a un bon système immunitaire... et un pare-feu.",
    ],
    "en": [
        "😄 Why do programmers confuse Halloween and Christmas? Because Oct 31 == Dec 25!",
        "🤣 A sysadmin walks into a bar. Nobody notices — the server is down.",
        "😂 Why did the Linux server go to therapy? Too many root issues.",
        "😆 There are only 10 types of people: those who understand binary, and those who don't.",
        "🙃 Real programmers don't comment their code. If it was hard to write, it should be hard to understand.",
    ],
    "es": [
        "😄 ¿Por qué los programadores confunden Halloween y Navidad? Porque Oct 31 == Dic 25.",
        "🤣 Un administrador de sistemas entra a un bar. Nadie lo nota — el servidor está caído.",
        "😂 ¿Qué le dice un bit a otro? Te veo en el bus.",
        "😆 Hay 10 tipos de personas: las que entienden binario y las que no.",
        "🙃 Los bugs no son errores, son características no documentadas.",
    ],
}

_LINUX_FACTS: Dict[Lang, List[str]] = {
    "fr": [
        "🐧 Linux a été créé par Linus Torvalds en 1991, alors qu'il était étudiant à Helsinki.",
        "📊 Environ 96% des serveurs web du monde tournent sous Linux.",
        "🔑 Le noyau Linux contient plus de 30 millions de lignes de code.",
        "🚀 La Station Spatiale Internationale (ISS) utilise Linux pour ses systèmes critiques.",
        "🤝 Android, le système mobile le plus utilisé au monde, est basé sur le noyau Linux.",
        "📦 Arch Linux suit un modèle de mise à jour continue appelé 'rolling release'.",
        "🛡️ Le mascotte de Linux, Tux le pingouin, a été choisi parce que Linus Torvalds aimait les pingouins.",
    ],
    "en": [
        "🐧 Linux was created by Linus Torvalds in 1991 while he was a student in Helsinki.",
        "📊 About 96% of the world's web servers run Linux.",
        "🔑 The Linux kernel contains over 30 million lines of code.",
        "🚀 The International Space Station (ISS) uses Linux for its critical systems.",
        "🤝 Android, the most used mobile OS, is based on the Linux kernel.",
        "📦 Arch Linux follows a rolling release update model.",
        "🛡️ Linux's mascot, Tux the penguin, was chosen because Linus Torvalds loved penguins.",
    ],
    "es": [
        "🐧 Linux fue creado por Linus Torvalds en 1991 mientras era estudiante en Helsinki.",
        "📊 Aproximadamente el 96% de los servidores web del mundo funcionan con Linux.",
        "🔑 El núcleo Linux contiene más de 30 millones de líneas de código.",
        "🚀 La Estación Espacial Internacional (ISS) usa Linux para sus sistemas críticos.",
        "🤝 Android, el sistema móvil más usado del mundo, está basado en el núcleo Linux.",
        "📦 Arch Linux sigue un modelo de actualización continua llamado 'rolling release'.",
        "🛡️ La mascota de Linux, Tux el pingüino, fue elegida porque Linus Torvalds amaba los pingüinos.",
    ],
}

_SYSTEM_SUMMARY_LABELS: Dict[Lang, Dict[str, str]] = {
    "fr": {
        "title": "📊 Résumé du système",
        "uptime": "⏱️  Uptime",
        "cpu": "⚙️  CPU",
        "ram_used": "💾 RAM utilisée",
        "ram_total": "💾 RAM totale",
        "disk_used": "💿 Disque utilisé",
        "disk_free": "💿 Disque libre",
    },
    "en": {
        "title": "📊 System summary",
        "uptime": "⏱️  Uptime",
        "cpu": "⚙️  CPU",
        "ram_used": "💾 RAM used",
        "ram_total": "💾 RAM total",
        "disk_used": "💿 Disk used",
        "disk_free": "💿 Disk free",
    },
    "es": {
        "title": "📊 Resumen del sistema",
        "uptime": "⏱️  Uptime",
        "cpu": "⚙️  CPU",
        "ram_used": "💾 RAM usada",
        "ram_total": "💾 RAM total",
        "disk_used": "💿 Disco usado",
        "disk_free": "💿 Disco libre",
    },
}

_CPU_LABELS: Dict[Lang, Dict[str, str]] = {
    "fr": {"title": "⚙️ Utilisation du CPU", "low": "Tout va bien, le CPU respire.", "mid": "Charge modérée.", "high": "Attention, le CPU est sous pression !"},
    "en": {"title": "⚙️ CPU usage", "low": "All good, the CPU is breathing easy.", "mid": "Moderate load.", "high": "Warning, the CPU is under pressure!"},
    "es": {"title": "⚙️ Uso del CPU", "low": "Todo bien, el CPU está tranquilo.", "mid": "Carga moderada.", "high": "¡Atención, el CPU está bajo presión!"},
}

_RAM_LABELS: Dict[Lang, Dict[str, str]] = {
    "fr": {"title": "💾 Mémoire RAM", "used": "Utilisée", "available": "Disponible", "total": "Total", "rate": "Taux"},
    "en": {"title": "💾 RAM memory", "used": "Used", "available": "Available", "total": "Total", "rate": "Usage"},
    "es": {"title": "💾 Memoria RAM", "used": "Usada", "available": "Disponible", "total": "Total", "rate": "Uso"},
}

_DISK_LABELS: Dict[Lang, Dict[str, str]] = {
    "fr": {"title": "💿 Espace disque", "used": "Utilisé", "free": "Libre", "total": "Total", "rate": "Taux"},
    "en": {"title": "💿 Disk space", "used": "Used", "free": "Free", "total": "Total", "rate": "Usage"},
    "es": {"title": "💿 Espacio en disco", "used": "Usado", "free": "Libre", "total": "Total", "rate": "Uso"},
}

_UPTIME_LABELS: Dict[Lang, str] = {
    "fr": "🕐 Temps de fonctionnement",
    "en": "🕐 System uptime",
    "es": "🕐 Tiempo de funcionamiento",
}

_WEATHER_LABELS: Dict[Lang, str] = {
    "fr": "🌤️ Météo",
    "en": "🌤️ Weather",
    "es": "🌤️ Clima",
}

_SEARCH_LABELS: Dict[Lang, str] = {
    "fr": "🔍 Résultats pour",
    "en": "🔍 Results for",
    "es": "🔍 Resultados para",
}

_FILES_LABELS: Dict[Lang, str] = {
    "fr": "📁 Contenu de",
    "en": "📁 Contents of",
    "es": "📁 Contenido de",
}

_CLEAR_LABELS: Dict[Lang, str] = {
    "fr": "🗑️ Conversation effacée. Nouvelle session démarrée.",
    "en": "🗑️ Conversation cleared. New session started.",
    "es": "🗑️ Conversación borrada. Nueva sesión iniciada.",
}


def get_greeting(lang: Lang) -> str:
    """Je retourne un message d'accueil aléatoire dans la bonne langue."""
    return random.choice(_GREETINGS.get(lang, _GREETINGS["fr"]))


def get_unknown(lang: Lang) -> str:
    """Je retourne une réponse pour une commande non reconnue."""
    return random.choice(_UNKNOWN.get(lang, _UNKNOWN["fr"]))


def get_thanks(lang: Lang) -> str:
    """Je retourne une réponse à un remerciement."""
    return random.choice(_THANKS.get(lang, _THANKS["fr"]))


def get_help(lang: Lang) -> str:
    """Je retourne le message d'aide complet dans la langue demandée."""
    return _HELP.get(lang, _HELP["fr"])


def get_joke(lang: Lang) -> str:
    """Je retourne une blague aléatoire dans la bonne langue."""
    return random.choice(_JOKES.get(lang, _JOKES["fr"]))


def get_linux_fact(lang: Lang) -> str:
    """Je retourne un fait aléatoire sur Linux dans la bonne langue."""
    return random.choice(_LINUX_FACTS.get(lang, _LINUX_FACTS["fr"]))


def format_cpu(lang: Lang, percent: float) -> str:
    """Je formate l'affichage de l'utilisation CPU selon la langue."""
    labels = _CPU_LABELS.get(lang, _CPU_LABELS["fr"])
    bar = _make_progress_bar(percent)
    if percent < 40:
        comment = labels["low"]
    elif percent < 75:
        comment = labels["mid"]
    else:
        comment = labels["high"]
    return f"{labels['title']} : {percent:.1f}%\n{bar}\n💬 {comment}"


def format_ram(lang: Lang, ram: dict) -> str:
    """Je formate l'affichage de la RAM selon la langue."""
    l = _RAM_LABELS.get(lang, _RAM_LABELS["fr"])
    bar = _make_progress_bar(ram["percent"])
    return (
        f"{l['title']} :\n"
        f"  • {l['used']} : {ram['used']:.1f} Go\n"
        f"  • {l['available']} : {ram['available']:.1f} Go\n"
        f"  • {l['total']} : {ram['total']:.1f} Go\n"
        f"  • {l['rate']} : {ram['percent']:.1f}%\n"
        f"{bar}"
    )


def format_disk(lang: Lang, disk: dict) -> str:
    """Je formate l'affichage du disque selon la langue."""
    l = _DISK_LABELS.get(lang, _DISK_LABELS["fr"])
    bar = _make_progress_bar(disk["percent"])
    return (
        f"{l['title']} :\n"
        f"  • {l['used']} : {disk['used']:.1f} Go\n"
        f"  • {l['free']} : {disk['free']:.1f} Go\n"
        f"  • {l['total']} : {disk['total']:.1f} Go\n"
        f"  • {l['rate']} : {disk['percent']:.1f}%\n"
        f"{bar}"
    )


def format_uptime(lang: Lang, uptime: str) -> str:
    """Je formate l'affichage de l'uptime selon la langue."""
    label = _UPTIME_LABELS.get(lang, _UPTIME_LABELS["fr"])
    return f"{label} : {uptime}"


def format_system_summary(lang: Lang, uptime: str, cpu: float, ram: dict, disk: dict) -> str:
    """Je formate un résumé complet du système dans la langue choisie."""
    l = _SYSTEM_SUMMARY_LABELS.get(lang, _SYSTEM_SUMMARY_LABELS["fr"])
    cpu_bar = _make_progress_bar(cpu)
    ram_bar = _make_progress_bar(ram["percent"])
    disk_bar = _make_progress_bar(disk["percent"])
    return (
        f"{l['title']}\n"
        f"{'─' * 30}\n"
        f"{l['uptime']} : {uptime}\n\n"
        f"{l['cpu']} : {cpu:.1f}%\n{cpu_bar}\n\n"
        f"{l['ram_used']} : {ram['used']:.1f} Go / {ram['total']:.1f} Go ({ram['percent']:.0f}%)\n{ram_bar}\n\n"
        f"{l['disk_used']} : {disk['used']:.1f} Go — {l['disk_free']} : {disk['free']:.1f} Go ({disk['percent']:.0f}%)\n{disk_bar}"
    )


def format_weather_label(lang: Lang, city: str) -> str:
    """Je retourne le label de météo localisé."""
    label = _WEATHER_LABELS.get(lang, _WEATHER_LABELS["fr"])
    return f"{label}{f' — {city}' if city else ''} :"


def format_search_label(lang: Lang, query: str) -> str:
    """Je retourne le label de recherche localisé."""
    label = _SEARCH_LABELS.get(lang, _SEARCH_LABELS["fr"])
    return f"{label} « {query} » :"


def format_files_label(lang: Lang, path: str) -> str:
    """Je retourne le label de liste de fichiers localisé."""
    label = _FILES_LABELS.get(lang, _FILES_LABELS["fr"])
    return f"{label} {path or '~'} :"


def get_clear_message(lang: Lang) -> str:
    """Je retourne le message de confirmation d'effacement."""
    return _CLEAR_LABELS.get(lang, _CLEAR_LABELS["fr"])


def _make_progress_bar(percent: float, width: int = 20) -> str:
    """Je génère une barre de progression ASCII pour les statistiques."""
    filled = int(round(percent / 100 * width))
    empty = width - filled
    bar = "█" * filled + "░" * empty
    return f"  [{bar}] {percent:.0f}%"
