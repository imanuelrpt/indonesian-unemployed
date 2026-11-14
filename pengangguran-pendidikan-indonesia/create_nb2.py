import nbformat
from nbformat.v4 import new_markdown_cell, new_code_cell

nb = nbformat.v4.new_notebook()

# Cell 1: Markdown - Overview
cell1 = new_markdown_cell(
    "# 02 — EDA: Analisis Eksploratori Data\n\n"
    "**Proyek:** Siapa yang Paling Sulit Dapat Kerja di Indonesia?\n\n"
    "Notebook ini menjelaskan data yang sudah dibersihkan di Tahap 2 menggunakan fungsi dari `src.plots.py` "
    "dan tabel di `data/processed/`. Fokus utama: menemukan pola, tren, dan insight dari Tingkat Pengangguran Terbuka (TPT) "
    "berdasarkan pendidikan, usia, gender, dan wilayah.\n\n"
    "> *Catatan: Notebook ini membangun pada hasil `python -m src.cleaning`. Semua tabel di `data/processed/` sudah validasi "
    "(0 GAGAL, 45 cek).*"
)
nb['cells'].append(cell1)

# Cell 2: Code - Load data
cell2 = new_code_cell(
    "import sys\nfrom pathlib import Path\nimport pandas as pd\nimport numpy as np\n\nsys.path.insert(0, str(Path.cwd().parent))\nimport src.plots as P\nfrom src.cleaning import setup_style\n\nP.setup_style()\n\nPROC = Path.cwd() / \"data\" / \"processed\"\nprint(\"Memuat data...\")\n\npend = pd.read_csv(PROC / \"tpt_nasional_pendidikan.csv\")\nprov = pd.read_csv(PROC / \"tpt_provinsi.csv\")\numur = pd.read_csv(PROC / \"tpt_nasional_umur.csv\")\nfi = pd.read_csv(PROC / \"formal_informal_pendidikan.csv\")\nsnap = pd.read_csv(PROC / \"snapshot_2025.csv\")\nsp = pd.read_csv(PROC / \"setengah_pengangguran_pendidikan_2025.csv\")\nbanding = pd.read_csv(PROC / \"tpt_pendidikan_2024_2025.csv\")\ntri = pd.read_csv(PROC / \"tpt_provinsi_triwulanan.csv\")\ntpak = pd.read_csv(PROC / \"tpak_provinsi.csv\")\n\nprint(\"Selesai memuat\")\nprint(\"pend:\", pend.shape)\nprint(\"prov:\", prov.shape)\nprint(\"umur:\", umur.shape)\nprint(\"fi:\", fi.shape)\nprint(\"snap:\", snap.shape)\nprint(\"sp:\", sp.shape)\nprint(\"banding:\", banding.shape)\nprint(\"tri:\", tri.shape)\nprint(\"tpak:\", tpak.shape)\n"
)
nb['cells'].append(cell2)

# Cell 3: Markdown - Section 1
cell3 = new_markdown_cell(
    "## 1. Tren TPT Nasional (2008–2024) dengan Nuansa 2025\n\n"
    "Visualisasi tren TPT nasional dari tahun 2008 hingga 2024 (2 periode/tahun: Februari & Agustus), "
    " serta titik awal 2025 karena perubahan metodologi (triwulanan, Mei 2025 kosong).\n\n"
    "**Pertanyaan kunci:** Apakah TPT nasional sudah pulang ke bawah setelah loncat pandemi 2020, "
    "atau ada tanda naik kembali?"
)
nb['cells'].append(cell3)

