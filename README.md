# Siapa yang Paling Sulit Dapat Kerja di Indonesia?

Analisis Tingkat Pengangguran Terbuka Berdasarkan Pendidikan, Usia, Gender, dan Wilayah

## Tujuan

Menjawab pertanyaan: **siapa yang paling sulit mendapatkan kerja** di Indonesia berdasarkan data BPS Sakernas, dan bagaimana pemandangan ini berubah seiring waktu berdasarkan pendidikan, usia, gender, dan wilayah.

## Maksud

Proyek ini menganalisis data Tingkat Pengangguran Terbuka (TPT) di Indonesia dari tahun 2008 hingga 2025 menggunakan sumber data BPS (Badan Pusat Statistik) dari survei Sakernas. Tujuan menciptakan data analisis yang terverifikasi dan visualisasi yang jelas untuk memahami pola pengangguran di berbagai segmentar populasi.

## Insight Utama

1. **Lulusan SMK memiliki TPT tertinggi** (sekitar 9,01% Agustus 2024), hampir ganda lipat TPT lulusan SD (2,42%). Ini menunjukkan bahwa keterampilan lulusan SMK masih tidak sejalan dengan butuhan pasar kerja.
2. **Pemuda 15-19 tahun berisiko sangat tinggi** (TPT 23,34% pada 2025), lebih lipat lipat dari usia 25-59 (~4,9%). Membutuhkan intervensi dini sebelum lulus SMA.
3. **Tidak ada selisih signifikan antara laki-laki dan perempuan** pada 2025 (4,85% vs 4,84%), namun kesenjangan ada di tingkat daerah: Perkotaan 5,75% vs Perdesaan 3,47%.
4. **Wilayah geografis mempengaruhi akses kerja dengan rentan 5x lipat** antara Jawa Barat (6,75%) dan Papua Pegunungan (1,32%).
5. **Lulusan pendidikan tinggi tetap kompetitif** (Sarjana TPT 5,25%), menentang narasi umum bahwa lulusan tinggi kesulitan menemukan kerja.
6. **Porsi pekerja informal sangat tinggi pada lulusan rendah** (SD 94,2%, SMA 67%), menunjukkan lulusan pendidikan rendah "dapat kerja" namun pekerjaan berkualitas rendah (informal, jam kerja pendek).
7. **Tren nasional menurun sejak 2015** (6,18% ke 4,91%), namun 2025 menunjukkan naik kembali karena metode survei triwulanan baru — tidak boleh dibandingkan langsung dengan tahun sebelumnya.
8. **Partisipasi kerja tinggi (TPAK) tidak menjamin TFT rendah** — korelasi hanya r=0,1 di level provinsi, membongkar asumsi populasi tentang "susah cari kerja".
9. **Setengah pengangguran ( bekerja < 35 jam/minggu) paling banyak pada lulusan SD** (8,81%), memperkuat konsep underemployment (bekerja tapi tidak sepenuhnya).
10. **Struktur pekerjaan pemuda sudah lama berlanjut tanpa perubahan signifikan** dari 2015 ke 2024 — rasio TFT usia 15-19 terhadap rata-rata 25-59 tetap 5-10x lipat.

## Sumber Data

Semua data diambil dari **BPS (Badan Pusat Statistik)** melalui situs bps.go.id. Setiap file mentah diunduh menggunakan tombol "Unduh CSV" pada halaman tabel statistik.

Berkas CSV mentah disimpan di `data/raw/`, dan hasil pembersihan diolah menjadi 12 tabel analisis di `data/processed/`. Semua logika pembersihan ada di `src/cleaning.py`, serta 11 fungsi grafik di `src/plots.py`.

---

## 🎁 Gift Khas Data Analyst

Sebagai hadiah akhir proyek, berikut "7 Golden Rules" Data Analyst yang harus Anda ingat:

1. **Cek data sebelum cek jawaban** — Distribusi data yang membingungkan menghasilkan conclusi yang salah.
2. **Visualisasi sebelum visualisasi akhir** — Plot data sebelum membuat grafik final, cari outlier dan anomali.
3. **Korelasi ≠ Kauzalitas** — Korelasi positif hanya petunjuk, bukan kesimpulan akhir.
4. **Data bersih lebih penting dari data lengkap** — Hilangkan outliers yang valid tapi tidak relevan, jangan diam-diam hapus.
5. **Semprebutasi bisa membunuh** — Selalu uji model/insight di periode yang berbeda, jangan anggap tren akan terus berlanjut.
6. **Komunikasi yang jelas lebih berharga dari akurasi yang tinggi** — Insight yang bisa dipahami stakeholder lebih baik daripada model yang kompleks tapi tidak dipahami.
7. **Semprebutasi data adalah keterampilan terbaik** — Selalu coba lihat data dari sudut pandang yang berbeda, carilah perseptif baru.

---

# Sumber Data

Semua data diambil dari **BPS (Badan Pusat Statistik)** melalui situs bps.go.id. Setiap file mentah diunduh menggunakan tombol "Unduh CSV" pada halaman tabel statistik.

Berkas CSV mentah disimpan di `data/raw/`, dan hasil pembersihan diolah menjadi 12 tabel analisis di `data/processed/`. Semua logika pembersihan ada di `src/cleaning.py`, serta 11 fungsi grafik di `src/plots.py`.

---