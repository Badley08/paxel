"""
Je construis ici l'interface en ligne de commande de Paxel avec Textual.
Je vise une interface propre et moderne directement dans le terminal.
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog, Static
from textual.containers import Container, Vertical
from textual.binding import Binding
from textual import events

from paxel.backend import process_message
from paxel.core.memory import add_message, get_history
from paxel.config import APP_NAME, APP_VERSION


class ChatMessage(Static):
    """Je représente un seul message dans l'historique du chat."""

    DEFAULT_CSS = """
    ChatMessage {
        width: 100%;
        margin-bottom: 1;
    }

    ChatMessage.user-message {
        align: right middle;
        background: $primary-darken-2;
        border-right: thick $primary;
        padding: 0 1;
        color: $text;
    }

    ChatMessage.bot-message {
        align: left middle;
        background: $surface;
        border-left: thick $accent;
        padding: 0 1;
        color: $text-muted;
    }
    """


class PaxelTUI(App):
    """Je suis l'application TUI principale de Paxel basée sur Textual."""

    TITLE = f"{APP_NAME} v{APP_VERSION}"
    CSS = """
    /* Je définis ici le style global de l'interface CLI */

    Screen {
        background: #1a1a1a;
    }

    #chat-log {
        height: 1fr;
        border: solid #333333;
        background: #1e1e1e;
        padding: 1 2;
        scrollbar-color: #444444;
    }

    #input-area {
        height: auto;
        padding: 1 2;
        background: #252525;
        border-top: solid #333333;
    }

    #message-input {
        width: 1fr;
        background: #2d2d2d;
        border: solid #444444;
        color: #e8e8e8;
    }

    #message-input:focus {
        border: solid #1e6fd9;
    }

    #welcome-panel {
        height: auto;
        padding: 1 2;
        background: #252525;
        border-bottom: solid #333333;
        color: #888888;
    }

    Header {
        background: #1a1a1a;
        color: #e8e8e8;
    }

    Footer {
        background: #1a1a1a;
        color: #666666;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quitter"),
        Binding("ctrl+l", "clear_chat", "Effacer"),
        Binding("escape", "quit", "Quitter", show=False),
    ]

    def compose(self) -> ComposeResult:
        """Je compose l'interface TUI de Paxel."""
        yield Header()

        yield Static(
            "👋 Paxel — Assistant Linux | Tape un message et appuie sur Entrée | Ctrl+L pour effacer | Ctrl+C pour quitter",
            id="welcome-panel",
        )

        yield RichLog(
            id="chat-log",
            markup=True,
            wrap=True,
            highlight=True,
            auto_scroll=True,
        )

        with Container(id="input-area"):
            yield Input(
                placeholder="Écris un message à Paxel... (ex: aide, cpu, météo Paris)",
                id="message-input",
            )

        yield Footer()

    def on_mount(self) -> None:
        """Je charge l'historique et prépare l'interface au démarrage."""
        log = self.query_one("#chat-log", RichLog)
        input_widget = self.query_one("#message-input", Input)

        # Je charge l'historique récent
        history = get_history(limit=10)
        if history:
            log.write("[dim]── Historique récent ──[/dim]")
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    log.write(f"[bold blue]Toi :[/bold blue] {content}")
                else:
                    log.write(f"[bold green]Paxel :[/bold green] {content}")
            log.write("[dim]── Conversation actuelle ──[/dim]")
        else:
            log.write("[bold green]Paxel :[/bold green] 👋 Bonjour ! Je suis Paxel, ton assistant Linux.")
            log.write("[bold green]Paxel :[/bold green] Tape [italic]aide[/italic] pour voir ce que je sais faire.")

        # Je focus le champ de saisie automatiquement
        input_widget.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Je traite l'envoi d'un message."""
        message = event.value.strip()
        if not message:
            return

        log = self.query_one("#chat-log", RichLog)
        input_widget = self.query_one("#message-input", Input)

        # J'affiche le message de l'utilisateur
        log.write(f"[bold blue]Toi :[/bold blue] {message}")
        add_message("user", message)

        # Je vide le champ de saisie
        input_widget.clear()

        # Je traite le message et j'affiche la réponse
        log.write("[dim]Paxel réfléchit...[/dim]")

        def respond():
            response = process_message(message)
            self.call_from_thread(self._display_response, response)

        import threading
        thread = threading.Thread(target=respond, daemon=True)
        thread.start()

    def _display_response(self, response: str) -> None:
        """J'affiche la réponse de Paxel dans le log."""
        log = self.query_one("#chat-log", RichLog)

        # Je supprime l'indicateur "Paxel réfléchit..." du dernier log
        # (Textual RichLog ne supporte pas la suppression, je l'écrase avec la réponse)
        log.write(f"[bold green]Paxel :[/bold green] {response}")
        add_message("paxel", response)

    def action_clear_chat(self) -> None:
        """J'efface le chat et l'historique."""
        from paxel.core.memory import clear_history
        clear_history()

        log = self.query_one("#chat-log", RichLog)
        log.clear()
        log.write("[dim]Conversation effacée.[/dim]")
        log.write("[bold green]Paxel :[/bold green] 👋 Nouvelle conversation. Comment puis-je t'aider ?")

    def action_quit(self) -> None:
        """Je quitte l'application proprement."""
        self.exit()


def run_tui():
    """Je lance l'interface TUI de Paxel."""
    app = PaxelTUI()
    app.run()
