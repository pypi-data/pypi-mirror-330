import subprocess
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn
from rich.prompt import Confirm
from rich.style import Style
from rich.table import Table
from rich.theme import Theme


class LogLevel(str, Enum):
    """Niveaux de log disponibles"""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


class ThemeManager:
    """
    Gestionnaire de thème centralisé pour la cohérence visuelle entre packages.
    Fournit des styles et méthodes pour afficher des messages et promptes de manière uniforme.
    """

    # Thème par défaut avec les couleurs et styles pour l'application
    DEFAULT_THEME = {
        # Couleurs principales
        "primary": "blue",
        "secondary": "cyan",
        "accent": "magenta",
        # Statuts
        "info": "blue",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "debug": "magenta",
        # Éléments d'interface
        "heading": "bold blue",
        "subheading": "bold cyan",
        "prompt": "bold yellow",
        "highlight": "bold",
        "dim": "dim",
        # Différenciation des données
        "filename": "blue",
        "directory": "cyan",
        "value": "green",
        "key": "yellow",
    }

    def __init__(self, custom_theme: Optional[Dict[str, str]] = None):
        """
        Initialise le gestionnaire de thème avec un thème personnalisé optionnel.

        Args:
            custom_theme: Dictionnaire de styles personnalisés qui sera fusionné avec le thème par défaut
        """
        # Fusion du thème par défaut avec le thème personnalisé
        theme_styles = self.DEFAULT_THEME.copy()
        if custom_theme:
            theme_styles.update(custom_theme)

        # Création du thème Rich
        self.theme = Theme(theme_styles)

        # Console avec le thème appliqué
        self.console = Console(theme=self.theme)

        # Instance Typer pour les commandes CLI
        self.app = typer.Typer()

    def log(
        self, message: str, level: LogLevel = LogLevel.INFO, emoji: bool = True
    ) -> None:
        """
        Affiche un message avec le style correspondant au niveau de log.

        Args:
            message: Le message à afficher
            level: Le niveau de log (info, success, warning, error, debug)
            emoji: Inclure un emoji au début du message
        """
        # Émojis pour chaque niveau de log
        emojis = {
            LogLevel.INFO: "ℹ️ ",
            LogLevel.SUCCESS: "✅ ",
            LogLevel.WARNING: "⚠️ ",
            LogLevel.ERROR: "❌ ",
            LogLevel.DEBUG: "🔍 ",
        }

        prefix = emojis[level] if emoji else ""
        style = f"bold {level}"

        self.console.print(f"{prefix}[{style}]{message}[/{style}]")

    def info(self, message: str, emoji: bool = True) -> None:
        """Affiche un message d'information."""
        self.log(message, LogLevel.INFO, emoji)

    def success(self, message: str, emoji: bool = True) -> None:
        """Affiche un message de succès."""
        self.log(message, LogLevel.SUCCESS, emoji)

    def warning(self, message: str, emoji: bool = True) -> None:
        """Affiche un message d'avertissement."""
        self.log(message, LogLevel.WARNING, emoji)

    def error(self, message: str, emoji: bool = True) -> None:
        """Affiche un message d'erreur."""
        self.log(message, LogLevel.ERROR, emoji)

    def debug(self, message: str, emoji: bool = True) -> None:
        """Affiche un message de débogage."""
        self.log(message, LogLevel.DEBUG, emoji)

    def header(self, title: str, subtitle: Optional[str] = None) -> None:
        """
        Affiche un en-tête avec un titre et un sous-titre optionnel.

        Args:
            title: Titre principal
            subtitle: Sous-titre optionnel
        """
        self.console.print(f"[heading]{title}[/heading]")
        if subtitle:
            self.console.print(f"[subheading]{subtitle}[/subheading]")
        self.console.print()

    def panel(
        self, content: str, title: Optional[str] = None, style: str = "primary"
    ) -> None:
        """
        Affiche un panneau stylisé avec un contenu et un titre optionnel.

        Args:
            content: Contenu du panneau
            title: Titre optionnel
            style: Style du panneau (primary, info, success, warning, error)
        """
        panel = Panel(content, title=title, border_style=style)
        self.console.print(panel)

    def confirm(self, prompt: str, default: bool = False) -> bool:
        """
        Demande une confirmation à l'utilisateur avec un style cohérent.

        Args:
            prompt: Question à poser
            default: Valeur par défaut

        Returns:
            bool: Réponse de l'utilisateur
        """
        return Confirm.ask(
            f"[prompt]{prompt}[/prompt]", console=self.console, default=default
        )

    def table(self, title: Optional[str] = None, headers: List[str] = None) -> Table:
        """
        Crée une table Rich avec le style du thème.

        Args:
            title: Titre optionnel de la table
            headers: En-têtes de colonne optionnels

        Returns:
            Table: Une table Rich configurée avec le thème
        """
        table = Table(title=title, header_style="heading", border_style="primary")
        if headers:
            for header in headers:
                table.add_column(header)
        return table

    def display_changes(
        self, changes: List[Tuple[str, str]], title: str = "Changements"
    ) -> None:
        """
        Affiche une liste de changements (avant/après) dans un format tabulaire.

        Args:
            changes: Liste de tuples (valeur_avant, valeur_après)
            title: Titre du tableau
        """
        if not changes:
            self.info("Aucun changement à afficher")
            return

        table = self.table(title=title, headers=["Avant", "Après"])
        for old, new in changes:
            table.add_row(f"[filename]{old}[/filename]", f"[value]{new}[/value]")

        self.console.print(table)

    def manage_progress(
        self,
        progress: Optional[Progress],
        task_id: Optional[TaskID],
        description: str,
        total: int,
    ) -> tuple[Progress, TaskID]:
        """Gère la barre de progression."""
        if progress is None:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console,
            )
            task_id = progress.add_task(description, total=total)
            progress.start()
        elif task_id is None:
            task_id = progress.add_task(description, total=total)

        return progress, task_id

    def update_progress(
        self,
        progress: Progress,
        task_id: TaskID,
        completed: int,
        description: Optional[str] = None,
    ) -> None:
        """Met à jour la barre de progression."""
        if description:
            progress.update(task_id, completed=completed, description=description)
        else:
            progress.update(task_id, completed=completed)

    def stop_progress(self, progress: Progress) -> None:
        """Arrête la barre de progression."""
        if progress and progress.live.is_started:
            progress.stop()

    def run_process_with_progress(
        self,
        cmd: List[str],
        progress: Progress,
        task_id: TaskID,
        total_progress: int,
        update_callback,
    ) -> int:
        """Exécute un processus et met à jour la barre de progression."""
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        completed = 0
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            completed = update_callback(line, completed)
            self.update_progress(
                progress, task_id, completed=completed * total_progress
            )

        return process.wait()
