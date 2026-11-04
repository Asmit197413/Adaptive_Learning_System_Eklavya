"""API endpoints. Each handler gets a Request and returns data or (status, data)."""
import json
import os
import random
import re
import secrets
import string
import time

import engine
from auth import ApiError, create_session, hash_password, verify_password
from config import GRADES, MATERIAL_KINDS, ROLES, UPLOAD_DIR

ROUTES = []


class Request:
    def __init__(self, conn, user, body, query, params, raw=b""):
        self.conn, self.user, self.body, self.query, self.params, self.raw = conn, user, body, query, params, raw


def route(method, path, auth=True):
    pattern = re.compile(
        "^" + re.sub(r"\{(\w+)\}", lambda m: "(?P<%s>\\d+)" % m.group(1), path) + "$")

    def deco(fn):
        ROUTES.append((method, pattern, fn, auth))
        return fn
    return deco


# ---------------------------------------------------------------- helpers
def now():
    return int(time.time())


def need(body, *fields):
    missing = [f for f in fields if body.get(f) in (None, "")]
    if missing:
        raise ApiError(400, "Missing field(s): " + ", ".join(missing))


def require_role(req, *roles):
    if req.user["role"] not in roles:
        raise ApiError(403, "Only " + "/".join(roles) + " can do this")


def to_int(value, name):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ApiError(400, f"{name} must be a number")


def public_user(u):
    return {k: u[k] for k in ("id", "name", "email", "role", "language")}


def q_public(row, reveal=False):
    d = {"id": row["id"], "topic_id": row["topic_id"], "difficulty": row["difficulty"],
         "language": row["language"], "text": row["text"], "options": json.loads(row["options"])}
    if reveal:
        d.update(correct_index=row["correct_index"], hint=row["hint"], explanation=row["explanation"])
    return d


def get_or_404(conn, table, row_id, label):
    row = conn.execute(f"SELECT * FROM {table} WHERE id=?", (row_id,)).fetchone()
    if not row:
        raise ApiError(404, f"{label} not found")
    return row


def own_class(req, class_id):
    cls = get_or_404(req.conn, "classes", class_id, "Class")
    if cls["teacher_id"] != req.user["id"]:
        raise ApiError(403, "This is not your class")
    return cls


def class_access(req, class_id):
    """Teacher owner or enrolled student may open a class."""
    cls = get_or_404(req.conn, "classes", class_id, "Class")
    u = req.user
    if u["role"] == "teacher" and cls["teacher_id"] == u["id"]:
        return cls
    if u["role"] == "student" and req.conn.execute(
            "SELECT 1 FROM enrollments WHERE class_id=? AND student_id=?", (class_id, u["id"])).fetchone():
        return cls
    raise ApiError(403, "No access to this class")


def can_view_student(conn, user, sid):
    if user["id"] == sid:
        return True
    if user["role"] == "teacher":
        return bool(conn.execute(
            "SELECT 1 FROM enrollments e JOIN classes c ON c.id=e.class_id"
            " WHERE e.student_id=? AND c.teacher_id=?", (sid, user["id"])).fetchone())
    if user["role"] == "parent":
        return bool(conn.execute(
            "SELECT 1 FROM users WHERE id=? AND role='student' AND parent_email=?", (sid, user["email"])).fetchone())
    return False


def target_student(req):
    """Student whose data is requested: self for students, ?student_id= for teacher/parent."""
    if req.query.get("student_id"):
        sid = to_int(req.query["student_id"], "student_id")
    elif req.user["role"] == "student":
        sid = req.user["id"]
    else:
        raise ApiError(400, "student_id is required")
    if not can_view_student(req.conn, req.user, sid):
        raise ApiError(403, "You cannot view this student")
    student = req.conn.execute("SELECT * FROM users WHERE id=? AND role='student'", (sid,)).fetchone()
    if not student:
        raise ApiError(404, "Student not found")
    return student


