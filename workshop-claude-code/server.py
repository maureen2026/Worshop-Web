#!/usr/bin/env python3
"""
Workshop Claude Code — Backend Server
Serves static files from this directory + handles POST /api/daftar.
Run: python3 server.py
"""

import datetime
import json
import os
import random
import string
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT      = 8773
DATA_FILE = Path(__file__).parent / 'data' / 'registrations.json'


def generate_ticket_code():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'CCWS-{suffix}'


def load_registrations():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    return []


def save_registration(record):
    DATA_FILE.parent.mkdir(exist_ok=True)
    registrations = load_registrations()
    registrations.append(record)
    DATA_FILE.write_text(
        json.dumps(registrations, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )


class Handler(SimpleHTTPRequestHandler):

    # ── API ───────────────────────────────────────
    def do_POST(self):
        if self.path != '/api/daftar':
            self._json(404, {'error': 'Endpoint tidak ditemukan.'})
            return

        length = int(self.headers.get('Content-Length', 0))
        try:
            payload       = json.loads(self.rfile.read(length))
            nama          = str(payload.get('nama',  '')).strip()
            email         = str(payload.get('email', '')).strip()
            jumlah_tiket  = int(payload.get('jumlah_tiket', 0))
        except (json.JSONDecodeError, ValueError):
            self._json(400, {'error': 'Format data tidak valid.'})
            return

        if not nama or not email or not (1 <= jumlah_tiket <= 10):
            self._json(400, {'error': 'Data tidak lengkap atau tidak valid.'})
            return

        kode_tiket = generate_ticket_code()
        save_registration({
            'kode_tiket':   kode_tiket,
            'nama':         nama,
            'email':        email,
            'jumlah_tiket': jumlah_tiket,
            'timestamp':    datetime.datetime.now().isoformat(timespec='seconds'),
        })

        self._json(200, {'success': True, 'kode_tiket': kode_tiket})

    # ── Static files (GET/HEAD handled by parent) ─
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def _json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, fmt, *args):
        # Hanya log request API dan error agar terminal tidak berisik
        line = args[0] if args else ''
        if '/api/' in line or (args[1:] and args[1] not in ('200', '304')):
            super().log_message(fmt, *args)


if __name__ == '__main__':
    os.chdir(Path(__file__).parent)   # root untuk file statis
    DATA_FILE.parent.mkdir(exist_ok=True)
    print(f'✓ Server berjalan → http://localhost:{PORT}')
    print(f'✓ Data disimpan  → {DATA_FILE}')
    HTTPServer(('', PORT), Handler).serve_forever()
