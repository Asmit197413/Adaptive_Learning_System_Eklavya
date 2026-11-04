"""End-to-end check of the whole flow:  python smoke_test.py
Uses a temporary database, so your real data is untouched."""
import json
import os
import tempfile
import threading
import urllib.error
import urllib.request

os.environ["LEARNER_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")   # must be set before imports

import server  # noqa: E402

PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"


def call(method, path, body=None, token=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def check(label, cond):
    print(("PASS  " if cond else "FAIL  ") + label)
    if not cond:
        raise SystemExit(1)


def main():
    srv = server.make_server("127.0.0.1", PORT)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    # 1. teacher registers, creates class
    s, t = call("POST", "/api/register", {"name": "T", "email": "t@x.com", "password": "secret1", "role": "teacher"})
    check("teacher registers", s == 201)
    tt = t["token"]
    s, c = call("POST", "/api/classes", {"name": "6A Maths", "grade": 6, "subject": "Maths"}, tt)
    check("teacher creates class", s == 201 and len(c["join_code"]) == 6)

    # 2. student registers and joins; parent registers and links
    s, st = call("POST", "/api/register", {"name": "S", "email": "s@x.com", "password": "secret1", "role": "student", "parent_email": "p@x.com"})
    stok, sid = st["token"], st["user"]["id"]
    s, _ = call("POST", "/api/classes/join", {"code": c["join_code"]}, stok)
    check("student joins class", s == 200)
    s, _ = call("POST", "/api/register", {"name": "S2", "email": "s2@x.com", "password": "secret1", "role": "student"})
    check("student signup requires parent email", s == 400)
    s, p = call("POST", "/api/register", {"name": "P", "email": "p@x.com", "password": "secret1",
                                          "role": "parent"})
    ptok = p["token"]

    # 3. teacher builds content
    s, topic = call("POST", "/api/topics", {"grade": 6, "subject": "Maths", "name": "Fractions"}, tt)
    tid = topic["id"]
    call("PUT", f"/api/topics/{tid}/lesson", {"language": "en", "title": "Fractions", "content": "Parts of a whole"}, tt)
    qs = [{"topic_id": tid, "difficulty": d, "text": f"Q{d}-{i}", "options": ["a", "b", "c"], "correct_index": 0,
           "hint": "h", "explanation": "e"} for d in (1, 2, 3) for i in range(2)]
    s, bulk = call("POST", "/api/questions/bulk", {"questions": qs}, tt)
    check("bulk question upload", s == 201 and bulk["created"] == 6)
    s, bad = call("POST", "/api/questions", {"topic_id": tid, "difficulty": 9, "text": "x", "options": ["a", "b"], "correct_index": 0}, tt)
    check("invalid question rejected", s == 400)
    s, _ = call("POST", "/api/questions", {"topic_id": tid}, stok)
    check("student cannot add questions (role check)", s == 403)
    s, lst = call("GET", f"/api/questions?topic_id={tid}", None, stok)
    check("students never see answers in question list", "correct_index" not in lst[0])
    s, _ = call("POST", f"/api/classes/{c['id']}/materials", {"kind": "lecture", "title": "Intro", "topic_id": tid}, tt)
    check("teacher posts material", s == 201)
    s, mats = call("GET", f"/api/classes/{c['id']}/materials", None, stok)
    check("student sees material", s == 200 and len(mats) == 1)

    # 4. adaptive practice: correct -> harder, wrong -> easier
    s, nxt = call("GET", f"/api/practice/next?topic_id={tid}", None, stok)
    check("first question is medium (smart start)", nxt["level"] == 2 and nxt["question"]["difficulty"] == 2)
    s, a = call("POST", "/api/answers", {"question_id": nxt["question"]["id"], "chosen": 0, "attempt_id": "a1"}, stok)
    check("correct answer raises level to 3", a["correct"] and a["new_level"] == 3)
    s, a2 = call("POST", "/api/answers", {"question_id": nxt["question"]["id"], "chosen": 0, "attempt_id": "a1"}, stok)
    check("double click is not counted twice", a2.get("duplicate") and a2["new_level"] == 3)
    s, nxt = call("GET", f"/api/practice/next?topic_id={tid}", None, stok)
    check("next question is hard", nxt["question"]["difficulty"] == 3)
    s, a = call("POST", "/api/answers", {"question_id": nxt["question"]["id"], "chosen": 1}, stok)
    check("wrong answer lowers level + gives hint/explanation", not a["correct"] and a["new_level"] == 2 and a["hint"] and a["explanation"])
    for _ in range(3):   # make the student weak
        s, nxt = call("GET", f"/api/practice/next?topic_id={tid}", None, stok)
        call("POST", "/api/answers", {"question_id": nxt["question"]["id"], "chosen": 2}, stok)

    # 4b. teacher uploads a PDF note and a video; student can open them, outsiders cannot
    def upload(path, data, token):
        r = urllib.request.Request(BASE + path, data=data, method="POST", headers={"Content-Type": "application/octet-stream", "Authorization": "Bearer " + token})
        try:
            with urllib.request.urlopen(r) as x:
                return x.status, json.loads(x.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())
    pdf = b"%PDF-1.4 test"
    s, up = upload(f"/api/classes/{c['id']}/upload?kind=note&title=Notes&filename=n.pdf", pdf, tt)
    check("teacher uploads PDF notes", s == 201)
    s, _ = upload(f"/api/classes/{c['id']}/upload?kind=note&title=Bad&filename=n.exe", pdf, tt)
    check("wrong file type rejected", s == 400)
    s, _ = upload(f"/api/classes/{c['id']}/upload?kind=lecture&title=Video&filename=v.mp4", b"\x00\x00\x00\x18ftypmp42", tt)
    check("teacher uploads video lecture", s == 201)
    s, _ = upload(f"/api/classes/{c['id']}/upload?kind=note&title=X&filename=n.pdf", pdf, stok)
    check("student cannot upload", s == 403)
    with urllib.request.urlopen(f"{BASE}/files/{up['id']}?token={stok}") as r:
        check("enrolled student downloads the PDF", r.read() == pdf)
    try:
        urllib.request.urlopen(f"{BASE}/files/{up['id']}?token={ptok}")
        check("parent cannot open class files", False)
    except urllib.error.HTTPError as e:
        check("parent cannot open class files", e.code == 403)

    # 5. test module
    s, test = call("POST", "/api/tests", {"title": "Fractions quiz", "class_id": c["id"], "topic_id": tid, "count": 4}, tt)
    check("teacher creates test", s == 201 and test["question_count"] == 4)
    s, tq = call("GET", f"/api/tests/{test['id']}", None, stok)
    check("test hides answers from student", "correct_index" not in tq["questions"][0])
    answers = {str(q["id"]): 0 for q in tq["questions"][:3]}   # one left blank
    s, res = call("POST", f"/api/tests/{test['id']}/submit", {"answers": answers}, stok)
    check("test auto-graded", s == 200 and res["score"] == 3 and res["total"] == 4)
    s, hist = call("GET", "/api/tests/history", None, stok)
    check("test history stored", len(hist) == 1)

    # 5b. timed test with deadline and answer key
    s, _ = call("POST", "/api/tests", {"title": "Old", "topic_id": tid, "deadline": 5}, tt)
    check("past deadline rejected", s == 400)
    soon = int(__import__("time").time()) + 3600
    s, tt2 = call("POST", "/api/tests", {"title": "Timed", "class_id": c["id"], "topic_id": tid, "count": 3,
                                          "time_limit_min": 10, "deadline": soon}, tt)
    check("teacher creates timed test", s == 201)
    s, st2 = call("POST", f"/api/tests/{tt2['id']}/start", None, stok)
    check("start returns the end time", s == 200 and st2["ends_at"] == st2["started_at"] + 600)
    s, key = call("GET", f"/api/tests/{tt2['id']}/key", None, stok)
    check("student cannot read key before submit/deadline", s == 403)
    s, key = call("GET", f"/api/tests/{tt2['id']}/key", None, tt)
    check("teacher reads the answer key", s == 200 and len(key) == 3 and "correct_option" in key[0])
    import sqlite3
    db = sqlite3.connect(os.environ["LEARNER_DB"]); db.execute("UPDATE test_starts SET started_at=started_at-9999"); db.commit(); db.close()
    s, _ = call("POST", f"/api/tests/{tt2['id']}/submit", {"answers": {}}, stok)
    check("late submission rejected (time limit)", s == 400)
    s, lst = call("GET", "/api/tests", None, tt)
    check("teacher lists tests", s == 200 and any(x["time_limit_min"] == 10 for x in lst))

    # 6. analysis for student, teacher, parent
    s, prog = call("GET", "/api/progress", None, stok)
    check("student progress tracked", prog["overall"]["attempts"] >= 8)
    check("mastery estimate + streak reported", all("mastery" in t for t in prog["topics"]) and prog["streak_days"] >= 1)
    s, _ = call("PUT", "/api/me/language", {"language": "hi"}, stok)
    check("student can switch language", s == 200)
    s, _ = call("PUT", "/api/me/language", {"language": "xx"}, stok)
    check("unsupported language rejected", s == 400)
    s, rec = call("GET", "/api/recommendations", None, stok)
    check("recommendations returned", len(rec["recommendations"]) >= 1)
    s, dash = call("GET", f"/api/classes/{c['id']}/dashboard", None, tt)
    check("teacher dashboard", s == 200 and dash["student_count"] == 1 and dash["tests_taken"] == 1)
    s, view = call("GET", f"/api/progress?student_id={sid}", None, tt)
    check("teacher can view own student", s == 200)
    s, p2 = call("POST", "/api/register", {"name": "P2", "email": "p2@x.com", "password": "secret1", "role": "parent"})
    s, _ = call("GET", f"/api/progress?student_id={sid}", None, p2["token"])
    check("other parent CANNOT see the student", s == 403)
    s, _ = call("GET", f"/api/progress?student_id={sid}", None, ptok)
    check("the named parent can see the student", s == 200)
    s, kids = call("GET", "/api/parent/children", None, ptok)
    check("parent sees child report", s == 200 and kids[0]["name"] == "S")
    s, _ = call("GET", f"/api/classes/{c['id']}/dashboard", None, stok)
    check("student blocked from dashboard", s == 403)
    s, _ = call("GET", "/api/progress")
    check("no token -> 401", s == 401)
    s, _ = call("DELETE", "/api/me", None, stok)
    check("student can delete own account and data", s == 200)
    s, _ = call("GET", "/api/me", None, stok)
    check("deleted account can no longer log in", s == 401)
    print("\nAll checks passed.")
    srv.shutdown()


if __name__ == "__main__":
    main()
