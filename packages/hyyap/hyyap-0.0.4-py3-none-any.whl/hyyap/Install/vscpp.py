import os
import requests
import subprocess
import shutil
import winreg
from tqdm.rich import tqdm
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn


class VS_CPP_Installer:
    # Visual Studio C++ 默认下载链接
    DEFAULT_VS_CPP_DOWNLOAD_URL = "https://aka.ms/vs/17/release/vs_community.exe"

    def __init__(self, show_progress=True, install_path=None, download_url=None, selected_modules=None):
        """
        初始化类，设置是否显示进度条和输出信息、安装路径、下载 URL 以及选择的安装模块
        :param show_progress: 是否显示进度条和输出信息
        :param install_path: 安装路径，若为 None 则使用默认路径
        :param download_url: 下载 URL，若为 None 则使用默认 URL
        :param selected_modules: 选择的安装模块列表，若为 None 则使用默认模块
        """
        self.show_progress = show_progress
        self.install_path = install_path
        self.download_url = download_url if download_url else self.DEFAULT_VS_CPP_DOWNLOAD_URL
        self.selected_modules = selected_modules if selected_modules else ["Microsoft.VisualStudio.Workload.NativeDesktop"]
        if not self.is_vs_cpp_installed():
            self.install()
        else:
            if self.show_progress:
                print("Visual Studio C++ is already installed. Installation will be stopped.")

    def is_vs_cpp_installed(self):
        """
        检测 Visual Studio C++ 是否已经安装
        :return: 如果安装返回 True，否则返回 False
        """
        try:
            # 打开注册表中 Visual Studio 的安装信息所在的键
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\VisualStudio\SxS\VS7")
            # 尝试获取版本信息，若能获取到则表示安装了 Visual Studio
            winreg.QueryValueEx(key, "17.0")
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

    def install_vs_cpp(self, installer_path):
        """
        安装 Visual Studio C++
        :param installer_path: 安装程序的路径
        """
        try:
            if self.show_progress:
                print("Starting to install Visual Studio C++...")
            install_args = [installer_path]
            for module in self.selected_modules:
                install_args.extend(["--add", module])
            install_args.extend(["--includeRecommended", "--quiet", "--norestart"])
            if self.install_path:
                install_args.extend(["--installPath", self.install_path])
            # 执行安装程序
            subprocess.run(install_args, check=True)
            if self.show_progress:
                print("Visual Studio C++ installed successfully.")
        except subprocess.CalledProcessError as e:
            if self.show_progress:
                print(f"Installation error: {e}")

    def install(self):
        """
        自动下载并安装 Visual Studio C++
        """
        # 下载路径
        download_path = os.path.join(os.getcwd(), "vs_cpp_installer.exe")
        if self.show_progress:
            print("Starting to download the Visual Studio C++ installer...")
        # 下载 Visual Studio C++ 安装程序
        self.download_file(self.download_url, download_path)

        # 安装 Visual Studio C++
        if os.path.exists(download_path):
            self.install_vs_cpp(download_path)
            # 安装完成后删除下载的安装程序
            os.remove(download_path)
        else:
            if self.show_progress:
                print("The downloaded installer file does not exist. Installation cannot proceed.")