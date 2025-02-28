import os
import requests
import zipfile
import winreg
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn


class GeekInstaller:
    # Geek 默认下载链接
    DEFAULT_GEEK_DOWNLOAD_URL = "https://geekuninstaller.com/geek.zip"

    def __init__(self, show_progress=True, install_path=None, download_url=None):
        """
        初始化类，设置是否显示进度条和输出信息、安装路径以及下载 URL
        :param show_progress: 是否显示进度条和输出信息
        :param install_path: 安装路径，若为 None 则使用默认路径
        :param download_url: 下载 URL，若为 None 则使用默认 URL
        """
        self.show_progress = show_progress
        self.install_path = install_path
        self.download_url = download_url if download_url else self.DEFAULT_GEEK_DOWNLOAD_URL
        if not self.is_geek_installed():
            self.install()
        else:
            if self.show_progress:
                print("Geek is already installed. Installation will be stopped.")

    def is_geek_installed(self):
        """
        检测 Geek 是否已经安装
        :return: 如果安装返回 True，否则返回 False
        """
        try:
            # 打开注册表中 Geek 的安装信息所在的键
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\GeekUninstaller")
            # 尝试获取显示名称，若能获取到则表示安装了 Geek
            winreg.QueryValueEx(key, "DisplayName")
            winreg.CloseKey(key)
            return True
        except (FileNotFoundError, OSError):
            return False

    def download_file(self, url, save_path):
        """
        下载文件并显示彩色进度条
        :param url: 文件下载链接
        :param save_path: 保存文件的路径
        """
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        if self.show_progress:
            # 自定义进度条样式，这里设置进度条颜色为绿色
            progress = Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(style="green"),
                "[progress.percentage]{task.percentage:>3.0f}%",
                "•",
                TransferSpeedColumn(),
                "•",
                TimeRemainingColumn(),
            )
            with progress:
                task = progress.add_task("[cyan]Downloading...", total=total_size)
                with open(save_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        file.write(data)
                        progress.update(task, advance=len(data))
        else:
            with open(save_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)

        if total_size != 0:
            file_size = os.path.getsize(save_path)
            if file_size != total_size:
                print("Download error: File size does not match.")

    def extract_zip(self, file_path, extract_path):
        """
        解压 ZIP 文件
        :param file_path: ZIP 文件路径
        :param extract_path: 解压目标路径
        """
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            if self.show_progress:
                print("ZIP file extracted successfully.")
        except Exception as e:
            if self.show_progress:
                print(f"Error extracting ZIP file: {e}")

    def install(self):
        """
        自动下载并安装 Geek
        """
        # 下载路径
        download_path = os.path.join(os.getcwd(), "geek.zip")
        if self.show_progress:
            print("Starting to download the Geek ZIP file...")
        # 下载 Geek ZIP 文件
        self.download_file(self.download_url, download_path)

        if self.install_path is None:
            self.install_path = os.path.join(os.getcwd(), "GeekUninstaller")

        # 解压 ZIP 文件
        if os.path.exists(download_path):
            self.extract_zip(download_path, self.install_path)
            # 安装完成后删除下载的 ZIP 文件
            os.remove(download_path)
        else:
            if self.show_progress:
                print("The downloaded ZIP file does not exist. Installation cannot proceed.")
