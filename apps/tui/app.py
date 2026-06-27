from textual.app import App
from textual.binding import Binding

from apps.tui.screens.history import HistoryScreen
from apps.tui.screens.home import HomeScreen
from apps.tui.screens.log import LogScreen
from apps.tui.screens.projects import ProjectScreen
from apps.tui.screens.search import SearchScreen


class LogyTUI(App):
    SCREENS = {
        "home": HomeScreen,
        "log": LogScreen,
        "history": HistoryScreen,
        "projects": ProjectScreen,
        "search": SearchScreen,
    }

    BINDINGS = [
        Binding("h", "switch_screen('home')", "Home", show=True),
        Binding("l", "switch_screen('log')", "Log", show=True),
        Binding("r", "switch_screen('history')", "Recent", show=True),
        Binding("p", "switch_screen('projects')", "Projects", show=True),
        Binding("s", "switch_screen('search')", "Search", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def on_mount(self) -> None:
        self.push_screen("home")


def main() -> None:
    app = LogyTUI()
    app.run()


if __name__ == "__main__":
    main()
