"""Pengujian unit untuk email_service.py.

Tidak ada email sungguhan yang dikirim. Pengujian pengiriman memakai
tiruan (mock) agar tidak bergantung pada jaringan atau akun Gmail.
"""

import smtplib
from unittest.mock import patch, MagicMock

import pytest

import email_service as mail


class TestValidasiAlamat:

    @pytest.mark.parametrize("alamat,valid", [
        ("budi@gmail.com", True),
        ("staf.tu@setda.go.id", True),
        ("tanpa-at.com", False),
        ("spasi di@mail.com", False),
        ("kosong@", False),
        ("", False),
        (None, False),
    ])
    def test_deteksi_alamat_tidak_sah(self, alamat, valid):
        assert mail.email_valid(alamat) is valid


class TestPenyamaranAlamat:

    def test_bagian_tengah_disamarkan(self):
        hasil = mail.samarkan_email("budi.santoso@gmail.com")
        assert hasil.startswith("bu")
        assert hasil.endswith("@gmail.com")
        assert "santoso" not in hasil

    def test_nama_sangat_pendek_tetap_disamarkan(self):
        for alamat in ["ab@dinas.go.id", "x@y.id"]:
            hasil = mail.samarkan_email(alamat)
            assert "*" in hasil
            assert hasil.endswith("@" + alamat.split("@")[1])

    def test_alamat_tidak_sah_tidak_bocor(self):
        assert mail.samarkan_email("bukan-email") == "email tidak diketahui"


class TestTemplat:

    def test_kode_muncul_di_kedua_versi(self):
        html, teks = mail.template_otp("143077", "Budi")
        assert "143077" in html
        assert "143077" in teks

    def test_peringatan_keamanan_disertakan(self):
        html, teks = mail.template_otp("123456", "Budi")
        assert "jangan teruskan" in html.lower()
        assert "jangan teruskan" in teks.lower()

    def test_html_utuh_sebagai_dokumen(self):
        html, _ = mail.template_otp("123456", "Budi")
        assert html.startswith("<!DOCTYPE html>")
        assert html.rstrip().endswith("</html>")

    def test_templat_konfirmasi_memuat_waktu(self):
        html, teks = mail.template_konfirmasi_reset("Budi", "02 September 2026 20:34")
        assert "20:34" in html
        assert "Budi" in teks

    def test_pratinjau_menghasilkan_berkas(self, tmp_path):
        path = mail.pratinjau(str(tmp_path / "pratinjau.html"))
        assert "Kode Verifikasi" in open(path, encoding="utf-8").read()


class TestKonfigurasi:

    def test_kredensial_kosong_terdeteksi(self):
        with patch.object(mail, "SMTP_EMAIL", ""), patch.object(mail, "SMTP_PASSWORD", ""):
            siap, pesan = mail.konfigurasi_siap()
            assert siap is False
            assert "SMTP_EMAIL" in pesan

    def test_alamat_pengirim_tidak_sah_terdeteksi(self):
        with patch.object(mail, "SMTP_EMAIL", "bukan-email"), \
             patch.object(mail, "SMTP_PASSWORD", "x" * 16):
            assert mail.konfigurasi_siap()[0] is False

    def test_konfigurasi_lengkap_lolos(self):
        with patch.object(mail, "SMTP_EMAIL", "bot@gmail.com"), \
             patch.object(mail, "SMTP_PASSWORD", "x" * 16):
            assert mail.konfigurasi_siap()[0] is True


class TestPengiriman:

    def test_gagal_bila_kredensial_belum_diisi(self):
        with patch.object(mail, "SMTP_EMAIL", ""), patch.object(mail, "SMTP_PASSWORD", ""):
            berhasil, pesan = mail.kirim_otp("tujuan@gmail.com", "123456", "Budi")
            assert berhasil is False
            assert "belum diatur" in pesan

    def test_alamat_tujuan_tidak_sah_ditolak(self):
        with patch.object(mail, "SMTP_EMAIL", "bot@gmail.com"), \
             patch.object(mail, "SMTP_PASSWORD", "x" * 16):
            assert mail.kirim_otp("bukan-email", "123456", "Budi")[0] is False

    def test_pengiriman_berhasil(self):
        server = MagicMock()
        with patch.object(mail, "SMTP_EMAIL", "bot@gmail.com"), \
             patch.object(mail, "SMTP_PASSWORD", "x" * 16), \
             patch("smtplib.SMTP", return_value=server):
            berhasil, _ = mail.kirim_otp("tujuan@gmail.com", "123456", "Budi")
            assert berhasil is True
            server.sendmail.assert_called_once()
            tujuan = server.sendmail.call_args[0][1]
            assert tujuan == "tujuan@gmail.com"

    def test_pesan_jelas_saat_app_password_salah(self):
        server = MagicMock()
        server.login.side_effect = smtplib.SMTPAuthenticationError(535, b"denied")
        with patch.object(mail, "SMTP_EMAIL", "bot@gmail.com"), \
             patch.object(mail, "SMTP_PASSWORD", "salah"), \
             patch("smtplib.SMTP", return_value=server):
            berhasil, pesan = mail.kirim_otp("tujuan@gmail.com", "123456", "Budi")
            assert berhasil is False
            assert "App Password" in pesan

    def test_jaringan_putus_tidak_membuat_error_tak_tertangani(self):
        with patch.object(mail, "SMTP_EMAIL", "bot@gmail.com"), \
             patch.object(mail, "SMTP_PASSWORD", "x" * 16), \
             patch("smtplib.SMTP", side_effect=OSError("tidak ada koneksi")):
            assert mail.kirim_otp("tujuan@gmail.com", "123456", "Budi")[0] is False
