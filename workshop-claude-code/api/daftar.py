"""
Vercel serverless function — POST /api/daftar
Menerima data pendaftaran, mengembalikan kode tiket unik.
Catatan: filesystem Vercel bersifat read-only; data tidak disimpan ke file di production.
"""

from http.server import BaseHTTPRequestHandler
import json
import random
import string


def generate_ticket_code():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'CCWS-{suffix}'


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            length  = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
            nama         = str(payload.get('nama',  '')).strip()
            email        = str(payload.get('email', '')).strip()
            jumlah_tiket = int(payload.get('jumlah_tiket', 0))
        except (json.JSONDecodeError, ValueError):
            self._respond(400, {'error': 'Format data tidak valid.'})
            return

        if not nama or not email or not (1 <= jumlah_tiket <= 10):
            self._respond(400, {'error': 'Data tidak lengkap atau tidak valid.'})
            return

        kode_tiket = generate_ticket_code()
        self._respond(200, {'success': True, 'kode_tiket': kode_tiket})

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _respond(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type',   'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
