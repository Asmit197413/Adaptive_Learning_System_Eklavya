"""Load demo data:  python seed.py
Logins (password for all: demo123):
    teacher@demo.com   student@demo.com   parent@demo.com
Class join code: DEMO01.  Pre-filled classmates: Riya (struggling), Aman (strong), Kabir (steady).
Questions are original, written to match NCERT Class 6 chapter names. A teacher should review them.
"""
import json
import time

import engine
from db import get_conn, init_db


def add_user(conn, name, email, role, parent_email=None):
    salt, digest = hash_password("demo123")
    return conn.execute(
        "INSERT INTO users(name,email,salt,password_hash,role,language,parent_email,created_at) VALUES(?,?,?,?,?,?,?,?)",
        (name, email, salt, digest, role, "en", parent_email, int(time.time()))).lastrowid


# (difficulty, question, options, correct_index, hint, explanation)
PLAYING = [
    (1, "Which of these is a factor of 12?", ["5", "4", "7", "9"], 1, "A factor divides the number exactly.", "12 / 4 = 3 with no remainder, so 4 is a factor."),
    (1, "Which number is prime?", ["9", "15", "11", "21"], 2, "A prime has exactly two factors: 1 and itself.", "11 can only be divided by 1 and 11."),
    (2, "What is the HCF of 12 and 18?", ["3", "6", "9", "2"], 1, "List the factors of both and pick the biggest common one.", "Common factors: 1, 2, 3, 6. The highest is 6."),
    (2, "Which is a multiple of both 3 and 4?", ["18", "20", "24", "14"], 2, "Check divisibility by 3 and by 4.", "24 = 3 x 8 = 4 x 6."),
    (3, "What is the LCM of 4 and 6?", ["24", "12", "10", "2"], 1, "List multiples of each until they meet.", "Multiples of 4: 4, 8, 12. Multiples of 6: 6, 12. First common: 12."),
    (3, "Which pair is co-prime?", ["8 and 12", "9 and 15", "7 and 10", "6 and 9"], 2, "Co-prime numbers share only the factor 1.", "7 and 10 have no common factor except 1."),
]
FRACTIONS = [
    (1, "What is 1/2 + 1/2?", ["1", "2", "1/4", "1/2"], 0, "Same denominator: add the tops.", "1/2 + 1/2 = 2/2 = 1."),
    (1, "Which fraction is the biggest?", ["1/8", "1/4", "1/2", "1/16"], 2, "A smaller denominator means bigger pieces.", "Halves are bigger than quarters, eighths and sixteenths."),
    (2, "What is 2/3 + 1/6?", ["3/9", "5/6", "1/2", "3/6"], 1, "Make the denominators equal first.", "2/3 = 4/6, so 4/6 + 1/6 = 5/6."),
    (2, "Simplify 12/18.", ["6/9", "2/3", "3/4", "4/6"], 1, "Divide top and bottom by their biggest common factor.", "The common factor is 6, so 12/18 = 2/3."),
    (3, "What is 3/4 - 2/5?", ["1/9", "7/20", "1/20", "5/20"], 1, "Use 20 as the common denominator.", "15/20 - 8/20 = 7/20."),
    (3, "What is 2/3 x 9/10?", ["3/5", "18/13", "11/13", "2/5"], 0, "Multiply tops, multiply bottoms, then simplify.", "18/30 simplifies to 3/5."),
]
FRACTIONS_HI = [
    (1, "1/2 + 1/2 कितना होता है?", ["1", "2", "1/4", "1/2"], 0, "हर समान है, तो अंशों को जोड़ें।", "1/2 + 1/2 = 2/2 = 1।"),
    (2, "12/18 को सरल रूप में लिखिए।", ["6/9", "2/3", "3/4", "4/6"], 1, "अंश और हर को उनके सबसे बड़े सामान्य गुणनखंड से भाग दें।", "सामान्य गुणनखंड 6 है, इसलिए 12/18 = 2/3।"),
]
DECIMALS = [
    (1, "Which is larger: 0.5 or 0.05?", ["0.5", "0.05", "Equal", "Cannot say"], 0, "Compare the tenths place.", "0.5 is five tenths; 0.05 is five hundredths."),
    (2, "What is 1.25 + 2.5?", ["3.75", "3.30", "4.75", "3.25"], 0, "Line up the decimal points.", "1.25 + 2.50 = 3.75."),
    (3, "What is 0.6 x 0.4?", ["2.4", "0.24", "0.024", "1.0"], 1, "Multiply 6 x 4, then count decimal places.", "6 x 4 = 24, with two decimal places gives 0.24."),
]
INTEGERS = [
    (1, "Which is the smallest?", ["-3", "0", "2", "-7"], 3, "On the number line, numbers to the left are smaller.", "-7 is farthest left, so it is the smallest."),
    (2, "What is -5 + 8?", ["-3", "3", "13", "-13"], 1, "Start at -5 and move 8 steps to the right.", "-5 + 8 = 3."),
    (3, "What is -4 - (-6)?", ["-10", "10", "2", "-2"], 2, "Subtracting a negative is the same as adding.", "-4 + 6 = 2."),
]
PLANTS = [
    (1, "Which part of a plant absorbs water from soil?", ["Leaf", "Root", "Flower", "Stem"], 1, "It grows underground.", "Roots absorb water and minerals."),
    (2, "Which gas do plants take in for photosynthesis?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], 2, "Animals breathe it out.", "Plants use CO2, water and sunlight to make food."),
    (3, "Where does photosynthesis mainly happen?", ["Roots", "Chloroplasts in leaves", "Flowers", "Bark"], 1, "Think green pigment.", "Chloroplasts contain chlorophyll that captures light."),
]
FOOD = [
    (1, "Which nutrient mainly gives us energy?", ["Vitamins", "Carbohydrates", "Minerals", "Water"], 1, "Rice and bread are rich in it.", "Carbohydrates are the main energy source."),
    (2, "Lack of which vitamin causes scurvy?", ["Vitamin A", "Vitamin C", "Vitamin D", "Iron"], 1, "Citrus fruits help prevent it.", "Scurvy is caused by lack of Vitamin C."),
    (3, "Which solution turns blue-black when starch is present?", ["Benedict's solution", "Iodine solution", "Litmus", "Lime water"], 1, "Think of the colour change in the test for starch.", "Iodine solution turns blue-black with starch."),
]
# (subject, chapter, questions, builds on)
CHAPTERS = [
    ("Maths", "Playing with Numbers", PLAYING, None),
    ("Maths", "Fractions", FRACTIONS, "Playing with Numbers"),
    ("Maths", "Decimals", DECIMALS, "Fractions"),
    ("Maths", "Integers", INTEGERS, None),
    ("Science", "Getting to Know Plants", PLANTS, None),
    ("Science", "Components of Food", FOOD, None),
]
LESSONS = {
    "Fractions": {"en": "A fraction names a part of a whole. In 3/4, the 4 tells how many equal parts the whole has and the 3 tells how many we take. To add fractions, first make the denominators equal.",
                  "hi": "भिन्न किसी पूरी चीज़ के हिस्से को दर्शाती है। 3/4 में 4 बताता है कि पूरे के कितने बराबर भाग हैं और 3 बताता है कि हमने कितने भाग लिए।",
                  "bn": "ভগ্নাংশ কোনো পূর্ণ বস্তুর একটি অংশ বোঝায়। 3/4 এ 4 বলে পূর্ণটি কয়টি সমান ভাগে ভাগ করা এবং 3 বলে আমরা কয়টি ভাগ নিয়েছি।"},
    "Playing with Numbers": {"en": "Factors divide a number exactly. Multiples are what you get by multiplying. The HCF is the biggest common factor and the LCM is the smallest common multiple."},
}
# classmates with a scripted history: c = right, w = wrong
CLASSMATES = [("Riya", {"Playing with Numbers": "wwcwwc", "Fractions": "wwcww", "Decimals": "www"}),
              ("Aman", {"Playing with Numbers": "cccccc", "Fractions": "cccccc", "Decimals": "ccc"}),
              ("Kabir", {"Playing with Numbers": "cccwc", "Fractions": "ccwcw", "Decimals": "cwc"})]


def main():
    init_db()
    conn = get_conn()
    if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        print("Database already has data. Delete database/eklavya.db to reseed.")
        return
    teacher = add_user(conn, "Demo Teacher", "teacher@demo.com", "teacher")
    add_user(conn, "Demo Parent", "parent@demo.com", "parent")   # sees only students who list this email
    student = add_user(conn, "Demo Student", "student@demo.com", "student", "parent@demo.com")
    now = int(time.time())
    class_id = conn.execute(
        "INSERT INTO classes(teacher_id,name,grade,subject,join_code,created_at) VALUES(?,?,?,?,?,?)",
        (teacher, "Class 6 Maths", 6, "Maths", "DEMO01", now)).lastrowid
    conn.execute("INSERT INTO enrollments VALUES(?,?,?)", (class_id, student, now))

    ids = {}
    for subject, name, qs, pre in CHAPTERS:
        tid = ids[name] = conn.execute("INSERT INTO topics(grade,subject,name,prereq_id) VALUES(6,?,?,?)",
                                       (subject, name, ids.get(pre))).lastrowid
        for lang, text in LESSONS.get(name, {"en": f"Lesson notes for {name}. Replace with your own notes."}).items():
            conn.execute("INSERT INTO lessons(topic_id,language,title,content) VALUES(?,?,?,?)", (tid, lang, name, text))
        extra = [("hi",) + q for q in FRACTIONS_HI] if name == "Fractions" else []
        for lang, d, text, opts, ci, hint, expl in [("en",) + q for q in qs] + extra:
            conn.execute(
                "INSERT INTO questions(topic_id,difficulty,language,text,options,correct_index,hint,"
                "explanation,created_by,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (tid, d, lang, text, json.dumps(opts), ci, hint, expl, teacher, now))

    for name, history in CLASSMATES:   # makes the teacher dashboard and root-gap story visible at once
        sid = add_user(conn, name, f"{name.lower()}@demo.com", "student", f"parent.{name.lower()}@demo.com")
        conn.execute("INSERT INTO enrollments VALUES(?,?,?)", (class_id, sid, now))
        for topic, pattern in history.items():
            qs = conn.execute("SELECT * FROM questions WHERE topic_id=? AND language='en' ORDER BY id", (ids[topic],)).fetchall()
            for i, ch in enumerate(pattern):
                q = qs[i % len(qs)]
                engine.record_answer(conn, sid, q, q["correct_index"] if ch == "c" else (q["correct_index"] + 1) % 2)
    conn.commit()
    conn.close()
    print("Seeded. Logins use password demo123: teacher@demo.com, student@demo.com, parent@demo.com | class code DEMO01")


if __name__ == "__main__":
    main()
