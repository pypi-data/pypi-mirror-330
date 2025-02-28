import sys
import threading
import platform
import subprocess
from .hyyaps import CommunicationResult

class HPopen:
    def __init__(self, args, shell=False, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        if shell:
            if platform.system() == 'Windows':
                shell_cmd = ['cmd', '/c'] + args
            else:
                shell_cmd = ['sh', '-c'] + args
            args = shell_cmd

        self.args = args
        self.stdout_data = []
        self.stderr_data = []
        self.process = None
        self._start_process()

    def _start_process(self):
        try:
            self.process = subprocess.Popen(
                self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )

            self.stdout_thread = threading.Thread(target=self._read_output, args=(self.process.stdout, self.stdout_data))
            self.stderr_thread = threading.Thread(target=self._read_output, args=(self.process.stderr, self.stderr_data))
            self.stdout_thread.start()
            self.stderr_thread.start()
        except Exception as e:
            print(f"Error starting process: {e}", file=sys.stderr)

    def _read_output(self, stream, data_list):
        try:
            encoding = 'gbk' if platform.system() == 'Windows' else 'utf-8'
            for line in iter(stream.readline, b''):
                try:
                    decoded_line = line.decode(encoding)
                except UnicodeDecodeError:
                    try:
                        decoded_line = line.decode('utf-8', errors='replace')
                    except UnicodeDecodeError:
                        continue
                data_list.append(decoded_line)
        except Exception as e:
            print(f"Error reading output: {e}", file=sys.stderr)
        finally:
            stream.close()

    def communicate(self, input_data=None):
        if self.process is None:
            return CommunicationResult("", f"Process failed to start: {self.args}", 1)

        if input_data:
            if isinstance(input_data, str):
                input_data = input_data.encode()
            self.process.stdin.write(input_data)
            self.process.stdin.flush()
        if self.process.stdin:
            self.process.stdin.close()

        if self.stdout_thread:
            self.stdout_thread.join()
        if self.stderr_thread:
            self.stderr_thread.join()

        if self.process:
            self.process.wait()
            status = self.process.returncode
            stdout_str = ''.join(self.stdout_data)
            stderr_str = ''.join(self.stderr_data)
            return CommunicationResult(stdout_str, stderr_str, status)
        return CommunicationResult("", "Process is None", 1)

    def wait(self):
        if self.process:
            self.process.wait()
            return self.process.returncode
        return 1


class _Ap_Popen:
    def __init__(self, args, shell=False, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        if shell:
            if platform.system() == 'Windows':
                shell_cmd = ['cmd', '/c'] + args
            else:
                shell_cmd = ['sh', '-c'] + args
            args = shell_cmd

        self.args = args
        self.stdout_data = []
        self.stderr_data = []
        self.process = None
        self._start_process()

    def _start_process(self):
        try:
            self.process = subprocess.Popen(
                self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )

            self.stdout_thread = threading.Thread(target=self._read_output, args=(self.process.stdout, self.stdout_data))
            self.stderr_thread = threading.Thread(target=self._read_output, args=(self.process.stderr, self.stderr_data))
            self.stdout_thread.start()
            self.stderr_thread.start()
        except Exception as e:
            print(f"Error starting process: {e}", file=sys.stderr)

    def _read_output(self, stream, data_list):
        try:
            encoding = 'gbk' if platform.system() == 'Windows' else 'utf-8'
            for line in iter(stream.readline, b''):
                try:
                    decoded_line = line.decode(encoding)
                except UnicodeDecodeError:
                    try:
                        decoded_line = line.decode('utf-8', errors='replace')
                    except UnicodeDecodeError:
                        continue
                data_list.append(decoded_line)
        except Exception as e:
            print(f"Error reading output: {e}", file=sys.stderr)
        finally:
            stream.close()

    def communicate(self, input_data=None):
        if self.process is None:
            return CommunicationResult("", f"Process failed to start: {self.args}", 1)

        if input_data:
            if isinstance(input_data, str):
                input_data = input_data.encode()
            self.process.stdin.write(input_data)
            self.process.stdin.flush()
        if self.process.stdin:
            self.process.stdin.close()

        if self.stdout_thread:
            self.stdout_thread.join()
        if self.stderr_thread:
            self.stderr_thread.join()

        if self.process:
            self.process.wait()
            status = self.process.returncode
            stdout_str = ''.join(self.stdout_data)
            stderr_str = ''.join(self.stderr_data)
            return CommunicationResult(stdout_str, stderr_str, status)
        return CommunicationResult("", "Process is None", 1)

    def wait(self):
        if self.process:
            self.process.wait()
            return self.process.returncode
        return 1