from textual import on, work
from textual.app import Screen, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, DataTable, Static, Label, Button, Input, ProgressBar
from src.config_manager import ConfigManager
from .message_screen import MessageScreen

class ConfigFormScreen(Screen):
    def __init__(self, config_name=None, is_copy=False):
        super().__init__()
        self.is_edit = config_name is not None and not is_copy
        self.is_copy = is_copy
        self.config_name = config_name
        self.config_manager = ConfigManager()

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="form-container"):
            yield Label("配置管理" + (" (编辑)" if self.is_edit else " (复制)" if self.is_copy else " (新建)"))
            yield Input(placeholder="配置名称", id="name", value=self.config_name or "")
            yield Input(placeholder="SecretId", id="secret_id")
            yield Input(placeholder="SecretKey", id="secret_key", password=True)
            yield Input(placeholder="Region", id="region")
            yield Input(placeholder="Bucket", id="bucket")
            yield Input(placeholder="前缀", id="prefix")
            with Container(id="button-container"):
                yield Button("保存", id="save")
                yield Button("取消", id="cancel")

    def on_mount(self):
        if self.is_edit or self.is_copy:
            config = self.config_manager.get_config(self.config_name)
            if config:
                self.query_one("#secret_id", Input).value = config["cos_secret_id"]
                self.query_one("#secret_key", Input).value = config["cos_secret_key"]
                self.query_one("#region", Input).value = config["cos_region"]
                self.query_one("#bucket", Input).value = config["cos_bucket"]
                self.query_one("#prefix", Input).value = config["prefix"]

    @on(Button.Pressed, "#save")
    def save_config(self):
        name = self.query_one("#name", Input).value
        fields = {
            "secret_id": self.query_one("#secret_id", Input).value,
            "secret_key": self.query_one("#secret_key", Input).value,
            "region": self.query_one("#region", Input).value,
            "bucket": self.query_one("#bucket", Input).value,
            "prefix": self.query_one("#prefix", Input).value,
        }
        
        if not all(fields.values()):
            self.app.push_screen(MessageScreen("所有字段都必须填写"))
            return

        try:
            if self.is_edit:
                self.config_manager.update_config(
                    self.config_name,
                    cos_secret_id=fields["secret_id"],
                    cos_secret_key=fields["secret_key"],
                    cos_region=fields["region"],
                    cos_bucket=fields["bucket"],
                    prefix=fields["prefix"]
                )
            elif self.is_copy:
                self.config_manager.create_config(
                    name,
                    fields["secret_id"],
                    fields["secret_key"],
                    fields["region"],
                    fields["bucket"],
                    fields["prefix"]
                )
            else:
                self.config_manager.create_config(
                    name,
                    fields["secret_id"],
                    fields["secret_key"],
                    fields["region"],
                    fields["bucket"],
                    fields["prefix"]
                )
            self.app.pop_screen()
            self.app.query_one("ConfigScreen").refresh_configs()
        except Exception as e:
            self.app.push_screen(MessageScreen(str(e)))
            raise

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        self.app.pop_screen()
