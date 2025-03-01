from .apopen import HPopen, _Ap_Popen
import time


def run(command, shell=False):
    """
    在 cmd 或 shell 中执行命令
    :param command: 要执行的命令，以列表形式传入
    :param shell: 是否使用 shell 执行命令，默认为 False
    :return: CommunicationResult 对象，包含标准输出、标准错误和退出状态码
    """
    process = _Ap_Popen(command, shell=shell)
    return process.communicate()
    

class RunTime:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.start = time.time()
        return cls._instance

    @property
    def time(self):
        return time.time() - self.start
    
Runtime = RunTime()