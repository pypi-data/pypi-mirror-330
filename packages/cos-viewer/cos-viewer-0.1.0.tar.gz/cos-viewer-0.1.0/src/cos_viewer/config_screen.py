from textual import on
from textual.app import Screen, ComposeResult
from textual.containers import Container
from textual.widgets import Header, DataTable, Button
from src.config_manager import ConfigManager
from .config_form_screen import ConfigFormScreen
from .file_browser_screen import FileBrowserScreen
from .message_screen import MessageScreen

class ConfigScreen(Screen):
    def __init__(self):
        super().__init__()
        self.row_keys = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="config-container"):
            self.table = DataTable(id="config-table")
            self.table.add_columns("配置名称", "Bucket", "Prefix", "Region")
            yield self.table
            with Container(id="config-buttons"):
                yield Button("新建", id="new")
                yield Button("编辑", id="edit")
                yield Button("删除", id="delete")
                yield Button("选择", id="select")
                yield Button("复制", id="copy")

    @on(Button.Pressed, "#copy")
    def copy_config(self):
        selected = self.table.cursor_row
        if selected is None or selected >= len(self.row_keys):
            return
        config_name = self.row_keys[selected]
        self.app.push_screen(ConfigFormScreen(config_name, is_copy=True))

    def on_mount(self):
        self.refresh_configs()

    def refresh_configs(self):
        self.table.clear()
        self.row_keys = []
        for config in ConfigManager().list_configs():
            config_data = ConfigManager().get_config(config)
            self.row_keys.append(config)
            self.table.add_row(
                config,
                config_data['cos_bucket'],
                config_data['prefix'],
                config_data['cos_region'],
                key=config
            )

    @on(Button.Pressed, "#new")
    def new_config(self):
        self.app.push_screen(ConfigFormScreen())

    @on(Button.Pressed, "#edit")
    def edit_config(self):
        selected = self.table.cursor_row
        if selected is None or selected >= len(self.row_keys):
            return
        config_name = self.row_keys[selected]
        self.app.push_screen(ConfigFormScreen(config_name))

    @on(Button.Pressed, "#delete")
    def delete_config(self):
        selected = self.table.cursor_row
        if selected is None or selected >= len(self.row_keys):
            return
        config_name = self.row_keys[selected]
        try:
            ConfigManager().delete_config(config_name)
            self.refresh_configs()
        except Exception as e:
            self.app.push_screen(MessageScreen(str(e)))
            raise

    @on(Button.Pressed, "#select")
    def select_config(self):
        selected = self.table.cursor_row
        if selected is None or selected >= len(self.row_keys):
            return
        config_name = self.row_keys[selected]
        self.app.push_screen(FileBrowserScreen(config_name))
