"""
Je construis ici l'interface graphique GTK4 de Paxel.
Je m'inspire de Google Gemini avec un thème sombre et une interface minimaliste.
"""

import sys
import threading
from typing import Optional

try:
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1")
    from gi.repository import Gtk, Adw, GLib, Gio, Pango
    _GTK_AVAILABLE = True
except (ImportError, ValueError) as e:
    _GTK_AVAILABLE = False
    _GTK_ERROR = str(e)

from paxel.backend import process_message
from paxel.core.memory import add_message, get_history


CSS_STYLE = """
/* Je définis ici le style CSS global de l'application */

.message-bubble-user {
    background-color: #1e6fd9;
    border-radius: 18px 18px 4px 18px;
    padding: 10px 16px;
    margin: 4px 0;
    color: white;
}

.message-bubble-bot {
    background-color: #2a2a2a;
    border-radius: 18px 18px 18px 4px;
    padding: 10px 16px;
    margin: 4px 0;
    color: #e8e8e8;
}

.chat-input {
    border-radius: 24px;
    padding: 8px 16px;
    background-color: #2a2a2a;
    color: #e8e8e8;
    border: 1px solid #404040;
    font-size: 14px;
}

.send-button {
    border-radius: 50%;
    background-color: #1e6fd9;
    min-width: 40px;
    min-height: 40px;
}

.header-title {
    font-size: 18px;
    font-weight: bold;
    color: #e8e8e8;
}

.welcome-label {
    font-size: 28px;
    font-weight: bold;
    color: #e8e8e8;
    margin-bottom: 8px;
}

.welcome-subtitle {
    font-size: 14px;
    color: #888888;
}
"""


def run_gui():
    """Je lance l'interface graphique GTK4."""
    if not _GTK_AVAILABLE:
        print(f"❌ GTK4 n'est pas disponible : {_GTK_ERROR}")
        print("   Installe GTK4 avec :")
        print("   Arch : sudo pacman -S python-gobject gtk4 libadwaita")
        print("   Ubuntu/Mint : sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1")
        sys.exit(1)

    app = PaxelApp()
    app.run(sys.argv)


