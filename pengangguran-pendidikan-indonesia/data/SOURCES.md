# Sumber Data

Semua angka dalam proyek ini harus dapat ditelusuri ke file di `data/raw/`.
File di `data/raw/` adalah **unduhan apa adanya** dari Tabel Statistik BPS
(format CSV hasil tombol *Unduh → CSV*), tanpa diedit manual.

- **Tanggal akses seluruh file:** 14 November 2026
- **Sumber utama:** Badan Pusat Statistik (BPS), Survei Angkatan Kerja Nasional (Sakernas)
- **Halaman indeks:** <https://www.bps.go.id/id/statistics-table?subject=520> (subjek *Tenaga Kerja*)

---

## 1. Daftar file mentah

| # | File (`data/raw/`) | Judul tabel BPS | ID tabel | Cakupan | URL |
|---|---|---|---|---|---|
| 1 | `bps_pendidikan_jenis_kegiatan_2008_2024.csv` | Penduduk Berumur 15 Tahun Ke Atas Menurut Pendidikan Tertinggi yang Ditamatkan dan Jenis Kegiatan Selama Seminggu yang Lalu, 2008–2024 | 1909 | Nasional, 2008–2024, Februari & Agustus | https://www.bps.go.id/id/statistics-table/1/MTkwOSMx/penduduk-berumur-15-tahun-ke-atas-menurut-pendidikan-tertinggi-yang-ditamatkan-dan-jenis-kegiatan-selama-seminggu-yang-lalu--2008-2024.html |
| 2 | `bps_pengangguran_pendidikan_1986_2024.csv` | Pengangguran Terbuka Menurut Pendidikan Tertinggi yang Ditamatkan 1986–2024 | 972 | Nasional, 1986–2024 (tahunan), jumlah orang | https://www.bps.go.id/id/statistics-table/1/OTcyIzE=/pengangguran-terbuka-menurut-pendidikan-tertinggi-yang-ditamatkan-1986---2024.html |
| 3 | `bps_provinsi_jenis_kegiatan_2008_2024.csv` | Penduduk Berumur 15 Tahun Ke Atas Menurut Provinsi dan Jenis Kegiatan Selama Seminggu yang Lalu, 2008–2024 | 1907 | 34 provinsi (2008–2022) → 38 provinsi (2023–2024), Februari & Agustus | https://www.bps.go.id/id/statistics-table/1/MTkwNyMx/penduduk-berumur-15-tahun-ke-atas-menurut-provinsi-dan-jenis-kegiatan-selama-seminggu-yang-lalu--2008---2024.html |
| 4 | `bps_umur_jenis_kegiatan_2008_2024.csv` | Penduduk Berumur 15 Tahun Ke Atas Menurut Golongan Umur dan Jenis Kegiatan Selama Seminggu yang Lalu, 2008–2024 | 1904 | Nasional, kelompok umur 5-tahunan, Februari & Agustus | https://www.bps.go.id/id/statistics-table/1/MTkwNCMx/penduduk-berumur-15-tahun-ke-atas-menurut-golongan-umur-dan-jenis-kegiatan-selama-seminggu-yang-lalu--2008---2024.html |
| 5 | `bps_status_pekerjaan_pendidikan_2008_2024.csv` | Penduduk Berumur 15 Tahun Ke Atas yang Bekerja ... Menurut Status Pekerjaan Utama dan Pendidikan Tertinggi yang Ditamatkan, 2008–2024 | 1936 | Nasional, 7 status pekerjaan × 8 jenjang pendidikan, Februari & Agustus | https://www.bps.go.id/id/statistics-table/1/MTkzNiMx/penduduk-berumur-15-tahun-ke-atas-yang-bekerja-selama-seminggu-yang-lalu-menurut-status-pekerjaan-utama-dan-pendidikan-tertinggi-yang-ditamatkan--2008-2024.html |
| 6 | `bps_lapangan_usaha_pendidikan_2008_2024.csv` | Penduduk Berumur 15 Tahun Ke Atas yang Bekerja ... Menurut Lapangan Pekerjaan Utama dan Pendidikan Tertinggi yang Ditamatkan, 2008–2024 | 1932 | Nasional, 17 lapangan usaha × pendidikan, Februari & Agustus | https://www.bps.go.id/id/statistics-table/1/MTkzMiMx/penduduk-berumur-15-tahun-ke-atas-yang-bekerja-selama-seminggu-yang-lalu-menurut-lapangan-pekerjaan-utama-dan-pendidikan-tertinggi-yang-ditamatkan--2008---2024.html |
| 7 | `bps_umur_jam_kerja_2008_2024.csv` | Penduduk Berumur 15 Tahun Ke Atas yang Bekerja ... Menurut Golongan Umur dan Jumlah Jam Kerja Seluruhnya, 2008–2024 | 1934 | Nasional, umur × kelompok jam kerja (0, 1–4, ..., 45+), Februari & Agustus | https://www.bps.go.id/id/statistics-table/1/MTkzNCMx/penduduk-berumur-15-tahun-ke-atas-yang-bekerja-selama-seminggu-yang-lalu-menurut-golongan-umur-dan-jumlah-jam-kerja-seluruhnya--2008---2024.html |
| 8 | `bps_tpt_pendidikan_2025.csv` | Tingkat Pengangguran Terbuka Berdasarkan Tingkat Pendidikan | 1179 | Nasional, 2025 (satu periode rilis) | https://www.bps.go.id/id/statistics-table/2/MTE3OSMy/tingkat-pengangguran-terbuka-berdasarkan-tingkat-pendidikan.html |
| 9 | `bps_tpt_jenis_kelamin_2025.csv` | Tingkat Pengangguran Terbuka Berdasarkan Jenis Kelamin | 1177 | Nasional, 2025 | https://www.bps.go.id/id/statistics-table/2/MTE3NyMy/tingkat-pengangguran-terbuka-berdasarkan-jenis-kelamin.html |
| 10 | `bps_tpt_kota_desa_2025.csv` | Tingkat Pengangguran Terbuka Berdasarkan Daerah Tempat Tinggal | 1178 | Nasional, 2025 (perkotaan/perdesaan) | https://www.bps.go.id/id/statistics-table/2/MTE3OCMy/tingkat-pengangguran-terbuka-berdasarkan-daerah-tempat-tinggal.html |
| 11 | `bps_tpt_kelompok_umur_2025.csv` | Tingkat Pengangguran Terbuka Berdasarkan Kelompok Umur | 1180 | Nasional, 2025, kelompok umur 5-tahunan (15-19 s.d. 60+) | https://www.bps.go.id/id/statistics-table/2/MTE4MCMy/tingkat-pengangguran-terbuka-berdasarkan-kelompok-umur.html |
| 12 | `bps_setengah_pengangguran_pendidikan_2025.csv` | Tingkat Setengah Pengangguran Menurut Tingkat Pendidikan (Persen) | 1184 | Nasional, 2025 | https://www.bps.go.id/id/statistics-table/2/MTE4NCMy/tingkat-setengah-pengangguran-menurut-tingkat-pendidikan-persen.html |
| 13 | `bps_informal_pendidikan_2023.csv` | Proporsi Lapangan Kerja Informal Menurut Tingkat Pendidikan | 2157 | Nasional, 2023 | https://www.bps.go.id/id/statistics-table/2/MjE1NyMy/proporsi-lapangan-kerja-informal-menurut-tingkat-pendidikan.html |
| 14 | `bps_tpak_provinsi_2026.csv` | Persentase Angkatan Kerja Terhadap Penduduk Usia Kerja (TPAK) menurut Provinsi (Persen) | 2396 | 38 provinsi, 2026 (Februari, Agustus) | https://www.bps.go.id/id/statistics-table/2/MjM5NiMy/persentase-angkatan-kerja-terhadap-penduduk-usia-kerja--tpak--menurut-provinsi--persen-.html |
| 15 | `bps_tpt_provinsi_triwulanan_2025.csv` | Tingkat Pengangguran Terbuka menurut Provinsi (Triwulanan) (Persen) | 2562 (tab 2025) | 38 provinsi, triwulanan 2025 | https://www.bps.go.id/id/statistics-table/2/MjU2MiMy/tingkat-pengangguran-terbuka-menurut-provinsi--triwulanan---persen-.html |
| 16 | `bps_tpt_provinsi_triwulanan_2026.csv` | Tingkat Pengangguran Terbuka menurut Provinsi (Triwulanan) (Persen) | 2562 (tab 2026) | 38 provinsi, triwulanan 2026 | https://www.bps.go.id/id/statistics-table/2/MjU2MiMy/tingkat-pengangguran-terbuka-menurut-provinsi--triwulanan---persen-.html |

