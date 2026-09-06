"""Pengujian unit untuk database.py."""

import time

import pytest

import database as db


# ==========================================================
# ENKRIPSI
# ==========================================================

class TestEnkripsi:

    def test_teks_pulang_utuh_setelah_dekripsi(self):
        asli = "Rapat memutuskan anggaran naik 12 persen."
        assert db.dekripsi_teks(db.enkripsi_teks(asli)) == asli

    def test_hasil_enkripsi_tidak_menyimpan_teks_asli(self):
        assert "anggaran" not in db.enkripsi_teks("pembahasan anggaran daerah")

    def test_nilai_kosong_ditangani(self):
        assert db.enkripsi_teks(None) is None
        assert db.dekripsi_teks(None) is None

    def test_kunci_salah_tidak_membuat_aplikasi_mati(self):
        hasil = db.dekripsi_teks("gAAAAABbukan_token_yang_sah")
        assert "Gagal Dekripsi" in hasil


# ==========================================================
# KATA SANDI
# ==========================================================

class TestKataSandi:

    def test_hash_memakai_format_pbkdf2(self):
        assert db.hash_password("RahasiaKu2026").startswith("pbkdf2_sha256$")

    def test_sandi_sama_menghasilkan_hash_berbeda(self):
        """Salt acak membuat dua hash tidak pernah kembar."""
        assert db.hash_password("sama123") != db.hash_password("sama123")

    def test_sandi_benar_diterima(self):
        h = db.hash_password("RahasiaKu2026")
        cocok, perlu_upgrade = db.cek_password("RahasiaKu2026", h)
        assert cocok is True
        assert perlu_upgrade is False

    def test_sandi_salah_ditolak(self):
        h = db.hash_password("RahasiaKu2026")
        assert db.cek_password("salah", h)[0] is False

    def test_hash_sha256_lama_masih_diterima(self):
        import hashlib
        lama = hashlib.sha256("sandilama".encode()).hexdigest()
        cocok, perlu_upgrade = db.cek_password("sandilama", lama)
        assert cocok is True
        assert perlu_upgrade is True

    def test_hash_rusak_tidak_membuat_error(self):
        assert db.cek_password("apa saja", "pbkdf2_sha256$rusak")[0] is False
        assert db.cek_password("apa saja", None)[0] is False

    @pytest.mark.parametrize("sandi,harusnya_valid", [
        ("RahasiaKu2026", True),
        ("abc12", False),
        ("", False),
    ])
    def test_aturan_panjang_minimum(self, sandi, harusnya_valid):
        assert db.validasi_password(sandi)[0] is harusnya_valid


# ==========================================================
# AUTENTIKASI
# ==========================================================

class TestAutentikasi:

    def test_login_berhasil(self, pegawai):
        assert db.verifikasi_login(pegawai, "RahasiaKu2026") is True

    def test_login_sandi_salah_ditolak(self, pegawai):
        assert db.verifikasi_login(pegawai, "SalahBesar") is False

    def test_akun_tidak_ada_ditolak(self):
        assert db.verifikasi_login("tidak_terdaftar", "apa saja") is False

    def test_masukan_kosong_ditolak(self):
        assert db.verifikasi_login("", "") is False
        assert db.verifikasi_login(None, None) is False

    def test_hash_lama_naik_otomatis_setelah_login(self):
        import hashlib
        with db.db() as conn:
            conn.execute(
                "INSERT INTO employees (nip, username, password_hash, nama) VALUES (?,?,?,?)",
                ("lama", "lama", hashlib.sha256("sandilama".encode()).hexdigest(), "Akun Lama")
            )
        assert db.verifikasi_login("lama", "sandilama") is True
        assert db.ambil_pegawai("lama")["password_hash"].startswith("pbkdf2_sha256$")
        assert db.verifikasi_login("lama", "sandilama") is True

    def test_ganti_sandi(self, pegawai):
        db.update_user_password(pegawai, "SandiBaru2026")
        assert db.verifikasi_login(pegawai, "SandiBaru2026") is True
        assert db.verifikasi_login(pegawai, "RahasiaKu2026") is False

    def test_username_berspasi_tetap_dikenali(self):
        db.simpan_pegawai("  spasi  ", "RahasiaKu2026")
        assert db.verifikasi_login("spasi", "RahasiaKu2026") is True


# ==========================================================
# OTP
# ==========================================================

