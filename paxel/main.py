"""
Je suis le point d'entrée principal de Paxel.
Je gère le choix entre l'interface GUI (GTK4) et l'interface CLI (Textual).
"""

import argparse
import sys

from paxel.config import APP_NAME, APP_VERSION


def parse_args() -> argparse.Namespace:
    """Je parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        prog="paxel",
        description=f"{APP_NAME} v{APP_VERSION} — Ton assistant Linux en Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python -m paxel.main          # Lance l'interface graphique (GTK4)\n"
            "  python -m paxel.main --cli    # Lance l'interface terminal (Textual)\n"
        ),
    )

    parser.add_argument(
        "--cli",
        action="store_true",
        default=False,
        help="Lance Paxel en mode terminal (Textual TUI)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
    )

    return parser.parse_args()


def main():
    """Je suis le point d'entrée principal. Je lance le bon mode selon les arguments."""
    args = parse_args()

    if args.cli:
        # Je lance le mode terminal
        try:
            from paxel.ui.tui import run_tui
            run_tui()
        except ImportError as e:
            print(f"❌ Erreur : Textual n'est pas installé.")
            print(f"   Installe-le avec : pip install textual")
            print(f"   Détail : {e}")
            sys.exit(1)
    else:
        # Je lance le mode graphique GTK4
        try:
            from paxel.ui.gui import run_gui
            run_gui()
        except Exception as e:
            print(f"❌ Impossible de lancer l'interface graphique : {e}")
            print(f"   Essaie le mode CLI avec : python -m paxel.main --cli")
            sys.exit(1)


if __name__ == "__main__":
    main()
