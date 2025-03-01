import os
import requests
import subprocess
import platform
import tarfile
import py7zr
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn


class SteamPlusPlusInstaller:
    # 不同操作系统的下载链接
    DOWNLOAD_URLS = {
        "Windows": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/321682465/3c878130-c1f5-429b-b4b0-612f878a72fe?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250227%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250227T142143Z&X-Amz-Expires=300&X-Amz-Signature=90480b9a2514948429cac7a51658143057a6a9398f8f269cfaf803bff391be73&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DSteam%2B%2B_v3.0.0-rc.15_win_x64.7z&response-content-type=application%2Foctet-stream",
        "Darwin": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/321682465/d7d4623c-306f-46cb-a5a0-5df31a2886ba?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250227%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250227T142223Z&X-Amz-Expires=300&X-Amz-Signature=e7e5220b433a0468ae2b05d53029ee9d5611080334f7bed86eb45a69b0452edb&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DSteam%2B%2B_v3.0.0-rc.15_macos.dmg&response-content-type=application%2Foctet-stream",
        "Linux_x64": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/321682465/6dd7d4ed-da8d-4786-b89a-6e8990dd9a7c?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250227%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250227T142331Z&X-Amz-Expires=300&X-Amz-Signature=e55d8fc63c0a2963973fe9fc0c389af21a4a838f79ce03b064bd7e6103aee637&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DSteam%2B%2B_v3.0.0-rc.15_linux_x64.tgz&response-content-type=application%2Foctet-stream",
        "Linux_arm64": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/321682465/96e5ede1-84de-497d-8c63-af9ad04f6942?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250227%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250227T142358Z&X-Amz-Expires=300&X-Amz-Signature=52fb03a8cfcda5f2ced6a2e885ce1b99679c904233689be169c27d742aa1ed51&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DSteam%2B%2B_v3.0.0-rc.15_linux_arm64.tgz&response-content-type=application%2Foctet-stream"
    }

    def __init__(self, show_progress=True, install_path=None):
        """
        初始化类，设置是否显示进度条和输出信息、安装路径
        :param show_progress: 是否显示进度条和输出信息
        :param install_path: 安装路径，若为 None 则使用默认路径
        """
        self.show_progress = show_progress
        self.install_path = install_path
        self.download_url = self.get_download_url()
        self.install()

    def get_download_url(self):
        """
        根据操作系统类型获取对应的下载链接
        :return: 下载链接
        """
        system = platform.system()
        if system == "Windows":
            return self.DOWNLOAD_URLS["Windows"]
        elif system == "Darwin":
            return self.DOWNLOAD_URLS["Darwin"]
        elif system == "Linux":
            machine = platform.machine()
            if machine == "x86_64":
                return self.DOWNLOAD_URLS["Linux_x64"]
            elif machine == "aarch64":
                return self.DOWNLOAD_URLS["Linux_arm64"]
        raise ValueError(f"Unsupported operating system: {system} {platform.machine()}")

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

    def extract_file(self, file_path, extract_path):
        """
        解压文件，支持 7z、dmg、tgz 格式
        :param file_path: 文件路径
        :param extract_path: 解压目标路径
        """
        if file_path.endswith('.7z'):
            try:
                with py7zr.SevenZipFile(file_path, mode='r') as z:
                    z.extractall(path=extract_path)
                if self.show_progress:
                    print("7z file extracted successfully.")
            except Exception as e:
                if self.show_progress:
                    print(f"Error extracting 7z file: {e}")
        elif file_path.endswith('.dmg'):
            if self.show_progress:
                print("Mounting DMG file...")
            try:
                subprocess.run(['hdiutil', 'attach', file_path], check=True)
                if self.show_progress:
                    print("DMG file mounted successfully.")
            except subprocess.CalledProcessError as e:
                if self.show_progress:
                    print(f"Error mounting DMG file: {e}")
        elif file_path.endswith('.tgz'):
            try:
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(path=extract_path)
                if self.show_progress:
                    print("TGZ file extracted successfully.")
            except Exception as e:
                if self.show_progress:
                    print(f"Error extracting TGZ file: {e}")

    def install(self):
        """
        自动下载并安装 Steam++
        """
        # 获取下载文件名
        file_name = self.download_url.split('filename=')[-1].split('&')[0]
        download_path = os.path.join(os.getcwd(), file_name)

        if self.show_progress:
            print(f"Starting to download {file_name}...")
        # 下载文件
        self.download_file(self.download_url, download_path)

        if self.install_path is None:
            self.install_path = os.path.join(os.getcwd(), os.path.splitext(file_name)[0])

        if os.path.exists(download_path):
            if self.show_progress:
                print(f"Starting to extract {file_name} to {self.install_path}...")
            # 解压文件
            self.extract_file(download_path, self.install_path)
            # 删除下载文件
            os.remove(download_path)
        else:
            if self.show_progress:
                print("The downloaded file does not exist. Installation cannot proceed.")