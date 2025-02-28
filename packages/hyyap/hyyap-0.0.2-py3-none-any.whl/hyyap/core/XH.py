import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import html
import requests


class Xmlhtml:
    def __init__(self, xml_content=None, html_content=None):
        """
        初始化类，可传入 XML 或 HTML 内容
        :param xml_content: XML 内容
        :param html_content: HTML 内容
        """
        self.xml_content = xml_content
        self.html_content = html_content
        if self.xml_content:
            self.xml_root = ET.fromstring(self.xml_content)
        else:
            self.xml_root = None

    def get_xml_info(self):
        """
        从 XML 中提取信息并返回
        :return: 包含 XML 信息的列表
        """
        if not self.xml_content:
            return []
        info = []

        def traverse(element):
            info.append((element.tag, element.text))
            for child in element:
                traverse(child)

        traverse(self.xml_root)
        return info

    def xml_to_html(self):
        """
        将 XML 转换为 HTML
        :return: 转换后的 HTML 内容
        """
        if not self.xml_content:
            return ""
        html_parts = []

        def build_html(element):
            tag = element.tag
            text = element.text or ""
            html_parts.append(f"<{tag}>")
            html_parts.append(html.escape(text))
            for child in element:
                build_html(child)
            html_parts.append(f"</{tag}>")

        build_html(self.xml_root)
        return ''.join(html_parts)

    def html_to_xml(self):
        """
        将 HTML 转换为 XML
        :return: 转换后的 XML 内容
        """
        if not self.html_content:
            return ""
        soup = BeautifulSoup(self.html_content, 'html.parser')
        xml_parts = []

        def build_xml(element):
            tag = element.name
            text = element.get_text()
            xml_parts.append(f"<{tag}>")
            xml_parts.append(html.escape(text))
            for child in element.children:
                if isinstance(child, BeautifulSoup):
                    continue
                build_xml(child)
            xml_parts.append(f"</{tag}>")

        build_xml(soup)
        return ''.join(xml_parts)

    def find_elements_by_tag(self, tag):
        """
        根据标签名查找 XML 中的元素
        :param tag: 要查找的标签名
        :return: 包含匹配元素的列表
        """
        if not self.xml_content:
            return []
        return self.xml_root.findall(f'.//{tag}')

    def modify_element_text(self, tag, new_text):
        """
        修改指定标签元素的文本内容
        :param tag: 要修改的标签名
        :param new_text: 新的文本内容
        :return: 修改后的 XML 字符串
        """
        if not self.xml_content:
            return ""
        elements = self.xml_root.findall(f'.//{tag}')
        for element in elements:
            element.text = new_text
        self.xml_content = ET.tostring(self.xml_root, encoding='unicode')
        return self.xml_content

    def delete_elements_by_tag(self, tag):
        """
        根据标签名删除 XML 中的元素
        :param tag: 要删除的标签名
        :return: 删除元素后的 XML 字符串
        """
        if not self.xml_content:
            return ""
        for parent in self.xml_root.findall('.//*'):
            for element in parent.findall(tag):
                parent.remove(element)
        self.xml_content = ET.tostring(self.xml_root, encoding='unicode')
        return self.xml_content

    def save_xml(self, file_path):
        """
        将 XML 数据保存到指定文件
        :param file_path: 保存文件的路径
        """
        if self.xml_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.xml_content)
        else:
            print("没有可用的 XML 数据进行保存。")

    def load_xml(self, file_path):
        """
        从指定文件加载 XML 数据
        :param file_path: 加载文件的路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.xml_content = file.read()
                self.xml_root = ET.fromstring(self.xml_content)
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到。")
        except ET.ParseError:
            print(f"无法解析 {file_path} 中的 XML 数据。")

    def load_xml_from_url(self, url):
        """
        从指定 URL 加载 XML 文件
        :param url: XML 文件的 URL
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.xml_content = response.text
            self.xml_root = ET.fromstring(self.xml_content)
        except requests.RequestException as e:
            print(f"请求 URL {url} 时出现错误: {e}")
        except ET.ParseError:
            print(f"无法解析从 {url} 获取的 XML 数据。")

    def load_html_from_url(self, url):
        """
        从指定 URL 加载 HTML 文件
        :param url: HTML 文件的 URL
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.html_content = response.text
        except requests.RequestException as e:
            print(f"请求 URL {url} 时出现错误: {e}")

