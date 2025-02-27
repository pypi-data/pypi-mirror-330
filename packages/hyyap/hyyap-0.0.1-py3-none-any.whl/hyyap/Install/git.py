import os
import requests
from tqdm import tqdm
from rich.progress import Progress, TransferSpeedColumn, DownloadColumn
from rich.console import Console
import tarfile
import winreg


class Git:
    def __init__(self, show_progress=False):
        self.url = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/23216272/11d3b37f-8499-4919-8f41-b797636cd982?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250226%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250226T125915Z&X-Amz-Expires=300&X-Amz-Signature=5d5901c157ad2e1e95e57285944ea7ae595bdfcaaef743ca34dd4339c5a08f83&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DGit-2.48.1-64-bit.tar.bz2&response-content-type=application%2Foctet-stream"
        self.save_path = os.path.join(os.path.expanduser("~"), "Git-2.48.1-64-bit.tar.bz2")
        self.extract_dir = os.path.join(os.path.expanduser("~"), "git")
        self.show_progress = show_progress
        self.install()

    def download_and_extract(self):
        """
        下载并解压 Git 的 tar.bz2 文件
        :return: 解压后的文件夹路径
        """
        # 下载文件
        if self.show_progress:
            console = Console()
            with Progress(
                    "[progress.description]{task.description}",
                    TransferSpeedColumn(),
                    DownloadColumn(),
                    console=console,
                    expand=True
            ) as progress:
                task = progress.add_task("[cyan]Downloading...", total=None)
                response = requests.get(self.url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                progress.update(task, total=total_size)
                with open(self.save_path, 'wb') as file:
                    for data in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB'):
                        file.write(data)
                        progress.update(task, advance=len(data))
                progress.update(task, description="[green]Download completed!")
        else:
            response = requests.get(self.url)
            with open(self.save_path, 'wb') as file:
                file.write(response.content)

        # 解压文件
        with tarfile.open(self.save_path, 'r:bz2') as tar_ref:
            tar_ref.extractall(self.extract_dir)

        # 删除 tar.bz2 文件
        if os.path.exists(self.save_path):
            os.remove(self.save_path)

        return self.extract_dir

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
        git_dir = self.download_and_extract()
        git_bin_path = os.path.join(git_dir, "bin")
        self.set_environment_variable(git_bin_path)