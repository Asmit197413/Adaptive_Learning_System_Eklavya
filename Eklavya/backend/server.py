"""Run with:  python server.py   (standard library only, no installs needed)"""
import json
import mimetypes
import os
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from auth import ApiError, user_from_token
from config import BASE_DIR, HOST, MAX_BODY, PORT
from db import get_conn, init_db
from routes import ROUTES, Request, file_for


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")   # lets the HTML/JS frontend call the API
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(data)

    def _static(self, path):
        """Serve the frontend folder so http://127.0.0.1:8000 opens the app."""
        root = os.path.normpath(os.path.join(BASE_DIR, "..", "frontend"))
        rel = path.lstrip("/")
        if rel.startswith("frontend/"):
            rel = rel[len("frontend/"):]
        full = os.path.normpath(os.path.join(root, rel or "index.html"))
        if not full.startswith(root) or not os.path.isfile(full):
            return self._send(404, {"error": "Route not found"})
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(full)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _file(self, path, query):
        """Stream an uploaded video/PDF (supports seeking). Token comes in the URL so <video> can use it."""
        conn = get_conn()
        try:
            user = user_from_token(conn, query.get("token", ""))
            if not user:
                raise ApiError(401, "Please log in")
            full, name = file_for(conn, user, int(path.rsplit("/", 1)[1]))
        except ApiError as e:
            return self._send(e.status, {"error": e.message})
        finally:
            conn.close()
        size = os.path.getsize(full)
        start, end, rng = 0, size - 1, self.headers.get("Range", "")
        if rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start, end = int(a or 0), int(b) if b else size - 1
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type", mimetypes.guess_type(name)[0] or "application/octet-stream")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if rng:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with open(full, "rb") as f:
            f.seek(start)
            left = end - start + 1
            while left > 0:
                chunk = f.read(min(65536, left))
                if not chunk:
                    break
                self.wfile.write(chunk)
                left -= len(chunk)

    def _handle(self, method):
        parsed = urlparse(self.path)
        if method == "GET" and parsed.path.startswith("/files/"):
            return self._file(parsed.path, {k: v[0] for k, v in parse_qs(parsed.query).items()})
        if method == "GET" and not parsed.path.startswith("/api"):
            return self._static(parsed.path)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        match = None
        for m, pattern, fn, needs_auth in ROUTES:
            found = pattern.match(parsed.path)
            if m == method and found:
                match = (fn, found.groupdict(), needs_auth)
                break
        if not match:
            return self._send(404, {"error": "Route not found"})
        fn, params, needs_auth = match

        body, raw = {}, b""
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self._send(413, {"error": "Upload is too large"})
        if length:
            data = self.rfile.read(length)
            if self.headers.get("Content-Type", "application/json").startswith("application/json"):
                try:
                    body = json.loads(data.decode("utf-8"))
                    if not isinstance(body, dict):
                        raise ValueError
                except ValueError:
                    return self._send(400, {"error": "Body must be a JSON object"})
            else:
                raw = data   # file upload

        conn = get_conn()
        try:
            user = None
            if needs_auth:
                token = self.headers.get("Authorization", "").replace("Bearer ", "", 1).strip()
                user = user_from_token(conn, token)
                if not user:
                    raise ApiError(401, "Please log in")
            result = fn(Request(conn, user, body, query, params, raw))
            status, data = result if isinstance(result, tuple) else (200, result)
            conn.commit()
            self._send(status, data)
        except ApiError as e:
            conn.rollback()
            self._send(e.status, {"error": e.message})
        except Exception:
            conn.rollback()
            traceback.print_exc()
            self._send(500, {"error": "Server error"})
        finally:
            conn.close()

    def do_GET(self): self._handle("GET")
    def do_POST(self): self._handle("POST")
    def do_PUT(self): self._handle("PUT")
    def do_DELETE(self): self._handle("DELETE")

    def do_OPTIONS(self):
        self._send(204, {})

    def log_message(self, fmt, *args):
        print("%s %s" % (self.command, self.path))


def make_server(host=HOST, port=PORT):
    init_db()
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    server = make_server()
    print(f"Adaptive Learning API running at http://{HOST}:{PORT}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