# ---------------------------------------------------------------- auth
@route("POST", "/api/register", auth=False)
def register(req):
    b = req.body
    need(b, "name", "email", "password", "role")
    if b["role"] not in ROLES:
        raise ApiError(400, "role must be one of: " + ", ".join(ROLES))
    if len(b["password"]) < 6:
        raise ApiError(400, "Password must be at least 6 characters")
    email = b["email"].strip().lower()
    if req.conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
        raise ApiError(409, "Email already registered")
    parent_email = None
    if b["role"] == "student":   # a student must name the one parent who may see their progress
        need(b, "parent_email")
        parent_email = b["parent_email"].strip().lower()
        if "@" not in parent_email or parent_email == email:
            raise ApiError(400, "Enter your parent's email address")
    salt, digest = hash_password(b["password"])
    cur = req.conn.execute(
        "INSERT INTO users(name,email,salt,password_hash,role,language,parent_email,created_at) VALUES(?,?,?,?,?,?,?,?)",
        (b["name"].strip(), email, salt, digest, b["role"], b.get("language", "en"), parent_email, now()))
    uid = cur.lastrowid
    user = req.conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    return 201, {"token": create_session(req.conn, uid), "user": public_user(user)}


@route("POST", "/api/login", auth=False)
def login(req):
    need(req.body, "email", "password")
    u = req.conn.execute("SELECT * FROM users WHERE email=?",
                         (req.body["email"].strip().lower(),)).fetchone()
    if not u or not verify_password(req.body["password"], u["salt"], u["password_hash"]):
        raise ApiError(401, "Wrong email or password")
    return {"token": create_session(req.conn, u["id"]), "user": public_user(u)}


@route("GET", "/api/me")
def me(req):
    return public_user(req.user)


@route("PUT", "/api/me/language")
def set_language(req):
    need(req.body, "language")
    if req.body["language"] not in ("en", "hi", "bn"):
        raise ApiError(400, "Supported languages: en, hi, bn")
    req.conn.execute("UPDATE users SET language=? WHERE id=?", (req.body["language"], req.user["id"]))
    return {"language": req.body["language"]}


@route("DELETE", "/api/me")
def delete_me(req):
    """Right to erase: a student or parent can delete their account and all their learning data."""
    require_role(req, "student", "parent")
    c, uid = req.conn, req.user["id"]
    for table in ("answers", "progress", "test_results", "test_starts", "enrollments"):
        c.execute(f"DELETE FROM {table} WHERE student_id=?", (uid,))
    c.execute("DELETE FROM sessions WHERE user_id=?", (uid,))
    c.execute("DELETE FROM users WHERE id=?", (uid,))
    return {"deleted": True}


# ---------------------------------------------------------------- topics & lessons
@route("GET", "/api/topics")
def list_topics(req):
    sql, args = "SELECT * FROM topics WHERE 1=1", []
    for key in ("grade", "subject"):
        if req.query.get(key):
            sql += f" AND {key}=?"
            args.append(req.query[key])
    return [dict(r) for r in req.conn.execute(sql + " ORDER BY grade, subject, name", args)]


@route("POST", "/api/topics")
def add_topic(req):
    require_role(req, "teacher")
    need(req.body, "grade", "subject", "name")
    grade = to_int(req.body["grade"], "grade")
    if grade not in GRADES:
        raise ApiError(400, "grade must be 6 to 10")
    pre = req.body.get("prereq_id") or None
    if pre:
        get_or_404(req.conn, "topics", to_int(pre, "prereq_id"), "Prerequisite topic")
    try:
        cur = req.conn.execute("INSERT INTO topics(grade,subject,name,prereq_id) VALUES(?,?,?,?)",
                               (grade, req.body["subject"].strip(), req.body["name"].strip(), pre))
    except Exception:
        raise ApiError(409, "Topic already exists")
    return 201, {"id": cur.lastrowid}


