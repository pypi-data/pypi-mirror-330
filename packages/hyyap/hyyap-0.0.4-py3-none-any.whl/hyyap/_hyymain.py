import requests
import warnings
from tqdm.rich import TqdmExperimentalWarning
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
import tarfile
import os
import shutil
import logging
import subprocess
import argparse
import sys
import re
import zipfile
from importlib.util import find_spec
from tqdm.rich import tqdm
from importlib.metadata import distributions
import configparser

# 工具版本信息
TOOL_VERSION = "hyyap -> hyy 0.0.4"

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 记录已经安装过的包
installed_packages = set()

# 红色文本的 ANSI 转义序列
RED = '\033[31m'
RESET = '\033[0m'


def get_installed_packages():
    """
    获取已安装的包列表
    """
    return {dist.metadata['Name'] for dist in distributions()}


def get_package_info(package_name, version=None, mirror_url='https://pypi.org'):
    """
    从指定镜像源获取包的信息
    :param package_name: 包名
    :param version: 包的版本，可选参数
    :param mirror_url: 镜像源的 URL，默认为 PyPI
    :return: 包的信息字典
    """
    try:
        pypi_url = f'{mirror_url}/pypi/{package_name}/json'
        response = requests.get(pypi_url)
        response.raise_for_status()  # 检查请求是否成功
        package_info = response.json()

        if version:
            if version in package_info['releases']:
                package_info['info']['version'] = version
            else:
                logging.error(f"{RED}Version {version} of {package_name} is not available on {mirror_url}.{RESET}")
                return None
        return package_info
    except requests.RequestException as e:
        logging.error(f"{RED}Failed to get package information from {mirror_url}: {e}{RESET}")
        return None


