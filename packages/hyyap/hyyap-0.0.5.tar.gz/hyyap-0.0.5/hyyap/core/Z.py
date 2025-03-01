import os
import zipfile
import gzip
import tarfile
import bz2


class CompressionHandler:
    def __init__(self, format):
        """format:压缩格式,仅支持'zip', 'gz', 'tar', 'bz2'."""
        self.format = format.lower()
        if self.format not in ['zip', 'gz', 'tar', 'bz2']:
            raise ValueError("不支持的压缩格式。支持的格式有：zip, gz, tar, bz2")

    def compress(self, source, destination):
        """压缩文件"""
        if self.format == 'zip':
            with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source):
                    zipf.write(source)
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            zipf.write(os.path.join(root, file))
        elif self.format == 'gz':
            with open(source, 'rb') as f_in, gzip.open(destination, 'wb') as f_out:
                f_out.writelines(f_in)
        elif self.format == 'tar':
            with tarfile.open(destination, 'w') as tar:
                if os.path.isfile(source):
                    tar.add(source)
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            tar.add(os.path.join(root, file))
        elif self.format == 'bz2':
            with open(source, 'rb') as f_in, bz2.open(destination, 'wb') as f_out:
                f_out.writelines(f_in)

    def decompress(self, source, destination):
        """解压文件"""
        if self.format == 'zip':
            with zipfile.ZipFile(source, 'r') as zipf:
                zipf.extractall(destination)
        elif self.format == 'gz':
            with gzip.open(source, 'rb') as f_in, open(destination, 'wb') as f_out:
                f_out.writelines(f_in)
        elif self.format == 'tar':
            with tarfile.open(source, 'r') as tar:
                tar.extractall(destination)
        elif self.format == 'bz2':
            with bz2.open(source, 'rb') as f_in, open(destination, 'wb') as f_out:
                f_out.writelines(f_in)