@route("GET", "/api/topics/{id}/lesson")
def get_lesson(req):
    tid = int(req.params["id"])
    topic = get_or_404(req.conn, "topics", tid, "Topic")
    lang = req.query.get("lang") or req.user["language"]
    rows = req.conn.execute("SELECT * FROM lessons WHERE topic_id=?", (tid,)).fetchall()
    by_lang = {r["language"]: r for r in rows}
    chosen = by_lang.get(lang) or by_lang.get("en") or (rows[0] if rows else None)
    if not chosen:
        raise ApiError(404, "No lesson written for this topic yet")
    return {"topic": topic["name"], "language": chosen["language"], "title": chosen["title"],
            "content": chosen["content"], "available_languages": sorted(by_lang)}


@route("PUT", "/api/topics/{id}/lesson")
def save_lesson(req):
    require_role(req, "teacher")
    tid = int(req.params["id"])
    get_or_404(req.conn, "topics", tid, "Topic")
    need(req.body, "title", "content")
    req.conn.execute(
        "INSERT INTO lessons(topic_id,language,title,content) VALUES(?,?,?,?)"
        " ON CONFLICT(topic_id,language) DO UPDATE SET title=excluded.title, content=excluded.content",
        (tid, req.body.get("language", "en"), req.body["title"], req.body["content"]))
    return {"saved": True}


# ---------------------------------------------------------------- question bank
def clean_question(conn, b):
    need(b, "topic_id", "difficulty", "text", "options", "correct_index")
    topic_id = to_int(b["topic_id"], "topic_id")
    get_or_404(conn, "topics", topic_id, "Topic")
    diff = to_int(b["difficulty"], "difficulty")
    if diff not in (1, 2, 3):
        raise ApiError(400, "difficulty must be 1 (easy), 2 (medium) or 3 (hard)")
    opts = b["options"]
    if not isinstance(opts, list) or len(opts) < 2:
        raise ApiError(400, "options must be a list of at least 2 choices")
    ci = to_int(b["correct_index"], "correct_index")
    if not 0 <= ci < len(opts):
        raise ApiError(400, "correct_index is outside options")
    return (topic_id, diff, b.get("language", "en"), b["text"], json.dumps(opts), ci,
            b.get("hint", ""), b.get("explanation", ""))


def insert_question(conn, user, b):
    return conn.execute(
        "INSERT INTO questions(topic_id,difficulty,language,text,options,correct_index,hint,"
        "explanation,created_by,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
        clean_question(conn, b) + (user["id"], now())).lastrowid


@route("GET", "/api/questions")
def list_questions(req):
    q = req.query
    sql = ("SELECT q.* FROM questions q JOIN topics t ON t.id=q.topic_id WHERE q.active=1")
    args = []
    for key, col in (("topic_id", "q.topic_id"), ("difficulty", "q.difficulty"),
                     ("language", "q.language"), ("grade", "t.grade"), ("subject", "t.subject")):
        if q.get(key):
            sql += f" AND {col}=?"
            args.append(q[key])
    limit = min(to_int(q.get("limit", 50), "limit"), 200)
    rows = req.conn.execute(sql + " ORDER BY q.id LIMIT ?", args + [limit]).fetchall()
    reveal = req.user["role"] == "teacher"   # students never see answers here
    return [q_public(r, reveal) for r in rows]


@route("POST", "/api/questions")
def add_question(req):
    require_role(req, "teacher")
    return 201, {"id": insert_question(req.conn, req.user, req.body)}


@route("POST", "/api/questions/bulk")
def bulk_questions(req):
    require_role(req, "teacher")
    items = req.body.get("questions")
    if not isinstance(items, list) or not items:
        raise ApiError(400, "questions must be a non-empty list")
    ids = [insert_question(req.conn, req.user, item) for item in items]
    return 201, {"created": len(ids), "ids": ids}


@route("PUT", "/api/questions/{id}")
def edit_question(req):
    require_role(req, "teacher")
    row = get_or_404(req.conn, "questions", int(req.params["id"]), "Question")
    if row["created_by"] != req.user["id"]:
        raise ApiError(403, "You can only edit your own questions")
    merged = {**q_public(row, True), **req.body}
    req.conn.execute(
        "UPDATE questions SET topic_id=?,difficulty=?,language=?,text=?,options=?,correct_index=?,"
        "hint=?,explanation=? WHERE id=?", clean_question(req.conn, merged) + (row["id"],))
    return {"updated": True}


