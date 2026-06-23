import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import _import_put, _import_get, _import_del, _import_cleanup_expired


class TestImportSession(unittest.TestCase):

    def setUp(self):
        _import_cleanup_expired()

    def test_import_put_get(self):
        import_id = "test_import_123"
        payload = {"candidates": [], "file_name": "test.txt"}
        
        _import_put(import_id, payload)
        
        result = _import_get(import_id)
        self.assertIsNotNone(result)
        self.assertEqual(result["candidates"], [])
        self.assertEqual(result["file_name"], "test.txt")

    def test_import_get_nonexistent(self):
        result = _import_get("nonexistent_id")
        self.assertIsNone(result)

    def test_import_delete(self):
        import_id = "test_delete_123"
        payload = {"candidates": [], "file_name": "test.txt"}
        
        _import_put(import_id, payload)
        result = _import_get(import_id)
        self.assertIsNotNone(result)
        
        _import_del(import_id)
        result = _import_get(import_id)
        self.assertIsNone(result)

    def test_import_cleanup_expired(self):
        import_id = "test_expired_123"
        payload = {"candidates": [], "file_name": "test.txt"}
        
        _import_put(import_id, payload)
        self.assertIsNotNone(_import_get(import_id))
        
        _import_cleanup_expired()


class TestImportWorkflow(unittest.TestCase):

    def setUp(self):
        _import_cleanup_expired()

    @patch('main.call_llm_chat')
    def test_import_flow_mocked(self, mock_llm):
        mock_llm.return_value = '[{"title": "测试节点", "content": "测试内容", "category": "测试", "tags": ["标签1"]}]'
        
        import_id = "test_flow_123"
        payload = {
            "candidates": [],
            "file_name": "test.txt",
            "raw_text": "测试文本内容"
        }
        _import_put(import_id, payload)
        
        result = _import_get(import_id)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