class PaxelApp(Adw.Application):
    """Je suis l'application principale GTK4 de Paxel."""

    def __init__(self):
        super().__init__(
            application_id="com.badley08.paxel",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.connect("activate", self._on_activate)

    def _on_activate(self, app):
        """Je crée et affiche la fenêtre principale au démarrage."""
        window = PaxelWindow(application=app)
        window.present()


class PaxelWindow(Adw.ApplicationWindow):
    """Je suis la fenêtre principale de l'assistant Paxel."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title("Paxel")
        self.set_default_size(720, 600)
        self.set_size_request(400, 400)

        # J'active le style libadwaita sombre
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

        # J'applique mon CSS personnalisé
        self._apply_css()

        # Je construis l'interface
        self._build_ui()

        # Je charge l'historique existant
        self._load_history()

    def _apply_css(self):
        """J'applique le style CSS à l'application."""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE.encode())
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _build_ui(self):
        """Je construis l'interface utilisateur complète."""
        # Je crée la structure principale
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # Je crée la barre de navigation
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="Paxel", css_classes=["header-title"]))

        # Je crée le bouton pour vider l'historique
        clear_button = Gtk.Button(icon_name="edit-clear-symbolic")
        clear_button.set_tooltip_text("Effacer la conversation")
        clear_button.connect("clicked", self._on_clear_history)
        header.pack_end(clear_button)

        main_box.append(header)

        # Je crée la zone de chat avec défilement
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.append(scrolled)

        # Je crée la liste des messages
        self.messages_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )
        scrolled.set_child(self.messages_box)

        # Je garde la référence au scrolled pour défiler vers le bas
        self.scrolled = scrolled

        # Je crée l'écran d'accueil (affiché quand la conversation est vide)
        self.welcome_box = self._build_welcome_screen()
        self.messages_box.append(self.welcome_box)

        # Je crée la barre de saisie
        input_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            margin_top=8,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )
        main_box.append(input_box)

        # Je crée le champ de saisie
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.set_placeholder_text("Écris un message à Paxel...")
        self.entry.add_css_class("chat-input")
        self.entry.connect("activate", self._on_send)
        input_box.append(self.entry)

        # Je crée le bouton d'envoi
        send_btn = Gtk.Button(icon_name="go-up-symbolic")
        send_btn.add_css_class("send-button")
        send_btn.set_tooltip_text("Envoyer")
        send_btn.connect("clicked", self._on_send)
        input_box.append(send_btn)

        self._has_messages = False

    def _build_welcome_screen(self) -> Gtk.Box:
        """Je crée l'écran d'accueil affiché avant le premier message."""
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            margin_top=80,
            margin_bottom=80,
        )

        # Icône
        icon = Gtk.Image.new_from_icon_name("computer-symbolic")
        icon.set_pixel_size(64)
        icon.set_opacity(0.6)
        box.append(icon)

        # Titre
        title = Gtk.Label(label="Bonjour, je suis Paxel 👋")
        title.add_css_class("welcome-label")
        title.set_margin_top(16)
        box.append(title)

        # Sous-titre
        subtitle = Gtk.Label(label="Ton assistant Linux. Tape 'aide' pour voir mes commandes.")
        subtitle.add_css_class("welcome-subtitle")
        subtitle.set_wrap(True)
        subtitle.set_justify(Gtk.Justification.CENTER)
        box.append(subtitle)

        return box

    def _load_history(self):
        """Je charge et affiche l'historique de conversation existant."""
        history = get_history(limit=20)
        if history:
            self.welcome_box.set_visible(False)
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                self._add_message_bubble(content, is_user=(role == "user"))
            self._has_messages = True

    def _on_send(self, *args):
        """Je traite l'envoi d'un message par l'utilisateur."""
        text = self.entry.get_text().strip()
        if not text:
            return

        # Je vide le champ de saisie immédiatement
        self.entry.set_text("")

        # Je cache l'écran d'accueil au premier message
        if not self._has_messages:
            self.welcome_box.set_visible(False)
            self._has_messages = True

        # J'affiche le message de l'utilisateur
        self._add_message_bubble(text, is_user=True)
        add_message("user", text)

        # Je montre un indicateur de réponse en cours
        typing_indicator = self._add_typing_indicator()

        # Je génère la réponse dans un thread séparé pour ne pas bloquer l'UI
        def generate_response():
            response = process_message(text)
            GLib.idle_add(self._on_response_ready, response, typing_indicator)

        thread = threading.Thread(target=generate_response, daemon=True)
        thread.start()

    def _on_response_ready(self, response: str, typing_indicator):
        """Je reçois et affiche la réponse de Paxel (appelé depuis le thread principal)."""
        # Je supprime l'indicateur de chargement
        self.messages_box.remove(typing_indicator)

        # J'affiche la réponse
        self._add_message_bubble(response, is_user=False)
        add_message("paxel", response)

        # Je fais défiler vers le bas
        self._scroll_to_bottom()
        return False

    def _add_message_bubble(self, text: str, is_user: bool) -> Gtk.Widget:
        """J'ajoute une bulle de message dans le chat."""
        outer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        label = Gtk.Label(label=text)
        label.set_wrap(True)
        label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_xalign(0.0)
        label.set_max_width_chars(60)
        label.set_selectable(True)

        if is_user:
            outer_box.set_halign(Gtk.Align.END)
            label.add_css_class("message-bubble-user")
        else:
            outer_box.set_halign(Gtk.Align.START)
            label.add_css_class("message-bubble-bot")

        outer_box.append(label)
        self.messages_box.append(outer_box)
        self._scroll_to_bottom()
        return outer_box

    def _add_typing_indicator(self) -> Gtk.Widget:
        """J'affiche l'indicateur de chargement pendant que Paxel réfléchit."""
        outer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        outer_box.set_halign(Gtk.Align.START)

        spinner = Gtk.Spinner()
        spinner.start()
        spinner.add_css_class("message-bubble-bot")
        spinner.set_margin_start(8)
        spinner.set_margin_top(4)

        outer_box.append(spinner)
        self.messages_box.append(outer_box)
        self._scroll_to_bottom()
        return outer_box

    def _scroll_to_bottom(self):
        """Je fais défiler la zone de chat vers le dernier message."""
        def do_scroll():
            vadj = self.scrolled.get_vadjustment()
            vadj.set_value(vadj.get_upper() - vadj.get_page_size())
            return False
        GLib.idle_add(do_scroll)

    def _on_clear_history(self, *args):
        """J'efface la conversation et reviens à l'écran d'accueil."""
        from paxel.core.memory import clear_history
        clear_history()

        # Je supprime toutes les bulles de message (sauf l'écran d'accueil)
        child = self.messages_box.get_first_child()
        while child is not None:
            next_child = child.get_next_sibling()
            if child != self.welcome_box:
                self.messages_box.remove(child)
            child = next_child

        self.welcome_box.set_visible(True)
        self._has_messages = False
