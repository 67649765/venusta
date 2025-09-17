import pytest
import requests
import json

BASE_URL = "http://localhost:8000"

@pytest.fixture
def test_paper():
    """创建测试试卷作为fixture"""
    # 生成试卷
    generate_url = f"{BASE_URL}/exams/generate"
    payload = {
        "grade": "junior",
        "subject": "math",
        "chapter": "quadratic",
        "knowledge_points": ["graph_properties"],
        "item_type_ratio": {"single_choice": 1, "subjective": 1},
        "difficulty": 3,
        "num_items": 2
    }
    response = requests.post(generate_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "paper_id" in data
    assert "item_ids" in data
    return data

def test_health():
    """测试健康检查接口"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_dashboard_metrics():
    """测试仪表板指标接口"""
    url = f"{BASE_URL}/dashboard/metrics"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "responses" in data
    assert "kappa" in data
    assert "mae" in data

def test_grading(test_paper):
    """测试评分接口"""
    paper_id = test_paper["paper_id"]
    item_id = test_paper["item_ids"][0]
    
    url = f"{BASE_URL}/grading/grade"
    payload = {
        "user_id": 1,
        "paper_id": paper_id,
        "item_id": item_id,
        "answer": "2",
        "steps": ["axis", "vertex"]
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data

def test_diagnosis(test_paper):
    """测试诊断接口"""
    paper_id = test_paper["paper_id"]
    
    url = f"{BASE_URL}/diagnosis"
    payload = {
        "user_id": 1,
        "paper_id": paper_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200

def test_review(test_paper):
    """测试讲评接口"""
    paper_id = test_paper["paper_id"]
    
    url = f"{BASE_URL}/review"
    payload = {
        "user_id": 1,
        "paper_id": paper_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200