### Catatan format file 1, 3, 4 (tabel "seri panjang" dari Statistik Indonesia)

File-file ini berbentuk **blok bertumpuk**: setiap tahun punya baris judul
(`2008 Februari`), baris sub-header, lalu 10–38 baris data. Kolom dipakai
bergantian untuk periode **Februari** lalu **Agustus** dalam satu baris
(susunan kolom: `Bekerja | Pengangguran | Jumlah AK | %Bekerja/AK |
Sekolah | Mengurus | Lainnya | Jumlah BAK | Jumlah Penduduk 15+ | TPAK`,
diulang untuk periode kedua). Karena itu, data ini **tidak bisa** dibaca
dengan `pd.read_csv(header=0)`; perlu parser khusus di `src/cleaning.py`.

### Catatan: tabel yang bermasalah di sisi BPS

- ID **971** ("Penduduk 15 Tahun Ke Atas Menurut Status Pekerjaan Utama 1986–2024")
  saat diakses menampilkan/mengunduh **isi tabel lain** (Golongan Umur × Jam Kerja
  Seluruhnya). Ini terlihat dari judul halaman vs isi CSV yang tidak cocok.
  File hasil unduhan tidak dipakai untuk analisis status pekerjaan; sebagai gantinya
  dipakai tabel ID 1936 (status pekerjaan × pendidikan). Perlu dilaporkan/dicek ulang
  bila ingin memakai seri status pekerjaan 1986–2024.

