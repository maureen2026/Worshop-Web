"""
Netlify serverless function — POST /api/daftar
Format handler(event, context) sesuai Netlify Python runtime.
"""

import json
import random
import string


def generate_ticket_code():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'CCWS-{suffix}'


def handler(event, context):
    # Hanya terima POST
    if event.get('httpMethod') != 'POST':
        return {'statusCode': 405, 'body': json.dumps({'error': 'Method not allowed.'})}

    try:
        payload      = json.loads(event.get('body') or '{}')
        nama         = str(payload.get('nama',  '')).strip()
        email        = str(payload.get('email', '')).strip()
        jumlah_tiket = int(payload.get('jumlah_tiket', 0))
    except (json.JSONDecodeError, ValueError):
        return {'statusCode': 400, 'body': json.dumps({'error': 'Format data tidak valid.'})}

    if not nama or not email or not (1 <= jumlah_tiket <= 10):
        return {'statusCode': 400, 'body': json.dumps({'error': 'Data tidak lengkap atau tidak valid.'})}

    kode_tiket = generate_ticket_code()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'success': True, 'kode_tiket': kode_tiket}),
    }
