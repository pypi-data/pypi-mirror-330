import subprocess, os, ctypes

def factorial(n):
    """计算阶乘"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def sin(x, num_terms=10):
    """使用泰勒级数展开计算正弦函数"""
    result = 0
    for n in range(num_terms):
        term = ((-1) ** n) * (x ** (2 * n + 1)) / factorial(2 * n + 1)
        result += term
    return result

def cos(x, num_terms=10):
    """使用泰勒级数展开计算余弦函数"""
    result = 0
    for n in range(num_terms):
        term = ((-1) ** n) * (x ** (2 * n)) / factorial(2 * n)
        result += term
    return result

def tan(x, num_terms=10):
    """计算正切函数"""
    cos_value = cos(x, num_terms)
    if cos_value == 0:
        return float('inf')  # 当 cos 为 0 时，tan 为无穷大
    return sin(x, num_terms) / cos_value

def cot(x, num_terms=10):
    """计算余切函数"""
    tan_value = tan(x, num_terms)
    if tan_value == 0:
        return float('inf')  # 当 tan 为 0 时，cot 为无穷大
    return 1 / tan_value

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        real_part = self.real * other.real - self.imag * other.imag
        imag_part = self.real * other.imag + self.imag * other.real
        return ComplexNumber(real_part, imag_part)

    def __truediv__(self, other):
        denominator = other.real ** 2 + other.imag ** 2
        real_part = (self.real * other.real + self.imag * other.imag) / denominator
        imag_part = (self.imag * other.real - self.real * other.imag) / denominator
        return ComplexNumber(real_part, imag_part)

    def __str__(self):
        return f"{self.real} + {self.imag}i"
    
def sqrt(a, tolerance=1e-6, max_iterations=100):
    x = a  # 初始猜测值
    for _ in range(max_iterations):
        f = x ** 2 - a
        f_prime = 2 * x
        delta_x = f / f_prime
        x -= delta_x
        if abs(delta_x) < tolerance:
            break
    return x

def exp(x, num_terms=10):
    result = 0
    for n in range(num_terms):
        term = (x ** n) / factorial(n)
        result += term
    return result

def ln(x, tolerance=1e-6, max_iterations=100):
    y = 1  # 初始猜测值
    for _ in range(max_iterations):
        f = exp(y) - x
        f_prime = exp(y)
        delta_y = f / f_prime
        y -= delta_y
        if abs(delta_y) < tolerance:
            break
    return y

def power(x, n):
    result = 1
    if n >= 0:
        for _ in range(n):
            result *= x
    else:
        for _ in range(-n):
            result /= x
    return result

import math

def combination(n, k):
    if k > n or k < 0:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def log10(x, tolerance=1e-6, max_iterations=100):
    """
    计算以 10 为底的对数 log10(x)
    :param x: 输入值
    :param tolerance: 收敛的容差
    :param max_iterations: 最大迭代次数
    :return: log10(x) 的近似值
    """
    ln_10 = ln(10, tolerance, max_iterations)
    return ln(x, tolerance, max_iterations) / ln_10

def sinh(x, num_terms=10):
    """
    计算双曲正弦函数 sinh(x) 的近似值
    :param x: 输入值
    :param num_terms: 计算指数函数时泰勒级数展开的项数
    :return: sinh(x) 的近似值
    """
    return (exp(x, num_terms) - exp(-x, num_terms)) / 2


def cosh(x, num_terms=10):
    """
    计算双曲余弦函数 cosh(x) 的近似值
    :param x: 输入值
    :param num_terms: 计算指数函数时泰勒级数展开的项数
    :return: cosh(x) 的近似值
    """
    return (exp(x, num_terms) + exp(-x, num_terms)) / 2


def tanh(x, num_terms=10):
    """
    计算双曲正切函数 tanh(x) 的近似值
    :param x: 输入值
    :param num_terms: 计算指数函数时泰勒级数展开的项数
    :return: tanh(x) 的近似值
    """
    sinh_val = sinh(x, num_terms)
    cosh_val = cosh(x, num_terms)
    return sinh_val / cosh_val

def floor(x):
    return int(x) if x >= 0 else int(x) - 1

def absolute_value(x):
    return x if x >= 0 else -x

def combination(n, k):
    if k > n or k < 0:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def home() -> str:
    """获取用户文件夹路径"""
    if system() == "Windows":
        return os.environ.get('USERPROFILE')

    else:
        return os.path.expanduser('~')
    
def cwd():
    """get? 获取当前工作目录"""
    if system() == 'Windows':
        kernel32 = ctypes.WinDLL('kernel32')
        buffer = ctypes.create_unicode_buffer(260)
        kernel32.GetCurrentDirectoryW(260, buffer)
        return buffer.value
    else:
        libc = ctypes.CDLL(ctypes.util.find_library('c'))
        buffer = ctypes.create_string_buffer(4096)
        libc.getcwd(buffer, 4096)
        return buffer.value.decode('utf-8')
    
def system(none = None):
    """通过调用系统命令识别操作系统"""
    if none == None:
        try:
            result = subprocess.run("ver", capture_output=True, text=True, shell=True)
            if "Microsoft" in result.stdout:
                return "Windows"
            result = subprocess.run("uname", capture_output=True, text=True, shell=True)
            if "Darwin" in result.stdout:
                return "macOS"
            result = subprocess.run("uname", capture_output=True, text=True, shell=True)
            if "Linux" in result.stdout:
                return "Linux"
        except Exception as e:
            return f"发生错误: {e}"
        return "未知操作系统"
    else:
        return none
    
import win32clipboard

def ctrlc(text):
    """复制指定的内容"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()

import subprocess
import os

def dependencies(file_path):
    """
    获取指定文件的依赖项
    :param file_path: 指定文件的路径
    :return: 包含依赖项的列表
    """
    # 获取文件所在的目录
    file_dir = os.path.dirname(os.path.abspath(file_path))
    try:
        # 调用 pipreqs 生成 requirements.txt 文件
        subprocess.run(['pipreqs', file_dir, '--force'], check=True)

        # 读取 requirements.txt 文件内容
        requirements_file = os.path.join(file_dir, 'requirements.txt')
        if os.path.exists(requirements_file):
            with open(requirements_file, 'r', encoding='utf-8') as f:
                dependencies = f.read().splitlines()
            # 删除生成的 requirements.txt 文件
            os.remove(requirements_file)
            return dependencies
        else:
            #print("未生成 requirements.txt 文件，请检查 pipreqs 运行是否正常。")
            return []
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        return []
    except Exception as e:
        print(f"ERROR: {e}")
        return []