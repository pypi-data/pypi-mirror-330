from fontTools.ttLib import TTFont, TTCollection
from fontTools.subset import Subsetter, Options
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen


class TTFFontHandler:
    def __init__(self, path):
        """
        初始化 TTFFontHandler 类，加载指定路径的 .ttf 字体文件。

        :param path: .ttf 字体文件的路径
        """
        self.path = path
        self.font = None
        try:
            self.font = TTFont(path)
        except Exception as e:
            print(f"加载 .ttf 字体文件出错: {e}")

    def info(self):
        """获取 .ttf 字体基本信息"""
        if self.font:
            try:
                name = self.font['name'].getName(4, 3, 1, 1033).toUnicode()
                glyph_count = len(self.font.getGlyphSet())
                return name, glyph_count
            except Exception as e:
                print(f"获取 .ttf 字体信息出错: {e}")
        return None, None

    def unicodes(self, num=10):
        """获取 .ttf 字体前 num 个字符 Unicode 编码"""
        if self.font:
            try:
                unicodes = []
                for table in self.font['cmap'].tables:
                    for code, _ in table.cmap.items():
                        unicodes.append(code)
                return unicodes[:num]
            except Exception as e:
                print(f"获取 .ttf 字体 Unicode 编码出错: {e}")
        return []

    def mod_copyright(self, new_copyright):
        """修改 .ttf 字体版权信息"""
        if self.font:
            try:
                for record in self.font['name'].names:
                    if record.nameID == 0:
                        record.string = new_copyright.encode('utf-16-be')
                self.font.save(self.path)
                return True
            except Exception as e:
                print(f"修改 .ttf 字体版权信息出错: {e}")
        return False

    def subset(self, output_path, unicodes):
        """对 .ttf 字体进行子集化"""
        if self.font:
            try:
                options = Options()
                subsetter = Subsetter(options=options)
                subsetter.populate(unicodes=unicodes)
                subsetter.subset(self.font)
                self.font.save(output_path)
                return True
            except Exception as e:
                print(f"子集化 .ttf 字体出错: {e}")
        return False

    def units_per_em(self):
        """获取 .ttf 字体每 em 单位数"""
        if self.font:
            try:
                return self.font['head'].unitsPerEm
            except Exception as e:
                print(f"获取 .ttf 每 em 单位数出错: {e}")
        return None

    def ascender(self):
        """获取 .ttf 字体上伸部高度"""
        if self.font:
            try:
                return self.font['hhea'].ascender
            except Exception as e:
                print(f"获取 .ttf 上伸部高度出错: {e}")
        return None

    def descender(self):
        """获取 .ttf 字体下伸部高度"""
        if self.font:
            try:
                return self.font['hhea'].descender
            except Exception as e:
                print(f"获取 .ttf 下伸部高度出错: {e}")
        return None

    def line_gap(self):
        """获取 .ttf 字体行间距"""
        if self.font:
            try:
                return self.font['hhea'].lineGap
            except Exception as e:
                print(f"获取 .ttf 行间距出错: {e}")
        return None

    def glyph_width(self, glyph_name):
        """获取 .ttf 字体指定字形宽度"""
        if self.font:
            try:
                return self.font['hmtx'][glyph_name][0]
            except Exception as e:
                print(f"获取 .ttf 字形宽度出错: {e}")
        return None

    def glyph_height(self, glyph_name):
        """获取 .ttf 字体指定字形高度"""
        if self.font:
            try:
                glyph_set = self.font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                bounds = pen.value.getBounds()
                if bounds:
                    return bounds[3] - bounds[1]
            except Exception as e:
                print(f"获取 .ttf 字形高度出错: {e}")
        return None

    def glyph_bbox(self, glyph_name):
        """获取 .ttf 字体指定字形边界框"""
        if self.font:
            try:
                glyph_set = self.font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                return pen.value.getBounds()
            except Exception as e:
                print(f"获取 .ttf 字形边界框出错: {e}")
        return None

    def scale_glyph(self, glyph_name, scale_x, scale_y, output_path):
        """缩放 .ttf 字体指定字形"""
        if self.font:
            try:
                glyph_set = self.font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                transform = (scale_x, 0, 0, scale_y, 0, 0)
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                new_glyph = glyph_set.fromPen(tpen.value)
                self.font['glyf'][glyph_name] = new_glyph
                self.font.save(output_path)
                return True
            except Exception as e:
                print(f"缩放 .ttf 字形出错: {e}")
        return False

    def skew_glyph(self, glyph_name, skew_x, skew_y, output_path):
        """倾斜 .ttf 字体指定字形"""
        if self.font:
            try:
                glyph_set = self.font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                transform = (1, skew_x, skew_y, 1, 0, 0)
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                new_glyph = glyph_set.fromPen(tpen.value)
                self.font['glyf'][glyph_name] = new_glyph
                self.font.save(output_path)
                return True
            except Exception as e:
                print(f"倾斜 .ttf 字形出错: {e}")
        return False

    def move_glyph(self, glyph_name, dx, dy, output_path):
        """平移 .ttf 字体指定字形"""
        if self.font:
            try:
                glyph_set = self.font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                transform = (1, 0, 0, 1, dx, dy)
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                new_glyph = glyph_set.fromPen(tpen.value)
                self.font['glyf'][glyph_name] = new_glyph
                self.font.save(output_path)
                return True
            except Exception as e:
                print(f"平移 .ttf 字形出错: {e}")
        return False

    def set_version(self, version):
        """设置 .ttf 字体版本号"""
        if self.font:
            try:
                self.font['head'].fontRevision = float(version)
                self.font.save(self.path)
                return True
            except Exception as e:
                print(f"设置 .ttf 版本号出错: {e}")
        return False

    def get_version(self):
        """获取 .ttf 字体版本号"""
        if self.font:
            try:
                return self.font['head'].fontRevision
            except Exception as e:
                print(f"获取 .ttf 版本号出错: {e}")
        return None

    def set_mac_style(self, bold=False, italic=False):
        """设置 .ttf 字体 Mac 样式"""
        if self.font:
            try:
                mac_style = 0
                if bold:
                    mac_style |= 1
                if italic:
                    mac_style |= 2
                self.font['head'].macStyle = mac_style
                self.font.save(self.path)
                return True
            except Exception as e:
                print(f"设置 .ttf Mac 样式出错: {e}")
        return False

    def get_mac_style(self):
        """获取 .ttf 字体 Mac 样式"""
        if self.font:
            try:
                return self.font['head'].macStyle
            except Exception as e:
                print(f"获取 .ttf Mac 样式出错: {e}")
        return None

    def set_fs_selection(self, bold=False, italic=False, underline=False):
        """设置 .ttf 字体 fsSelection 字段"""
        if self.font:
            try:
                fs_selection = 0
                if bold:
                    fs_selection |= 0x01
                if italic:
                    fs_selection |= 0x02
                if underline:
                    fs_selection |= 0x04
                self.font['OS/2'].fsSelection = fs_selection
                self.font.save(self.path)
                return True
            except Exception as e:
                print(f"设置 .ttf fsSelection 字段出错: {e}")
        return False

    def get_fs_selection(self):
        """获取 .ttf 字体 fsSelection 字段"""
        if self.font:
            try:
                return self.font['OS/2'].fsSelection
            except Exception as e:
                print(f"获取 .ttf fsSelection 字段出错: {e}")
        return None

    def close(self):
        """关闭 .ttf 字体文件"""
        if self.font:
            self.font.close()


