"""
reset_password_ui.py — Alur "Lupa Kata Sandi" untuk GovScribe (TANPA OTP)

Menggantikan blok lupa password di notelensi_pemerintah.py (baris 671-745).
Cukup panggil satu fungsi:

    import reset_password_ui
    ...
    if st.session_state.get("show_forgot_pass"):
        reset_password_ui.render()
        st.stop()

Dua tahap (OTP dihapus atas permintaan, supaya tidak bergantung ke SMTP):
    1. verifikasi_akun -> masukkan NIP/Username DAN Email, keduanya harus
                          cocok dengan satu akun yang sama di database
    2. sandi_baru       -> tentukan kata sandi baru

PERINGATAN KEAMANAN:
    Versi ini TIDAK mengirim kode verifikasi ke email. Siapa pun yang tahu
    NIP/username dan email seseorang bisa mereset password akun itu tanpa
    perlu akses ke email sungguhan. Cocok untuk demo/latihan, tapi kurang
    aman untuk pemakaian produksi sungguhan. Kalau nanti SMTP sudah beres
    dan mau kembali ke alur OTP, tinggal pakai versi reset_password_ui.py
    sebelumnya (yang memanggil db.buat_otp / db.verifikasi_otp).

Semua state disimpan dengan awalan "rp_" supaya tidak bentrok dengan
session_state yang sudah ada di file utama.
"""

from datetime import datetime

import streamlit as st

import database as db
import email_service as mail

# Kalau True, sistem tidak memberi tahu secara spesifik apakah NIP/username
# atau email yang salah. Ubah ke False kalau mau pesan error lebih detail
# saat uji coba.
SEMBUNYIKAN_KEBERADAAN_AKUN = True


# ==========================================================
# STATE
# ==========================================================

def _init_state():
    default = {
        "rp_tahap": "verifikasi_akun",
        "rp_username": "",
        "rp_akun_terverifikasi": False,
        "rp_pesan": None,      # (jenis, teks) -> jenis: info | sukses | error
    }
    for kunci, nilai in default.items():
        st.session_state.setdefault(kunci, nilai)


def reset_state():
    for kunci in list(st.session_state.keys()):
        if kunci.startswith("rp_"):
            del st.session_state[kunci]


def _pesan(jenis, teks):
    st.session_state["rp_pesan"] = (jenis, teks)


def _tampilkan_pesan():
    data = st.session_state.get("rp_pesan")
    if not data:
        return
    jenis, teks = data
    {"sukses": st.success, "error": st.error}.get(jenis, st.info)(teks)
    st.session_state["rp_pesan"] = None


# ==========================================================
# TAMPILAN
# ==========================================================

def _tahap_verifikasi_akun():
    st.subheader("Lupa Kata Sandi")
    st.caption("Masukkan NIP/Username DAN alamat email yang terdaftar pada akun "
               "Anda. Keduanya harus cocok dengan data yang tersimpan.")

    username_input = st.text_input("NIP / Username", key="rp_input_username",
                                   placeholder="contoh: pns_19850110")
    email_input = st.text_input("Alamat Email", key="rp_input_email",
                                placeholder="nama@instansi.go.id")

    kolom_verifikasi, kolom_batal = st.columns(2)

    with kolom_verifikasi:
        if st.button("Verifikasi Akun", type="primary", use_container_width=True):
            username_bersih = (username_input or "").strip()
            email_bersih = (email_input or "").strip()

            pesan_gagal = ("NIP/Username dan Email tidak cocok dengan data yang "
                          "terdaftar. Periksa kembali kedua isian tersebut.")

            if not username_bersih or not email_bersih:
                _pesan("error", "NIP/Username dan Email wajib diisi.")
            else:
                pegawai = db.ambil_pegawai(username_bersih)
                cocok = (
                    pegawai is not None
                    and (pegawai.get("email") or "").strip().lower() == email_bersih.lower()
                )
                if cocok:
                    st.session_state["rp_username"] = pegawai["username"]
                    st.session_state["rp_akun_terverifikasi"] = True
                    st.session_state["rp_tahap"] = "sandi_baru"
                    _pesan("sukses", "Akun terverifikasi. Silakan buat kata sandi baru.")
                else:
                    if SEMBUNYIKAN_KEBERADAAN_AKUN:
                        _pesan("error", pesan_gagal)
                    else:
                        _pesan("error", "NIP/Username tidak ditemukan atau email tidak cocok.")
            st.rerun()

    with kolom_batal:
        if st.button("Kembali ke Login", use_container_width=True):
            reset_state()
            st.session_state["show_forgot_pass"] = False
            st.rerun()


def _tahap_sandi_baru():
    st.subheader("Buat Kata Sandi Baru")
    st.caption(f"Minimal {db.PASSWORD_MIN_PANJANG} karakter. Password boleh berisi huruf, angka, spasi, dan simbol.")

    sandi = st.text_input("Kata Sandi Baru", type="password", key="rp_sandi1")
    ulangi = st.text_input("Ulangi Kata Sandi", type="password", key="rp_sandi2")

    if sandi:
        valid, catatan = db.validasi_password(sandi)
        (st.success if valid else st.warning)(catatan)

    if st.button("Simpan Kata Sandi", type="primary", use_container_width=True):
        if not st.session_state.get("rp_akun_terverifikasi"):
            _pesan("error", "Sesi verifikasi tidak valid. Silakan ulangi dari awal.")
            st.session_state["rp_tahap"] = "verifikasi_akun"
            st.rerun()

        if sandi != ulangi:
            _pesan("error", "Konfirmasi kata sandi tidak cocok.")
            st.rerun()

        valid, catatan = db.validasi_password(sandi)
        if not valid:
            _pesan("error", catatan)
            st.rerun()

        username = st.session_state["rp_username"]
        pegawai = db.ambil_pegawai(username)

        if pegawai is None:
            _pesan("error", "Akun tidak ditemukan. Silakan ulangi dari awal.")
            st.session_state["rp_tahap"] = "verifikasi_akun"
            st.rerun()

        sama, _ = db.cek_password(sandi, pegawai["password_hash"])
        if sama:
            _pesan("error", "Kata sandi baru tidak boleh sama dengan yang lama.")
            st.rerun()

        db.update_user_password(username, sandi)

        # Coba beri tahu pemilik akun lewat email kalau SMTP tersedia.
        # Kalau SMTP belum diatur / gagal kirim, proses ganti password tetap
        # dianggap berhasil -- pemberitahuan email di sini murni bonus,
        # bukan syarat.
        try:
            if mail.email_valid(pegawai.get("email")):
                mail.kirim_konfirmasi_reset(
                    pegawai["email"],
                    pegawai.get("nama") or username,
                    datetime.now().strftime("%d %B %Y %H:%M"),
                )
        except Exception:
            pass

        reset_state()
        st.session_state["show_forgot_pass"] = False
        st.session_state["rp_pesan"] = ("sukses", "Kata sandi berhasil diperbarui. "
                                                  "Silakan login dengan kata sandi baru.")
        st.rerun()

    if st.button("Batalkan"):
        reset_state()
        st.session_state["show_forgot_pass"] = False
        st.rerun()


def render():
    """Titik masuk tunggal. Panggil ini menggantikan blok lupa password lama."""
    _init_state()
    _tampilkan_pesan()

    tahap = st.session_state["rp_tahap"]
    urutan = {"verifikasi_akun": 1, "sandi_baru": 2}
    st.progress(urutan[tahap] / 2, text=f"Langkah {urutan[tahap]} dari 2")

    if tahap == "verifikasi_akun":
        _tahap_verifikasi_akun()
    else:
        _tahap_sandi_baru()