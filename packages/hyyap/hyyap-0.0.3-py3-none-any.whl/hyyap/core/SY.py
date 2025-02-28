import psutil
import platform
import pynvml
import subprocess
import wmi
import win32api,win32con,os


class CPUInfo:
    def __init__(self):
        pass

    def get_physical_core_count(self):
        return psutil.cpu_count(logical=False)

    def get_logical_core_count(self):
        return psutil.cpu_count(logical=True)

    def get_cpu_percent(self, interval=1):
        return psutil.cpu_percent(interval=interval)


class MemoryInfo:
    def __init__(self):
        pass

    def get_total_memory(self):
        memory = psutil.virtual_memory()
        return memory.total / (1024 ** 3)

    def get_used_memory(self):
        memory = psutil.virtual_memory()
        return memory.used / (1024 ** 3)

    def get_memory_percent(self):
        memory = psutil.virtual_memory()
        return memory.percent


class DiskInfo:
    def __init__(self, path='/'):
        self.path = path

    def get_total_disk_space(self):
        disk = psutil.disk_usage(self.path)
        return disk.total / (1024 ** 3)

    def get_used_disk_space(self):
        disk = psutil.disk_usage(self.path)
        return disk.used / (1024 ** 3)

    def get_disk_percent(self):
        disk = psutil.disk_usage(self.path)
        return disk.percent


class GPUInfo:
    def __init__(self):
        self.is_windows = platform.system() == 'Windows'
        if self.is_windows:
            self.w = wmi.WMI()
        try:
            pynvml.nvmlInit()
            self.has_nvidia_gpu = True
        except pynvml.NVMLError:
            self.has_nvidia_gpu = False

    def get_gpu_names(self):
        if self.is_windows:
            gpu_names = []
            for gpu in self.w.Win32_VideoController():
                gpu_names.append(gpu.Name)
            return gpu_names
        return []

    def get_nvidia_gpu_memory_info(self):
        if self.has_nvidia_gpu:
            device_count = pynvml.nvmlDeviceGetCount()
            gpu_memory_info = []
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                total_memory = info.total / (1024 ** 3)
                used_memory = info.used / (1024 ** 3)
                memory_percent = (used_memory / total_memory) * 100
                gpu_memory_info.append({
                    'total': total_memory,
                    'used': used_memory,
                    'percent': memory_percent
                })
            return gpu_memory_info
        return []

    def __del__(self):
        if self.has_nvidia_gpu:
            pynvml.nvmlShutdown()


class MotherboardInfo:
    def __init__(self):
        self.w = wmi.WMI()

    def get_motherboard_manufacturer(self):
        """获取主板制造商信息"""
        for board in self.w.Win32_BaseBoard():
            return board.Manufacturer
        return None

    def get_motherboard_product(self):
        """获取主板产品型号信息"""
        for board in self.w.Win32_BaseBoard():
            return board.Product
        return None

    def get_motherboard_serial_number(self):
        """获取主板序列号信息"""
        for board in self.w.Win32_BaseBoard():
            return board.SerialNumber
        return None

class NetworkAdapterInfo:
    def __init__(self):
        self.system = platform.system()
        if self.system == 'Windows':
            self.w = wmi.WMI()

    def get_network_adapter_names(self):
        if self.system == 'Windows':
            adapter_names = []
            for nic in self.w.Win32_NetworkAdapter():
                adapter_names.append(nic.Name)
            return adapter_names
        elif self.system == 'Linux':
            return list(psutil.net_if_addrs().keys())
        return []

    def get_network_adapter_mac_addresses(self):
        if self.system == 'Windows':
            mac_addresses = []
            for nic in self.w.Win32_NetworkAdapterConfiguration(IPEnabled=1):
                mac_addresses.append(nic.MACAddress)
            return mac_addresses
        elif self.system == 'Linux':
            mac_addresses = {}
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        mac_addresses[interface] = addr.address
            return mac_addresses
        return []

