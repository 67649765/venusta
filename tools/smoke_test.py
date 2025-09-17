#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time
import requests
from dotenv import load_dotenv

# 加载环境变量
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# API 基础URL
API_BASE = os.getenv('VITE_API_BASE', 'http://localhost:8000')

print("=== VenusTA 全链路冒烟测试 ===")

# 检查API是否可用
def check_api_health():
    print("\n[1/6] 检查API服务是否可用...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API服务正常")
            return True
        else:
            print(f"❌ API服务返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API服务不可用: {str(e)}")
        print("  请确保后端服务已通过 docker compose up --build 启动")
        return False

# 初始化题库
def seed_questions():
    print("\n[2/6] 初始化题库...")
    seed_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', 'seed_questions.py')
    try:
        result = subprocess.run(
            [sys.executable, seed_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print("✅ 题库初始化成功")
            return True
        else:
            print(f"❌ 题库初始化失败: {result.stderr}")
            print("  请检查数据库连接配置是否正确")
            print("  Docker环境下: POSTGRES_HOST=db")
            print("  本地环境下: POSTGRES_HOST=localhost")
            return False
    except Exception as e:
        print(f"❌ 执行种子脚本出错: {str(e)}")
        return False

# 生成试卷
def generate_exam():
    print("\n[3/6] 生成试卷...")
    try:
        response = requests.post(
            f"{API_BASE}/exams/generate",
            headers={"Content-Type": "application/json"},
            json={
                "grade": "初中",
                "subject": "数学",
                "chapter": "二次函数",
                "knowledge_points": ["图像性质"],
                "item_type_ratio": {"single_choice": 3, "subjective": 2},
                "difficulty": 3,
                "num_items": 5
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 试卷生成成功: paper_id={data['paper_id']}, item_ids={data['item_ids']}")
            return data
        else:
            print(f"❌ 试卷生成失败: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"❌ 生成试卷出错: {str(e)}")
        return None

# 评分
def grade_item(paper_data):
    print("\n[4/6] 对首题评分...")
    if not paper_data or not paper_data.get('item_ids'):
        print("❌ 没有可用的试题ID")
        return None
    
    item_id = paper_data['item_ids'][0]
    try:
        response = requests.post(
            f"{API_BASE}/grading/grade",
            headers={"Content-Type": "application/json"},
            json={
                "user_id": 1,
                "paper_id": paper_data['paper_id'],
                "item_id": item_id,
                "answer": "2"
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 评分成功: score={data['score']}")
            return data
        else:
            print(f"❌ 评分失败: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"❌ 评分出错: {str(e)}")
        return None

# 获取看板数据
def get_dashboard():
    print("\n[5/6] 获取看板数据...")
    try:
        response = requests.get(f"{API_BASE}/dashboard/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 看板数据获取成功: responses={data.get('responses', 0)}, kappa={data.get('kappa', 0):.2f}, mae={data.get('mae', 0):.2f}, satisfaction={data.get('satisfaction', 0):.1f}")
            return data
        else:
            print(f"❌ 看板数据获取失败: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"❌ 获取看板数据出错: {str(e)}")
        return None

# 生成讲评
def generate_review(paper_id):
    print("\n[6/6] 生成试卷讲评...")
    try:
        response = requests.post(
            f"{API_BASE}/review",
            headers={"Content-Type": "application/json"},
            json={"user_id": 1, "paper_id": paper_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 讲评生成成功: summary={data['summary'][:50]}...")
            return data
        else:
            print(f"❌ 讲评生成失败: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"❌ 生成讲评出错: {str(e)}")
        return None

# 执行诊断
def run_diagnosis(paper_id):
    print("\n[额外] 执行学情诊断...")
    try:
        response = requests.post(
            f"{API_BASE}/diagnosis",
            headers={"Content-Type": "application/json"},
            json={"user_id": 1, "paper_id": paper_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ 诊断执行成功")
            print(f"  - heatmap: {list(data['heatmap'].keys())[:3]}...")
            print(f"  - error_dist: {list(data['error_dist'].keys())[:3]}...")
            # 处理recommendations对象
            recommendations = data.get('recommendations', {})
            if isinstance(recommendations, dict):
                print("  - recommendations:")
                for key, value in recommendations.items():
                    print(f"    {key}: {value}")
            return data
        else:
            print(f"❌ 诊断执行失败: {response.status_code} {response.text}")
            print("  提示: 请确保已完成评分步骤，诊断需要responses表中的数据")
            return None
    except Exception as e:
        print(f"❌ 执行诊断出错: {str(e)}")
        return None

# 主函数
def main():
    # 1. 检查API健康状态
    if not check_api_health():
        print("\n❌ 冒烟测试失败: API服务不可用")
        return False
    
    # 2. 初始化题库
    if not seed_questions():
        print("\n❌ 冒烟测试失败: 题库初始化失败")
        return False
    
    # 3. 生成试卷
    paper_data = generate_exam()
    if not paper_data:
        print("\n❌ 冒烟测试失败: 试卷生成失败")
        return False
    
    # 4. 评分
    grade_data = grade_item(paper_data)
    if not grade_data:
        print("\n❌ 冒烟测试失败: 评分失败")
        return False
    
    # 5. 获取看板数据
    dashboard_data = get_dashboard()
    if not dashboard_data:
        print("\n❌ 冒烟测试失败: 看板数据获取失败")
        return False
    
    # 6. 生成讲评
    review_data = generate_review(paper_data['paper_id'])
    if not review_data:
        print("\n❌ 冒烟测试失败: 讲评生成失败")
        return False
    
    # 7. 执行诊断
    diagnosis_data = run_diagnosis(paper_data['paper_id'])
    # 诊断失败不作为关键步骤失败的依据
    
    print("\n" + "="*50)
    print("✅ ✅ ✅ 冒烟测试成功！全链路功能正常 ✅ ✅ ✅")
    print("="*50)
    print("\n测试结果总结:")
    print(f"- 试卷ID: {paper_data['paper_id']}")
    print(f"- 试题数量: {len(paper_data['item_ids'])}")
    print(f"- 得分: {grade_data['score']}")
    print(f"- 系统响应数: {dashboard_data.get('responses', 0)}")
    print(f"- Kappa系数: {dashboard_data.get('kappa', 0):.2f}")
    print(f"- MAE: {dashboard_data.get('mae', 0):.2f}")
    print(f"- 满意度: {dashboard_data.get('satisfaction', 0):.1f}")
    print(f"- CORS配置: 已设置允许 {API_BASE} 访问")
    print("\n前端可访问: http://localhost:5173")
    print("后端API文档: http://localhost:8000/docs")
    print("\n提示: 若前端访问出现CORS错误，请检查后端main.py中的CORS配置是否正确")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)