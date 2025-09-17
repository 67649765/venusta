import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import execute, fetchall

def seed_sample_questions():
    # 检查items表是否已存在
    tables = fetchall("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='items'")
    
    if not tables:
        # 创建items表
        execute('''
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            grade TEXT,
            subject TEXT,
            chapter TEXT,
            knowledge_points JSONB,
            item_type TEXT,
            difficulty INTEGER,
            content TEXT,
            answer TEXT,
            analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建papers表
        execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            grade TEXT,
            subject TEXT,
            chapter TEXT,
            knowledge_points JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建responses表
        execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            paper_id INTEGER,
            item_id INTEGER,
            answer TEXT,
            steps TEXT[],
            score FLOAT,
            judge_meta JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建diagnosis表
        execute('''
        CREATE TABLE IF NOT EXISTS diagnosis (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            paper_id INTEGER,
            heatmap JSONB,
            error_dist JSONB,
            recommendations JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建review表
        execute('''
        CREATE TABLE IF NOT EXISTS review (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            paper_id INTEGER,
            review_content JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
    # 插入样例题目
    sample_items = [
        {
            "grade": "初中",
            "subject": "数学",
            "chapter": "二次函数",
            "knowledge_points": ["图像性质"],
            "item_type": "single_choice",
            "difficulty": 3,
            "content": "二次函数y=x²+2x+1的顶点坐标是？",
            "answer": "2",
            "analysis": "顶点坐标公式为(-b/2a, f(-b/2a))，代入a=1, b=2得顶点坐标为(-1, 0)"
        },
        {
            "grade": "初中",
            "subject": "数学",
            "chapter": "二次函数",
            "knowledge_points": ["图像性质"],
            "item_type": "subjective",
            "difficulty": 4,
            "content": "请描述二次函数y=x²-4x+3的开口方向、对称轴和顶点坐标。",
            "answer": "开口向上，对称轴为x=2，顶点坐标为(2, -1)",
            "analysis": "因为a=1>0，所以开口向上；对称轴为x=-b/2a=4/2=2；顶点纵坐标为f(2)=4-8+3=-1"
        }
    ]
    
    for item in sample_items:
        execute(
            "INSERT INTO items (grade, subject, chapter, knowledge_points, item_type, difficulty, content, answer, analysis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                item["grade"],
                item["subject"],
                item["chapter"],
                json.dumps(item["knowledge_points"]),
                item["item_type"],
                item["difficulty"],
                item["content"],
                item["answer"],
                item["analysis"]
            )
        )
    
    print("Seeded sample items.")

if __name__ == "__main__":
    seed_sample_questions()