def download_package(download_url, download_location='.'):
    """
    下载包文件并显示进度条
    :param download_url: 包的下载链接
    :param download_location: 下载文件保存的位置
    :return: 下载的文件名
    """
    try:
        logging.info(f"Downloading package from {download_url}")
        file_name = os.path.basename(download_url)
        full_path = os.path.join(download_location, file_name)
        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        # 创建下载目录（如果不存在）
        os.makedirs(download_location, exist_ok=True)

        with open(full_path, 'wb') as file, tqdm(
                desc=file_name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

        return file_name
    except requests.RequestException as e:
        logging.error(f"{RED}Failed to download package: {e}{RESET}")
        return None


def extract_package(file_name):
    """
    解压包文件
    :param file_name: 包的文件名
    :return: 解压后的目录名
    """
    try:
        logging.info(f"Extracting package {file_name}")
        if file_name.endswith('.whl'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall()
            package_dir = os.path.splitext(file_name)[0]
        elif file_name.endswith('.tar.gz'):
            with tarfile.open(file_name, 'r:gz') as tar:
                tar.extractall()
            package_dir = os.path.splitext(os.path.splitext(file_name)[0])[0]
        else:
            logging.error(f"{RED}Unsupported file format: {file_name}{RESET}")
            return None
        return package_dir
    except (tarfile.TarError, OSError, zipfile.BadZipFile) as e:
        logging.error(f"{RED}Failed to extract package: {e}{RESET}")
        return None


def print_dependencies(package_info):
    """
    打印包的依赖信息
    :param package_info: 包的信息字典
    """
    requires_dist = package_info['info'].get('requires_dist', [])
    if requires_dist:
        logging.info("Package dependencies:")
        for dep in requires_dist:
            logging.info(f"  - {dep}")
    else:
        logging.info("No dependencies found for this package.")


def install_package(package_dir):
    """
    完善的安装包函数
    :param package_dir: 解压后的包目录
    """
    if package_dir and os.path.exists(package_dir):
        try:
            site_packages_dir = os.path.join(os.path.dirname(os.__file__), 'site-packages')
            logging.info(f"Package will be installed to {site_packages_dir}")

            setup_py_path = os.path.join(package_dir, 'setup.py')
            if os.path.exists(setup_py_path):
                # 如果存在 setup.py 文件，执行安装命令
                logging.info("Found setup.py, running installation command...")
                try:
                    subprocess.run([sys.executable, setup_py_path, 'install'], check=True)
                    logging.info("Package installed successfully using setup.py")
                except subprocess.CalledProcessError as e:
                    logging.error(f"{RED}Failed to install package using setup.py: {e}{RESET}")
            else:
                # 没有 setup.py 文件，直接复制文件到 site-packages 目录
                for root, dirs, files in os.walk(package_dir):
                    relative_path = os.path.relpath(root, package_dir)
                    target_dir = os.path.join(site_packages_dir, relative_path)
                    os.makedirs(target_dir, exist_ok=True)
                    for file in files:
                        source_file = os.path.join(root, file)
                        target_file = os.path.join(target_dir, file)
                        shutil.copy2(source_file, target_file)
                logging.info("Package installed successfully by copying files")
        except (OSError, shutil.Error) as e:
            logging.error(f"{RED}Failed to install package: {e}{RESET}")
    else:
        logging.error(f"{RED}Package directory does not exist.{RESET}")


def clean_up(file_name):
    """
    清理临时文件
    :param file_name: 临时文件名
    """
    if file_name and os.path.exists(file_name):
        try:
            os.remove(file_name)
            logging.info(f"Cleaned up {file_name}")
        except OSError as e:
            logging.error(f"{RED}Failed to clean up {file_name}: {e}{RESET}")


def is_package_installed(package_name):
    """
    检测包是否已经安装
    :param package_name: 包名
    :return: 如果已安装返回 True，否则返回 False
    """
    installed = get_installed_packages()
    return package_name in installed


def handle_dependencies(package_info, mirror_url='https://pypi.org'):
    """
    处理包的依赖关系
    :param package_info: 包的信息字典
    :param mirror_url: 镜像源的 URL，默认为 PyPI
    """
    requires_dist = package_info['info'].get('requires_dist', [])
    for dep in requires_dist:
        # 使用正则表达式提取包名
        match = re.match(r'^([a-zA-Z0-9_\-]+)', dep)
        if match:
            dep_name = match.group(1)
        else:
            logging.error(f"{RED}Failed to parse dependency: {dep}{RESET}")
            continue

        if dep_name in installed_packages:
            continue

        dep_version = None
        if '(' in dep and ')' in dep:
            version_spec = dep[dep.index('(') + 1:dep.index(')')]
            # 这里简单处理，只取第一个版本限制
            if '>=' in version_spec:
                dep_version = version_spec.split('>=')[1].strip()
            elif '==' in version_spec:
                dep_version = version_spec.split('==')[1].strip()

        if not is_package_installed(dep_name):
            logging.info(f"Installing dependency: {dep_name} {dep_version or 'latest'}")
            installed_packages.add(dep_name)
            handle_install(dep_name, dep_version, mirror_url)


def handle_install(package_name, version=None, mirror_url='https://pypi.org'):
    if package_name in installed_packages:
        return

    is_installed = is_package_installed(package_name)
    if is_installed:
        logging.info(f"The package {package_name} is already installed. Skipping installation.")
        installed_packages.add(package_name)

    package_info = get_package_info(package_name, version, mirror_url)
    if not package_info:
        return

    print_dependencies(package_info)

    # 处理依赖关系
    handle_dependencies(package_info, mirror_url)

    if is_installed:
        return

    # 获取指定版本的下载链接
    target_version = package_info['info']['version']
    if target_version in package_info['releases']:
        download_url = package_info['releases'][target_version][0]['url']
    else:
        logging.error(f"{RED}Version {target_version} of {package_name} is not available on {mirror_url}.{RESET}")
        return

    file_name = download_package(download_url)
    if not file_name:
        return

    package_dir = extract_package(file_name)
    if not package_dir:
        clean_up(file_name)
        return

    install_package(package_dir)
    clean_up(file_name)
    installed_packages.add(package_name)


def handle_download(package_name, version=None, mirror_url='https://pypi.org', download_location='.', only_gz=False, gz_and_whl=False):
    package_info = get_package_info(package_name, version, mirror_url)
    if not package_info:
        return

    if not version:
        # 如果没有指定版本，使用最新版本
        version = package_info['info']['version']

    # 获取指定版本的下载链接
    if version in package_info['releases']:
        releases = package_info['releases'][version]
        if only_gz:
            gz_links = [rel['url'] for rel in releases if rel['filename'].endswith('.tar.gz')]
            if not gz_links:
                logging.error(f"{RED}No .gz files available for {package_name} version {version} on {mirror_url}.{RESET}")
                return
            for link in gz_links:
                file_name = download_package(link, download_location)
                if file_name:
                    logging.info(f"Package downloaded successfully to {download_location} as {file_name}")
        elif gz_and_whl:
            gz_links = [rel['url'] for rel in releases if rel['filename'].endswith('.tar.gz')]
            whl_links = [rel['url'] for rel in releases if rel['filename'].endswith('.whl')]
            if not gz_links:
                logging.error(f"{RED}No .gz files available for {package_name} version {version} on {mirror_url}.{RESET}")
            else:
                for link in gz_links:
                    file_name = download_package(link, download_location)
                    if file_name:
                        logging.info(f"Package downloaded successfully to {download_location} as {file_name}")
            if not whl_links:
                logging.error(f"{RED}No .whl files available for {package_name} version {version} on {mirror_url}.{RESET}")
            else:
                for link in whl_links:
                    file_name = download_package(link, download_location)
                    if file_name:
                        logging.info(f"Package downloaded successfully to {download_location} as {file_name}")
        else:
            # 正常下载逻辑
            download_url = releases[0]['url']
            file_name = download_package(download_url, download_location)
            if file_name:
                logging.info(f"Package downloaded successfully to {download_location} as {file_name}")
    else:
        logging.error(f"{RED}Version {version} of {package_name} is not available on {mirror_url}.{RESET}")


def uninstall_package(package_name):
    """
    卸载包
    :param package_name: 包名
    """
    if not is_package_installed(package_name):
        logging.info(f"The package {package_name} is not installed. Skipping uninstallation.")
        return

    site_packages_dir = os.path.join(os.path.dirname(os.__file__), 'site-packages')
    package_dir = os.path.join(site_packages_dir, package_name)
    egg_info_dir = None
    for item in os.listdir(site_packages_dir):
        if item.endswith('.egg-info') and item.startswith(package_name):
            egg_info_dir = os.path.join(site_packages_dir, item)
            break

    try:
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
            logging.info(f"Removed package directory: {package_dir}")
        if egg_info_dir:
            shutil.rmtree(egg_info_dir)
            logging.info(f"Removed egg-info directory: {egg_info_dir}")
        logging.info(f"Package {package_name} uninstalled successfully.")
    except (OSError, shutil.Error) as e:
        logging.error(f"{RED}Failed to uninstall package {package_name}: {e}{RESET}")


def list_installed_packages():
    """
    列出所有已安装的模块
    """
    logging.info("List of installed packages:")
    for dist in distributions():
        logging.info(f"{dist.metadata['Name']}=={dist.metadata['Version']}")


def handle_update(package_name, mirror_url='https://pypi.org'):
    """
    更新包
    :param package_name: 包名
    :param mirror_url: 镜像源的 URL，默认为 PyPI
    """
    if not is_package_installed(package_name):
        logging.info(f"The package {package_name} is not installed. Skipping update.")
        return
    uninstall_package(package_name)
    handle_install(package_name, mirror_url=mirror_url)


def set_permanent_mirror(mirror_url):
    """
    设置永久的镜像源
    :param mirror_url: 镜像源的 URL
    """
    config = configparser.ConfigParser()
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.getenv('APPDATA'), 'your_package_manager')
        config_file = os.path.join(config_dir, 'config.ini')
    else:  # Linux/Mac
        config_dir = os.path.join(os.path.expanduser('~'), '.your_package_manager')
        config_file = os.path.join(config_dir, 'config.ini')

    os.makedirs(config_dir, exist_ok=True)

    if not config.has_section('mirror'):
        config.add_section('mirror')
    config.set('mirror', 'url', mirror_url)

    with open(config_file, 'w') as f:
        config.write(f)

    logging.info(f"Permanent mirror set to {mirror_url}")


def get_permanent_mirror():
    """
    获取永久设置的镜像源
    :return: 镜像源的 URL，如果未设置则返回默认值
    """
    config = configparser.ConfigParser()
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.getenv('APPDATA'), 'your_package_manager')
        config_file = os.path.join(config_dir, 'config.ini')
    else:  # Linux/Mac
        config_dir = os.path.join(os.path.expanduser('~'), '.your_package_manager')
        config_file = os.path.join(config_dir, 'config.ini')

    if os.path.exists(config_file):
        config.read(config_file)
        if config.has_section('mirror') and config.has_option('mirror', 'url'):
            return config.get('mirror', 'url')
    return 'https://pypi.org'


