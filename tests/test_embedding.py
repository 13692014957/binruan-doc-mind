import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import text_to_embedding, _batch_text_to_embeddings, bytes_to_vector
import numpy as np


class TestEmbedding(unittest.TestCase):

    def test_text_to_embedding_basic(self):
        emb = text_to_embedding("测试标题", "测试内容")
        self.assertIsNotNone(emb)
        self.assertIsInstance(emb, bytes)
        self.assertGreater(len(emb), 0)

    def test_text_to_embedding_empty(self):
        emb = text_to_embedding("", "")
        self.assertIsNone(emb)

    def test_text_to_embedding_empty_title(self):
        emb = text_to_embedding("", "测试内容")
        self.assertIsNotNone(emb)

    def test_text_to_embedding_empty_content(self):
        emb = text_to_embedding("测试标题", "")
        self.assertIsNotNone(emb)

    def test_bytes_to_vector(self):
        emb = text_to_embedding("测试标题", "测试内容")
        vec = bytes_to_vector(emb)
        self.assertIsNotNone(vec)
        self.assertIsInstance(vec, np.ndarray)
        self.assertEqual(vec.ndim, 1)
        self.assertEqual(vec.shape[0], 384)

    def test_batch_text_to_embeddings_basic(self):
        texts = ["测试文本1", "测试文本2", "测试文本3"]
        embeddings = _batch_text_to_embeddings(texts)
        
        self.assertEqual(len(embeddings), 3)
        for emb in embeddings:
            self.assertIsNotNone(emb)
            self.assertIsInstance(emb, bytes)

    def test_batch_text_to_embeddings_with_empty(self):
        texts = ["测试文本1", "", "测试文本3", "   ", None]
        embeddings = _batch_text_to_embeddings(texts)
        
        self.assertEqual(len(embeddings), 5)
        self.assertIsNotNone(embeddings[0])
        self.assertIsNone(embeddings[1])
        self.assertIsNotNone(embeddings[2])
        self.assertIsNone(embeddings[3])
        self.assertIsNone(embeddings[4])

    def test_batch_text_to_embeddings_empty_list(self):
        embeddings = _batch_text_to_embeddings([])
        self.assertEqual(embeddings, [])

    def test_batch_text_to_embeddings_single(self):
        texts = ["单个测试文本"]
        embeddings = _batch_text_to_embeddings(texts)
        
        self.assertEqual(len(embeddings), 1)
        self.assertIsNotNone(embeddings[0])


if __name__ == "__main__":
    unittest.main()