class ScreenInfo:
    def __init__(self):
        self.system = platform.system()

    def get_screen_count(self):
        if self.system == 'Windows':
            return win32api.GetSystemMetrics(win32con.SM_CMONITORS)
        elif self.system == 'Linux':
            try:
                output = subprocess.check_output(['xrandr', '--listmonitors']).decode('utf-8')
                lines = output.strip().split('\n')
                return len(lines) - 1
            except subprocess.CalledProcessError:
                return 0
        return 0

    def get_screen_resolutions(self):
        resolutions = []
        if self.system == 'Windows':
            for i in range(self.get_screen_count()):
                monitor_info = win32api.EnumDisplayMonitors()[i]
                monitor = win32api.GetMonitorInfo(monitor_info[0])
                left, top, right, bottom = monitor["Monitor"]
                width = right - left
                height = bottom - top
                resolutions.append((width, height))
        elif self.system == 'Linux':
            try:
                output = subprocess.check_output(['xrandr']).decode('utf-8')
                lines = output.strip().split('\n')
                for line in lines:
                    if ' connected ' in line:
                        parts = line.split()
                        for part in parts:
                            if 'x' in part:
                                try:
                                    width, height = map(int, part.split('x'))
                                    resolutions.append((width, height))
                                    break
                                except ValueError:
                                    continue
            except subprocess.CalledProcessError:
                pass
        return resolutions

import cv2

class HardwareInfo:
    def __init__(self):
        self.system = platform.system()
        if self.system == 'Windows':
            self.w = wmi.WMI()

    def get_sound_card_info(self):
        if self.system == 'Windows':
            sound_cards = []
            for sound_card in self.w.Win32_SoundDevice():
                sound_cards.append({
                    'Name': sound_card.Name,
                    'Manufacturer': sound_card.Manufacturer
                })
            return sound_cards
        elif self.system == 'Linux':
            sound_cards = []
            if os.path.exists('/proc/asound/cards'):
                with open('/proc/asound/cards', 'r') as f:
                    lines = f.readlines()
                    card_info = {}
                    for line in lines:
                        if line.startswith(' '):
                            parts = line.strip().split(':')
                            if len(parts) == 2:
                                key = parts[0].strip()
                                value = parts[1].strip()
                                if key == 'Card':
                                    card_info['Name'] = value
                                elif key == 'Driver':
                                    card_info['Driver'] = value
                        elif line.strip() == '':
                            if card_info:
                                sound_cards.append(card_info)
                                card_info = {}
                    if card_info:
                        sound_cards.append(card_info)
            return sound_cards
        return []

    def get_camera_info(self):
        if self.system == 'Windows':
            camera_indexes = []
            index = 0
            while True:
                cap = cv2.VideoCapture(index)
                if not cap.read()[0]:
                    break
                else:
                    camera_indexes.append(index)
                cap.release()
                index += 1
            return camera_indexes
        elif self.system == 'Linux':
            cameras = []
            for i in range(10):
                device_path = f'/dev/video{i}'
                if os.path.exists(device_path):
                    cameras.append(device_path)
            return cameras
        return []


demoy1 = """# CPU 信息
cpu = CPUInfo()
print(f"物理核心数: {cpu.get_physical_core_count()}")
print(f"逻辑核心数: {cpu.get_logical_core_count()}")
print(f"CPU 使用率: {cpu.get_cpu_percent()}%")

# 内存信息
memory = MemoryInfo()
print(f"总内存: {memory.get_total_memory():.2f} GB")
print(f"已使用内存: {memory.get_used_memory():.2f} GB")
print(f"内存使用率: {memory.get_memory_percent()}%")

# 磁盘信息
disk = DiskInfo()
print(f"总磁盘空间: {disk.get_total_disk_space():.2f} GB")
print(f"已使用磁盘空间: {disk.get_used_disk_space():.2f} GB")
print(f"磁盘使用率: {disk.get_disk_percent()}%")

# 显卡和显存信息
gpu = GPUInfo()
print(f"显卡名称: {gpu.get_gpu_names()}")
nvidia_gpu_memory_info = gpu.get_nvidia_gpu_memory_info()
for i, info in enumerate(nvidia_gpu_memory_info):
    print(f"NVIDIA GPU {i} 总显存: {info['total']:.2f} GB")
    print(f"NVIDIA GPU {i} 已使用显存: {info['used']:.2f} GB")
    print(f"NVIDIA GPU {i} 显存使用率: {info['percent']:.2f}%")
    
motherboard = MotherboardInfo()
print(f"主板制造商: {motherboard.get_motherboard_manufacturer()}")
print(f"主板产品型号: {motherboard.get_motherboard_product()}")
print(f"主板序列号: {motherboard.get_motherboard_serial_number()}")

network_info = NetworkAdapterInfo()
print("网卡名称:", network_info.get_network_adapter_names())
print("网卡 MAC 地址:", network_info.get_network_adapter_mac_addresses())

screen = ScreenInfo()
print(f"屏幕数量: {screen.get_screen_count()}")
print(f"屏幕分辨率: {screen.get_screen_resolutions()}")

hardware_info = HardwareInfo()
print("声卡信息:", hardware_info.get_sound_card_info())
print("摄像头信息:", hardware_info.get_camera_info())"""