@route("DELETE", "/api/questions/{id}")
def delete_question(req):
    require_role(req, "teacher")
    row = get_or_404(req.conn, "questions", int(req.params["id"]), "Question")
    if row["created_by"] != req.user["id"]:
        raise ApiError(403, "You can only delete your own questions")
    req.conn.execute("UPDATE questions SET active=0 WHERE id=?", (row["id"],))
    return {"deleted": True}


# ---------------------------------------------------------------- classes & materials
@route("POST", "/api/classes")
def create_class(req):
    require_role(req, "teacher")
    need(req.body, "name", "grade", "subject")
    grade = to_int(req.body["grade"], "grade")
    if grade not in GRADES:
        raise ApiError(400, "grade must be 6 to 10")
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not req.conn.execute("SELECT 1 FROM classes WHERE join_code=?", (code,)).fetchone():
            break
    cur = req.conn.execute(
        "INSERT INTO classes(teacher_id,name,grade,subject,join_code,created_at) VALUES(?,?,?,?,?,?)",
        (req.user["id"], req.body["name"], grade, req.body["subject"], code, now()))
    return 201, {"id": cur.lastrowid, "join_code": code}


@route("GET", "/api/classes")
def my_classes(req):
    if req.user["role"] == "teacher":
        rows = req.conn.execute("SELECT * FROM classes WHERE teacher_id=?", (req.user["id"],))
    elif req.user["role"] == "student":
        rows = req.conn.execute(
            "SELECT c.* FROM classes c JOIN enrollments e ON e.class_id=c.id WHERE e.student_id=?",
            (req.user["id"],))
    else:
        return []
    out = []
    for r in rows:
        d = dict(r)
        if req.user["role"] != "teacher":
            d.pop("join_code")
        out.append(d)
    return out


@route("POST", "/api/classes/join")
def join_class(req):
    require_role(req, "student")
    need(req.body, "code")
    cls = req.conn.execute("SELECT * FROM classes WHERE join_code=?",
                           (req.body["code"].strip().upper(),)).fetchone()
    if not cls:
        raise ApiError(404, "Invalid class code")
    req.conn.execute("INSERT OR IGNORE INTO enrollments VALUES(?,?,?)", (cls["id"], req.user["id"], now()))
    return {"joined": True, "class_id": cls["id"], "name": cls["name"]}


@route("POST", "/api/classes/{id}/materials")
def post_material(req):
    require_role(req, "teacher")
    cls = own_class(req, int(req.params["id"]))
    need(req.body, "kind", "title")
    if req.body["kind"] not in MATERIAL_KINDS:
        raise ApiError(400, "kind must be one of: " + ", ".join(MATERIAL_KINDS))
    topic_id, test_id = req.body.get("topic_id"), req.body.get("test_id")
    if topic_id:
        get_or_404(req.conn, "topics", to_int(topic_id, "topic_id"), "Topic")
    if test_id:
        get_or_404(req.conn, "tests", to_int(test_id, "test_id"), "Test")
    cur = req.conn.execute(
        "INSERT INTO materials(class_id,kind,title,body,topic_id,test_id,created_at) VALUES(?,?,?,?,?,?,?)",
        (cls["id"], req.body["kind"], req.body["title"], req.body.get("body", ""),
         topic_id, test_id, now()))
    return 201, {"id": cur.lastrowid}


@route("GET", "/api/classes/{id}/materials")
def list_materials(req):
    cls = class_access(req, int(req.params["id"]))
    sql, args = "SELECT * FROM materials WHERE class_id=?", [cls["id"]]
    if req.query.get("kind"):
        sql += " AND kind=?"
        args.append(req.query["kind"])
    out = []
    for r in req.conn.execute(sql + " ORDER BY created_at DESC, id DESC", args):
        d = dict(r)
        d["has_file"] = bool(d.pop("file_path"))
        if d["test_id"]:
            t = req.conn.execute("SELECT time_limit_min, deadline FROM tests WHERE id=?", (d["test_id"],)).fetchone()
            d.update(time_limit_min=t["time_limit_min"], deadline=t["deadline"])
        out.append(d)
    return out


