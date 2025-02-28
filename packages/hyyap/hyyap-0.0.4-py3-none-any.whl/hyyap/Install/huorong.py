import os
import requests
import subprocess
import winreg
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn


class HuorongInstaller:
    DEFAULT_HUORONG_DOWNLOAD_URL = "https://down-tencent.huorong.cn/sysdiag-all-x64-6.0.5.3-2025.02.27.1.exe"

    def __init__(self, show_progress=True, install_path=None, download_url=None):
        """
        初始化类，设置是否显示进度条和输出信息、安装路径以及下载 URL
        :param show_progress: 是否显示进度条和输出信息
        :param install_path: 安装路径，若为 None 则使用默认路径
        :param download_url: 下载 URL，若为 None 则使用默认 URL
        """
        self.show_progress = show_progress
        self.install_path = install_path
        self.download_url = download_url if download_url else self.DEFAULT_HUORONG_DOWNLOAD_URL
        if not self.is_huorong_installed():
            self.install()
        else:
            if self.show_progress:
                print("火绒安全软件 is already installed. Installation will be stopped.")

    def is_huorong_installed(self):
        """
        检测火绒安全软件是否已经安装
        :return: 如果安装返回 True，否则返回 False
        """
        try:
            # 打开注册表中 火绒安全软件 的安装信息所在的键
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\火绒安全软件")
            # 尝试获取显示名称，若能获取到则表示安装了 火绒安全软件
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

    def install_huorong(self, installer_path):
        """
        安装 火绒安全软件
        :param installer_path: 安装程序的路径
        """
        try:
            if self.show_progress:
                print("Starting to install 火绒安全软件...")
            install_args = [installer_path]
            if self.install_path:
                # 假设 火绒安全软件 安装程序支持 /DIR 参数指定安装路径，实际可能需要调整
                install_args.extend(["/DIR", self.install_path])
            # 执行安装程序
            subprocess.run(install_args, check=True)
            if self.show_progress:
                print("火绒安全软件 installed successfully.")
        except subprocess.CalledProcessError as e:
            if self.show_progress:
                print(f"Installation error: {e}")

    def install(self):
        """
        自动下载并安装 火绒安全软件
        """
        # 下载路径
        download_path = os.path.join(os.getcwd(), "huorong_installer.exe")
        if self.show_progress:
            print("Starting to download the 火绒安全软件 installer...")
        # 下载 火绒安全软件 安装程序
        self.download_file(self.download_url, download_path)

        # 安装 火绒安全软件
        if os.path.exists(download_path):
            self.install_huorong(download_path)
            # 安装完成后删除下载的安装程序
            os.remove(download_path)
        else:
            if self.show_progress:
                print("The downloaded installer file does not exist. Installation cannot proceed.")