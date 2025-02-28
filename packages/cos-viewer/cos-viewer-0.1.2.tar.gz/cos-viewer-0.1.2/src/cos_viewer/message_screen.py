from textual.app import Screen, ComposeResult, on
from textual.containers import Center
from textual.widgets import Header, Label, Button


class MessageScreen(Screen):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Label(self.message, markup=False)
        with Center():
            yield Button("确定", id="ok")

    @on(Button.Pressed, "#ok")
    def close_screen(self):
        self.app.pop_screen()