UPLOAD_RULES = {"lecture": ({".mp4", ".webm"}, 100 * 2**20), "note": ({".pdf"}, 20 * 2**20)}


@route("POST", "/api/classes/{id}/upload")
def upload_material(req):
    """Raw file in the request body; ?kind=lecture|note&title=...&filename=..."""
    require_role(req, "teacher")
    cls = own_class(req, int(req.params["id"]))
    kind, title = req.query.get("kind"), req.query.get("title", "").strip()
    name = os.path.basename(req.query.get("filename", ""))
    if kind not in UPLOAD_RULES or not title:
        raise ApiError(400, "kind must be lecture or note, and a title is required")
    exts, limit = UPLOAD_RULES[kind]
    ext = os.path.splitext(name)[1].lower()
    if ext not in exts:
        raise ApiError(400, "Lectures must be .mp4 or .webm videos; notes must be .pdf")
    if not req.raw:
        raise ApiError(400, "Empty file")
    if len(req.raw) > limit:
        raise ApiError(413, f"File is too large (max {limit // 2**20} MB)")
    if ext == ".pdf" and not req.raw.startswith(b"%PDF"):
        raise ApiError(400, "This is not a real PDF file")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    stored = secrets.token_hex(12) + ext
    with open(os.path.join(UPLOAD_DIR, stored), "wb") as f:
        f.write(req.raw)
    cur = req.conn.execute(
        "INSERT INTO materials(class_id,kind,title,file_name,file_path,created_at) VALUES(?,?,?,?,?,?)",
        (cls["id"], kind, title, name, stored, now()))
    return 201, {"id": cur.lastrowid}


def file_for(conn, user, material_id):
    """Path of an uploaded file, only for the class teacher or enrolled students."""
    m = conn.execute("SELECT * FROM materials WHERE id=? AND file_path IS NOT NULL", (material_id,)).fetchone()
    if not m:
        raise ApiError(404, "File not found")
    class_access(Request(conn, user, {}, {}, {}), m["class_id"])
    return os.path.join(UPLOAD_DIR, m["file_path"]), m["file_name"]


@route("GET", "/api/classes/{id}/dashboard")
def class_dashboard(req):
    require_role(req, "teacher")
    return engine.class_overview(req.conn, own_class(req, int(req.params["id"])))


# ---------------------------------------------------------------- practice
@route("GET", "/api/practice/next")
def practice_next(req):
    require_role(req, "student")
    need(req.query, "topic_id")
    tid = to_int(req.query["topic_id"], "topic_id")
    get_or_404(req.conn, "topics", tid, "Topic")
    q, level = engine.pick_question(req.conn, req.user["id"], tid,
                                    req.query.get("language") or req.user["language"])
    if not q:
        raise ApiError(404, "No questions available for this topic yet")
    return {"level": level, "question": q_public(q)}


@route("POST", "/api/answers")
def submit_answer(req):
    require_role(req, "student")
    need(req.body, "question_id", "chosen")
    q = get_or_404(req.conn, "questions", to_int(req.body["question_id"], "question_id"), "Question")
    chosen = to_int(req.body["chosen"], "chosen")
    aid = str(req.body.get("attempt_id") or "")[:64] or None
    if aid:   # same attempt sent twice (double click / retry): do not count it again
        prev = req.conn.execute("SELECT is_correct FROM answers WHERE student_id=? AND attempt_id=?",
                                (req.user["id"], aid)).fetchone()
        if prev:
            return {"correct": bool(prev["is_correct"]), "correct_index": q["correct_index"],
                    "new_level": engine.get_level(req.conn, req.user["id"], q["topic_id"]), "duplicate": True}
    ok, level = engine.record_answer(req.conn, req.user["id"], q, chosen)
    if aid:
        req.conn.execute("UPDATE answers SET attempt_id=? WHERE id=(SELECT MAX(id) FROM answers WHERE student_id=?)",
                         (aid, req.user["id"]))
    res = {"correct": bool(ok), "correct_index": q["correct_index"], "new_level": level}
    if not ok:   # hint, explanation, and the earlier concept that may be the real cause
        res.update(hint=q["hint"], explanation=q["explanation"], review_topic_id=q["topic_id"],
                   root_gap=engine.root_gap(req.conn, req.user["id"], q["topic_id"]))
    return res