---

## 2. Definisi indikator (konsep BPS/Sakernas)

Kutipan rumus TPT bersumber dari metadata indikator SIRUSA–BPS
(<https://sirusa.web.bps.go.id/metadata/indikator/86e8ecc7-8553-a5e6-075d-d0b64f29777a>):

> **TPT** = (jumlah pengangguran / jumlah angkatan kerja) × 100%

Definisi konsep (BPS, Sakernas). *Kutipan kata-per-kata akan diverifikasi dari
glosarium publikasi Sakernas pada Tahap 2.*

| Istilah | Definisi ringkas |
|---|---|
| Penduduk usia kerja | Penduduk berumur 15 tahun ke atas. |
| Angkatan kerja (AK) | Penduduk 15+ yang **bekerja** atau **menganggur**. |
| Bekerja | Melakukan kegiatan ekonomi paling sedikit 1 jam secara berturut-turut selama seminggu yang lalu. |
| Pengangguran terbuka | (a) tidak punya pekerjaan dan mencari kerja; (b) tidak punya pekerjaan dan mempersiapkan usaha; (c) tidak punya pekerjaan dan tidak mencari kerja karena merasa tidak mungkin mendapatkannya (putus asa); (d) sudah punya pekerjaan tetapi belum mulai bekerja. |
| TPT | Persentase pengangguran terhadap angkatan kerja. |
| TPAK | Persentase angkatan kerja terhadap penduduk usia kerja (15+). |
| Bukan angkatan kerja (BAK) | Penduduk 15+ yang bersekolah, mengurus rumah tangga, atau lainnya. |
| Setengah pengangguran | Pekerja dengan jam kerja **kurang dari 35 jam per minggu**. BPS membedakan setengah penganggur *tidak kasat mata* (masih mencari kerja/mau menambah jam kerja) dan *kasat mata* (tidak mencari). |
| Pekerja formal | Berstatus **berusaha dibantu buruh tetap/dibayar** dan **buruh/karyawan/pegawai**. |
| Pekerja informal | Berstatus **berusaha sendiri**, **berusaha dibantu buruh tidak tetap/tidak dibayar**, **pekerja bebas**, dan **pekerja keluarga/tidak dibayar**. |
| Status pekerjaan utama | 7 kategori: (1) berusaha sendiri; (2) berusaha dibantu buruh tidak tetap; (3) berusaha dibantu buruh tetap; (4) buruh/karyawan/pegawai; (5) pekerja bebas di pertanian; (6) pekerja bebas di non-pertanian; (7) pekerja keluarga/tidak dibayar. |

---

## 3. Perubahan metodologi & kategori yang WAJIB ditandai

1. **Kategori pendidikan tidak konsisten antar tabel.**
   - Tabel seri 2008–2024 (ID 1909) memakai 8 kategori: *Tidak/belum pernah sekolah;
     Tidak/belum tamat SD; SD; SLTP; SLTA Umum/SMU; SLTA Kejuruan/SMK;
     Akademi/Diploma; Universitas* (+ *Tak Terjawab*).
   - Tabel 2025 (ID 1179, 1184, 2157) memakai 6 kategori dan **menggabungkan**
     "Tidak/Belum Pernah Sekolah/Belum Tamat SD & Tamat SD" menjadi satu.
   → Saat membandingkan 2025 dengan seri sebelumnya, kategori harus diagregasi ulang.
2. **Pembobotan berubah beberapa kali** (tertulis di catatan kaki tabel BPS):
   2011–2013 *backcasting* proyeksi 2010–2035; 2018–2020 *backcasting* SUPAS 2015;
   mulai Agustus 2023 memakai proyeksi **SP2020**. Artinya level TPT antar tahun
   tidak sepenuhnya Apple-to-apple, terutama 2018–2023.
3. **Pemekaran provinsi Papua.** 2023–2024 memuat 38 provinsi: Papua Barat Daya (92),
   Papua Selatan (95), Papua Tengah (96), Papua Pegunungan (97). Sebelumnya 34.
4. **Frekuensi survei berubah.** Sampai 2024 Sakernas Februari & Agustus; sejak 2025
   BPS merilis **triwulanan** (Februari, Mei, Agustus, November) — terlihat pada tabel
   ID 2562 dan siaran pers TPT Mei/November 2025–2026. Mei 2025 kosong ("-").
5. **Angka 2025/2026 adalah angka sangat baru** (rilis 2026). Untuk analisis tren
   panjang, titik 2025–2026 perlu diperlakukan sebagai periode terpisah.

---

## 4. Yang TIDAK tersedia di Tabel Statistik nasional (perlu keputusan)

| Kebutuhan | Status | Alternatif |
|---|---|---|
| **TPT provinsi × jenjang pendidikan** (sub-pertanyaan 3) | **Tidak ada** tabel nasionalnya. Sudah dicek: tidak ada di 105 tabel subjek Tenaga Kerja. | (a) unduh manual tabel TPT-per-pendidikan dari 38 publikasi *Sakernas Provinsi* (berat, format tidak seragam); (b) pakai mikrodata Sakernas (silastik.bps.go.id, perlu registrasi); (c) ganti sub-pertanyaan menjadi TPT provinsi total + pola kota/desa. |
| **TPT gender × jenjang pendidikan** | Tidak ada tabel silang; gender hanya tersedia agregat (2025). | Sama seperti di atas; atau batasi analisis gender ke level nasional 2025. |
| **TPT menurut provinsi, seri 1986–2024** | Tabel ID 543 ("TPT Menurut Provinsi") saat ini **gagal memuat** (halaman kosong). | Sudah tercakup oleh ID 1907 (dihitung dari pengangguran/AK per provinsi, 2008–2024). |
| **UMP per provinsi 2024–2026** | Tabel nasional ID 220 hanya berisi 2020; UMP terbaru hanya ada di situs BPS provinsi (terpisah-pisah). | Unduh manual / pakai data Kemnaker. |
| **Pertumbuhan ekonomi (PDRB) per provinsi** | Ada sebagai tabel/publikasi terpisah (subjek Neraca Ekonomi), strukturnya berlapis (`statistics-table/3/...`). | Unduh manual 1 tabel PDRB per kapita atau laju pertumbuhan 2024. |
| **TPAK menurut pendidikan** | Tidak ada tabel TPAK × pendidikan di Tabel Statistik. | TPAK tersedia menurut provinsi (ID 2396) dan kelompok umur. |

---

## 5. Aturan yang dipegang

- Tidak ada angka yang diketik dari ingatan. Semua nilai berasal dari file di atas.
- Angka **turunan** (mis. TPT = pengangguran/AK) selalu diberi label "dihitung"
  dan rumusnya ditulis di notebook/kode.
- Bila ada keraguan pada suatu tabel (mis. ID 971), tabel itu tidak dipakai.

---

## 6. Tabel turunan di `data/processed/`

Dibangun ulang dengan `python -m src.cleaning` (logika: `src/cleaning.py`).
Semua baris menyimpan kolom `sumber_file` yang menunjuk ke file di `data/raw/`.

| File | Isi | Kunci | Baris |
|---|---|---|---|
| `tpt_nasional_pendidikan.csv` | TPT nasional per jenjang pendidikan, Feb & Agu 2008–2024 | `periode`, `pendidikan` | 306 |
| `tpt_provinsi.csv` | TPT 38 provinsi + Indonesia, 2008–2024 | `periode`, `kode_provinsi` | 1.198 |
| `tpt_nasional_umur.csv` | TPT nasional per kelompok umur | `periode`, `kelompok_umur` | 374 |
| `status_pekerjaan_pendidikan.csv` | Jumlah pekerja per status pekerjaan x pendidikan | `periode`, `status_pekerjaan`, `pendidikan` | 2.736 |
| `formal_informal_pendidikan.csv` | Porsi formal/informal per pendidikan (turunan tabel status) | `periode`, `pendidikan` | 306 |
| `snapshot_2025.csv` | TPT 2025 menurut pendidikan, gender, kota/desa, umur | `dimensi`, `kategori` | 22 |
| `tpt_pendidikan_2024_2025.csv` | TPT 6 jenjang yang sebanding: Feb 2024, Agu 2024, 2025 | `periode`, `kelompok_pendidikan` | 18 |
| `informal_pendidikan_2023.csv` | Porsi pekerja informal per pendidikan (2023) | `tahun`, `kategori` | 9 |
| `setengah_pengangguran_pendidikan_2025.csv` | Setengah pengangguran per pendidikan (2025) | `tahun`, `kategori` | 6 |
| `tpt_provinsi_triwulanan.csv` | TPT provinsi triwulanan 2025–2026 (ID 2562) | `periode`, `kode_provinsi` | 234 |
| `tpak_provinsi.csv` | TPAK provinsi 2026 | `periode`, `kode_provinsi` | 39 |
| `_validasi.csv` | Log validasi + catatan keputusan pembersihan | — | 45 |

### Keputusan pembersihan yang perlu diketahui pembaca

1. **Kolom `pendidikan` vs `kelompok_pendidikan`.**
   `pendidikan` mempertahankan label terbitan BPS (8 kategori untuk 2008–2024).
   `kelompok_pendidikan` adalah agregasi 6 level yang membuat 2008–2024 bisa
   dibandingkan dengan 2025/2026 (SD ke bawah, SMP, SMA, SMK, Diploma, Sarjana).
2. **`TPT` dihitung ulang** dengan rumus `pengangguran / angkatan_kerja x 100`
   (kolom `sumber_tpt`). Angka verifikasi cocok dengan publikasi BPS:
   nasional Feb 2024 = 4,82%; Agu 2024 = 4,91%; SMK Agu 2024 = 9,01%.
3. **Baris `Tak Terjawab` dibuang** dari `tpt_nasional_pendidikan.csv` karena
   angkatan kerjanya 0 di seluruh periode (TPT tidak terdefinisi, bukan nol).
4. **Kalimantan Utara kosong 2008–2014** (14 sel): provinsi dimekarkan 2012 dan
   baru disurvei terpisah pada Sakernas 2015. Tidak diimputasi, diberi `catatan`.
5. **Provinsi Papua hasil pemekaran** (92, 95, 96, 97) hanya ada mulai 2023;
   tidak ada baris untuk tahun sebelumnya.
6. **Blok 2024 ganda pada tabel status pekerjaan.** BPS mengulang blok 2024
   dengan 6 kategori (versi harmonisasi); blok 8 kategori yang dipakai agar
   tidak terjadi penghitungan ganda. Tercatat di `_validasi.csv`.
7. **Mei 2025 tidak ada** di tabel triwulanan (Sakernas Mei 2025 tidak
   diterbitkan); sel `-` dibiarkan kosong, bukan diisi nol.

### Validasi yang dijalankan otomatis

- tidak ada duplikat pada kunci utama;
- semua persentase di rentang 0–100;
- `pengangguran <= angkatan_kerja`;
- jumlah rincian = baris `Indonesia` untuk setiap periode;
- total pekerja (tabel status) = `bekerja` (tabel pendidikan), selisih 0 orang;
- total pengangguran 38 provinsi = total nasional, selisih 0 orang.