class TTCFontHandler:
    def __init__(self, path):
        """
        初始化 TTCFontHandler 类，加载指定路径的 .ttc 字体集合文件。

        :param path: .ttc 字体集合文件的路径
        """
        self.path = path
        self.ttc = None
        try:
            self.ttc = TTCollection(path)
        except Exception as e:
            print(f"加载 .ttc 字体集合文件出错: {e}")

    def names(self):
        """
        获取 .ttc 字体集合中各字体名称。

        :return: 包含各字体名称的列表，出错则返回空列表
        """
        if self.ttc:
            try:
                return [font['name'].getName(4, 3, 1, 1033).toUnicode() for font in self.ttc.fonts]
            except Exception as e:
                print(f"获取 .ttc 字体名称出错: {e}")
        return []

    def extract(self, index=0, output_path='extracted_font.ttf'):
        """
        从 .ttc 中提取指定索引字体保存为 .ttf。

        :param index: 要提取的字体索引，默认为 0
        :param output_path: 提取后保存的 .ttf 文件路径，默认为 'extracted_font.ttf'
        :return: 提取成功返回 True，失败返回 False
        """
        if self.ttc:
            try:
                if 0 <= index < len(self.ttc.fonts):
                    self.ttc.fonts[index].save(output_path)
                    return True
                print("索引超出 .ttc 字体集合范围")
            except Exception as e:
                print(f"提取 .ttc 字体出错: {e}")
        return False

    def info(self, index=0):
        """
        获取 .ttc 中指定索引字体基本信息。

        :param index: 字体索引，默认为 0
        :return: 包含字体名称和字符集数量的元组，出错则返回 (None, None)
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                name = font['name'].getName(4, 3, 1, 1033).toUnicode()
                glyph_count = len(font.getGlyphSet())
                return name, glyph_count
            except Exception as e:
                print(f"获取 .ttc 字体信息出错: {e}")
        return None, None

    def unicodes(self, index=0, num=10):
        """
        获取 .ttc 中指定索引字体前 num 个字符 Unicode 编码。

        :param index: 字体索引，默认为 0
        :param num: 要获取的字符数量，默认为 10
        :return: 包含前 num 个字符 Unicode 编码的列表，出错则返回空列表
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                unicodes = []
                for table in font['cmap'].tables:
                    for code, _ in table.cmap.items():
                        unicodes.append(code)
                return unicodes[:num]
            except Exception as e:
                print(f"获取 .ttc 字体 Unicode 编码出错: {e}")
        return []

    def mod_copyright(self, index=0, new_copyright=""):
        """
        修改 .ttc 中指定索引字体版权信息。

        :param index: 字体索引，默认为 0
        :param new_copyright: 新的版权信息
        :return: 修改成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                for record in font['name'].names:
                    if record.nameID == 0:
                        record.string = new_copyright.encode('utf-16-be')
                font.save(self.path)
                return True
            except Exception as e:
                print(f"修改 .ttc 字体版权信息出错: {e}")
        return False

    def subset(self, index=0, output_path='subset_font.ttf', unicodes=[]):
        """
        对 .ttc 中指定索引字体进行子集化。

        :param index: 字体索引，默认为 0
        :param output_path: 子集化后保存的 .ttf 文件路径，默认为 'subset_font.ttf'
        :param unicodes: 要保留的 Unicode 字符列表
        :return: 子集化成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                options = Options()
                subsetter = Subsetter(options=options)
                subsetter.populate(unicodes=unicodes)
                subsetter.subset(font)
                font.save(output_path)
                return True
            except Exception as e:
                print(f"子集化 .ttc 字体出错: {e}")
        return False

    def units_per_em(self, index=0):
        """
        获取 .ttc 中指定索引字体每 em 单位数。

        :param index: 字体索引，默认为 0
        :return: 每 em 单位数，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['head'].unitsPerEm
            except Exception as e:
                print(f"获取 .ttc 每 em 单位数出错: {e}")
        return None

    def ascender(self, index=0):
        """
        获取 .ttc 中指定索引字体上伸部高度。

        :param index: 字体索引，默认为 0
        :return: 上伸部高度，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['hhea'].ascender
            except Exception as e:
                print(f"获取 .ttc 上伸部高度出错: {e}")
        return None

    def descender(self, index=0):
        """
        获取 .ttc 中指定索引字体下伸部高度。

        :param index: 字体索引，默认为 0
        :return: 下伸部高度，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['hhea'].descender
            except Exception as e:
                print(f"获取 .ttc 下伸部高度出错: {e}")
        return None

    def line_gap(self, index=0):
        """
        获取 .ttc 中指定索引字体行间距。

        :param index: 字体索引，默认为 0
        :return: 行间距，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['hhea'].lineGap
            except Exception as e:
                print(f"获取 .ttc 行间距出错: {e}")
        return None

    def glyph_width(self, index=0, glyph_name=""):
        """
        获取 .ttc 中指定索引字体指定字形宽度。

        :param index: 字体索引，默认为 0
        :param glyph_name: 字形名称
        :return: 字形宽度，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['hmtx'][glyph_name][0]
            except Exception as e:
                print(f"获取 .ttc 字形宽度出错: {e}")
        return None

    def glyph_height(self, index=0, glyph_name=""):
        """
        获取 .ttc 中指定索引字体指定字形高度。

        :param index: 字体索引，默认为 0
        :param glyph_name: 字形名称
        :return: 字形高度，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                glyph_set = font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                bounds = pen.value.getBounds()
                if bounds:
                    return bounds[3] - bounds[1]
            except Exception as e:
                print(f"获取 .ttc 字形高度出错: {e}")
        return None

    def glyph_bbox(self, index=0, glyph_name=""):
        """
        获取 .ttc 中指定索引字体指定字形边界框。

        :param index: 字体索引，默认为 0
        :param glyph_name: 字形名称
        :return: 字形边界框，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                glyph_set = font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                return pen.value.getBounds()
            except Exception as e:
                print(f"获取 .ttc 字形边界框出错: {e}")
        return None

    def scale_glyph(self, index=0, glyph_name="", scale_x=1, scale_y=1, output_path='scaled_font.ttf'):
        """
        缩放 .ttc 中指定索引字体指定字形。

        :param index: 字体索引，默认为 0
        :param glyph_name: 字形名称
        :param scale_x: x 方向缩放比例，默认为 1
        :param scale_y: y 方向缩放比例，默认为 1
        :param output_path: 处理后保存的 .ttf 文件路径，默认为 'scaled_font.ttf'
        :return: 缩放成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                glyph_set = font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                transform = (scale_x, 0, 0, scale_y, 0, 0)
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                new_glyph = glyph_set.fromPen(tpen.value)
                font['glyf'][glyph_name] = new_glyph
                font.save(output_path)
                return True
            except Exception as e:
                print(f"缩放 .ttc 字形出错: {e}")
        return False

    def skew_glyph(self, index=0, glyph_name="", skew_x=0, skew_y=0, output_path='skewed_font.ttf'):
        """
        倾斜 .ttc 中指定索引字体指定字形。

        :param index: 字体索引，默认为 0
        :param glyph_name: 字形名称
        :param skew_x: x 方向倾斜比例，默认为 0
        :param skew_y: y 方向倾斜比例，默认为 0
        :param output_path: 处理后保存的 .ttf 文件路径，默认为 'skewed_font.ttf'
        :return: 倾斜成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                glyph_set = font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                transform = (1, skew_x, skew_y, 1, 0, 0)
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                new_glyph = glyph_set.fromPen(tpen.value)
                font['glyf'][glyph_name] = new_glyph
                font.save(output_path)
                return True
            except Exception as e:
                print(f"倾斜 .ttc 字形出错: {e}")
        return False

    def move_glyph(self, index=0, glyph_name="", dx=0, dy=0, output_path='moved_font.ttf'):
        """
        平移 .ttc 中指定索引字体指定字形。

        :param index: 字体索引，默认为 0
        :param glyph_name: 字形名称
        :param dx: x 方向平移量，默认为 0
        :param dy: y 方向平移量，默认为 0
        :param output_path: 处理后保存的 .ttf 文件路径，默认为 'moved_font.ttf'
        :return: 平移成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                glyph_set = font.getGlyphSet()
                glyph = glyph_set[glyph_name]
                pen = RecordingPen()
                glyph.draw(pen)
                transform = (1, 0, 0, 1, dx, dy)
                tpen = TransformPen(pen, transform)
                glyph.draw(tpen)
                new_glyph = glyph_set.fromPen(tpen.value)
                font['glyf'][glyph_name] = new_glyph
                font.save(output_path)
                return True
            except Exception as e:
                print(f"平移 .ttc 字形出错: {e}")
        return False

    def set_version(self, index=0, version=1.0):
        """
        设置 .ttc 中指定索引字体版本号。

        :param index: 字体索引，默认为 0
        :param version: 版本号，默认为 1.0
        :return: 设置成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                font['head'].fontRevision = float(version)
                font.save(self.path)
                return True
            except Exception as e:
                print(f"设置 .ttc 版本号出错: {e}")
        return False

    def version(self, index=0):
        """
        获取 .ttc 中指定索引字体版本号。

        :param index: 字体索引，默认为 0
        :return: 版本号，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['head'].fontRevision
            except Exception as e:
                print(f"获取 .ttc 版本号出错: {e}")
        return None

    def mac_style(self, index=0, bold=False, italic=False):
        """
        设置 .ttc 中指定索引字体 Mac 样式。

        :param index: 字体索引，默认为 0
        :param bold: 是否为粗体，默认为 False
        :param italic: 是否为斜体，默认为 False
        :return: 设置成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                mac_style = 0
                if bold:
                    mac_style |= 1
                if italic:
                    mac_style |= 2
                font['head'].macStyle = mac_style
                font.save(self.path)
                return True
            except Exception as e:
                print(f"设置 .ttc Mac 样式出错: {e}")
        return False

    def mac_style(self, index=0):
        """
        获取 .ttc 中指定索引字体 Mac 样式。

        :param index: 字体索引，默认为 0
        :return: Mac 样式，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['head'].macStyle
            except Exception as e:
                print(f"获取 .ttc Mac 样式出错: {e}")
        return None

    def fs_selection(self, index=0, bold=False, italic=False, underline=False):
        """
        设置 .ttc 中指定索引字体的 fsSelection 字段。

        :param index: 字体在 .ttc 集合中的索引，默认为 0
        :param bold: 是否设置为粗体，默认为 False
        :param italic: 是否设置为斜体，默认为 False
        :param underline: 是否设置有下划线，默认为 False
        :return: 设置成功返回 True，失败返回 False
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                font = self.ttc.fonts[index]
                fs_selection = 0
                if bold:
                    fs_selection |= 0x01
                if italic:
                    fs_selection |= 0x02
                if underline:
                    fs_selection |= 0x04
                font['OS/2'].fsSelection = fs_selection
                font.save(self.path)
                return True
            except Exception as e:
                print(f"设置 .ttc 字体 fsSelection 字段出错: {e}")
        return False

    def fs_selection(self, index=0):
        """
        获取 .ttc 中指定索引字体的 fsSelection 字段。

        :param index: 字体在 .ttc 集合中的索引，默认为 0
        :return: fsSelection 字段的值，出错则返回 None
        """
        if self.ttc and 0 <= index < len(self.ttc.fonts):
            try:
                return self.ttc.fonts[index]['OS/2'].fsSelection
            except Exception as e:
                print(f"获取 .ttc 字体 fsSelection 字段出错: {e}")
        return None

    def close(self):
        """
        关闭相关资源，尝试释放可能占用的资源。
        """
        try:

            if self.ttc:
                self.ttc = None
        except Exception as e:
            print(f"Error: {e}")