def main():
    parser = argparse.ArgumentParser(description='Simple Python package manager')
    parser.add_argument('--version', action='version', version=f'%(prog)s {TOOL_VERSION}')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # install 命令
    install_parser = subparsers.add_parser('install', help='Install a Python package')
    install_parser.add_argument('package_name', help='Name of the package to install')
    install_parser.add_argument('-v', '--package-version', help='Version of the package to install')
    install_parser.add_argument('-m', '--mirror-url', help='Mirror URL to use, will override permanent setting')

    # download 命令
    download_parser = subparsers.add_parser('download', help='Download a Python package')
    download_parser.add_argument('package_name', help='Name of the package to download')
    download_parser.add_argument('-v', '--package-version', help='Version of the package to download')
    download_parser.add_argument('-m', '--mirror-url', help='Mirror URL to use, will override permanent setting')
    download_parser.add_argument('-d', '--download-location', default='.', help='Location to save the downloaded package')
    download_parser.add_argument('-g', action='store_true', help='Only download .gz files')
    download_parser.add_argument('-gw', action='store_true', help='Download both .gz and .whl files')

    # uninstall 命令
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall a Python package')
    uninstall_parser.add_argument('package_name', help='Name of the package to uninstall')

    # list 命令
    list_parser = subparsers.add_parser('list', help='List all installed Python packages')

    # update 命令
    update_parser = subparsers.add_parser('update', help='Update a Python package')
    update_parser.add_argument('package_name', help='Name of the package to update')
    update_parser.add_argument('-m', '--mirror-url', help='Mirror URL to use, will override permanent setting')

    # set-mirror 命令
    set_mirror_parser = subparsers.add_parser('set-mirror', help='Set a permanent mirror URL')
    set_mirror_parser.add_argument('mirror_url', help='Mirror URL to set as permanent')

    args = parser.parse_args()

    if args.command == 'install':
        mirror_url = args.mirror_url if args.mirror_url else get_permanent_mirror()
        logging.info(f"Using mirror: {mirror_url}")
        try:
            handle_install(args.package_name, args.package_version, mirror_url)
        except Exception as e:
            logging.error(f"{RED}Installation failed: {e}{RESET}")
    elif args.command == 'download':
        mirror_url = args.mirror_url if args.mirror_url else get_permanent_mirror()
        download_location = args.download_location
        only_gz = args.g
        gz_and_whl = args.gw
        logging.info(f"Using mirror: {mirror_url}")
        try:
            handle_download(args.package_name, args.package_version, mirror_url, download_location, only_gz, gz_and_whl)
        except Exception as e:
            logging.error(f"{RED}Download failed: {e}{RESET}")

    elif args.command == 'uninstall':
        try:
            uninstall_package(args.package_name)
        except Exception as e:
            logging.error(f"{RED}Uninstallation failed: {e}{RESET}")
    elif args.command == 'list':
        list_installed_packages()
    elif args.command == 'update':
        mirror_url = args.mirror_url if args.mirror_url else get_permanent_mirror()
        logging.info(f"Using mirror: {mirror_url}")
        try:
            handle_update(args.package_name, mirror_url)
        except Exception as e:
            logging.error(f"{RED}Update failed: {e}{RESET}")
    elif args.command == 'set-mirror':
        set_permanent_mirror(args.mirror_url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()