class TestOTP:

    def test_kode_berupa_enam_angka(self, pegawai):
        kode, error = db.buat_otp(pegawai)
        assert error is None
        assert len(kode) == 6 and kode.isdigit()

    def test_kode_asli_tidak_tersimpan_di_database(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        with db.db() as conn:
            tersimpan = conn.execute("SELECT otp_hash FROM otp_reset").fetchone()[0]
        assert kode not in tersimpan

    def test_kode_benar_diterima(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        assert db.verifikasi_otp(pegawai, kode)[0] is True

    def test_kode_hanya_bisa_dipakai_sekali(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        db.verifikasi_otp(pegawai, kode)
        assert db.verifikasi_otp(pegawai, kode)[0] is False

    def test_kode_hangus_setelah_lima_kali_salah(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        for _ in range(db.OTP_MAKS_PERCOBAAN):
            db.verifikasi_otp(pegawai, "000000")
        berhasil, pesan = db.verifikasi_otp(pegawai, kode)
        assert berhasil is False
        assert "kode baru" in pesan.lower()

    def test_permintaan_dibatasi_per_jam(self, pegawai):
        for _ in range(db.OTP_MAKS_PER_JAM):
            db.buat_otp(pegawai)
        kode, error = db.buat_otp(pegawai)
        assert kode is None
        assert "terlalu sering" in error.lower()

    def test_kode_baru_menghanguskan_kode_lama(self, pegawai):
        kode_lama, _ = db.buat_otp(pegawai)
        db.buat_otp(pegawai)
        assert db.verifikasi_otp(pegawai, kode_lama)[0] is False

    def test_tanpa_kode_aktif_ditolak(self, pegawai):
        assert db.verifikasi_otp(pegawai, "123456")[0] is False


# ==========================================================
# RESET KATA SANDI
# ==========================================================

class TestResetKataSandi:

    def test_alur_lengkap_berhasil(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        berhasil, _ = db.reset_password_dengan_otp(pegawai, kode, "SandiBaru2026")
        assert berhasil is True
        assert db.verifikasi_login(pegawai, "SandiBaru2026") is True

    def test_sandi_baru_tidak_boleh_sama(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        berhasil, pesan = db.reset_password_dengan_otp(pegawai, kode, "RahasiaKu2026")
        assert berhasil is False
        assert "sama" in pesan.lower()

    def test_sandi_lemah_ditolak(self, pegawai):
        kode, _ = db.buat_otp(pegawai)
        assert db.reset_password_dengan_otp(pegawai, kode, "abc")[0] is False

    def test_kode_salah_menggagalkan_reset(self, pegawai):
        db.buat_otp(pegawai)
        assert db.reset_password_dengan_otp(pegawai, "999999", "SandiBaru2026")[0] is False
        assert db.verifikasi_login(pegawai, "RahasiaKu2026") is True


# ==========================================================
# ABSENSI
# ==========================================================

class TestAbsensi:

    def test_absen_masuk_tercatat(self, pegawai):
        db.catat_absensi(pegawai, kegiatan="Rapat Koordinasi")
        riwayat = db.riwayat_absensi(nip=pegawai)
        assert len(riwayat) == 1
        assert riwayat[0]["arah"] == "masuk"

    def test_absen_keluar_ditandai_berbeda(self, pegawai):
        db.catat_absensi(pegawai, is_logout=True)
        assert db.absensi_terakhir(pegawai)["arah"] == "keluar"

    def test_riwayat_terurut_dari_terbaru(self, pegawai):
        db.catat_absensi(pegawai, kegiatan="Pertama")
        time.sleep(1.05)
        db.catat_absensi(pegawai, kegiatan="Kedua")
        assert db.riwayat_absensi(nip=pegawai)[0]["kegiatan"] == "Kedua"

    def test_riwayat_tersaring_per_pegawai(self, pegawai):
        db.simpan_pegawai("pegawai_lain", "RahasiaKu2026")
        db.catat_absensi(pegawai)
        db.catat_absensi("pegawai_lain")
        assert len(db.riwayat_absensi(nip=pegawai)) == 1
        assert len(db.riwayat_absensi()) == 2

    def test_ekspor_menghasilkan_berkas_terenkripsi(self, pegawai, tmp_path):
        db.catat_absensi(pegawai, kegiatan="Rapat Koordinasi")
        path, jumlah = db.ekspor_absensi_terenkripsi(str(tmp_path / "arsip.csv"))
        isi = open(path, encoding="utf-8").read()
        assert jumlah == 1
        assert "Rapat Koordinasi" not in isi
        assert "gAAAAA" in isi


# ==========================================================
# NOTULENSI
# ==========================================================

class TestNotulensi:

    def test_simpan_dan_ambil_kembali(self, pegawai):
        nid = db.simpan_notulensi("Rapat Anggaran", "Isi transkrip rahasia.",
                                  dibuat_oleh=pegawai)
        assert db.ambil_notulensi(nid)["transkrip"] == "Isi transkrip rahasia."

    def test_transkrip_tersimpan_terenkripsi(self, pegawai):
        nid = db.simpan_notulensi("Rapat", "kata kunci rahasia", dibuat_oleh=pegawai)
        with db.db() as conn:
            mentah = conn.execute(
                "SELECT transkrip_enc FROM notulensi WHERE id=?", (nid,)).fetchone()[0]
        assert "rahasia" not in mentah

    def test_status_awal_adalah_draf(self, pegawai):
        nid = db.simpan_notulensi("Rapat", "isi", dibuat_oleh=pegawai)
        assert db.ambil_notulensi(nid)["status"] == "draft"

    def test_perbarui_judul(self, pegawai):
        nid = db.simpan_notulensi("Judul Lama", "isi", dibuat_oleh=pegawai)
        db.update_notulensi(nid, judul="Judul Baru")
        assert db.ambil_notulensi(nid)["judul"] == "Judul Baru"

    def test_daftar_tersaring_per_pembuat(self, pegawai):
        db.simpan_notulensi("Milik A", "isi", dibuat_oleh=pegawai)
        db.simpan_notulensi("Milik B", "isi", dibuat_oleh="orang_lain")
        assert len(db.daftar_notulensi(dibuat_oleh=pegawai)) == 1

    def test_hapus_notulensi(self, pegawai):
        nid = db.simpan_notulensi("Rapat", "isi", dibuat_oleh=pegawai)
        db.hapus_notulensi(nid)
        assert db.ambil_notulensi(nid) is None

    def test_id_tidak_ada_mengembalikan_none(self):
        assert db.ambil_notulensi(99999) is None


# ==========================================================
# BERITA PUBLIK
# ==========================================================

class TestBeritaPublik:

    def test_publikasi_mengubah_status_notulensi(self, pegawai):
        nid = db.simpan_notulensi("Rapat", "isi", dibuat_oleh=pegawai)
        db.publish_notulensi("Rapat", "Aula", "poin", "artikel", pegawai, notulensi_id=nid)
        assert db.ambil_notulensi(nid)["status"] == "published"

    def test_berita_terhubung_ke_notulensi(self, pegawai):
        nid = db.simpan_notulensi("Rapat", "isi", dibuat_oleh=pegawai)
        db.publish_notulensi("Rapat", "Aula", "poin", "artikel", pegawai, notulensi_id=nid)
        assert db.load_published_data()[0]["notulensi_id"] == nid

    def test_perbarui_dan_hapus_berita(self, pegawai):
        bid = db.publish_notulensi("Rapat", "Aula", "poin", "artikel", pegawai)
        db.update_berita(bid, judul="Judul Revisi")
        assert db.load_published_data()[0]["judul"] == "Judul Revisi"
        db.hapus_berita(bid)
        assert db.load_published_data() == []


# ==========================================================
# SKEMA
# ==========================================================

class TestSkema:

    def test_seluruh_tabel_terbentuk(self):
        with db.db() as conn:
            tabel = {r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"employees", "attendance", "notulensi",
                "published_news", "otp_reset"} <= tabel

    def test_versi_skema_terbaru(self):
        with db.db() as conn:
            assert conn.execute("PRAGMA user_version").fetchone()[0] == db.SKEMA_VERSI

    def test_init_db_aman_dipanggil_berulang(self):
        db.init_db()
        db.init_db()
        with db.db() as conn:
            assert conn.execute("PRAGMA user_version").fetchone()[0] == db.SKEMA_VERSI

    def test_nip_dan_username_unik(self, pegawai):
        db.simpan_pegawai(pegawai, "SandiLain2026")
        with db.db() as conn:
            assert conn.execute(
                "SELECT COUNT(*) FROM employees WHERE username=?", (pegawai,)
            ).fetchone()[0] == 1

    def test_statistik_menghitung_benar(self, pegawai):
        db.catat_absensi(pegawai)
        db.simpan_notulensi("Rapat", "isi", dibuat_oleh=pegawai)
        stat = db.statistik_dashboard()
        assert stat["total_pegawai"] == 1
        assert stat["total_absensi"] == 1
        assert stat["total_notulensi"] == 1


# ==========================================================
# PENCARIAN PEGAWAI LEWAT EMAIL (baru di skema versi 5)
# ==========================================================

class TestCariLewatEmail:

    def test_email_terdaftar_ditemukan(self, pegawai):
        assert db.ambil_pegawai_by_email("uji@contoh.go.id")["username"] == pegawai

    def test_pencocokan_abai_huruf_besar_kecil(self, pegawai):
        assert db.ambil_pegawai_by_email("UJI@CONTOH.GO.ID") is not None

    def test_spasi_berlebih_dipangkas(self, pegawai):
        assert db.ambil_pegawai_by_email("  uji@contoh.go.id  ") is not None

    def test_email_tidak_terdaftar_mengembalikan_none(self):
        assert db.ambil_pegawai_by_email("bukan@siapa.com") is None

    def test_masukan_kosong_ditangani(self):
        assert db.ambil_pegawai_by_email("") is None
        assert db.ambil_pegawai_by_email(None) is None

    def test_email_kembar_mengembalikan_akun_terlama(self):
        """Kolom email tidak unik, jadi urutan hasilnya harus dapat diprediksi."""
        db.simpan_pegawai("kembar_a", "RahasiaKu2026", email="sama@dinas.go.id")
        db.simpan_pegawai("kembar_b", "RahasiaKu2026", email="sama@dinas.go.id")
        assert db.ambil_pegawai_by_email("sama@dinas.go.id")["username"] == "kembar_a"
