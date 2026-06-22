/* ============================================
   Workshop Claude Code — Form Logic
   Tanggung jawab:
   1. Tampilkan & perbarui total harga secara real-time
   2. Validasi field Nama, Email, dan Jumlah Tiket sebelum submit
   3. POST ke /api/daftar dan tampilkan kode tiket dari respons
   ============================================ */

const TICKET_PRICE = 50000;
const MIN_TICKETS  = 1;
const MAX_TICKETS  = 10;

// ── Referensi elemen DOM ──────────────────────
const form         = document.getElementById('registrationForm');
const nameInput    = document.getElementById('name');
const emailInput   = document.getElementById('email');
const ticketsInput = document.getElementById('tickets');
const priceDisplay = document.getElementById('priceDisplay');
const submitBtn    = document.getElementById('submitBtn');
const successState = document.getElementById('successState');
const ticketCode   = document.getElementById('ticketCode');
const ticketName   = document.getElementById('ticketName');
const ticketQty    = document.getElementById('ticketQty');
const qrCode       = document.getElementById('qrCode');


// ── Format angka ke Rupiah ────────────────────
function formatRupiah(amount) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(amount);
}

// ── Kalkulasi harga ───────────────────────────
function updatePrice() {
  const qty   = parseInt(ticketsInput.value, 10);
  const valid = !isNaN(qty) && qty >= MIN_TICKETS && qty <= MAX_TICKETS;
  priceDisplay.textContent = valid ? formatRupiah(qty * TICKET_PRICE) : '—';
}

ticketsInput.addEventListener('input', updatePrice);
updatePrice();


// ── Validasi field ────────────────────────────
const validationRules = {
  name(value) {
    if (!value.trim())           return 'Nama tidak boleh kosong.';
    if (value.trim().length < 2) return 'Nama terlalu pendek.';
    return '';
  },
  email(value) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!value.trim())        return 'Email tidak boleh kosong.';
    if (!pattern.test(value)) return 'Format email tidak valid.';
    return '';
  },
  tickets(value) {
    if (value === '' || value === null) return 'Jumlah tiket tidak boleh kosong.';
    const qty = parseInt(value, 10);
    if (isNaN(qty))        return 'Jumlah tiket harus berupa angka.';
    if (qty < MIN_TICKETS) return `Jumlah tiket minimal ${MIN_TICKETS}.`;
    if (qty > MAX_TICKETS) return `Jumlah tiket maksimal ${MAX_TICKETS}.`;
    return '';
  },
};

function validateField(input) {
  const rule    = validationRules[input.id];
  const errorEl = document.getElementById(input.id + 'Error');
  const message = rule ? rule(input.value) : '';

  if (message) {
    input.classList.add('error');
    errorEl.textContent = message;
    errorEl.classList.add('visible');
    return false;
  }

  input.classList.remove('error');
  errorEl.classList.remove('visible');
  return true;
}

[nameInput, emailInput, ticketsInput].forEach(el => {
  el.addEventListener('blur',  ()  => validateField(el));
  el.addEventListener('input', ()  => { if (el.classList.contains('error')) validateField(el); });
});


// ── Submit form → POST /api/daftar ───────────
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const nameOk    = validateField(nameInput);
  const emailOk   = validateField(emailInput);
  const ticketsOk = validateField(ticketsInput);
  if (!nameOk || !emailOk || !ticketsOk) return;

  submitBtn.disabled    = true;
  submitBtn.textContent = 'Memproses...';

  try {
    const res  = await fetch('/api/daftar', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        nama:         nameInput.value.trim(),
        email:        emailInput.value.trim(),
        jumlah_tiket: parseInt(ticketsInput.value, 10),
      }),
    });

    const data = await res.json();

    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Terjadi kesalahan pada server.');
    }

    // Isi e-tiket dengan data peserta + QR code dari api.qrserver.com
    const qty = parseInt(ticketsInput.value, 10);
    ticketName.textContent = nameInput.value.trim();
    ticketQty.textContent  = `${qty} tiket`;
    ticketCode.textContent = data.kode_tiket;
    qrCode.src = `https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(data.kode_tiket)}&format=png&qzone=1`;

    form.style.display = 'none';
    successState.classList.add('visible');

  } catch (err) {
    // Tampilkan error di bawah tombol tanpa me-reset form
    submitBtn.disabled    = false;
    submitBtn.textContent = 'Beli Tiket →';

    let apiError = document.getElementById('apiError');
    if (!apiError) {
      apiError    = document.createElement('p');
      apiError.id = 'apiError';
      apiError.classList.add('field-error', 'visible');
      apiError.style.textAlign = 'center';
      apiError.style.marginTop = '8px';
      submitBtn.after(apiError);
    }
    apiError.textContent = `Gagal: ${err.message}`;
  }
});
