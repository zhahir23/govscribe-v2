"""
Konfigurasi pytest untuk GovScribe.

Berkas ini dijalankan pytest SEBELUM modul apa pun diimpor, sehingga
environment variable di bawah sempat terpasang lebih dulu. Ini penting
karena database.py membaca lokasi database dan kunci enkripsi pada saat
modul diimpor, bukan saat fungsinya dipanggil.

Efeknya: seluruh pengujian memakai database sementara di folder temp dan
tidak pernah menyentuh govscribe.db milik pengguna.
"""

import os
import tempfile

from cryptography.fernet import Fernet

_TMP = tempfile.mkdtemp(prefix="govscribe_uji_")
os.environ["GOVSCRIBE_DB"] = os.path.join(_TMP, "uji.db")
os.environ["GOVSCRIBE_KEY"] = Fernet.generate_key().decode()
os.environ.setdefault("SMTP_EMAIL", "")
os.environ.setdefault("SMTP_PASSWORD", "")

import pytest

import database as db


@pytest.fixture(autouse=True)
def database_bersih():
    """Kosongkan seluruh tabel sebelum tiap pengujian agar saling bebas."""
    db.init_db()
    with db.db() as conn:
        for tabel in ["attendance", "notulensi", "published_news", "otp_reset", "employees"]:
            conn.execute(f"DELETE FROM {tabel}")
    yield


@pytest.fixture
def pegawai():
    """Satu akun pegawai siap pakai."""
    db.simpan_pegawai("uji_pns", "RahasiaKu2026", nip="uji_pns",
                      nama="Pegawai Uji", email="uji@contoh.go.id")
    return "uji_pns"
