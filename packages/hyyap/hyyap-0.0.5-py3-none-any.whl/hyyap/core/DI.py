import ctypes
from ctypes import wintypes
from PIL import Image
import io


class DLLImageProcessor:
    def __init__(self, dll_path, resource_name='IMAGE_NAME', resource_type='PNG', output_path='processed_image.png'):
        self.dll_path = dll_path
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.output_path = output_path

        # 定义 Windows API 函数
        self.LoadLibrary = ctypes.windll.kernel32.LoadLibraryW
        self.LoadLibrary.argtypes = [wintypes.LPCWSTR]
        self.LoadLibrary.restype = wintypes.HMODULE

        self.FindResource = ctypes.windll.kernel32.FindResourceW
        self.FindResource.argtypes = [wintypes.HMODULE, wintypes.LPCWSTR, wintypes.LPCWSTR]
        self.FindResource.restype = wintypes.HRSRC

        self.SizeofResource = ctypes.windll.kernel32.SizeofResource
        self.SizeofResource.argtypes = [wintypes.HMODULE, wintypes.HRSRC]
        self.SizeofResource.restype = wintypes.DWORD

        self.LoadResource = ctypes.windll.kernel32.LoadResource
        self.LoadResource.argtypes = [wintypes.HMODULE, wintypes.HRSRC]
        self.LoadResource.restype = wintypes.HGLOBAL

        self.LockResource = ctypes.windll.kernel32.LockResource
        self.LockResource.argtypes = [wintypes.HGLOBAL]
        self.LockResource.restype = ctypes.c_void_p

    def extract_image_from_dll(self):
        # 加载 DLL 文件
        hModule = self.LoadLibrary(self.dll_path)
        if hModule == 0:
            print("Failed to load DLL.")
            return None

        # 查找图片资源
        hResInfo = self.FindResource(hModule, self.resource_name, self.resource_type)
        if hResInfo == 0:
            print("Failed to find resource.")
            return None

        # 获取资源大小
        resource_size = self.SizeofResource(hModule, hResInfo)

        # 加载资源
        hGlobal = self.LoadResource(hModule, hResInfo)

        # 锁定资源
        lpResource = self.LockResource(hGlobal)

        # 读取资源数据
        resource_data = ctypes.string_at(lpResource, resource_size)

        return resource_data

    def process_and_save_image(self, image_data, resize=None, convert_to_gray=False):
        try:
            # 将二进制数据转换为 Pillow 的 Image 对象
            image = Image.open(io.BytesIO(image_data))

            # 调整图片大小
            if resize:
                image = image.resize(resize, Image.Resampling.LANCZOS)

            # 转换为灰度图
            if convert_to_gray:
                image = image.convert('L')

            # 保存图片
            image.save(self.output_path)
            print(f"Image saved to {self.output_path}")
        except Exception as e:
            print(f"Error processing or saving image: {e}")

    def run(self, resize=None, convert_to_gray=False):
        # 提取图片数据
        image_data = self.extract_image_from_dll()
        if image_data:
            # 处理并保存图片
            self.process_and_save_image(image_data, resize=resize, convert_to_gray=convert_to_gray)