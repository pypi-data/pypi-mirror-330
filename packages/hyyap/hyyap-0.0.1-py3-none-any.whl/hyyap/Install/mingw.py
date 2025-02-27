import os
import requests
from tqdm import tqdm
from rich.progress import Progress, TransferSpeedColumn, DownloadColumn
from rich.console import Console
import py7zr
import winreg

def download_and_extract_mingw(arch='i686', show_progress=True):
    """
    下载并解压 MinGW 的 7z 文件

    :param arch: MinGW 的架构，可选 'i686' 或 'x86_64'
    :param show_progress: 是否显示下载进度条
    :return: 解压后的文件夹路径
    """
    if arch == 'i686':
        url = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/446033510/743a1268-21b9-4041-8f7f-8c0ac84c5843?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250225%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250225T160901Z&X-Amz-Expires=300&X-Amz-Signature=5b0c3af7c200844871473d3f5b457bc39b5cbcc8695e58ddcd5ef85ebbac881d&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Di686-14.2.0-release-mcf-dwarf-ucrt-rt_v12-rev1.7z&response-content-type=application%2Foctet-stream"
        save_path = os.path.join(os.path.expanduser("~"), "i686-14.2.0-release-mcf-dwarf-ucrt-rt_v12-rev1.7z")
        extract_dir = os.path.join(os.path.expanduser("~"), "mingw64")
        new_name = "i686mingw64"
    else:
        url = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/446033510/aba497ad-caca-4f91-8aa8-d62e183feab9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250225%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250225T162851Z&X-Amz-Expires=300&X-Amz-Signature=bb3067eb988aa64c8af3c247ddf48b24de21b13b429653db1095738552e0f082&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Dx86_64-14.2.0-release-mcf-seh-ucrt-rt_v12-rev1.7z&response-content-type=application%2Foctet-stream"
        save_path = os.path.join(os.path.expanduser("~"), "x86_64-14.2.0-release-mcf-seh-ucrt-rt_v12-rev1.7z")
        extract_dir = os.path.join(os.path.expanduser("~"), "mingw64")
        new_name = "x86_64mingw64"

    # 下载文件
    if show_progress:
        console = Console()
        with Progress(
            "[progress.description]{task.description}",
            TransferSpeedColumn(),
            DownloadColumn(),
            console=console,
            expand=True
        ) as progress:
            task = progress.add_task("[cyan]Downloading...", total=None)
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            progress.update(task, total=total_size)
            with open(save_path, 'wb') as file:
                for data in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB'):
                    file.write(data)
                    progress.update(task, advance=len(data))
            progress.update(task, description="[green]Download completed!")
    else:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)

    # 解压文件
    with py7zr.SevenZipFile(save_path, mode='r') as z:
        z.extractall(path=extract_dir)

    # 重命名文件夹
    new_extract_dir = os.path.join(os.path.dirname(extract_dir), new_name)
    if os.path.exists(extract_dir):
        os.rename(extract_dir, new_extract_dir)

    # 删除 7z 文件
    if os.path.exists(save_path):
        os.remove(save_path)

    return new_extract_dir

def set_mingw_environment_variable(mingw_bin_path):
    """
    设置 MinGW 的环境变量

    :param mingw_bin_path: MinGW 的 bin 文件夹路径
    """
    # 打开注册表项
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_ALL_ACCESS)

    try:
        # 获取当前的 PATH 环境变量
        path_var, _ = winreg.QueryValueEx(key, 'PATH')
        paths = path_var.split(';')

        # 移除包含 \mingw64 或 \mingw64\bin 的路径
        new_paths = [p for p in paths if not ('\\mingw64' in p or '\\mingw64\\bin' in p)]

        # 添加新的 mingw64\bin 路径
        if mingw_bin_path not in new_paths:
            new_paths.append(mingw_bin_path)

        # 更新 PATH 环境变量
        new_path_var = ';'.join(new_paths)
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path_var)
    finally:
        # 关闭注册表项
        winreg.CloseKey(key)

class MinGW:
    """show_progress: 是否开启进度条"""
    def __init__(self,show_progress = False):
        self.show_progress = show_progress

    def i686(self):
        """show_progress: 是否开启进度条"""
        arch = 'i686'
        mingw_dir = download_and_extract_mingw(arch, self.show_progress)
        mingw_bin_path = os.path.join(mingw_dir, "bin")
        set_mingw_environment_variable(mingw_bin_path)


    def x86_64(self):
        """show_progress: 是否开启进度条"""
        arch = 'x86_64'
        mingw_dir = download_and_extract_mingw(arch, self.show_progress)
        mingw_bin_path = os.path.join(mingw_dir, "bin")
        set_mingw_environment_variable(mingw_bin_path)