# ---------------------------------------------------------------- tests
def test_access(req, test):
    u = req.user
    if u["role"] == "teacher":
        if test["created_by"] != u["id"]:
            raise ApiError(403, "Not your test")
    elif test["class_id"]:
        class_access(req, test["class_id"])


@route("POST", "/api/tests")
def create_test(req):
    require_role(req, "teacher")
    need(req.body, "title")
    cls_id = req.body.get("class_id")
    if cls_id:
        own_class(req, to_int(cls_id, "class_id"))
    ids = req.body.get("question_ids")
    if ids:
        ids = [to_int(i, "question_ids") for i in ids]
        found = req.conn.execute(
            f"SELECT id FROM questions WHERE active=1 AND id IN ({','.join('?'*len(ids))})", ids).fetchall()
        if len(found) != len(set(ids)):
            raise ApiError(400, "Some question_ids do not exist")
    else:
        need(req.body, "topic_id")
        sql, args = "SELECT id FROM questions WHERE active=1 AND topic_id=?", [to_int(req.body["topic_id"], "topic_id")]
        if req.body.get("language"):
            sql += " AND language=?"
            args.append(req.body["language"])
        rows = req.conn.execute(sql + " ORDER BY RANDOM() LIMIT ?",
                                args + [to_int(req.body.get("count", 5), "count")]).fetchall()
        ids = [r["id"] for r in rows]
        if not ids:
            raise ApiError(400, "No questions found for this topic")
    limit = to_int(req.body.get("time_limit_min") or 0, "time_limit_min")
    if not 0 <= limit <= 300:
        raise ApiError(400, "Time limit must be 0 (no limit) to 300 minutes")
    deadline = to_int(req.body["deadline"], "deadline") if req.body.get("deadline") else None
    if deadline and deadline <= now():
        raise ApiError(400, "The deadline must be in the future")
    cur = req.conn.execute(
        "INSERT INTO tests(class_id,title,created_by,created_at,time_limit_min,deadline) VALUES(?,?,?,?,?,?)",
        (cls_id, req.body["title"], req.user["id"], now(), limit or None, deadline))
    tid = cur.lastrowid
    req.conn.executemany("INSERT OR IGNORE INTO test_questions VALUES(?,?)", [(tid, i) for i in ids])
    if cls_id:   # also post it to the class so students see it
        req.conn.execute(
            "INSERT INTO materials(class_id,kind,title,test_id,created_at) VALUES(?,?,?,?,?)",
            (cls_id, "test", req.body["title"], tid, now()))
    return 201, {"id": tid, "question_count": len(ids)}


def test_questions(conn, test_id):
    return conn.execute(
        "SELECT q.* FROM test_questions tq JOIN questions q ON q.id=tq.question_id"
        " WHERE tq.test_id=? ORDER BY q.id", (test_id,)).fetchall()


@route("GET", "/api/tests/{id}")
def get_test(req):
    test = get_or_404(req.conn, "tests", int(req.params["id"]), "Test")
    test_access(req, test)
    reveal = req.user["role"] == "teacher"
    return test_payload(req.conn, test, reveal)


def test_payload(conn, test, reveal=False):
    return {"id": test["id"], "title": test["title"], "class_id": test["class_id"],
            "time_limit_min": test["time_limit_min"], "deadline": test["deadline"],
            "questions": [q_public(q, reveal) for q in test_questions(conn, test["id"])]}


