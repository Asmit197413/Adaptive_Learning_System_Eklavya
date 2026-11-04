"""Learning logic: adaptive difficulty, progress, weak topics, recommendations.

Everything here is simple, readable rules (no ML) as planned in the project doc.
"""
import time

from datetime import date

START_LEVEL = 2        # start in the middle: one answer places a student at easy, medium or hard
START_MASTERY = 0.5    # we know nothing yet about a new student
LEARN = 0.10           # chance a student learns the skill from one more attempt
GUESS = {1: 0.30, 2: 0.20, 3: 0.10}   # chance of a lucky right answer, by difficulty
SLIP = {1: 0.05, 2: 0.10, 3: 0.20}    # chance of a careless wrong answer, by difficulty


def bkt_update(p, correct, difficulty):
    """New mastery estimate after one answer. A right answer on a HARD question is stronger
    evidence than on an easy one; a wrong answer on an EASY question is stronger evidence of a gap."""
    g, s = GUESS[difficulty], SLIP[difficulty]
    post = p * (1 - s) / (p * (1 - s) + (1 - p) * g) if correct else p * s / (p * s + (1 - p) * (1 - g))
    return post + (1 - post) * LEARN


def level_from_mastery(p):
    return 1 if p < 0.40 else 2 if p < 0.70 else 3

from config import MAX_LEVEL, WEAK_ACCURACY, WEAK_MIN_ATTEMPTS


def _acc(correct, attempts):
    return round(correct / attempts, 3) if attempts else 0.0


# ---------------------------------------------------------------- adaptive
def get_level(conn, student_id, topic_id):
    row = conn.execute(
        "SELECT level FROM progress WHERE student_id=? AND topic_id=?",
        (student_id, topic_id),
    ).fetchone()
    return row["level"] if row else START_LEVEL


def pick_question(conn, student_id, topic_id, language=None):
    """Next question at the student's current level (nearest level as fallback).
    Prefers questions the student has seen the fewest times."""
    level = get_level(conn, student_id, topic_id)
    order = sorted(range(1, MAX_LEVEL + 1), key=lambda l: (abs(l - level), l))
    for lang in ([language, None] if language else [None]):
        for lvl in order:
            sql = (
                "SELECT q.*, (SELECT COUNT(*) FROM answers a "
                "WHERE a.student_id=? AND a.question_id=q.id) AS asked "
                "FROM questions q WHERE q.topic_id=? AND q.difficulty=? AND q.active=1"
            )
            args = [student_id, topic_id, lvl]
            if lang:
                sql += " AND q.language=?"
                args.append(lang)
            sql += " ORDER BY asked, RANDOM() LIMIT 1"
            row = conn.execute(sql, args).fetchone()
            if row:
                return row, level
    return None, level


def record_answer(conn, student_id, question, chosen, test_id=None, adapt=True):
    """Store one answer and update the student's mastery of the topic.
    adapt=False (tests): the answer is recorded but does not move the practice level."""
    ok = 1 if chosen == question["correct_index"] else 0
    now = int(time.time())
    conn.execute(
        "INSERT INTO answers(student_id,question_id,topic_id,chosen,is_correct,test_id,answered_at)"
        " VALUES(?,?,?,?,?,?,?)",
        (student_id, question["id"], question["topic_id"], chosen, ok, test_id, now))
    p = conn.execute("SELECT * FROM progress WHERE student_id=? AND topic_id=?",
                     (student_id, question["topic_id"])).fetchone()
    attempts, correct, mastery, streak = (
        (p["attempts"], p["correct"], p["mastery"], p["streak"]) if p else (0, 0, START_MASTERY, 0))
    attempts += 1
    correct += ok
    streak = streak + 1 if ok else 0
    if adapt:
        mastery = bkt_update(mastery, ok, question["difficulty"])
    level = level_from_mastery(mastery)
    conn.execute(
        "INSERT INTO progress(student_id,topic_id,attempts,correct,level,streak,mastery,updated_at)"
        " VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(student_id,topic_id) DO UPDATE SET "
        "attempts=excluded.attempts, correct=excluded.correct, level=excluded.level,"
        " streak=excluded.streak, mastery=excluded.mastery, updated_at=excluded.updated_at",
        (student_id, question["topic_id"], attempts, correct, level, streak, mastery, now))
    return ok, level


def streak_days(conn, student_id):
    """Consecutive days (up to today) on which the student practised."""
    days = [date.fromisoformat(r[0]) for r in conn.execute(
        "SELECT DISTINCT date(answered_at,'unixepoch','localtime') d FROM answers"
        " WHERE student_id=? ORDER BY d DESC", (student_id,))]
    if not days or (date.today() - days[0]).days > 1:
        return 0
    n = 1
    for a, b in zip(days, days[1:]):
        if (a - b).days != 1:
            break
        n += 1
    return n


def answers_today(conn, student_id):
    return conn.execute("SELECT COUNT(*) FROM answers WHERE student_id=? AND"
                        " date(answered_at,'unixepoch','localtime')=date('now','localtime')",
                        (student_id,)).fetchone()[0]