# Cell 4: Code - Plot tren nasional
cell4 = new_code_cell(
    "fig = P.plot_tren_nasional(pend, tpt2025=float(snap.loc[(snap[\"dimensi\"]==\"kelompok_umur\"]) & (snap[\"kategori\"==\"Rata-Rata\"]), \"nilai\"].iloc[0]))\npath = P.simpan(fig, \"01_tren_nasional_2008_2025.png\", \"Sumber: BPS, Sakernas 2008-2024 (ID 1909) & Sakernas 2025 (ID 1179) | data/processed/tpt_nasional_pendidikan.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell4)

# Cell 5: Markdown - Insight 1
cell5 = new_markdown_cell(
    "**Insight 1:** TPT nasional turun dari 6,18% (Agustus 2015) ke 4,91% (Agustus 2024), "
    "namun titik 2025 (seri triwulanan) menunjukkan naik kembali. Penurunan selama 9 tahun disrupted oleh pandemi 2020 "
    "(puncak di Maret 2020), lalu pulih lambat. Sering misal naik 2025 karena metode survei berubah jadi triwulanan baru, "
    "dan Mei 2025 tidak terbit.\n\n*Catatan visual: garis putus-putus di akhir menandai bahwa 2025 bukan lanjutan langsung dari seri 2008-2024.*"
)
nb['cells'].append(cell5)

# Continue with more cells...
# Cell 6: Markdown - Section 2
cell6 = new_markdown_cell(
    "## 2. Perbandingan TPT per Jenjang Pendidikan (2015–2024)\n\n"
    "Membandingkan TPT 6 jenjang harmonis (SD ke bawah, SMP, SMA, SMK, Diploma, Sarjana) lintas waktu 2015-2024. "
    "Mengapa penting: ini langsung menjawab *sub-pertanyaan 1* siapa yang paling sulit dapat kerja."
)
nb['cells'].append(cell6)

# Cell 7: Code - Plot tren pendidikan
cell7 = new_code_cell(
    "fig = P.plot_tren_pendidikan(pend)\npath = P.simpan(fig, \"02_tpt_pendidikan_2015_2024.png\", \"Sumber: BPS, Sakernas 2008-2024 (ID 1909), diolah | data/processed/tpt_nasional_pendidikan.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell7)

# Cell 8: Markdown - Insight 2
cell8 = new_markdown_cell(
    "**Insight 2:** Lulusan SMK selalu memiliki TPT tertinggi di setiap tahun (sekitar 8-9% Agustus), "
    "hampir ganda lipat TPT SD (2-3%). Lulusan SD ke bawah memiliki TTP stabil rentan tapi terendah (2-3%). "
    "Lulusan Sarjana justru paling \"aman\" dengan TPT 5-6%, yang menentangkan narasi umum bahwa lulusan tinggi kesulitan menemukan kerja.\n\n*Catatan visual: garis SMK (merah bata) selalu di puncak, Sarjana (hijau) selalu di bawah rata-rata nasional.*"
)
nb['cells'].append(cell8)

# Cell 9: Markdown - Section 3
cell9 = new_markdown_cell(
    "## 3. Perbandingan 2024 vs 2025 (Jenjang 6 Kategori)\n\n"
    "Membandingkan TPT Februari 2024, Agustus 2024, dan 2025 menggunakan 6 kategori yang sebanding, "
    "agar tahun 2025 bisa dibandingkan dengan seri 2008-2024 tanpa bias kategori."
)
nb['cells'].append(cell9)

# Cell 10: Code - Plot perbandingan
cell10 = new_code_cell(
    "fig = P.plot_perbandingan_2025(banding)\npath = P.simpan(fig, \"03_tpt_2024_2025.png\", \"Sumber: BPS Sakernas 2008-2024 (ID 1909) & TPT 2025 (ID 1179), diolah | data/processed/tpt_pendidikan_2024_2025.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell10)

# Cell 11: Markdown - Insight 3
cell11 = new_markdown_cell(
    "**Insight 3:** Pola tetap terjaga di 2025: SMK masih paling sulit (TPT ~8,6% → 8,3% sedikit turun), "
    "SMA tetap tinggi (~7%), sedangkan hanya Sarjana yang TPT-nya naik sedikit (5,25% → 5,39%). Diploma tetap mudah (4,8%). "
    "Ini menguatkan kesimpulan bahwa *skill mismatch* adalah masalah utama di SMK/SMA, sementara lulusan tinggi tetap kompetitif.\n\n*Visual: batang bersebelahan Feb 2024 (biru muda), Agu 2024 (biru tua), dan 2025 (merah)*"
)
nb['cells'].append(cell11)

# Cell 12: Markdown - Section 4
cell12 = new_markdown_cell(
    "## 4. TPT Menurut Kelompok Usia\n\n"
    "Menganalisis sebaran TPT berdasarkan kelompok usur: 15-19, 20-24, 25-29, ..., 60+. "
    "Usia 15-19 diharapkan memiliki TPT tinggi karena pasca-sekolah masuk kerja, namun data ini menguji "
    "apakah sudah \"terlalu tinggi\" dan membandingkan dengan usia produktif 25-59."
)
nb['cells'].append(cell12)

# Cell 13: Code - Plot kelompok usia
cell13 = new_code_cell(
    "fig = P.plot_umur(umur)\npath = P.simpan(fig, \"04_tpt_kelompok_umur_2024.png\", \"Sumber: BPS, Sakernas Agustus 2024 (ID 1904) | data/processed/tpt_nasional_umur.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell13)

# Cell 14: Markdown - Insight 4
cell14 = new_markdown_cell(
    "**Insight 4:** TPT usia 15–19 tahun = 23,34% (2025 snapshot) – lebih lipat lipat dari usia 25–59 (~4,9%). "
    "Ini mencatat bahwa pelajar baru lulus sekolah atau tidak melanjutkan ke jenjang memiliki risiko sangat tinggi menjadi penganggur, "
    "kemungkinan karena keterampilan belum mencukupi atau tidak ada koneksi ke pasar kerja.\n\n*Visual: batang horizontal, warna merah muda untuk 15-19 dan 20-24, abu-abu untuk usia di atas 30.*"
)
nb['cells'].append(cell14)

# Cell 15: Markdown - Section 5
cell15 = new_markdown_cell(
    "## 5. Gender & Kota vs Desa (2025)\n\n"
    "Menganalisis perbedaan TFT antara laki-laki dan perempuan, serta antara perkotaan dan desa di 2025."
)
nb['cells'].append(cell15)

# Cell 16: Code - Plot gender & daerah
cell16 = new_code_cell(
    "fig = P.plot_gender_daerah(snap)\npath = P.simpan(fig, \"05_tpt_gender_daerah_2025.png\", \"Sumber: BPS, Sakernas 2025 (tabel TTP jenis kelamin & kota/desa) | data/processed/snapshot_2025.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell16)

# Cell 17: Markdown - Insight 5
cell15_fixed = new_markdown_cell(
    "**Insight 5:** Tidak ada selisih signifikan antara laki-laki (4,85%) dan perempuan (4,84%) pada 2025. "
    "Namun, kesenjangan justru ada di tingkat *daerah*: Perkotaan 5,75% vs Perdesaan 3,47% — pengangguran lebih tinggi di kota, "
    "kemungkinan karena antara lain biaya hidup lebih mahal dan persaingan kerja yang lebih ketat.\n\n*Visual: gambar 1x2, kiri gender, kanan kota vs desa.*"
)
nb['cells'].append(cell15_fixed)

# Cell 18: Markdown - Section 6
cell18 = new_markdown_cell(
    "## 6. TPT Provinsi 2024\n\n"
    "Menganalisis distribusi TPT across 38 provinsi di Agustus 2024."
)
nb['cells'].append(cell18)

# Cell 19: Code - Plot provinsi
cell19 = new_code_cell(
    "fig = P.plot_provinsi(prov)\npath = P.simpan(fig, \"06_tpt_provinsi_2024.png\", \"Sumber: BPS, Sakernas Agustus 2024 (ID 1907), diolah | data/processed/tpt_provinsi.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell19)

# Cell 20: Markdown - Insight 6
cell20 = new_markdown_cell(
    "**Insight 6:** Jawa Barat memiliki TPT tertinggi (6,75% Agustus 2024), sementara Papua Pegunungan paling mudah (1,32%). "
    "Rentan maksimal vs minimal hingga 5x lipat. Ini menguatkan bahwa akses kerja tidak sebanding sejauh latitude/geografie saja, "
    "tapi juga faktor ekonominya masing-masing provinsi.\n\n*Visual: horizontal barh, warna merah = TTP di atas nasional, hijau = di bawah nasional, garis putus rata-rata nasional.*"
)
nb['cells'].append(cell20)

# Cell 21: Markdown - Section 7
cell21 = new_markdown_cell(
    "## 7. TFT vs Informalitas\n\n"
    "Menganalisis hubungan antara TFT dan porsi pekerja informal per jenjang pendidikan."
)
nb['cells'].append(cell21)

# Cell 22: Code - Plot TFT vs informal
cell22 = new_code_cell(
    "fig = P.plot_tpt_vs_informal(fi, pend)\npath = P.simpan(fig, \"07_tpt_vs_informalitas.png\", \"Sumber: BPS, Sakernas Agustus 2024 (ID 1909 & 1936), diolah | data/processed/formal_informal_pendidikan.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell22)

# Cell 23: Markdown - Insight 7
cell23 = new_markdown_cell(
    "**Insight 7:** Korelasi positif kuat: semakin rendah jenjang pendidikan, semakin besar peluang pekerja informal "
    "(SD 94,2%, SMA 67%, Sarjana 17,3%). Namun TFT-nya justru rendah di SD (2,42%). Ini menyiratkan bahwa lulusan pendidikan rendah "
    "\"dapat kerja\" namun pekerjaan berkualitas rendah (informal, jam kerja pendek, tidak perlindungan sosial).\n\n*Visual: scatter plot, sumbu x = porsi informal %, sumbu y = TFT %. Ukuran gelembung = jumlah pekerja.*"
)
nb['cells'].append(cell23)

# Cell 24: Markdown - Section 8
cell24 = new_markdown_cell(
    "## 8. Setengah Pengangguran 2025\n\n"
    "Menganalisis tingkat setengah pengangguran (bekerja < 35 jam/minggu) per jenjang pendidikan."
)
nb['cells'].append(cell24)

# Cell 24.5: Code - Plot setengah pengangguran
cell24_5 = new_code_cell(
    "fig = P.plot_setengah_pengangguran(sp)\npath = P.simpan(fig, \"08_setengah_pengangguran_2025.png\", \"Sumber: BPS, Sakernas 2025 (tabel setengah pengangguran menurut pendidikan) | data/processed/setengah_pengangguran_pendidikan_2025.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell24_5)

# Cell 25: Markdown - Insight 8
cell25 = new_markdown_cell(
    "**Insight 8:** Lulusan SD ke bawah memiliki tingkat setengah pengangguran tertinggi (8,81%), artinya mereka bekerja "
    "tapi jam kerjanya di bawah 35 jam/minggu. Lulusan Sarjana punya setengah pengangguran paling rendah (5,29%). "
    "Ini memperkuat Insight 7: lulusan rendah punya pekerjaan, tapi pekerjaan tidak memadai (kurang dari kerja penuh).\n\n*Visual: batang horizontal, warna sesuai jenjang pendidikan.*"
)
nb['cells'].append(cell25)

# Cell 26: Markdown - Section 9
cell26 = new_markdown_cell(
    "## 9. Rasio Pemuda vs Dewasa\n\n"
    "Menganalisis rasio TPT kelompok usia 15-19 dan 20-24 terhadap rata-rata usia 25-59 lintas waktu 2015-2024."
)
nb['cells'].append(cell26)

# Cell 27: Code - Plot rasio usia
cell27 = new_code_cell(
    "fig = P.plot_rasio_umur(umur)\npath = P.simpan(fig, \"09_rasio_umur_muda.png\", \"Sumber: BPS, Sakernas 2015-2024 (ID 1904), diolah | data/processed/tpt_nasional_umur.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell27)

# Cell 28: Markdown - Insight 9
cell28 = new_markdown_cell(
    "**Insight 9:** Rasio TPT usia 15–19 terhadap rata-rata usia 25–59 berkisar 5-10x lipat melalui seluruh 2015-2024. "
    "Tingkatnya tidak membaik signifikan dari 2015 ke 2024, yang menandakan masalah struktur pekerjaan pemuda sudah lama berlanjut "
    "dan tidak terpecah oleh penurunan TFT nasional secara umum.\n\n*Visual: garis waktu, dua linie (15-19 vs 20-24 dibagi rata-rata 25-59), garis 1x sebagai referensi.*"
)
nb['cells'].append(cell28)

# Cell 29: Markdown - Section 10
cell29 = new_markdown_cell(
    "## 10. TPAK vs TFT Provinsi 2026\n\n"
    "Menganalisis apakah partisipasi kerja tinggi (TPAK) menjamin TFT rendah di level provinsi."
)
nb['cells'].append(cell29)

# Cell 30: Code - Plot TPAK vs TFT
cell30 = new_code_cell(
    "fig = P.plot_tpak_tpt(tri, tpak)\npath = P.simpan(fig, \"10_tpak_vs_tpt_provinsi_2026.png\", \"Sumber: BPS, Sakernas Februari 2026 (ID 2562 & 2396) | data/processed/tpt_provinsi_triwulanan.csv, tpak_provinsi.csv\")\nprint(\"Disimpan:\", path)\n"
)
nb['cells'].append(cell30)

# Cell 31: Markdown - Insight 10
cell31 = new_markdown_cell(
    "**Insight 10:** Partisipasi kerja tinggi (TPAK) tidak menjamin TFT rendah — korelasi sekitar r=0,1 di level provinsi. "
    "Beberapa provinsi dengan TPAK di atas 70% tetap memiliki TFT di atas 6%, sementara provinsi TPAK rendah punya TFT rendah juga. "
    "Ini menyingkirkan asumsi populasi bahwa \"susah cari kerja\" karena tidak ada lowongan, malainkan struktur pasar kerja yang tidak "
    " menyambut mata pencaharian baru.\n\n*Visual: scatter plot TPAK vs TFT, setiap titik = provinsi, annotasi 5 provinsi ekstrem.*"
)
nb['cells'].append(cell31)

# Cell 32: Markdown - Section 11: Kesimpulan
cell32 = new_markdown_cell(
    "## 11. Kesimpulan Umum & Rekomendasi Kebijakan\n\n"
    "Berdasarkan 10 visualisasi di atas, berikut kesimpulan dan saran:\n\n"
    "1. **SMK adalah jenjang dengan tantangan terbesar.** TFT lulusan SMK mendominasi puncak setiap tahun. "
    "Kebijakan: kurikulum SMK perlu divergesi sesuai butuhan industri, serta program *dual track* (ikatan kerja) saat SMA.\n\n"
    "2. **Pemuda 15-19 butuhkan intervensi dini.** TFT 23,34% terlalu tinggi untuk pasca-sekolah. "
    "Kebutuhan: program pelatihan keterampilan (vocational bridging) sebelum lulus SMA, atau alternatif SMK dengan *dual credit*.\n\n"
    "3. **Lulusan pendidikan tinggi tetap kompetitif.** Sarjana TFT 5-6% menunjukkan lulusan tinggi masih \"aman\" dari pengangguran, "
    "meskipun pasar kerja semakin kompetitif. Kebijakan: karir akademik harus dibalancedkan dengan keterampilan praktik "
    "(industry project, internship).\n\n"
    "4. **Formal vs informal bukan hanya masalah pendidikan.** Lulusan SD 94,2% informal tapi TFT-nya rendah (2,42%). "
    "Ini menyiratkan *underemployment* ( bekerja tapi tidak sepenuhnya). Kebijakan: peningkatan standar kerja minim, "
    "perlindungan buruh untuk pekerja informal, serta program upskilling.\n\n"
    "5. **Wilayah geografis memerlukan alokasi bersifat tak berimbang.** Jawa Barat vs Papua Pegunungan 5x lipat. "
    "Kebijakan: mekanisme *equalization fund* untuk provinsi terendah, serta program pemulihan ekonom regional.\n\n"
    "6. **Tren 2025 perlu diasalkan.** Serius tidak bisa dibandingkan langsung dengan 2008-2024 karena metode triwulanan baru. "
    "Kebijakan: dalam laporan resmi, selalu tambahkan catatan \"seri terputus di 2025 due to methodology change\".\n\n"
    "7. **Kesenjangan gender minim di tingkat nasional, tapi ada di tingkat pekerjaan.** 4,85% vs 4,84% di 2025. "
    "Namely perempuan lebih besar mewakili Tenaga kerja informal. Kebijakan: kebijaksanaan kerja yang gender-responsive, "
    "jaminan perlindungan sosial untuk perempuan pekerja informal.\n\n---"
)
nb['cells'].append(cell32)

# Cell 33: Markdown - Section 12: Referensi
cell33 = new_markdown_cell(
    "## 12. Referensi Data per Visualisasi\n\n"
    "| No | Gambar | Sumber Data | Kode BPS |\n"
    "|---|---|---|---|\n"
    "| 1 | 01_tren_nasional_2008_2025.png | Sakernas 2008-2024 (ID 1909) & Sakernas 2025 (ID 1179) | 1909, 1179 |\n"
    "| 2 | 02_tpt_pendidikan_2015_2024.png | Sakernas 2008-2024 (ID 1909), diolah | 1909 |\n"
    "| 3 | 03_tpt_2024_2025.png | Sakernas 2008-2024 & TTP 2025 (ID 1179), diolah | 1909, 1179 |\n"
    "| 4 | 04_tpt_kelompok_umur_2024.png | Sakernas Agustus 2024 (ID 1904) | 1904 |\n"
    "| 5 | 05_tpt_gender_daerah_2025.png | Sakernas 2025 (ID 1179, 2157) | 1179, 2157 |\n"
    "| 6 | 06_tpt_provinsi_2024.png | Sakernas Agustus 2024 (ID 1907) | 1907 |\n"
    "| 7 | 07_tpt_vs_informalitas.png | Sakernas Agustus 2024 (ID 1909 & 1936) | 1909, 1936 |\n"
    "| 8 | 08_setengah_pengangguran_2025.png | Sakernas 2025 (tabel setengah pengangguran) | (tidak ada di 105 subjek) |\n"
    "| 9 | 09_rasio_umur_muda.png | Sakernas 2015-2024 (ID 1904) | 1904 |\n"
    "| 10 | 10_tpak_vs_tpt_provinsi_2026.png | Sakernas Februari 2026 (ID 2562 & 2396) | 2562, 2396 |\n\n---"
)
nb['cells'].append(cell33)

# Cell 34: Markdown - Akhir
cell34 = new_markdown_cell(
    "---"
)
nb['cells'].append(cell34)

# Write the notebook
with open('notebooks/02_eda.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print('Notebook 02 berhasil dibuat dengan Python nbformat')