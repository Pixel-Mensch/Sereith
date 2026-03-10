from ai_pnp.ui.desktop.main_window import MainWindow


class DesktopApp:
    def __init__(self, engine) -> None:
        self.engine = engine

    def launch(self) -> None:
        window = MainWindow(self.engine)
        window.launch()
