 GovScribe   
  *Portal informasi rapat pemerintah daerah*

\[LiveDemo\]  
([https://govscribe-v2-mp3afgk8abxvrndh38s8my.streamlit.app/](https://govscribe-v2-mp3afgk8abxvrndh38s8my.streamlit.app/)) 

Github : ([https://github.com/zhahir23/govscribe-v2/settings/access](https://github.com/zhahir23/govscribe-v2)) 

\[License\]  
([https://github.com/zhahir23/govscribe-v2/blob/main/LICENSE](https://github.com/zhahir23/govscribe-v2/blob/main/LICENSE))  
(LICENSE) 

Submission for ITECHNO CUP 2026 \- Web Development 

 DevSpectra

\#\# 📋 Daftar Isi

[**\#\# 👥 Tim Developer	2**](###-👥-tim-developer)

[**\#\# 🎯Tentang Proyek	3**](###-🎯tentang-proyek)

[**\#\# ✨ Fitur Unggulan	7**](###-✨-fitur-unggulan)

[**\#\# 📸 Demo & Screenshot	8**](###-📸-demo-&-screenshot)

[**\#\# 🛠️ Teknologi	15**](###-🛠️-teknologi)

[**\#\# 🏗️ Arsitektur Sistem	18**](###-🏗️-arsitektur-sistem)

[Penjelasan Relasi Tabel Database:	19](#penjelasan-relasi-tabel-database:)

[**\#\# ⚙️ Instalasi & Setup	22**](###-⚙️-instalasi-&-setup)

[**\#\# 🚀 Penggunaan	25**](###-🚀-penggunaan)

[**\#\# 📚 API Documentation	27**](###-📚-api-documentation)

[**\#\# 🧪 Testing	29**](###-🧪-testing)

[**\#\# 📄 Lisensi	31**](###-📄-lisensi)

\---

# \#\# 👥 Tim Developer

**Karol Efrido Sanggam Purba** | Project Lead & Backend Developer |   
Github : [https://github.com/KEvisual](https://github.com/KEvisual)

**Zhahir Furqon**  | Front End  
Github : [https://github.com/zhahir23](https://github.com/zhahir23)

**Bagus Adi Wibowo**  | Backend Developer |  
Github : [https://github.com/bagusaw0983](https://github.com/bagusaw0983)

\---

# \#\# 🎯Tentang Proyek

\#\#\# Latar Belakang

Dalam tata kelola pemerintahan yang modern, rapat koordinasi, pleno, dan evaluasi lintas sektor merupakan instrumen vital dalam merumuskan kebijakan publik serta menyelaraskan alur kerja birokrasi. Namun, efisiensi operasional di tingkat administrasi publik kerap terhambat oleh proses dokumentasi yang masih bersifat manual. Saat ini, penyusunan notulensi rapat di berbagai instansi pemerintahan masih mengandalkan staf administrasi untuk mendengarkan rekaman audio berdurasi 2 hingga 4 jam secara berulang kali. Proses pengetikan transkrip secara manual ini menyita waktu 1 hingga 2 hari kerja hanya untuk merampungkan satu dokumen rapat resmi.  
Keterlambatan dalam penyusunan notulensi berampak langsung pada lambatnya distribusi ringkasan keputusan rapat dan lembar *Action Items*. Akibatnya, eksekusi kebijakan publik maupun instruksi kerja antardinas kerap mengalami penundaan. Di sisi lain, akumulasi file audio mentah berukuran besar (.wav/.mp3) pada server lokal instansi menciptakan masalah akumulasi sampah digital (*digital waste*). Tanpa adanya konversi ke dalam teks yang terstruktur, kapasitas penyimpanan server cepat penuh dan menyulitkan proses audit data di masa mendatang.  
Untuk mengatasi keterbatasan waktu tersebut, sebagian staf berinisiatif menggunakan platform AI transkripsi komersial berbasis web gratis. Kendati menawarkan kemudahan, praktik ini menimbulkan risiko kerentanan keamanan yang sangat serius bagi instansi publik. Penggunaan platform cloud publik pihak ketiga berpotensi menyebabkan kebocoran materi rapat rahasia negara ke server luar negeri. Selain itu, solusi komersial luar negeri umumnya tidak dioptimalkan untuk mengenali akronim maupun terminologi birokrasi Indonesia (seperti *ASN, Bappeda,* atau *Pemkot*), sehingga menghasilkan tingkat kesalahan transkripsi yang tinggi.  
Guna menjawab tantangan efisiensi, akurasi, dan keamanan data tersebut, dikembangkan sebuah inovasi berbasis perangkat lunak murni yang diberi nama **GovScribe-Pipeline**. Sistem ini memanfaatkan arsitektur *pipeline* Python terintegrasi yang menggabungkan *Speech-to-Text* (STT) berbasis OpenAI Whisper, pemrosesan bahasa alami (*Natural Language Processing*/NLP), serta enkripsi kriptografi tingkat tinggi secara *on-premise*. 

\#\#\# Solusi yang Ditawarkan

1. **Status Realisasi & Prototipe Sistem (Minimum Viable Product / MVP)**

   
Sebagai wujud realisasi nyata dari gagasan ini, GovScribe-Pipeline telah diwujudkan dalam bentuk prototipe aplikasi web (MVP) berbasis Python dan Streamlit yang berfungsi secara end-to-end. Prototipe yang telah dibangun meliputi:  
   
·         Antarmuka Web Streamlit (Functional UI): Dasbor interaktif untuk mengunggah file audio rapat (.mp3/.wav), memilih mode transkripsi, serta menampilkan kemajuan pemrosesan secara real-time.  
   
·         Integrasi Core AI Engine (STT & NLP): Pemanfaatan pipeline lokal OpenAI Whisper untuk ekstraksi suara ke teks serta modul NLP untuk pengelompokan otomatis poin pembahasan, keputusan, dan Action Items.  
   
·         Otomatisasi Generator Dokumen (.docx): Fungsi ekspor otomatis yang langsung memetakan teks hasil ekstraksi ke dalam templat dokumen notulensi formal.

.      Sistem Proteksi Lokal: Penerapan modul enkripsi dasar berbasis enkripsi file lokal (Data-at-Rest) untuk memastikan aspek keamanan on-premise sudah berjalan sejak tahap prototipe.

**2 Arsitektur Sistem dan Metode Eksekusi Program**  
   
Solusi yang diusulkan adalah mengembangkan sebuah sistem pipeline perangkat lunak (aplikasi web internal) murni menggunakan bahasa pemrograman Python dan framework Streamlit untuk mengotomatiskan konversi audio menjadi dokumen notulensi formal. Metode eksekusi program dibagi menjadi 4 tahapan berbasis kode:  
 

1. **Modul Audio Ingestion (Python standard library)**: Menyediakan fitur unggah file audio rapat (.mp3, .wav, atau .m4a) melalui antarmuka web Streamlit. Sistem akan otomatis melakukan kompresi ukuran file dan normalisasi audio di latar belakang agar siap diproses.  
      
2. **Modul Speech-to-Text (STT Engine)**: Mengintegrasikan model kecerdasan buatan OpenAI Whisper secara lokal (diinstal di server internal instansi). Python akan mengeksekusi konversi audio menjadi teks mentah (raw transcript) lengkap dengan penanda waktu (timestamp).  
      
3. **Modul Pemrosesan Bahasa Alami (NLP Processor)**: Teks mentah diolah menggunakan teknik Natural Language Processing (NLP) untuk melakukan ekstraksi otomatis yang memilah isi teks menjadi tiga bagian terstruktur: Poin Utama Pembahasan, Keputusan Rapat, dan Daftar Tugas (Action Items beserta PIC yang ditunjuk).  
      
4. **Modul Document Generator & UI Streamlit**: Hasil ekstraksi ditampilkan secara rahasia dan aman pada dasbor Streamlit. Skrip Python (*python-docx*) akan otomatis mengemas teks tersebut ke dalam templat dokumen resmi instansi (.docx/.pdf) sehingga staf cukup melakukan validasi akhir dan mengunduhnya dengan satu klik.

\#\#\#  Tujuan Proyek

**Target Pengguna/Pasar**  
 

1. **Target Utama**: Bagian Sekretariat Daerah (Setda) Kota/Kabupaten, khususnya sub-bagian Tata Usaha, Kepegawaian, dan Kompilasi Rapat Kerja.  
      
2. **Target Sekunder**: Kantor Dinas Pemerintahan Daerah (Pemda) yang memiliki intensitas rapat koordinasi, rapat pleno, dan evaluasi lintas sektor yang tinggi setiap minggunya.  
      
3. **Target Tersier**: Institusi pelayanan publik non-kementerian, sekretariat lembaga legislatif daerah (DPRD), serta bagian administrasi internal perguruan tinggi negeri/swasta.

 **Apa yang membuat GovScribe-Pipeline berbeda dari solusi lain?**

1\. Keamanan Data On-Premise (Bukan Cloud Publik)

Mayoritas layanan transkripsi AI mengirim data ke server pihak ketiga. GovScribe-Pipeline memproses seluruh data di server internal instansi sehingga cocok untuk dokumen rapat pemerintahan yang bersifat rahasia. Sistem juga menerapkan AES-256, TLS 1.3, dan SHA-256.

2\. Dirancang Khusus untuk Birokrasi Indonesia

Berbeda dengan AI transkripsi umum, GovScribe-Pipeline menggunakan **custom vocabulary** yang mengenali istilah seperti ASN, Bappeda, Pemkot, DPRD, dan terminologi pemerintahan lainnya sehingga hasil transkripsi lebih akurat.

3\. Tidak Hanya Transkripsi, tetapi Langsung Menjadi Notulensi

Solusi lain biasanya hanya menghasilkan teks mentah. GovScribe-Pipeline secara otomatis mengekstraksi:

* Poin pembahasan utama  
* Keputusan rapat  
* Action Items  
* PIC (penanggung jawab tugas)

Kemudian langsung menghasilkan dokumen notulensi formal siap unduh.

4\. Efisiensi Waktu hingga 90%

Penyusunan notulensi yang biasanya membutuhkan 12–24 jam dapat dipangkas menjadi kurang dari 15 menit.

5\. Tidak Membutuhkan Hardware Tambahan

Solusi dikembangkan sebagai **pure software**, sehingga instansi tidak perlu membeli perangkat khusus, sensor IoT, atau alat rekam tambahan.

6\. Sudah Memiliki MVP dan Siap Demonstrasi

Banyak proposal masih berupa konsep. GovScribe-Pipeline sudah memiliki prototipe Streamlit yang dapat mengunggah audio, melakukan transkripsi, ekstraksi NLP, dan menghasilkan dokumen secara otomatis.

\---

# \#\# ✨ Fitur Unggulan

\#\#\# Fitur Utama

| Fitur | Deskripsi | Keunggulan |
| ----- | ----- | ----- |
| **\[Transkripsi Rapat Otomatis\]** | \[Rekam audio rapat, ubah jadi teks dengan Whisper\] | \[Menghapus pekerjaan ketik ulang. Diproses lokal, isi rapat tidak dikirim ke server luar\] |
| **\[Ekstraksi Poin Keputusan\]** | \[Memilah teks transkrip menjadi poin-poin utama hasil rapat\] | \[Staf tidak perlu membaca ulang transkrip panjang untuk mencari inti pembahasan\] |
| **\[Generator Dokumen .docx\]** | \[Hasil Ekstraksi otomatis dikemas ke templat notulensi resmi\] | \[Dokumen siap validasi dan unduh dengan satu klik, tanpa menyalin manual\] |
| **\[Proteksi Data On-Premise\]** | \[Enkripsi berkas tersimpan dan login berkata sandi ter hash\] | \[Dokumen rahasia tetap aman meski file mentah disalin dari server instansi\] |

\#\#\# Fitur Tambahan

**\-  \[Antarmuka Streamlit Sederhana\]** \- Hanya tiga langkah, ramah bagi pegawai awam   
					teknologi

**\- \[Nol Biaya Perangkat Keras\]**      \- Murni perangkat lunak, tanpa sensor atau alat   
					tambahan

**\- \[Arsitektur Kode Modular\]**         \- Mudah direplikasi dari Setda hingga DPRD tanpa   
					mengubah struktur dasar

**\- \[Prototipe Siap Demo\]** 	          \- Sistem sudah berjalan end-to-end, bukan sekadar   
					konsep

\---

# \#\# 📸 Demo & Screenshot

\#\#\# Live Demo

🔗 https://govscribe-v2-mp3afgk8abxvrndh38s8my.streamlit.app/

\#\#\# Screenshot Aplikasi
<div align="center">
	<img src="docs/1.jpeg" alt="Portal berita publik" width="800"/>
	<p>
		<strong>Form portal berita publik</strong><br/>
		<em>Masyarakat umum dapat mengaksesnya tanpa login atau registrasi, dan memperoleh keterangan berita terkini.</em>
	</p>	
	<img src="docs/2.jpeg" alt="Login" width="800"/>
	<p>
		<strong>form login</strong><br/>
		<em>user dapat melakukan login pada web ini terkhusus untuk karyawan yang sudah mendaftar atau pekerja pnsnya, ada keteragan button lupa kata sandi dan button kembali ke portal berita.</em>
	</p>	
	<img src="docs/3.jpeg" alt="Register" width="800"/>
	<p>
    <strong>form register</strong><br/>
	<em>user baru/ karwayan baru dapat melakukan register pada akun emai dinas mereka atau menggunakan akun pribaadinya lalu data dapat diakses juga menggunakan verifikasi wajah agar bisa masuk kedalam dashboard webnya.</em>
	</p>	
	<img src="docs/4.jpeg" alt="Dashbord" width="800"/>
	<p>
    <strong>Menu Dashbord</strong><br/>
	<em>pada Menu ini ada tampilan aktifitas yang sedang berjalan seperti login register atau uplod berita ktereangan berikut ini juga bisa menjadi keterangan absen pegawai. Begitu juga dengan keterangan lainnua seperti jumalh karyawannya dan berita yang sudah terbit.</em>
	</p>	
	<img src="docs/5.jpeg" alt="Rekam dan Transkripsi" width="800"/>
	<p>
    <strong>Perekam suara & Transkripsi Otomatis</strong><br/>
	<em>yang dimana merekam suara pas rapat untuk notelensi rapat setelah di rekam bakal otomatis hasil dari rekam suaranya dan juga bisa di edit, selain itu juga bisa unduh, rekaman nya, dokumen notelensi nya untuk dikirim ke internal pemerintah sebelum publish ke berita. Selain itu juga bisa di unduh.</em>
	</p>
	<img src="docs/6.jpeg" alt="Notulensi Rapat Digital" width="800"/>
	<p>
    <strong>notulensi rapat digital</strong><br/>
	<em>keterangan untuk megoupod notulensi rapat digital untuk mentranskrip textnya dan merevisi serta menulis ulang/ merevisi text berita yang akan diterbitkan. ada pula keterangan judul dan lokasi rapatnya ada dimana.</em>
	</p>
	<img src="docs/7.jpeg" alt="Daftar Karyawan" width="800"/>
	<p>
    <strong>Form Daftar Karyawan</strong><br/>
	<em>form ini ada keteragan daftar karyawan masuk kayawan keluar karyawan ishoma metode loginnya mengunaakn apa foto atau tidak dan waktu serta tanggalnya.</em>
	</p>
	<img src="docs/8.jpeg" alt="Profil" width="800"/>
	<p>
    <strong>Menu Profile</strong><br/>
	<em>disini keterangan nama user jabatan pegawai peran dll. ada juga keterangaan status dari karyawannya total absensi dan total beritaa yang telah diuplod ke publik.</em>
	</p>
	<img src="docs/9.jpeg" alt="Logout" width="800"/>
	<p>
    <strong>Tampilan Menu Logout</strong><br/>
	<em>berikut ini adalah tampilan dari form logout untuk karyawan yang inngin keluar ishoma atau telah menyeleksaikan pekerjaannya/pulang ada keterangan nip, password dan foto bukti absen keluar.</em>
	</p>
</div>

\# Video Demo

https://www.youtube.com/watch?v=hrK5ytmt9k0

\---

# \#\# 🛠️ Teknologi

\#\#\# Tech Stack

\#\#\#\# Frontend  
\`\`\`  
Framework	: \[Streamlit\]  
UI Library	: \[Bawaan Streamlit (streamlit markdown) \+ audio-recorder-streamlit\]  
State Mgmt	: \[Bawaan Streamlit (streamlit session\_state)\]  
Validation	: \[Regex\]  
\`\`\`

\#\#\#\# Backend  
\`\`\`  
Runtime	: \[Python 3.11\]  
Framework	: \[Streamlit\]  
Database	: \[SQLite 3\]  
ORM		: \[-\]  
Auth		: \[Hash PBKDF2-SHA256 260.000 iterasi bersalt\]  
\`\`\`

\#\#\#\# DevOps & Tools  
\`\`\`  
Deployment	: \[Netlify\]  
CI/CD		: \[-\]  
Testing		: \[-\]  
Monitoring	: \[-\]  
\`\`\`

\#\#\# Alasan Pemilihan Teknologi

### 

| Teknologi | Alasan Pemilihan |
| ----- | ----- |
| **Streamlit** | Membuat antarmuka web lengkap hanya dengan Python. Tim kecil bisa fokus ke logika transkripsi ketimbang membangun frontend dan backend terpisah. Komponen bawaannya sudah mencakup unggah berkas, tabel, dan tombol unduh yang persis dibutuhkan alur kerja notulensi |
| **OpenAI Whisper** | Berjalan sepenuhnya di komputer lokal, sehingga audio rapat rahasia tidak pernah keluar dari lingkungan instansi. Akurasinya untuk Bahasa Indonesia jauh di atas pustaka pengenalan suara sumber terbuka lain, dan modelnya gratis tanpa biaya per menit seperti layanan transkripsi komersial |
| **SQLite** | Sudah menyatu dengan Python, jadi tidak perlu memasang atau menjalankan server database terpisah. Seluruh data cukup satu berkas yang mudah dicadangkan dengan menyalinnya. Untuk satu instansi dengan puluhan pengguna, performanya lebih dari memadai dan tidak menambah beban pemeliharaan |
| **Cryptography (Fernet)** | Menyediakan enkripsi simetris yang sudah teruji tanpa mengharuskan pengembang merangkai sendiri algoritma, mode operasi, dan verifikasi keaslian. Setiap data terenkripsi otomatis disertai penanda anti-manipulasi, sehingga berkas yang diubah diam-diam akan langsung terdeteksi saat dibuka |
| **python-docx** | Menghasilkan berkas Word asli yang bisa langsung dibuka, disunting, dan ditandatangani staf. Format .docx dipilih karena sudah menjadi standar dokumen resmi di instansi pemerintahan Indonesia |

\#\#\# Dependencies Utama

\`\`\`  
streamlit==1.63.0  
openai-whisper==20250625  
opencv-python-headless==4.13.0.92  
cryptography==46.0.6  
python-docx==1.2.0  
pandas==3.0.2  
numpy==2.4.4  
scipy==1.17.1  
Pillow==12.1.1  
audio-recorder-streamlit==0.0.8

\`\`\`

\---

# \#\# 🏗️ Arsitektur Sistem

\#\#\# System Architecture

\`\`\`  
menggunakan Mermaid PNG 
<div align="center">
	<img src="docs/Layanan Pemrosesan Kata-2026-09-06-204355.png" alt="Our System Architecture" width="800"/>
</div>

\`\`\`

\#\#\# Database Schema

<div align="center">
	<img src="docs/Picture.png" alt="Our ERD Schema" width="800"/>
</div>

### **Penjelasan Relasi Tabel Database:**

* **employees**: Tabel utama yang menyimpan data pegawai/user, dengan kunci utama id serta atribut unik seperti nip dan username.  
* **attendance**: Menyimpan riwayat absensi pegawai. Relasi logis terhubung ke pegawai melalui kolom nip.  
* **notulensi**: Menyimpan draf dan dokumen notulensi rapat, yang dapat direferensikan ke berita publik.  
* **published\_news**: Menyimpan berita hasil publikasi yang memiliki relasi luar (*foreign key*) ke tabel notulensi melalui kolom notulensi\_id (REFERENCES notulensi(id) ON DELETE SET NULL).  
* **otp\_reset**: Tabel terpisah yang bertugas untuk manajemen kode OTP pemulihan kata sandi berdasarkan

\#\#\# Folder Structure

```
govscribe-v2/
│
├── notelensi_pemerintah.py      # Aplikasi utama Streamlit, seluruh antarmuka
├── database.py                  # Lapisan data: CRUD, autentikasi, OTP, enkripsi
├── email_service.py             # Pengiriman email OTP dan templat HTML
├── reset_password_ui.py         # Alur lupa kata sandi
├── migrasi_csv_ke_db.py         # Skrip sekali pakai, migrasi data versi lama
│
├── tests/                       # Pengujian otomatis (81 test, cakupan 86%)
│   ├── test_database.py         # 58 test: auth, OTP, notulensi, absensi, skema
│   └── test_email_service.py    # 23 test: validasi, templat, penanganan galat SMTP
├── conftest.py                  # Konfigurasi pytest, database sementara terisolasi
├── pytest.ini                   # Pengaturan penemuan berkas uji
│
├── docs/                        # Tangkapan layar dan aset dokumentasi
│
├── registered_faces/            # Foto wajah pegawai (isi diabaikan Git)
│   └── .gitkeep
│
├── requirements.txt             # Dependensi Python
├── packages.txt                 # Dependensi sistem (ffmpeg)
├── runtime.txt                  # Versi Python (3.11)
│
├── README.md                    # Dokumentasi utama
├── CARA_MENJALANKAN.md          # Panduan pemasangan dan pemakaian
├── LICENSE                      # Lisensi MIT
└── .gitignore                   # Berkas yang tidak ikut ke repositori
```
\---

# \#\# ⚙️ Instalasi & Setup

\#\#\# Prerequisites

Pastikan Anda telah menginstall:  
\- **Python** 	(v3.11 atau lebih tinggi)  
\- **pip** 		(sudah termasuk dalam instalasi Python)  
\- **FFmpeg** 	(wajib, dibutuhkan Whisper untuk membaca berkas audio)  
\- **Git**

\> Database tidak perlu diinstal. **SQLite** sudah termasuk dalam **Python**,  
\> dan berkas \`**govscribe.db**\` dibuat otomatis saat aplikasi pertama dijalankan.

\#\#\# Langkah Instalasi

\#\#\#\# 1️⃣ Clone Repository

\`\`\`bash  
git clone https://github.com/zhahir23/govscribe-v2.git  
cd govscribe-v2  
\`\`\`

\#\#\#\# 2️⃣ Install Dependencies

\`\`\`bash  
\# Disarankan membuat virtual environment terlebih dahulu  
python \-m venv .venv

\# Aktifkan (Windows)  
.venv\\Scripts\\activate

\# Aktifkan (macOS / Linux)  
source .venv/bin/activate

\# Pasang seluruh dependensi Python  
pip install \-r requirements.txt  
\`\`\`

\#\#\#\# 3️⃣ Setup Environment Variables (Install FFmpeg)  
\`\`\`bash  
\# Windows  
winget install ffmpeg

\# macOS  
brew install ffmpeg

\# Linux (Debian/Ubuntu)  
sudo apt install ffmpeg  
\`\`\`

Setelah itu tutup terminal, lalu buka kembali, dan klik prompt  
\`\`\`bash  
ffmpeg \-version  
\`\`\`  
\#\#\#\# 4️⃣ Setup Database  
Salin `.streamlit/secrets.toml.contoh` menjadi `.streamlit/secrets.toml`, lalu isi: 

\`\`\`toml  
\# Kredensial pengirim email OTP  
\# Wajib App Password 16 digit dari Google, bukan password akun biasa  
SMTP\_EMAIL \= "govscribe.bot@gmail.com"  
SMTP\_PASSWORD \= "abcdefghijklmnop"

\# Identitas instansi yang tampil di email  
NAMA\_INSTANSI \= "Sekretariat Daerah"  
ALAMAT\_INSTANSI \= "Jl. Raya Pemerintahan No. 1"

\# Kunci enkripsi. Kosongkan saat pemasangan lokal,  
\# aplikasi akan membuat secret.key otomatis.  
\# Wajib diisi hanya jika di-deploy ke hosting.  
\# GOVSCRIBE\_KEY \= ""  
\`\`\`

\#\#\#\# 5️⃣ Run Development Server

\`\`\`bash  
streamlit run notelensi\_pemerintah.py  
\`\`\`

Aplikasi akan berjalan di \`http://localhost:8501\`

\---

# \#\# 🚀 Penggunaan

\#\#\# Menjalankan Aplikasi

\`\`\`bash  
\# Menjalankan aplikasi  
streamlit run notelensi\_pemerintah.py

\# Menjalankan pada port lain  
streamlit run notelensi\_pemerintah.py \--server.port 8502

\# Menjalankan tanpa membuka browser otomatis  
streamlit run notelensi\_pemerintah.py \--server.headless true

\# Menghentikan aplikasi  
\# Tekan Ctrl+C pada terminal  
\`\`\`

\#\#\# User Guide

\#\#\#\# Untuk Masyarakat Umum (Tanpa Login) 

1\. **Membaca Berita:** Buka http://localhost:8501. Halaman utama menampilkan portal berita   
    berisi hasil rapat yang sudah dipublikasikan, tanpa perlu akun.  
2\. **Melihat Detail:** Klik tombol Baca Selengkapnya pada kartu berita untuk membuka artikel   
    lengkapnya.

\#\#\#\# Untuk Pegawai (Perlu Login) 

1\. **Registrasi:** Klik Login sebagai pegawai di kanan atas, pilih tab Registrasi. Isi NIP, email   
		Gmail aktif, dan kata sandi, lalu ambil foto wajah lewat kamera. Sistem   
		memverifikasi bahwa foto benar-benar memuat wajah sebelum akun dibuat.  
2\. **Login dan Absensi**: Pada tab **Absensi Manual**, masukkan NIP dan kata sandi. Kehadiran   
			  otomatis tercatat begitu login berhasil.  
3\. **Lupa Kata Sandi**: Klik *Lupa kata sandi?*, masukkan NIP, lalu periksa email untuk kode   
			enam digit. Kode berlaku sepuluh menit dan hanya bisa dipakai sekali.   
4\. **Membuat Notulensi**: Buka menu **Workspace Rapat**, rekam audio langsung dari browser   
			    atau unggah berkas, lalu jalankan transkripsi. Hasilnya otomatis   
			    tersimpan sebagai draf.   
5\. **Melanjutkan Draf**: Masih di Workspace Rapat, buka panel *Lanjutkan notulensi tersimpan*   
			 untuk membuka pekerjaan yang belum selesai.   
6\. **Menerbitkan ke Publik**: Setelah menyunting poin dan artikel, klik *Publikasikan ke*   
			          *Masyarakat*. Notulensi langsung tampil di portal berita.   
7\. **Mengunduh Dokumen**: Gunakan tombol unduh untuk menyimpan notulensi sebagai   
			         berkas Word (.docx).  
8\. **Absen Keluar**: Klik *Keluar dan absen* di sidebar, pilih ISHOMA atau Jam Pulang, lalu   
		      ambil foto sebagai bukti.    
\---

# \#\# 📚 API Documentation

\#\#\# Arsitektur Komunikasi

Aplikasi ini \*\*tidak menyediakan REST API\*\*. GovScribe berjalan sebagai monolit Streamlit, dengan antarmuka dan logika bisnis berada dalam satu proses Python. Komunikasi antar bagian terjadi melalui pemanggilan fungsi langsung di memori, bukan permintaan HTTP.

\`\`\`  
Development: http://localhost:8501  
\`\`\`

\#\#\# Antarmuka Antar Modul

Sebagai pengganti endpoint, berikut fungsi publik yang menghubungkan lapisan antarmuka dengan lapisan data.

\#\#\#\# Autentikasi (\`database.py\`)

\`\`\`python  
simpan\_pegawai(username, password, nip, nama, email, foto\_path, foto\_blob)  
verifikasi\_login(username, password)          \# \-\> bool  
update\_user\_password(username, password\_baru)  
ambil\_pegawai(username)                       \# \-\> dict | None  
buat\_otp(username)                            \# \-\> (kode, error)  
verifikasi\_otp(username, kode)                \# \-\> (berhasil, pesan)  
reset\_password\_dengan\_otp(username, kode, password\_baru)  
\`\`\`

\#\#\#\# Notulensi (\`database.py\`)

\`\`\`python  
simpan\_notulensi(judul, transkrip, lokasi, poin\_utama, dibuat\_oleh)   \# \-\> id  
ambil\_notulensi(notulensi\_id)                                        \# \-\> dict  
daftar\_notulensi(dibuat\_oleh, status, limit)                         \# \-\> list  
update\_notulensi(notulensi\_id, judul, transkrip, poin\_utama, status)  
hapus\_notulensi(notulensi\_id)  
\`\`\`

\#\#\#\# Absensi (\`database.py\`)

\`\`\`python  
catat\_absensi(nip\_username, kegiatan, metode, status, foto\_path, is\_logout)  
riwayat\_absensi(nip, limit)                   \# \-\> list  
absensi\_terakhir(nip)                         \# \-\> dict | None  
ekspor\_absensi\_terenkripsi(path\_output, nip)  \# \-\> (path, jumlah)  
\`\`\`

\#\#\#\# Berita Publik (\`database.py\`)

\`\`\`python  
publish\_notulensi(judul, lokasi, poin\_utama, isi\_artikel, publisher, notulensi\_id)  
load\_published\_data(limit)                    \# \-\> list  
update\_berita(berita\_id, judul, poin\_utama, isi\_artikel)  
hapus\_berita(berita\_id)  
\`\`\`

\#\#\#\# Email (\`email\_service.py\`)

\`\`\`python  
kirim\_otp(email\_tujuan, kode, nama\_pengguna)          \# \-\> (berhasil, pesan)  
kirim\_konfirmasi\_reset(email\_tujuan, nama, waktu)     \# \-\> (berhasil, pesan)  
\`\`\`

\#\#\# Contoh Pemanggilan

\`\`\`python  
import database as db  
import email\_service as mail

\# Login dan pencatatan kehadiran  
if db.verifikasi\_login("admin\_setda", "admin123"):  
    db.catat\_absensi("admin\_setda", kegiatan="Rapat Koordinasi")

\# Kirim kode OTP untuk reset kata sandi  
kode, error \= db.buat\_otp("pns\_19850110")  
if kode:  
    pegawai \= db.ambil\_pegawai("pns\_19850110")  
    mail.kirim\_otp(pegawai\["email"\], kode, pegawai\["nama"\])  
\`\`\`

\#\#\# Rencana Pengembangan

Modul \`database.py\` sudah terpisah sepenuhnya dari lapisan antarmuka. Bila sistem perlu diakses aplikasi lain, misalnya dashboard instansi atau aplikasi mobile, lapisan REST API berbasis FastAPI dapat ditambahkan di atas modul tersebut tanpa mengubah logika yang sudah ada.  
\---

# \#\# 🧪 Testing

\#\#\# Running Tests

\`\`\`bash  
\# Unit tests  
pytest

\# Unit tests per modul  
pytest tests/test\_database.py  
pytest tests/test\_email\_service.py

\# Test coverage  
pytest \--cov=database \--cov=email\_service \--cov-report=term-missing

\# Coverage dalam bentuk HTML  
pytest \--cov=database \--cov=email\_service \--cov-report=html  
\`\`\`

\#\#\# Test Coverage

\`\`\`  
Statements   : 86%  
Branches     : 87%  
Functions    : —  
Lines        : 86%

81 passed in 6.37s  
\`\`\`

| Modul | Statements | Cover |  
|---|---|---|  
| \`database.py\` | 331 | 87% |  
| \`email\_service.py\` | 107 | 83% |  
| \*\*TOTAL\*\* | \*\*438\*\* | \*\*86%\*\* |

\---

# \#\# 📄 Lisensi

Proyek ini dilisensikan di bawah \[MIT License\](LICENSE) \- lihat file LICENSE untuk detail lebih lanjut.

\---

Made with ❤️ by DevSpectra for ITECHNO CUP 2026\*\*
