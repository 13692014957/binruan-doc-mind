import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db, Base


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        
        def override_get_db():
            try:
                db = self.Session()
                yield db
            finally:
                db.close()
        
        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_node(self):
        response = self.client.post(
            "/api/nodes",
            json={"title": "API测试节点", "content": "API测试内容", "category": "测试"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "API测试节点")
        self.assertEqual(data["content"], "API测试内容")
        self.assertEqual(data["category"], "测试")
        self.assertIn("id", data)

    def test_list_nodes(self):
        self.client.post("/api/nodes", json={"title": "节点1", "content": "内容1"})
        self.client.post("/api/nodes", json={"title": "节点2", "content": "内容2"})
        
        response = self.client.get("/api/nodes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_get_node(self):
        create_response = self.client.post("/api/nodes", json={"title": "查询节点", "content": "查询内容"})
        node_id = create_response.json()["id"]
        
        response = self.client.get(f"/api/nodes/{node_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], node_id)
        self.assertEqual(data["title"], "查询节点")

    def test_update_node(self):
        create_response = self.client.post("/api/nodes", json={"title": "更新节点", "content": "原始内容"})
        node_id = create_response.json()["id"]
        
        response = self.client.put(
            f"/api/nodes/{node_id}",
            json={"title": "更新后节点", "content": "更新后内容", "category": "新分类"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "更新后节点")
        self.assertEqual(data["content"], "更新后内容")
        self.assertEqual(data["category"], "新分类")

    def test_delete_node(self):
        create_response = self.client.post("/api/nodes", json={"title": "删除节点", "content": "删除内容"})
        node_id = create_response.json()["id"]
        
        response = self.client.delete(f"/api/nodes/{node_id}")
        self.assertEqual(response.status_code, 200)
        
        get_response = self.client.get(f"/api/nodes/{node_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_get_categories(self):
        self.client.post("/api/nodes", json={"title": "节点1", "content": "内容1", "category": "分类A"})
        self.client.post("/api/nodes", json={"title": "节点2", "content": "内容2", "category": "分类B"})
        self.client.post("/api/nodes", json={"title": "节点3", "content": "内容3", "category": "分类A"})
        
        response = self.client.get("/api/categories")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("分类A", data)
        self.assertIn("分类B", data)

    def test_import_upload_invalid_file(self):
        with open("tests/test_data/test.txt", "rb") as f:
            response = self.client.post("/api/import/upload", files={"file": ("test.invalid", f)})
        self.assertEqual(response.status_code, 400)

    def test_import_upload_txt(self):
        with open("tests/test_data/test.txt", "rb") as f:
            response = self.client.post("/api/import/upload", files={"file": ("test.txt", f)})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("import_id", data)

    def test_import_upload_md(self):
        with open("tests/test_data/test.md", "rb") as f:
            response = self.client.post("/api/import/upload", files={"file": ("test.md", f)})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("import_id", data)


if __name__ == "__main__":
    unittest.main()