@route("POST", "/api/tests/{id}/start")
def start_test(req):
    """Starts the clock. The server keeps the start time, so the limit cannot be cheated from the browser."""
    require_role(req, "student")
    test = get_or_404(req.conn, "tests", int(req.params["id"]), "Test")
    test_access(req, test)
    if test["deadline"] and now() > test["deadline"]:
        raise ApiError(403, "The deadline for this test has passed")
    t = now()
    req.conn.execute("INSERT OR REPLACE INTO test_starts VALUES(?,?,?)", (test["id"], req.user["id"], t))
    out = test_payload(req.conn, test)
    out.update(started_at=t, server_time=t,
               ends_at=t + test["time_limit_min"] * 60 if test["time_limit_min"] else None)
    return out


@route("GET", "/api/tests/{id}/key")
def answer_key(req):
    """Answer key: teacher any time; a student only after submitting and after the deadline."""
    test = get_or_404(req.conn, "tests", int(req.params["id"]), "Test")
    test_access(req, test)
    if req.user["role"] == "student":
        done = req.conn.execute("SELECT 1 FROM test_results WHERE test_id=? AND student_id=?",
                                (test["id"], req.user["id"])).fetchone()
        if not done or (test["deadline"] and now() < test["deadline"]):
            raise ApiError(403, "The answer key opens after you submit and the deadline has passed")
    elif req.user["role"] != "teacher":
        raise ApiError(403, "Not allowed")
    return [{**q_public(q, True), "correct_option": json.loads(q["options"])[q["correct_index"]]}
            for q in test_questions(req.conn, test["id"])]


@route("GET", "/api/tests")
def list_tests(req):
    require_role(req, "teacher")
    rows = req.conn.execute(
        "SELECT t.*, (SELECT COUNT(*) FROM test_questions WHERE test_id=t.id) AS qn,"
        " (SELECT COUNT(*) FROM test_results WHERE test_id=t.id) AS subs FROM tests t"
        " WHERE t.created_by=? ORDER BY t.id DESC", (req.user["id"],)).fetchall()
    return [{"id": r["id"], "title": r["title"], "class_id": r["class_id"], "question_count": r["qn"],
             "time_limit_min": r["time_limit_min"], "deadline": r["deadline"], "submissions": r["subs"]} for r in rows]


@route("POST", "/api/tests/{id}/submit")
def submit_test(req):
    require_role(req, "student")
    test = get_or_404(req.conn, "tests", int(req.params["id"]), "Test")
    test_access(req, test)
    limit = test["time_limit_min"]
    if limit:
        st = req.conn.execute("SELECT started_at FROM test_starts WHERE test_id=? AND student_id=?",
                              (test["id"], req.user["id"])).fetchone()
        if not st or now() > st["started_at"] + limit * 60 + 30:   # 30 s grace for slow networks
            raise ApiError(400, "Time is up. Start the test again to retry.")
    elif test["deadline"] and now() > test["deadline"] + 30:
        raise ApiError(403, "The deadline for this test has passed")
    given = req.body.get("answers")
    if not isinstance(given, dict):
        raise ApiError(400, 'answers must be an object like {"<question_id>": <chosen_index>}')
    score, review = 0, []
    show_key = not test["deadline"] or now() > test["deadline"]   # no answer sharing before the deadline
    questions = test_questions(req.conn, test["id"])
    for q in questions:
        raw = given.get(str(q["id"]))
        if raw is None:
            review.append({"question_id": q["id"], "correct": False, "chosen": None,
                           "correct_index": q["correct_index"] if show_key else None,
                       "explanation": q["explanation"] if show_key else None})
            continue
        chosen = to_int(raw, "answer")
        ok, _ = engine.record_answer(req.conn, req.user["id"], q, chosen, test_id=test["id"], adapt=False)
        score += ok
        review.append({"question_id": q["id"], "correct": bool(ok), "chosen": chosen,
                       "correct_index": q["correct_index"] if show_key else None,
                       "explanation": q["explanation"] if show_key else None})
    req.conn.execute("INSERT INTO test_results(test_id,student_id,score,total,taken_at) VALUES(?,?,?,?,?)",
                     (test["id"], req.user["id"], score, len(questions), now()))
    total = len(questions)
    return {"score": score, "total": total,
            "percent": round(score * 100 / total, 1) if total else 0, "review": review}


