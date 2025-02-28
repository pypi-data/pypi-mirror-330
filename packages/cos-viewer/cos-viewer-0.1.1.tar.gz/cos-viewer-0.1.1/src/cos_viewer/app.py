from textual.app import App
from .screens import ConfigScreen


class COSViewerApp(App):
    CSS_PATH = "css/style.css"

    def on_mount(self) -> None:
        self.push_screen(ConfigScreen())
