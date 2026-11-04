"""Password hashing, session tokens, and the shared ApiError."""
import hashlib
import hmac
import secrets
import time

from config import SESSION_SECONDS


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 120_000
    ).hex()
    return salt, digest


def verify_password(password, salt, digest):
    return hmac.compare_digest(hash_password(password, salt)[1], digest)


def create_session(conn, user_id):
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions(token, user_id, created_at) VALUES(?,?,?)",
        (token, user_id, int(time.time())),
    )
    return token


def user_from_token(conn, token):
    if not token:
        return None
    return conn.execute(
        "SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id "
        "WHERE s.token = ? AND s.created_at > ?",
        (token, int(time.time()) - SESSION_SECONDS),
    ).fetchone()
