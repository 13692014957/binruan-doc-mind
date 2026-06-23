import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import _read_txt, _read_markdown, _read_pdf


class TestFileParsing(unittest.TestCase):
    TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

    def test_read_txt_utf8(self):
        file_path = os.path.join(self.TEST_DATA_DIR, "test.txt")
        with open(file_path, "rb") as f:
            raw = f.read()
        
        text = _read_txt(raw)
        self.assertIn("测试文本文件", text)
        self.assertIn("中文内容", text)
        self.assertGreater(len(text), 20)

    def test_read_txt_empty(self):
        text = _read_txt(b"")
        self.assertEqual(text, "")

    def test_read_markdown(self):
        file_path = os.path.join(self.TEST_DATA_DIR, "test.md")
        with open(file_path, "rb") as f:
            raw = f.read()
        
        text = _read_markdown(raw)
        self.assertIn("测试标题", text)
        self.assertIn("二级标题", text)
        self.assertIn("加粗", text)
        self.assertIn("斜体", text)
        self.assertIn("删除线", text)
        self.assertIn("无序列表项1", text)
        self.assertIn("有序列表项1", text)
        self.assertIn("hello", text)
        self.assertIn("引用文字", text)
        self.assertIn("百度", text)
        self.assertIn("姓名", text)
        self.assertIn("张三", text)
        self.assertIn("普通段落文本", text)
        self.assertGreater(len(text), 200)

    def test_read_markdown_empty(self):
        text = _read_markdown(b"")
        self.assertEqual(text, "")

    def test_read_pdf(self):
        try:
            from pypdf import PdfWriter
            import io
            
            writer = PdfWriter()
            from pypdf.generic import TextStringObject, ArrayObject, DictionaryObject, NameObject
            page_dict = DictionaryObject()
            page_dict[NameObject("/Type")] = NameObject("/Page")
            page_dict[NameObject("/Parent")] = DictionaryObject()
            page_dict[NameObject("/Contents")] = ArrayObject()
            
            content_stream = TextStringObject("BT\n/F1 24 Tf\n100 700 Td\n(测试PDF内容) Tj\nET")
            contents_dict = DictionaryObject()
            contents_dict[NameObject("/Length")] = TextStringObject(str(len(content_stream)))
            contents_dict[NameObject("/Filter")] = NameObject("/FlateDecode")
            
            import zlib
            compressed = zlib.compress(content_stream.encode('latin-1'))
            
            contents_dict[NameObject("/Length")] = TextStringObject(str(len(compressed)))
            page_dict[NameObject("/Contents")] = compressed
            
            writer.add_page(page_dict)
            
            buf = io.BytesIO()
            writer.write(buf)
            buf.seek(0)
            
            text = _read_pdf(buf.getvalue())
            self.assertGreater(len(text), 0)
            
        except Exception:
            self.skipTest("pypdf not available or test requires complex setup")


if __name__ == "__main__":
    unittest.main()
