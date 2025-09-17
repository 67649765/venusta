-- 创建数据库扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 创建items表
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    grade TEXT NOT NULL,
    subject TEXT NOT NULL,
    chapter TEXT NOT NULL,
    knowledge_points JSONB NOT NULL,
    item_type TEXT NOT NULL,
    stem TEXT NOT NULL,
    options JSONB,
    answer TEXT,
    solution TEXT,
    difficulty INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建papers表
CREATE TABLE IF NOT EXISTS papers (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL DEFAULT 'Auto Paper',
    teacher_id INTEGER NOT NULL DEFAULT 1,
    user_id INTEGER,
    grade TEXT,
    subject TEXT,
    chapter TEXT,
    knowledge_points JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建paper_items表（试卷题目关系表）
CREATE TABLE IF NOT EXISTS paper_items (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    UNIQUE (paper_id, item_id)
);

-- 创建responses表
CREATE TABLE IF NOT EXISTS responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    paper_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    steps TEXT[],
    score FLOAT NOT NULL,
    judge_meta JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);

-- 创建diagnosis表
CREATE TABLE IF NOT EXISTS diagnosis (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    paper_id INTEGER NOT NULL,
    heatmap JSONB NOT NULL,
    error_dist JSONB NOT NULL,
    recommendations JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id)
);

-- 创建review表
CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    paper_id INTEGER NOT NULL,
    review_content JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id)
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_items_grade_subject ON items(grade, subject);
CREATE INDEX IF NOT EXISTS idx_items_knowledge_points ON items USING GIN(knowledge_points);
CREATE INDEX IF NOT EXISTS idx_papers_user_id ON papers(user_id);
CREATE INDEX IF NOT EXISTS idx_responses_user_paper ON responses(user_id, paper_id);
CREATE INDEX IF NOT EXISTS idx_diagnosis_user_paper ON diagnosis(user_id, paper_id);
CREATE INDEX IF NOT EXISTS idx_review_user_paper ON review(user_id, paper_id);

-- 赋予权限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO venusta;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO venusta;