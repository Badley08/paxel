#!/usr/bin/env bash
# Je détecte automatiquement la distribution Linux et j'installe les dépendances.
# Auteur : Badley08

set -e

# Je détecte la distribution
detect_distro() {
    if [ -f /etc/arch-release ]; then
        echo "arch"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/fedora-release ]; then
        echo "fedora"
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)
echo "🐧 Distribution détectée : $DISTRO"

# J'installe les dépendances système
install_system_deps() {
    case "$DISTRO" in
        arch)
            echo "📦 Installation des dépendances Arch Linux..."
            sudo pacman -S --needed python python-pip python-gobject gtk4 libadwaita
            ;;
        debian)
            echo "📦 Installation des dépendances Ubuntu/Debian/Mint..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-gi python3-gi-cairo \
                gir1.2-gtk-4.0 libadwaita-1-0 gir1.2-adw-1
            ;;
        fedora)
            echo "📦 Installation des dépendances Fedora..."
            sudo dnf install -y python3 python3-pip python3-gobject gtk4 libadwaita
            ;;
        *)
            echo "⚠️  Distribution non reconnue. J'installe les dépendances manuellement."
            echo "   GTK4 et libadwaita doivent être installés via ton gestionnaire de paquets."
            ;;
    esac
}

# Je crée et active l'environnement virtuel
setup_venv() {
    echo "🐍 Création de l'environnement virtuel Python..."
    python3 -m venv .venv --system-site-packages
    source .venv/bin/activate
    echo "📦 Installation des dépendances Python..."
    pip install -r requirements.txt
    echo "✅ Environnement virtuel prêt."
}

install_system_deps
setup_venv

echo ""
echo "✅ Paxel est prêt !"
echo ""
echo "Pour lancer Paxel :"
echo "  source .venv/bin/activate"
echo "  python -m paxel.main          # Interface GTK4"
echo "  python -m paxel.main --cli    # Interface terminal"
