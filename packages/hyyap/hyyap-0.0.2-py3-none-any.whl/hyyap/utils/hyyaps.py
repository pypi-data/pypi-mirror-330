from .apopen import HPopen, _Ap_Popen

class CommunicationResult:
    def __init__(self, stdout, stderr, status):
        self.stdout = stdout
        self.stderr = stderr
        self.status = status


def run(command, shell=False):
    """
    在 cmd 或 shell 中执行命令
    :param command: 要执行的命令，以列表形式传入
    :param shell: 是否使用 shell 执行命令，默认为 False
    :return: CommunicationResult 对象，包含标准输出、标准错误和退出状态码
    """
    process = _Ap_Popen(command, shell=shell)
    return process.communicate()


def _Gethyyaps(Get,*code):
    """Get"""
    if Get == "exit":
        return exit(code)
    
    if Get == "quit":
        return quit(code)

    def exit(code):
        SystemExit(code)

    def quit(code):
        SystemExit(code)