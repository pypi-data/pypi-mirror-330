class HBytes:
    """
    filebytes = TxBytes("path/to/your/whl.whl","utf-8").getbytes() -> 获取指定文件的bytes.
    TxBytes("path/to/your/whl.whl","utf-8").bytestofile("Output_folder",filebytes) -> 将指定的bytes还原成文件.
    """
    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.encoding = encoding
        try:
            if self._is_binary_file():
                with open(self.file_path, 'rb') as file:
                    self.bytes_data = file.read()
            else:
                with open(self.file_path, 'r', encoding=self.encoding) as file:
                    text_data = file.read()
                    self.bytes_data = text_data.encode(self.encoding)
        except FileNotFoundError:
            print(f"未找到指定的文件: {self.file_path}")
            self.bytes_data = None
        except UnicodeDecodeError:
            print(f"读取文件时发生编码错误，可能指定的编码 {self.encoding} 不正确。")
            self.bytes_data = None
        except Exception as e:
            print(f"ERROR: {e}")
            self.bytes_data = None

    def _is_binary_file(self):
        """简单判断文件是否为二进制文件"""
        with open(self.file_path, 'rb') as file:
            head = file.read(1024)
            return b'\0' in head

    def __str__(self):
        if self.bytes_data is not None:
            return str(self.bytes_data)
        return "无法获取文件的字节数据。"

    def getbytes(self):
        return self.bytes_data

    def bytestofile(self, output_file_path, bytes_content=None):
        if bytes_content is None:
            bytes_content = self.bytes_data
        if bytes_content is None:
            print("没有有效的字节数据可供写入文件。")
            return
        try:
            if self._is_binary_file():
                with open(output_file_path, 'wb') as file:
                    file.write(bytes_content)
            else:
                text_data = bytes_content.decode(self.encoding)
                with open(output_file_path, 'w', encoding=self.encoding) as file:
                    file.write(text_data)
            #print(f"成功将字节数据写入文件: {output_file_path}")
        except UnicodeDecodeError:
            print(f"写入文件时发生编码错误，可能指定的编码 {self.encoding} 不正确。")
        except Exception as e:
            print(f"ERROR: {e}")
