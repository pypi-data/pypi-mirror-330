from textual import on, work
from textual.app import Screen, ComposeResult
from textual.containers import Container
from textual.widgets import Header, DataTable, Button
from src.cos_client import COSClient
from .message_screen import MessageScreen
from .download_screen import DownloadScreen
from .file_details_screen import FileDetailsScreen

class FileBrowserScreen(Screen):
    def __init__(self, config_name):
        super().__init__()
        self.config_name = config_name
        self.cos_client = COSClient(config_name)
        
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="file-container"):
            self.table = DataTable(id="file-table")
            self.table.add_columns("文件名", "大小", "修改时间", "ETag")
            yield self.table
            with Container(id="download-button-container"):
                yield Button("刷新", id="refresh")
                yield Button("详情", id="details")
                yield Button("下载", id="download")
                yield Button("删除", id="delete")
                yield Button("返回", id="back")

    async def on_mount(self):
        await self.load_files()

    async def load_files(self):
        self.table.clear()
        try:
            files = self.cos_client.list_objects()
            for file in files:
                if int(file['Size']) == 0:  # 过滤掉目录（大小为0的对象）
                    continue
                # 处理文件单位
                size = int(file['Size'])
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                elif size < 1024 * 1024 * 1024:
                    size_str = f"{size/1024/1024:.1f} MB"
                else:
                    size_str = f"{size/1024/1024/1024:.1f} GB"
                self.table.add_row(
                    file["Key"],
                    size_str, 
                    file["LastModified"],
                    file['ETag'].strip('"')
                )
        except Exception as e:
            # self.app.query_one('#download-button-container').tooltip = str(e)
            self.app.push_screen(MessageScreen(str(e)))

    @on(Button.Pressed, "#refresh")
    async def refresh_files(self):
        await self.load_files()

    @on(Button.Pressed, "#delete")
    async def delete_file(self):
        selected = self.table.cursor_row
        if selected is None:
            return
            
        filename = self.table.get_row_at(selected)[0]
        key = f"{filename}"
        
        try:
            self.cos_client.delete_object(key)
            await self.load_files()
        except Exception as e:
            self.app.push_screen(MessageScreen(str(e)))

    @on(Button.Pressed, "#download")
    async def download_file(self):
        selected = self.table.cursor_row
        if selected is None:
            return
            
        prefix = self.cos_client.prefix.rstrip('/') + '/'
        filename = self.table.get_row_at(selected)[0]
        
        self.download_progress = 0
        self.download_cancelled = False
        
        # 显示下载进度界面
        self.app.push_screen(DownloadScreen(filename=filename, on_cancel=self.download_cancelled, prefix=prefix, config_name=self.config_name))

    def handle_download_cancel(self):
        self.download_cancelled = True

    def update_progress(self, downloaded, total):
        progress = downloaded / total * 100
        for screen in self.app.screen_stack:
            if isinstance(screen, DownloadScreen):
                screen.update_progress(downloaded, total)
    @on(Button.Pressed, "#details")
    async def show_details(self):
        selected = self.table.cursor_row
        if selected is None:
            return
            
        prefix = self.cos_client.prefix.rstrip('/') + '/'
        filename = self.table.get_row_at(selected)[0]
        key = f"{filename}"
        
        try:
            file_info = self.cos_client.get_object(key)
            self.app.push_screen(FileDetailsScreen(file_info, self.config_name))
        except Exception as e:
            self.app.push_screen(MessageScreen(str(e)))
            raise

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()
