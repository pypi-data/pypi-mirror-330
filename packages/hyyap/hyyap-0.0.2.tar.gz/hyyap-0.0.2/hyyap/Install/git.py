import os
import requests
import io
import tarfile
import winreg
from tqdm.rich import trange
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
import urllib3

# 抑制 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GitInstaller:
    # 假设这是你指定的 tar.bz2 文件的 bytes 数据
    TAR_BYTES = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\xed\x99...'  # 这里需要替换为实际的 bytes 数据
    URL = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/23216272/11d3b37f-8499-4919-8f41-b797636cd982?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250227%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250227T132929Z&X-Amz-Expires=300&X-Amz-Signature=de1553f96abb67440beeff9adf010938a0ee1acc22d529e9ce297340db37cd54&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DGit-2.48.1-64-bit.tar.bz2&response-content-type=application%2Foctet-stream"
    SAVE_PATH = os.path.join(os.path.expanduser("~"), "Git-2.48.1-64-bit.tar.bz2")
    EXTRACT_DIR = os.path.join(os.path.expanduser("~"), "git")

    def __init__(self, use_download=True, show_progress=False):
        self.use_download = use_download
        self.show_progress = show_progress
        self.install()

    def download_file(self):
        """
        下载 Git 的 tar.bz2 文件
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if self.show_progress:
                    with Progress(
                            TextColumn("[progress.description]{task.description}"),
                            BarColumn(bar_width=None),
                            "[progress.percentage]{task.percentage:>3.0f}%",
                            "•",
                            TransferSpeedColumn(),
                            "•",
                            TimeRemainingColumn(),
                    ) as progress:
                        task = progress.add_task("[cyan]Downloading...", total=None)
                        # 忽略 SSL 验证
                        response = requests.get(self.URL, stream=True, verify=False)

                        # 由于 Content-Length 为 0，按块计数更新进度条
                        print("Content-Length is 0. Progress will be estimated by chunks.")

                        with open(self.SAVE_PATH, 'wb') as file:
                            chunk_count = 0
                            for data in response.iter_content(chunk_size=1024):
                                if not data:
                                    continue
                                file.write(data)
                                chunk_count += 1
                                progress.update(task, advance=1, total=chunk_count)
                else:
                    # 忽略 SSL 验证
                    response = requests.get(self.URL, verify=False)
                    with open(self.SAVE_PATH, 'wb') as file:
                        file.write(response.content)

                return self.SAVE_PATH
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Download attempt {attempt + 1} failed. Retrying... Error: {e}")
                else:
                    print(f"Failed to download after {max_retries} attempts. Error: {e}")
                    raise

    def extract_file(self, file_source):
        """
        解压 Git 的 tar.bz2 文件
        :param file_source: 文件来源，可以是文件路径或 bytes 对象
        :return: 解压后的文件夹路径
        """
        try:
            if isinstance(file_source, bytes):
                file_obj = io.BytesIO(file_source)
            else:
                file_obj = open(file_source, 'rb')

            with tarfile.open(fileobj=file_obj, mode='r:bz2') as tar_ref:
                members = tar_ref.getmembers()
                if self.show_progress:
                    with Progress(
                            TextColumn("[progress.description]{task.description}"),
                            BarColumn(bar_width=None),
                            "[progress.percentage]{task.percentage:>3.0f}%",
                            "•",
                            TransferSpeedColumn(),
                            "•",
                            TimeRemainingColumn(),
                    ) as progress:
                        task = progress.add_task("[cyan]Extracting...", total=len(members))
                        for member in members:
                            tar_ref.extract(member, self.EXTRACT_DIR)
                            progress.update(task, advance=1)
                else:
                    tar_ref.extractall(self.EXTRACT_DIR)

            if isinstance(file_source, str) and os.path.exists(file_source):
                os.remove(file_source)

            return self.EXTRACT_DIR
        except Exception as e:
            print(f"Failed to extract. Error: {e}")
            raise

    def set_environment_variable(self, git_bin_path):
        """
        设置 Git 的环境变量
        :param git_bin_path: Git 的 bin 文件夹路径
        """
        # 打开注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_ALL_ACCESS)

        try:
            # 获取当前的 PATH 环境变量
            path_var, _ = winreg.QueryValueEx(key, 'PATH')
            paths = path_var.split(';')

            # 移除已有的 Git 相关路径（可根据实际情况调整移除逻辑）
            new_paths = [p for p in paths if not ('\\git\\' in p or '\\git\\bin' in p)]

            # 添加新的 Git bin 路径
            if git_bin_path not in new_paths:
                new_paths.append(git_bin_path)

            # 更新 PATH 环境变量
            new_path_var = ';'.join(new_paths)
            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path_var)
        finally:
            # 关闭注册表项
            winreg.CloseKey(key)

    def install(self):
        if self.use_download:
            file_source = self.download_file()
        else:
            file_source = self.TAR_BYTES

        git_dir = self.extract_file(file_source)
        git_bin_path = os.path.join(git_dir, "bin")
        self.set_environment_variable(git_bin_path)