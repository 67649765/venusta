import os, json
import psycopg
from psycopg.rows import dict_row

conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB","venusta"),
    user=os.getenv("POSTGRES_USER","venusta"),
    password=os.getenv("POSTGRES_PASSWORD","venusta"),
    host=os.getenv("POSTGRES_HOST","db"),   # 容器内连接 DB 用服务名
    port=os.getenv("POSTGRES_PORT","5432"),
    autocommit=True,
    row_factory=dict_row,
)

items = [
    {
        "grade":"初中","subject":"数学","chapter":"二次函数","knowledge_points":["图像性质","顶点坐标"],
        "item_type":"single_choice",
        "stem":"已知抛物线 y=ax^2+bx+c 的对称轴为 x=2，则顶点横坐标为（ ）。",
        "options":["-2","0","1","2"], "answer":"2", "solution":"对称轴 x=-b/(2a)=2 → 顶点横坐标为 2", "difficulty":2
    },
    {
        "grade":"初中","subject":"数学","chapter":"二次函数","knowledge_points":["实际应用","单位换算"],
        "item_type":"subjective",
        "stem":"一物体竖直上抛的高度(米)关于时间(秒)的函数为 h(t)=-5t^2+20t。求 1≤t≤3 内的最大高度，并说明过程。",
        "answer":"最大高度为 20 米",
        "solution":"抛物线开口向下，顶点 t=-b/(2a)=2，高度 h(2)=-5*4+40=20m",
        "difficulty":3
    }
]

with conn.cursor() as cur:
    for it in items:
        cur.execute(
            "INSERT INTO items (grade,subject,chapter,knowledge_points,item_type,stem,options,answer,solution,difficulty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (it["grade"],it["subject"],it["chapter"],it["knowledge_points"],it["item_type"],it["stem"],it.get("options"),it.get("answer"),it.get("solution"),it["difficulty"])
        )
print("Seeded sample items.")