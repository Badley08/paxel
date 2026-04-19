# Paxel — Assistant Linux en Python

> Assistant IA local pour Linux, simple, léger et rapide.

Auteur : [Badley08](https://github.com/Badley08)

---

## Présentation

Paxel est un assistant Linux open source écrit en Python. Il tourne entièrement en local, sans base de données complexe ni dépendance cloud. Il propose deux interfaces :

- **GUI** — Interface graphique sombre avec GTK4 + libadwaita, inspirée de Google Gemini
- **CLI** — Interface terminal moderne avec Textual

---

## Langues supportées

Paxel détecte automatiquement la langue de chaque message et répond dans la même langue.

| Langue | Exemple de commande |
|--------|-------------------|
| 🇫🇷 Français | `aide`, `cpu`, `météo Paris`, `blague` |
| 🇬🇧 English | `help`, `cpu`, `weather London`, `joke` |
| 🇪🇸 Español | `ayuda`, `cpu`, `clima Madrid`, `chiste` |

## Fonctionnalités

| Commande (FR / EN / ES) | Description |
|--------------------------|-------------|
| `cpu` | Utilisation du processeur |
| `ram` / `memory` / `memoria` | Statistiques RAM avec barre de progression |
| `disque` / `disk` / `disco` | Espace disque avec barre de progression |
| `système` / `system` / `sistema` | Résumé complet du système |
| `uptime` | Temps de fonctionnement |
| `météo [ville]` / `weather [city]` / `clima [ciudad]` | Météo via wttr.in |
| `cherche [requête]` / `search [query]` / `busca [consulta]` | Recherche DuckDuckGo |
| `liste [dossier]` / `list [folder]` / `lista [carpeta]` | Lister les fichiers |
| `blague` / `joke` / `chiste` | Blague aléatoire |
| `info linux` / `linux fact` / `dato linux` | Fait sur Linux |
| `effacer` / `clear` / `borrar` | Effacer la conversation |
| `aide` / `help` / `ayuda` | Afficher l'aide |

## Architecture Backend

```
Backend Mock ──► Détection de langue (FR/EN/ES)
                      │
                      ▼
              Routage par commande
                      │
           ┌──────────┼──────────┐
           ▼          ▼          ▼
        Système    Fichiers   Météo/Web
     (system.py) (files.py) (weather, web)
           │
           ▼
    Réponse localisée (mock_backend.py)
```

---

## Installation

### Prérequis système

**Arch Linux :**
```bash
sudo pacman -S python python-pip python-gobject gtk4 libadwaita
```

**Ubuntu / Linux Mint :**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 libadwaita-1-0 gir1.2-adw-1
```

### Installation automatique

```bash
git clone https://github.com/Badley08/paxel.git
cd paxel
chmod +x install.sh
./install.sh
```

### Installation manuelle

```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Utilisation

```bash
# Activer l'environnement
source .venv/bin/activate

# Interface graphique GTK4 (par défaut)
python -m paxel.main

# Interface terminal (Textual)
python -m paxel.main --cli
```

---

## Structure du projet

```
paxel/
├── paxel/
│   ├── main.py          # Point d'entrée principal
│   ├── backend.py       # Moteur de traitement des messages
│   ├── config.py        # Configuration globale
│   ├── core/
│   │   ├── system.py    # Informations système (CPU, RAM, disque)
│   │   ├── files.py     # Gestion sécurisée des fichiers
│   │   ├── memory.py    # Mémoire persistante JSON
│   │   ├── weather.py   # Météo via wttr.in
│   │   └── web.py       # Recherche DuckDuckGo
│   ├── ui/
│   │   ├── gui.py       # Interface GTK4 + libadwaita
│   │   └── tui.py       # Interface Textual (CLI)
│   └── integrations/
│       ├── gnome/       # Intégration GNOME (future)
│       └── openbox/     # Intégration Openbox (future)
├── requirements.txt
├── setup.py
├── install.sh
└── README.md
```

---

## Données locales

Paxel stocke l'historique de conversation dans :
```
~/.local/share/paxel/memory.json
```

Aucune donnée n'est envoyée sur internet (sauf pour la météo et la recherche web, à ta demande).

---

## Sécurité

- Aucune commande root automatique
- Accès limité aux dossiers utilisateur autorisés
- Aucune action destructive sans confirmation

---

## Licence

MIT — libre de modifier et redistribuer.
