import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, KnowledgeNode


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_create_node(self):
        node = KnowledgeNode(title="测试节点", content="测试内容", category="测试分类", tags="标签1,标签2")
        self.db.add(node)
        self.db.commit()
        
        self.assertIsNotNone(node.id)
        self.assertEqual(node.title, "测试节点")
        self.assertEqual(node.content, "测试内容")
        self.assertEqual(node.category, "测试分类")
        self.assertEqual(node.tags, "标签1,标签2")
        self.assertIsNotNone(node.create_time)

    def test_query_node(self):
        node = KnowledgeNode(title="查询测试", content="查询内容")
        self.db.add(node)
        self.db.commit()
        
        queried = self.db.query(KnowledgeNode).filter_by(id=node.id).first()
        self.assertIsNotNone(queried)
        self.assertEqual(queried.title, "查询测试")

    def test_update_node(self):
        node = KnowledgeNode(title="更新测试", content="原始内容")
        self.db.add(node)
        self.db.commit()
        
        node.title = "更新后的标题"
        node.content = "更新后的内容"
        node.category = "新分类"
        self.db.commit()
        
        updated = self.db.query(KnowledgeNode).filter_by(id=node.id).first()
        self.assertEqual(updated.title, "更新后的标题")
        self.assertEqual(updated.content, "更新后的内容")
        self.assertEqual(updated.category, "新分类")

    def test_delete_node(self):
        node = KnowledgeNode(title="删除测试", content="删除内容")
        self.db.add(node)
        self.db.commit()
        node_id = node.id
        
        self.db.delete(node)
        self.db.commit()
        
        deleted = self.db.query(KnowledgeNode).filter_by(id=node_id).first()
        self.assertIsNone(deleted)

    def test_list_nodes(self):
        for i in range(5):
            node = KnowledgeNode(title=f"节点{i}", content=f"内容{i}", category="测试")
            self.db.add(node)
        self.db.commit()
        
        nodes = self.db.query(KnowledgeNode).all()
        self.assertEqual(len(nodes), 5)

    def test_node_with_embedding(self):
        import numpy as np
        import io
        
        vec = np.random.randn(384).astype(np.float32)
        buf = io.BytesIO()
        np.save(buf, vec)
        emb = buf.getvalue()
        
        node = KnowledgeNode(title="带向量节点", content="内容", embedding=emb)
        self.db.add(node)
        self.db.commit()
        
        queried = self.db.query(KnowledgeNode).filter_by(id=node.id).first()
        self.assertIsNotNone(queried.embedding)
        self.assertEqual(len(queried.embedding), len(emb))

    def test_node_default_values(self):
        node = KnowledgeNode(title="标题")
        self.db.add(node)
        self.db.commit()
        
        self.assertEqual(node.content, "")
        self.assertEqual(node.category, "")
        self.assertEqual(node.tags, "")
        self.assertIsNone(node.embedding)


if __name__ == "__main__":
    unittest.main()
