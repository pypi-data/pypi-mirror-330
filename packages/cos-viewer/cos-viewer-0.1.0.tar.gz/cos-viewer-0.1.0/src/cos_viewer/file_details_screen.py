from textual import on
from textual.app import Screen, ComposeResult
from textual.containers import Container
from textual.widgets import Header, DataTable, Button


class FileDetailsScreen(Screen):
    def __init__(self, file_info, config_name):
        super().__init__()
        self.file_info = file_info
        self.config_name = config_name

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="file-details-container"):
            self.table = DataTable(id="file-details-table")
            self.table.add_columns("属性", "值")
            self.table.add_row("对象名称", self.file_info['Key'])
            self.table.add_row("对象大小", self.file_info['Size'])
            self.table.add_row("修改时间", self.file_info['LastModified'])
            self.table.add_row("ETag", self.file_info['ETag'].strip('"'))
            self.table.add_row("对象地址", self.file_info.get('Location', 'N/A'))
            tags = ', '.join([f"{k}: {v}" for k, v in self.file_info.get('Tags', {}).items()])
            self.table.add_row("对象标签", tags)
            yield self.table
            yield Button("返回", id="back")

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()
