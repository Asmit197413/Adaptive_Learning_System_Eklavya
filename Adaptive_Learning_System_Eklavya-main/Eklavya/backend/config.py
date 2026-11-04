"""Central settings for the Adaptive Learning System backend."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLite file lives in ../database (override with LEARNER_DB env var)
DB_PATH = os.environ.get(
    "LEARNER_DB",
    os.path.normpath(os.path.join(BASE_DIR, "..", "database", "eklavya.db")),
)

HOST = os.environ.get("LEARNER_HOST", "127.0.0.1")
PORT = int(os.environ.get("LEARNER_PORT", "8000"))

UPLOAD_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "database", "uploads"))
MAX_BODY = 105 * 2**20            # biggest request accepted (videos up to 100 MB)

SESSION_SECONDS = 7 * 24 * 3600   # login stays valid for 7 days
MAX_LEVEL = 3                     # 1 = easy, 2 = medium, 3 = hard
GRADES = range(6, 11)             # Class 6 to 10
ROLES = ("student", "teacher", "parent")
MATERIAL_KINDS = ("lecture", "note", "practice", "test")

# Analysis thresholds (tune these freely)
WEAK_ACCURACY = 0.60
WEAK_MIN_ATTEMPTS = 3
