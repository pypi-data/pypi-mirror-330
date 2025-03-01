import os
import requests
import subprocess
import winreg
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn


class QuarkProductInstaller:
    # 夸克浏览器默认下载链接
    DEFAULT_QUARK_BROWSER_DOWNLOAD_URL = "https://umcdn.quark.cn/download/37212/quarkpc/pcquark@homepage_oficial/QuarkPC_V2.1.0.234_pc_pf30002_(zh-cn)_release_(Build2086145-250219204913-x64).exe"
    # 夸克网盘默认下载链接（假设的，你需要替换为实际链接）
    DEFAULT_QUARK_CLOUD_DRIVE_DOWNLOAD_URL = "https://example.com/quark_cloud_drive_installer.exe"

    def __init__(self, product_type, show_progress=True, install_path=None, download_url=None):
        """
        初始化类，设置要安装的产品类型、是否显示进度条和输出信息、安装路径以及下载 URL
        :param product_type: 产品类型，'browser' 表示夸克浏览器，'cloud_drive' 表示夸克网盘
        :param show_progress: 是否显示进度条和输出信息
        :param install_path: 安装路径，若为 None 则使用默认路径
        :param download_url: 下载 URL，若为 None 则使用默认 URL
        """
        self.product_type = product_type
        self.show_progress = show_progress
        self.install_path = install_path
        if product_type == 'browser':
            self.download_url = download_url if download_url else self.DEFAULT_QUARK_BROWSER_DOWNLOAD_URL
            if not self.is_quark_browser_installed():
                self.install()
            else:
                if self.show_progress:
                    print("夸克浏览器 is already installed. Installation will be stopped.")
        elif product_type == 'cloud_drive':
            self.download_url = download_url if download_url else self.DEFAULT_QUARK_CLOUD_DRIVE_DOWNLOAD_URL
            if not self.is_quark_cloud_drive_installed():
                self.install()
            else:
                if self.show_progress:
                    print("夸克网盘 is already installed. Installation will be stopped.")
        else:
            raise ValueError("Invalid product type. Supported types are 'browser' and 'cloud_drive'.")

    def is_quark_browser_installed(self):
        """
        检测夸克浏览器是否已经安装
        :return: 如果安装返回 True，否则返回 False
        """
        try:
            # 打开注册表中夸克浏览器的安装信息所在的键
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\夸克浏览器")
            # 尝试获取显示名称，若能获取到则表示安装了夸克浏览器
            winreg.QueryValueEx(key, "DisplayName")
            winreg.CloseKey(key)
            return True
        except (FileNotFoundError, OSError):
            return False

    def is_quark_cloud_drive_installed(self):
        """
        检测夸克网盘是否已经安装
        :return: 如果安装返回 True，否则返回 False
        """
        try:
            # 打开注册表中夸克网盘的安装信息所在的键
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\夸克网盘")
            # 尝试获取显示名称，若能获取到则表示安装了夸克网盘
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

    def install_quark_product(self, installer_path):
        """
        安装夸克产品
        :param installer_path: 安装程序的路径
        """
        try:
            if self.show_progress:
                if self.product_type == 'browser':
                    print("Starting to install 夸克浏览器...")
                elif self.product_type == 'cloud_drive':
                    print("Starting to install 夸克网盘...")
            install_args = [installer_path]
            if self.install_path:
                # 假设夸克产品安装程序支持 /DIR 参数指定安装路径，实际可能需要调整
                install_args.extend(["/DIR", self.install_path])
            # 执行安装程序
            subprocess.run(install_args, check=True)
            if self.show_progress:
                if self.product_type == 'browser':
                    print("夸克浏览器 installed successfully.")
                elif self.product_type == 'cloud_drive':
                    print("夸克网盘 installed successfully.")
        except subprocess.CalledProcessError as e:
            if self.show_progress:
                if self.product_type == 'browser':
                    print(f"夸克浏览器 Installation error: {e}")
                elif self.product_type == 'cloud_drive':
                    print(f"夸克网盘 Installation error: {e}")

    def install(self):
        """
        自动下载并安装夸克产品
        """
        if self.product_type == 'browser':
            download_path = os.path.join(os.getcwd(), "quark_browser_installer.exe")
        elif self.product_type == 'cloud_drive':
            download_path = os.path.join(os.getcwd(), "quark_cloud_drive_installer.exe")
        if self.show_progress:
            if self.product_type == 'browser':
                print("Starting to download the 夸克浏览器 installer...")
            elif self.product_type == 'cloud_drive':
                print("Starting to download the 夸克网盘 installer...")
        # 下载夸克产品安装程序
        self.download_file(self.download_url, download_path)

        # 安装夸克产品
        if os.path.exists(download_path):
            self.install_quark_product(download_path)
            # 安装完成后删除下载的安装程序
            os.remove(download_path)
        else:
            if self.show_progress:
                if self.product_type == 'browser':
                    print("The downloaded 夸克浏览器 installer file does not exist. Installation cannot proceed.")
                elif self.product_type == 'cloud_drive':
                    print("The downloaded 夸克网盘 installer file does not exist. Installation cannot proceed.")