@route("GET", "/api/tests/{id}/results")
def test_results(req):
    test = get_or_404(req.conn, "tests", int(req.params["id"]), "Test")
    test_access(req, test)
    sql = ("SELECT r.*, u.name FROM test_results r JOIN users u ON u.id=r.student_id WHERE r.test_id=?")
    args = [test["id"]]
    if req.user["role"] == "student":
        sql += " AND r.student_id=?"
        args.append(req.user["id"])
    return [{"student_id": r["student_id"], "student": r["name"], "score": r["score"], "total": r["total"],
             "percent": round(r["score"] * 100 / r["total"], 1) if r["total"] else 0, "taken_at": r["taken_at"]}
            for r in req.conn.execute(sql + " ORDER BY r.taken_at", args)]


@route("GET", "/api/tests/history")
def test_history(req):
    """Test history with change versus the previous attempt."""
    student = target_student(req)
    rows = req.conn.execute(
        "SELECT r.*, t.title FROM test_results r JOIN tests t ON t.id=r.test_id"
        " WHERE r.student_id=? ORDER BY r.taken_at, r.id", (student["id"],)).fetchall()
    out, prev = [], None
    for r in rows:
        pct = round(r["score"] * 100 / r["total"], 1) if r["total"] else 0
        out.append({"test_id": r["test_id"], "title": r["title"], "score": r["score"], "total": r["total"],
                    "percent": pct, "change_vs_previous": None if prev is None else round(pct - prev, 1),
                    "taken_at": r["taken_at"]})
        prev = pct
    return out


# ---------------------------------------------------------------- progress & reports
@route("GET", "/api/progress")
def progress(req):
    student = target_student(req)
    stats = engine.topic_stats(req.conn, student["id"])
    history = req.conn.execute(
        "SELECT a.answered_at, a.is_correct, a.test_id, q.text, t.name AS topic FROM answers a"
        " JOIN questions q ON q.id=a.question_id JOIN topics t ON t.id=a.topic_id"
        " WHERE a.student_id=? ORDER BY a.id DESC LIMIT ?",
        (student["id"], min(to_int(req.query.get("limit", 20), "limit"), 200))).fetchall()
    return {"student": {"id": student["id"], "name": student["name"]},
            "streak_days": engine.streak_days(req.conn, student["id"]),
            "answers_today": engine.answers_today(req.conn, student["id"]), "daily_goal": 5,
            "overall": engine.overall(stats), "topics": stats,
            "weak_topics": engine.weak_topics(stats),
            "history": [{**dict(h), "is_correct": bool(h["is_correct"])} for h in history]}


@route("GET", "/api/recommendations")
def recommendations(req):
    student = target_student(req)
    return {"student": {"id": student["id"], "name": student["name"]},
            "recommendations": engine.recommend(req.conn, student["id"])}


@route("GET", "/api/weak-topics")
def weak(req):
    student = target_student(req)
    return engine.weak_topics(engine.topic_stats(req.conn, student["id"]))


# ---------------------------------------------------------------- parents
@route("GET", "/api/parent/children")
def parent_children(req):
    require_role(req, "parent")
    kids = req.conn.execute(
        "SELECT id, name FROM users WHERE role='student' AND parent_email=?", (req.user["email"],)).fetchall()
    out = []
    for k in kids:
        stats = engine.topic_stats(req.conn, k["id"])
        out.append({"student_id": k["id"], "name": k["name"], "overall": engine.overall(stats),
                    "weak_topics": [w["name"] for w in engine.weak_topics(stats)],
                    "next_steps": engine.recommend(req.conn, k["id"])[:3]})
    return out
