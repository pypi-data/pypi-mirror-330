from textual import on, work
from textual.app import Screen, ComposeResult
from textual.widgets import Header, Label, ProgressBar, Button
from textual.containers import Center, VerticalScroll
from src.cos_client import COSClient
from .message_screen import MessageScreen


class DownloadScreen(Screen):
    def __init__(self, filename, on_cancel, prefix, config_name):
        super().__init__()
        self.filename = filename
        self.on_cancel = on_cancel
        self.prefix = prefix
        self.cos_client = COSClient(config_name)

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Label(f"正在下载：{self.filename}")
            yield ProgressBar(id="download-progress", total=100, show_eta=False)
        with Center():
            yield Button("取消", id="cancel-download")
            yield Button("开始下载", id="start")

    def update_progress(self, total, value):
        progress = (value / total) * 100
        self.query_one("#download-progress", ProgressBar).update(progress=progress)

    @on(Button.Pressed, "#cancel-download")
    def cancel(self):
        self.app.pop_screen()

    @work(thread=True)
    def start_download(self):
        """后台下载任务"""
        try:
            self.cos_client.download_object(
                key=self.filename,
                download_path=".",
                progress_callback=self.update_progress
            )
            self.app.call_from_thread(self.app.push_screen,
                                      MessageScreen(f"下载完成: {self.filename}"))
        except Exception as e:
            self.app.call_from_thread(self.app.push_screen,
                                      MessageScreen(f"下载失败: {str(e)}"))
            raise

    @on(Button.Pressed, "#start")
    def start(self):
        self.start_download()
