"""SQLite storage: schema + connection helper."""
import os
import sqlite3

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    salt TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student','teacher','parent')),
    language TEXT NOT NULL DEFAULT 'en',
    parent_email TEXT,                 -- students only: the one parent allowed to see their data
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions(
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS parent_links(
    parent_id INTEGER NOT NULL REFERENCES users(id),
    student_id INTEGER NOT NULL REFERENCES users(id),
    PRIMARY KEY(parent_id, student_id)
);
CREATE TABLE IF NOT EXISTS classes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK(grade BETWEEN 6 AND 10),
    subject TEXT NOT NULL,
    join_code TEXT NOT NULL UNIQUE,
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS enrollments(
    class_id INTEGER NOT NULL REFERENCES classes(id),
    student_id INTEGER NOT NULL REFERENCES users(id),
    joined_at INTEGER NOT NULL,
    PRIMARY KEY(class_id, student_id)
);
CREATE TABLE IF NOT EXISTS topics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade INTEGER NOT NULL CHECK(grade BETWEEN 6 AND 10),
    subject TEXT NOT NULL,
    name TEXT NOT NULL,
    prereq_id INTEGER REFERENCES topics(id),   -- earlier concept this topic builds on
    UNIQUE(grade, subject, name)
);
CREATE TABLE IF NOT EXISTS lessons(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    language TEXT NOT NULL DEFAULT 'en',
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    UNIQUE(topic_id, language)
);
CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    difficulty INTEGER NOT NULL CHECK(difficulty BETWEEN 1 AND 3),
    language TEXT NOT NULL DEFAULT 'en',
    text TEXT NOT NULL,
    options TEXT NOT NULL,              -- JSON list of strings
    correct_index INTEGER NOT NULL,
    hint TEXT DEFAULT '',
    explanation TEXT DEFAULT '',
    created_by INTEGER REFERENCES users(id),
    active INTEGER NOT NULL DEFAULT 1,  -- soft delete keeps answer history valid
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS tests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER REFERENCES classes(id),
    title TEXT NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at INTEGER NOT NULL,
    time_limit_min INTEGER,             -- NULL = untimed
    deadline INTEGER                    -- epoch seconds, NULL = no deadline
);
CREATE TABLE IF NOT EXISTS test_starts(
    test_id INTEGER NOT NULL REFERENCES tests(id),
    student_id INTEGER NOT NULL REFERENCES users(id),
    started_at INTEGER NOT NULL,
    PRIMARY KEY(test_id, student_id)
);
CREATE TABLE IF NOT EXISTS test_questions(
    test_id INTEGER NOT NULL REFERENCES tests(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    PRIMARY KEY(test_id, question_id)
);
CREATE TABLE IF NOT EXISTS test_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL REFERENCES tests(id),
    student_id INTEGER NOT NULL REFERENCES users(id),
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    taken_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS answers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES users(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    chosen INTEGER NOT NULL,
    is_correct INTEGER NOT NULL,
    test_id INTEGER REFERENCES tests(id),
    attempt_id TEXT,                    -- stops double-clicks counting twice
    answered_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS progress(
    student_id INTEGER NOT NULL REFERENCES users(id),
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    attempts INTEGER NOT NULL DEFAULT 0,
    correct INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 2,   -- current adaptive difficulty
    streak INTEGER NOT NULL DEFAULT 0,
    mastery REAL NOT NULL DEFAULT 0.5,  -- estimated chance the student has mastered the topic
    updated_at INTEGER NOT NULL,
    PRIMARY KEY(student_id, topic_id)
);
CREATE TABLE IF NOT EXISTS materials(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL REFERENCES classes(id),
    kind TEXT NOT NULL CHECK(kind IN ('lecture','note','practice','test')),
    title TEXT NOT NULL,
    body TEXT DEFAULT '',
    topic_id INTEGER REFERENCES topics(id),
    test_id INTEGER REFERENCES tests(id),
    file_name TEXT,
    file_path TEXT,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_answers_student ON answers(student_id);
CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic_id, difficulty);
"""


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    for table, col, typ in (("users", "parent_email", "TEXT"), ("topics", "prereq_id", "INTEGER"),
                            ("answers", "attempt_id", "TEXT"), ("materials", "file_name", "TEXT"),
                            ("materials", "file_path", "TEXT"), ("tests", "time_limit_min", "INTEGER"),
                            ("tests", "deadline", "INTEGER"), ("progress", "mastery", "REAL NOT NULL DEFAULT 0.5")):   # upgrade older databases
        if col not in [r["name"] for r in conn.execute(f"PRAGMA table_info({table})")]:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_answer_attempt ON answers(student_id, attempt_id)"
                 " WHERE attempt_id IS NOT NULL")
    conn.commit()
    conn.close()