import socket

class System:
    def __init__(self):
        self.system = platform.system()
        if self.system == 'Windows':
            self.w = wmi.WMI()

    def get_os_info(self):
        """获取操作系统信息"""
        os_name = platform.system()
        os_version = platform.version()
        return {
            'name': os_name,
            'version': os_version
        }

    def get_cpu_info(self):
        """获取 CPU 信息"""
        cpu_count = psutil.cpu_count(logical=False)  # 物理核心数
        cpu_count_logical = psutil.cpu_count(logical=True)  # 逻辑核心数
        cpu_percent = psutil.cpu_percent(interval=1)  # CPU 使用率
        return {
            'physical_cores': cpu_count,
            'logical_cores': cpu_count_logical,
            'usage_percent': cpu_percent
        }

    def get_memory_info(self):
        """获取内存信息"""
        memory = psutil.virtual_memory()
        total_memory = memory.total / (1024 ** 3)  # 总内存（GB）
        used_memory = memory.used / (1024 ** 3)  # 已使用内存（GB）
        memory_percent = memory.percent  # 内存使用率
        return {
            'total_gb': total_memory,
            'used_gb': used_memory,
            'usage_percent': memory_percent
        }

    def get_disk_info(self, path='/'):
        """获取磁盘信息"""
        disk = psutil.disk_usage(path)
        total_disk = disk.total / (1024 ** 3)  # 总磁盘空间（GB）
        used_disk = disk.used / (1024 ** 3)  # 已使用磁盘空间（GB）
        disk_percent = disk.percent  # 磁盘使用率
        return {
            'total_gb': total_disk,
            'used_gb': used_disk,
            'usage_percent': disk_percent
        }

    def get_network_info(self):
        """获取网络信息"""
        network_info = psutil.net_if_addrs()
        network_stats = psutil.net_io_counters()
        interfaces = []
        for interface, addrs in network_info.items():
            interface_info = {
                'name': interface,
                'addresses': []
            }
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    interface_info['addresses'].append({
                        'family': 'IPv4',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
                elif addr.family == socket.AF_INET6:
                    interface_info['addresses'].append({
                        'family': 'IPv6',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
            interfaces.append(interface_info)

        return {
            'interfaces': interfaces,
            'bytes_sent': network_stats.bytes_sent,
            'bytes_recv': network_stats.bytes_recv
        }

    def get_motherboard_info(self):
        """获取主板信息"""
        if self.system == 'Windows':
            for board in self.w.Win32_BaseBoard():
                return {
                    'manufacturer': board.Manufacturer,
                    'product': board.Product,
                    'serial_number': board.SerialNumber
                }
        elif self.system == 'Linux':
            motherboard_info = {}
            board_vendor_path = '/sys/class/dmi/id/board_vendor'
            board_name_path = '/sys/class/dmi/id/board_name'
            board_serial_path = '/sys/class/dmi/id/board_serial'

            if os.path.exists(board_vendor_path):
                with open(board_vendor_path, 'r') as f:
                    motherboard_info['manufacturer'] = f.read().strip()
            if os.path.exists(board_name_path):
                with open(board_name_path, 'r') as f:
                    motherboard_info['product'] = f.read().strip()
            if os.path.exists(board_serial_path):
                with open(board_serial_path, 'r') as f:
                    motherboard_info['serial_number'] = f.read().strip()
            return motherboard_info
        return {}

    def get_gpu_info(self):
        """获取显卡信息"""
        if self.system == 'Windows':
            gpu_names = []
            for gpu in self.w.Win32_VideoController():
                gpu_names.append(gpu.Name)
            return {
                'names': gpu_names
            }
        elif self.system == 'Linux':
            try:
                output = subprocess.check_output(['lspci']).decode('utf-8')
                gpu_names = []
                for line in output.splitlines():
                    if 'VGA compatible controller' in line:
                        parts = line.split(':')
                        gpu_names.append(parts[-1].strip())
                return {
                    'names': gpu_names
                }
            except subprocess.CalledProcessError:
                return {}
        return {}

def demoy():
    # CPU 信息
    cpu = CPUInfo()
    print(f"物理核心数: {cpu.get_physical_core_count()}")
    print(f"逻辑核心数: {cpu.get_logical_core_count()}")
    print(f"CPU 使用率: {cpu.get_cpu_percent()}%")

    # 内存信息
    memory = MemoryInfo()
    print(f"总内存: {memory.get_total_memory():.2f} GB")
    print(f"已使用内存: {memory.get_used_memory():.2f} GB")
    print(f"内存使用率: {memory.get_memory_percent()}%")

    # 磁盘信息
    disk = DiskInfo()
    print(f"总磁盘空间: {disk.get_total_disk_space():.2f} GB")
    print(f"已使用磁盘空间: {disk.get_used_disk_space():.2f} GB")
    print(f"磁盘使用率: {disk.get_disk_percent()}%")

    # 显卡和显存信息
    gpu = GPUInfo()
    print(f"显卡名称: {gpu.get_gpu_names()}")
    nvidia_gpu_memory_info = gpu.get_nvidia_gpu_memory_info()
    for i, info in enumerate(nvidia_gpu_memory_info):
        print(f"NVIDIA GPU {i} 总显存: {info['total']:.2f} GB")
        print(f"NVIDIA GPU {i} 已使用显存: {info['used']:.2f} GB")
        print(f"NVIDIA GPU {i} 显存使用率: {info['percent']:.2f}%")

    motherboard = MotherboardInfo()
    print(f"主板制造商: {motherboard.get_motherboard_manufacturer()}")
    print(f"主板产品型号: {motherboard.get_motherboard_product()}")
    print(f"主板序列号: {motherboard.get_motherboard_serial_number()}")

    network_info = NetworkAdapterInfo()
    print("网卡名称:", network_info.get_network_adapter_names())
    print("网卡 MAC 地址:", network_info.get_network_adapter_mac_addresses())

    screen = ScreenInfo()
    print(f"屏幕数量: {screen.get_screen_count()}")
    print(f"屏幕分辨率: {screen.get_screen_resolutions()}")

    hardware_info = HardwareInfo()
    print("声卡信息:", hardware_info.get_sound_card_info())
    print("摄像头信息:", hardware_info.get_camera_info())

    print("\n刚刚代码:")
    print(demoy1)

class SystemInfo:
    def __init__(self):
        self.system = platform.system()
        if self.system == 'Windows':
            self.w = wmi.WMI()
        self.detailed_system_name = self.get_detailed_system_name()

    def get_detailed_system_name(self):
        if self.system == 'Windows':
            for os_info in self.w.Win32_OperatingSystem():
                return os_info.Caption
        elif self.system == 'Linux':
            try:
                with open('/etc/os-release', 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith('PRETTY_NAME='):
                            return line.split('=')[1].strip().strip('"')
            except FileNotFoundError:
                pass
        elif self.system == 'Darwin':
            try:
                output = subprocess.check_output(['sw_vers']).decode('utf-8')
                lines = output.splitlines()
                version = None
                product_name = None
                for line in lines:
                    if line.startswith('ProductName:'):
                        product_name = line.split(':')[1].strip()
                    elif line.startswith('ProductVersion:'):
                        version = line.split(':')[1].strip()
                if product_name and version:
                    return f"{product_name} 版本: {version}"
            except subprocess.CalledProcessError:
                pass
        return None

    def __str__(self):
        if self.detailed_system_name:
            return self.detailed_system_name
        return "无法获取详细系统名。"