# ---------------------------------------------------------------- analysis
def topic_stats(conn, student_id):
    rows = conn.execute(
        "SELECT p.topic_id, t.name, t.subject, t.grade, p.attempts, p.correct,"
        " p.level, p.streak, p.mastery FROM progress p JOIN topics t ON t.id=p.topic_id"
        " WHERE p.student_id=? ORDER BY t.subject, t.name",
        (student_id,),
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["accuracy"] = _acc(r["correct"], r["attempts"])
        d["mastery"] = round(r["mastery"], 3)
        out.append(d)
    return out


def overall(stats):
    attempts = sum(s["attempts"] for s in stats)
    correct = sum(s["correct"] for s in stats)
    return {"attempts": attempts, "correct": correct, "accuracy": _acc(correct, attempts)}


def weak_topics(stats):
    weak = [
        s for s in stats
        if s["attempts"] >= WEAK_MIN_ATTEMPTS and s["accuracy"] < WEAK_ACCURACY
    ]
    return sorted(weak, key=lambda s: s["accuracy"])


def root_gap(conn, student_id, topic_id):
    """If a topic is weak, check the earlier concept it builds on. Returns that topic if it is weak/unseen."""
    pre = conn.execute("SELECT p.id, p.name FROM topics t JOIN topics p ON p.id=t.prereq_id WHERE t.id=?",
                       (topic_id,)).fetchone()
    if not pre:
        return None
    pr = conn.execute("SELECT attempts, correct FROM progress WHERE student_id=? AND topic_id=?",
                      (student_id, pre["id"])).fetchone()
    if pr is None or pr["attempts"] < WEAK_MIN_ATTEMPTS or _acc(pr["correct"], pr["attempts"]) < WEAK_ACCURACY:
        return {"topic_id": pre["id"], "name": pre["name"]}
    return None


def recommend(conn, student_id):
    """Rule-based next step per topic: learn / revise / practice / test."""
    recs = []
    for s in topic_stats(conn, student_id):
        a, acc = s["attempts"], s["accuracy"]
        if a >= WEAK_MIN_ATTEMPTS and acc < 0.5:
            action, prio, why = "revise", 1, f"Accuracy is only {int(acc*100)}%. Re-read the lesson, then try easier questions."
        elif a < 5:
            action, prio, why = "practice", 3, "Not enough attempts yet. Keep practising."
        elif acc < 0.8:
            action, prio, why = "practice", 2, f"Accuracy is {int(acc*100)}%. A little more practice will help."
        elif s["level"] >= MAX_LEVEL:
            action, prio, why = "test", 4, f"Strong ({int(acc*100)}%) at the hardest level. Ready for a test."
        else:
            action, prio, why = "practice", 3, f"Strong ({int(acc*100)}%). Moving to harder questions."
        gap = root_gap(conn, student_id, s["topic_id"]) if a >= 2 and acc < WEAK_ACCURACY else None
        if gap:
            recs.append({"topic_id": gap["topic_id"], "topic": gap["name"], "subject": s["subject"], "action": "revise",
                         "priority": 0, "reason": f"Root gap: {s['name']} builds on {gap['name']}. Revise {gap['name']} first."})
        recs.append({"topic_id": s["topic_id"], "topic": s["name"], "subject": s["subject"],
                     "action": action, "priority": prio, "reason": why})
    started = {r["topic_id"] for r in recs}
    new_topics = conn.execute(
        "SELECT DISTINCT t.id, t.name, t.subject FROM enrollments e"
        " JOIN classes c ON c.id=e.class_id"
        " JOIN topics t ON t.grade=c.grade AND t.subject=c.subject"
        " WHERE e.student_id=?", (student_id,),
    ).fetchall()
    for t in new_topics:
        if t["id"] not in started:
            recs.append({"topic_id": t["id"], "topic": t["name"], "subject": t["subject"],
                         "action": "learn", "priority": 5,
                         "reason": "Not started yet. Read the lesson first."})
    return sorted(recs, key=lambda r: r["priority"])


def class_overview(conn, cls):
    """Teacher dashboard data for one class."""
    students = conn.execute(
        "SELECT u.id, u.name, u.email FROM enrollments e JOIN users u ON u.id=e.student_id"
        " WHERE e.class_id=? ORDER BY u.name", (cls["id"],),
    ).fetchall()
    rows = []
    for s in students:
        stats = [x for x in topic_stats(conn, s["id"])
                 if x["subject"] == cls["subject"] and x["grade"] == cls["grade"]]
        o = overall(stats)
        rows.append({"student_id": s["id"], "name": s["name"], **o,
                     "weak_topics": [w["name"] for w in weak_topics(stats)]})
    topic_rows = conn.execute(
        "SELECT t.id, t.name, SUM(p.attempts) att, SUM(p.correct) cor,"
        " SUM(CASE WHEN p.attempts>=? AND p.correct*1.0/p.attempts<? THEN 1 ELSE 0 END) struggling"
        " FROM topics t JOIN progress p ON p.topic_id=t.id"
        " WHERE t.grade=? AND t.subject=? AND p.student_id IN"
        " (SELECT student_id FROM enrollments WHERE class_id=?) GROUP BY t.id",
        (WEAK_MIN_ATTEMPTS, WEAK_ACCURACY, cls["grade"], cls["subject"], cls["id"]),
    ).fetchall()
    topics = [{"topic_id": r["id"], "topic": r["name"], "attempts": r["att"],
               "accuracy": _acc(r["cor"], r["att"]), "students_struggling": r["struggling"]}
              for r in topic_rows]
    avg = conn.execute(
        "SELECT AVG(r.score*100.0/r.total) a, COUNT(*) n FROM test_results r"
        " JOIN tests t ON t.id=r.test_id WHERE t.class_id=?", (cls["id"],),
    ).fetchone()
    return {
        "class": {"id": cls["id"], "name": cls["name"], "grade": cls["grade"],
                  "subject": cls["subject"], "join_code": cls["join_code"]},
        "student_count": len(rows),
        "students": rows,
        "topics": sorted(topics, key=lambda t: t["accuracy"]),
        "class_weak_topics": [t for t in topics if t["attempts"] >= 5 and t["accuracy"] < WEAK_ACCURACY],
        "test_average_percent": round(avg["a"], 1) if avg["a"] is not None else None,
        "tests_taken": avg["n"],
    }
