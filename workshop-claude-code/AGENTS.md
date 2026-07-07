# AGENTS.md — Workshop Claude Code

Panduan ini dibaca oleh AI coding agents (OpenAI Codex CLI, Claude Code, dll.)
sebelum menyentuh proyek ini. Ikuti instruksi di bawah dengan ketat.

---

## Gambaran Proyek

Landing page pendaftaran untuk event **Workshop Claude Code** — satu hari, Jakarta Selatan, 12 Juli 2026.
Stack: vanilla HTML + CSS + JavaScript (frontend) dan Python built-in `http.server` (backend lokal).
Tidak ada framework, tidak ada build step, tidak ada dependency eksternal.

---

## Struktur File

```
workshop-claude-code/
├── index.html              # Halaman utama (satu-satunya halaman)
├── style.css               # Semua styling — tema ungu gelap, WCAG AA
├── script.js               # Form logic: validasi, fetch API, tampilkan e-tiket
├── server.py               # Server lokal (static files + /api/daftar)
├── vercel.json             # Konfigurasi deploy Vercel
├── netlify.toml            # Konfigurasi deploy Netlify
├── api/
│   └── daftar.py           # Vercel serverless function
├── netlify/
│   └── functions/
│       └── daftar.py       # Netlify serverless function
└── data/
    └── registrations.json  # Data pendaftaran lokal (di-ignore oleh git)
```

---

## Cara Menjalankan Lokal

```bash
cd workshop-claude-code
python3 server.py
# Buka http://localhost:8773
```

Tidak perlu `npm install`, `pip install`, atau langkah build apapun.

---

## API Endpoint

### `POST /api/daftar`

**Request body (JSON):**
```json
{
  "nama": "string — nama lengkap peserta",
  "email": "string — alamat email valid",
  "jumlah_tiket": "integer — 1 sampai 10"
}
```

**Response sukses (200):**
```json
{ "success": true, "kode_tiket": "CCWS-XXXXXX" }
```

**Response error (400):**
```json
{ "error": "pesan error" }
```

Format kode tiket: `CCWS-` diikuti 6 karakter acak (huruf kapital + angka).

---

## Tema & Design Token

Semua warna didefinisikan sebagai CSS custom properties di `:root` dalam `style.css`.
**Jangan hardcode warna** — selalu gunakan variabel CSS.

| Variabel | Nilai | Dipakai untuk |
|---|---|---|
| `--color-bg` | `#0d0b14` | Background halaman |
| `--color-surface` | `#13101e` | Kartu, form |
| `--color-surface-2` | `#1c1829` | Input, price summary |
| `--color-accent` | `#7c3aed` | Tombol, focus ring |
| `--color-accent-light` | `#a78bfa` | Judul, harga, kode tiket |
| `--color-text` | `#ede9fe` | Teks utama |
| `--color-text-muted` | `#9384b0` | Teks sekunder, label |
| `--color-error` | `#f85149` | Pesan error validasi |
| `--color-success` | `#3fb950` | Status sukses |

Contrast ratio semua pasangan warna sudah memenuhi **WCAG 2.1 AA**.

---

## Konvensi Kode

### HTML
- Satu file (`index.html`) — jangan buat halaman baru kecuali diminta eksplisit
- Semua ID elemen yang diakses JS harus unik dan deskriptif

### CSS
- Gunakan CSS custom properties, bukan nilai literal
- Gunakan `clamp()` untuk font size responsif
- Breakpoint: `≤900px` (info cards 2 kolom), `≤768px` (layout 1 kolom)

### JavaScript
- Vanilla JS, tidak ada library/framework
- Semua DOM reference di-cache di atas file (`const form = document.getElementById(...)`)
- Validasi field menggunakan objek `validationRules` — tambah aturan baru di situ
- API call menggunakan `fetch` dengan `async/await`

### Python (server & functions)
- Tidak ada dependency eksternal — hanya Python standard library
- `server.py` untuk lokal; `api/daftar.py` untuk Vercel; `netlify/functions/daftar.py` untuk Netlify
- Format kode tiket dihasilkan oleh `generate_ticket_code()` — jangan ubah formatnya

---

## Aturan Penting

- **Jangan tambahkan library/framework** tanpa persetujuan eksplisit
- **Jangan ubah skema warna** — tema ungu gelap sudah final
- **Jangan sentuh `data/registrations.json`** — file ini di-generate saat runtime
- **Harga tiket** (`TICKET_PRICE = 50000`) dan **batas tiket** (`MAX_TICKETS = 10`) didefinisikan
  sebagai konstanta di `script.js` — ubah di sana jika perlu
- Setiap perubahan CSS harus bump versi di `<link rel="stylesheet" href="style.css?v=N" />`

---

## Deploy

| Platform | Cara | Root directory |
|---|---|---|
| **Lokal** | `python3 server.py` | `workshop-claude-code/` |
| **Vercel** | Push ke `main`, set Root Dir di dashboard | `workshop-claude-code` |
| **Netlify** | Push ke `main`, set Base Dir di dashboard | `workshop-claude-code` |

Setelah deploy ke Vercel/Netlify, API `/api/daftar` otomatis aktif via serverless function.
Data pendaftaran **tidak persisten** di cloud (filesystem ephemeral) — gunakan database eksternal
jika persistensi diperlukan.
