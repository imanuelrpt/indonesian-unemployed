"""
cleaning.py
===========
Modul pembersihan data mentah BPS Sakernas -> tabel tidy (long) di `data/processed/`.

Prinsip:
1. File di `data/raw/` TIDAK PERNAH diubah. Semua transformasi terjadi di memori.
2. Tidak ada imputasi. Nilai kosong ("-") dibiarkan NaN dan alasannya dicatat.
3. Angka TPT yang dihitung sendiri (pengangguran / angkatan kerja) diberi
   penanda kolom `sumber_tpt`, sehingga jelas mana yang terbitan BPS dan mana turunan.
4. Setiap tabel keluaran menyimpan `sumber_file` agar bisa ditelusuri ke raw.

Jalankan:  python -m src.cleaning
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Path
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

PERIODE_KE_BULAN = {"Februari": "02", "Mei": "05", "Agustus": "08", "November": "11"}

# Catatan pembersihan yang dikumpulkan selama proses dan ditulis ke _validasi.csv
CATATAN: list[dict] = []

# --------------------------------------------------------------------------
# Kamus standardisasi
# --------------------------------------------------------------------------
# Label pendidikan apa adanya dari BPS -> label standar + kelompok harmonis 6 level.
# Kelompok harmonis dipakai agar 2008-2024 (8 kategori) bisa dibandingkan dengan
# 2025 (6 kategori, SD ke bawah digabung).
EDU_MAP: dict[str, tuple[str, str]] = {
    "Tidak/belum pernah sekolah": ("Tidak/belum pernah sekolah", "SD ke bawah"),
    "Tidak/belum tamat SD": ("Tidak/belum tamat SD", "SD ke bawah"),
    "SD": ("SD", "SD ke bawah"),
    "SLTP": ("SMP", "SMP"),
    "SLTA Umum/SMU": ("SMA", "SMA"),
    "SLTA Kejuruan/SMK": ("SMK", "SMK"),
    "Akademi/Diploma": ("Diploma", "Diploma"),
    "Universitas": ("Sarjana", "Sarjana"),
    "Tak Terjawab": ("Tak terjawab", "Tak terjawab"),
    "Total": ("Indonesia", "Indonesia"),
    # --- varian tabel snapshot 2023/2025 ---
    # Perhatikan: pada tabel 2023 "Tidak Sekolah" dan "Tidak Tamat SD/MI" masih
    # dipisah. Keduanya TIDAK digabung di kolom `pendidikan` supaya nilai
    # terbitan BPS tidak berubah; penggabungan hanya di `kelompok_pendidikan`.
    "Tidak/Belum Pernah Sekolah/Belum Tamat & Tamat SD": ("SD ke bawah", "SD ke bawah"),
    "Tidak Sekolah": ("Tidak sekolah", "SD ke bawah"),
    "Tidak Tamat SD/MI": ("Tidak tamat SD", "SD ke bawah"),
    "SMP": ("SMP", "SMP"),
    "SMA umum": ("SMA", "SMA"),
    "SMA Kejuruan": ("SMK", "SMK"),
    "Diploma I/II/III": ("Diploma", "Diploma"),
    "Universitas": ("Sarjana", "Sarjana"),
    "Indonesia": ("Indonesia", "Indonesia"),
}

# Kunci pencarian dibuat case-insensitive supaya "SMA Umum" dan "SMA umum"
# jatuh ke label yang sama.
EDU_LOOKUP = {re.sub(r"\s+", " ", k).strip().lower(): v for k, v in EDU_MAP.items()}

# Kode provinsi BPS (38 provinsi, penamaan 2024)
PROV_KODE: dict[str, str] = {
    "Aceh": "11",
    "Sumatera Utara": "12",
    "Sumatera Barat": "13",
    "Riau": "14",
    "Jambi": "15",
    "Sumatera Selatan": "16",
    "Bengkulu": "17",
    "Lampung": "18",
    "Kep. Bangka Belitung": "19",
    "Kep. Riau": "21",
    "DKI Jakarta": "31",
    "Jawa Barat": "32",
    "Jawa Tengah": "33",
    "DI Yogyakarta": "34",
    "Jawa Timur": "35",
    "Banten": "36",
    "Bali": "51",
    "Nusa Tenggara Barat": "52",
    "Nusa Tenggara Timur": "53",
    "Kalimantan Barat": "61",
    "Kalimantan Tengah": "62",
    "Kalimantan Selatan": "63",
    "Kalimantan Timur": "64",
    "Kalimantan Utara": "65",
    "Sulawesi Utara": "71",
    "Sulawesi Tengah": "72",
    "Sulawesi Selatan": "73",
    "Sulawesi Tenggara": "74",
    "Gorontalo": "75",
    "Sulawesi Barat": "76",
    "Maluku": "81",
    "Maluku Utara": "82",
    "Papua Barat": "91",
    "Papua Barat Daya": "92",
    "Papua": "94",
    "Papua Selatan": "95",
    "Papua Tengah": "96",
    "Papua Pegunungan": "97",
}

# Alias nama provinsi dari tabel triwulanan (HURUF BESAR) -> nama kanonik
PROV_ALIAS = {
    "BANGKA BELITUNG": "Kep. Bangka Belitung",
    "KEP BANGKA BELITUNG": "Kep. Bangka Belitung",
    "KEPULAUAN RIAU": "Kep. Riau",
    "KEP RIAU": "Kep. Riau",
    "D I Y": "DI Yogyakarta",
    "DIY": "DI Yogyakarta",
    "YOGYAKARTA": "DI Yogyakarta",
    "DI YOGYAKARTA": "DI Yogyakarta",
}

STATUS_MAP = {
    "1 Berusaha Sendiri": ("Berusaha sendiri", "Informal"),
    "2 Berusaha dibantu Buruh Tidak Tetap/Tidak Dibayar": ("Berusaha dibantu buruh tidak tetap", "Informal"),
    "3 Berusaha dibantu Buruh Tetap/Dibayar": ("Berusaha dibantu buruh tetap", "Formal"),
    "4 Buruh/Karyawan/Pegawai": ("Buruh/karyawan/pegawai", "Formal"),
    "5 Pekerja bebas pertanian": ("Pekerja bebas di pertanian", "Informal"),
    "6 Pekerja bebas non pertanian": ("Pekerja bebas di non-pertanian", "Informal"),
    "7 Pekerja keluarga/tak dibayar": ("Pekerja keluarga/tidak dibayar", "Informal"),
    "9 Tak Terjawab": ("Tak terjawab", "Tak terjawab"),
    "Total": ("Total", "Total"),
}


# --------------------------------------------------------------------------
# Utilitas
# --------------------------------------------------------------------------
def to_num(x) -> float:
    """Ubah sel BPS menjadi float.

    Format di CSV BPS adalah format Inggris: '1,437,402.00' -> 1437402.0.
    Sel kosong, '-' (data tidak tersedia), dan '...' -> NaN (tanpa imputasi).
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    s = str(x).strip()
    if s in {"", "-", "nan", "None", "...", "*"}:
        return np.nan
    s = s.replace(",", "").replace(" ", "")
    try:
        return float(s)
    except ValueError:
        return np.nan


def periode_label(tahun: int, periode: str) -> str:
    """'2024-08' - format periode yang konsisten untuk seluruh proyek."""
    return f"{tahun}-{PERIODE_KE_BULAN[periode]}"


def std_pendidikan(label: str) -> tuple[str, str]:
    """Label pendidikan BPS -> (label standar, kelompok harmonis 6 level)."""
    key = re.sub(r"\s+", " ", str(label)).strip()
    if key.lower() in EDU_LOOKUP:
        return EDU_LOOKUP[key.lower()]
    return (key, key)


def std_provinsi(label: str) -> tuple[str, str]:
    """Kembalikan (kode, nama kanonik). Menerima '11 Aceh' atau 'ACEH' atau 'D I Y'."""
    s = str(label).strip()
    if s.lower() == "total" or s.upper() == "INDONESIA":
        return ("00", "Indonesia")

    m = re.match(r"^(\d{2})\s+(.*)$", s)
    if m:
        kode, nama = m.group(1), m.group(2)
        # nama di file seri sudah dalam Title Case; rapikan alias
        kanonik = PROV_ALIAS.get(nama.upper(), nama)
        # 'Kepulauan Riau' (seri) vs 'Kep. Riau' (kanonik)
        if kanonik.upper() == "KEPULAUAN RIAU":
            kanonik = "Kep. Riau"
        if kanonik.upper() == "BANGKA-BELITUNG":
            kanonik = "Kep. Bangka Belitung"
        return (kode, kanonik)

    key = re.sub(r"[.\-]", " ", s.upper())
    key = re.sub(r"\s+", " ", key).strip()
    kanonik = PROV_ALIAS.get(key, s.title())
    return (PROV_KODE.get(kanonik, "??"), kanonik)


def read_raw(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name, header=None, dtype=str, encoding="utf-8-sig")


def find_blocks(df: pd.DataFrame) -> list[tuple[int, int, int, str]]:
    """Deteksi blok tahun pada tabel 'seri panjang' BPS.

    Tabel disusun bertumpuk: baris berisi '2008 Februari' di kolom 1, diikuti
    baris header AK/BAK, lalu baris data. Kolom 11-20 = periode Agustus.

    Mengembalikan list (tahun, baris_awal_data, baris_akhir_data, periode).
    """
    pat = re.compile(r"^(19|20)\d{2} (Februari|Agustus)$")
    starts: list[tuple[int, int, str]] = []
    for i in range(len(df)):
        m = pat.match(str(df.iloc[i, 1]).strip())
        if m:
            starts.append((int(str(df.iloc[i, 1]).split()[0]), i, str(df.iloc[i, 1]).split()[1]))

    blocks = []
    for k, (tahun, row, per) in enumerate(starts):
        end = starts[k + 1][1] if k + 1 < len(starts) else len(df)
        blocks.append((tahun, row + 3, end, per))
    return blocks


# --------------------------------------------------------------------------
# Parser per jenis tabel
# --------------------------------------------------------------------------
def parse_kegiatan(path_name: str, dim_name: str) -> pd.DataFrame:
    """Tabel 'jenis kegiatan': Bekerja | Pengangguran | Jumlah AK | %Bekerja/AK | BAK... | TPAK.

    Berlaku untuk tabel pendidikan, provinsi (ID 1907), dan kelompok umur (ID 1904).
    """
    df = read_raw(path_name)
    rows = []
    for tahun, start, end, _per in find_blocks(df):
        for r in range(start, end):
            label = df.iloc[r, 0]
            if pd.isna(label):
                continue
            for per, c in (("Februari", 1), ("Agustus", 11)):
                peng = to_num(df.iloc[r, c + 1])
                ak = to_num(df.iloc[r, c + 2])
                if np.isnan(peng) and np.isnan(ak):
                    continue  # baris catatan kaki / kosong
                rows.append(
                    {
                        dim_name: str(label).strip(),
                        "periode": periode_label(tahun, per),
                        "tahun": tahun,
                        "periode_survei": per,
                        "bekerja": to_num(df.iloc[r, c]),
                        "pengangguran": peng,
                        "angkatan_kerja": ak,
                        "bukan_angkatan_kerja": to_num(df.iloc[r, c + 7]),
                        "penduduk_usia_kerja": to_num(df.iloc[r, c + 8]),
                        "tpak": to_num(df.iloc[r, c + 9]),
                        "sumber_file": path_name,
                    }
                )
    out = pd.DataFrame(rows)
    out["tpt"] = (out["pengangguran"] / out["angkatan_kerja"] * 100).round(2)
    out["sumber_tpt"] = "dihitung (pengangguran/AK)"
    return out


def _header_groups(df: pd.DataFrame, bounds_row: int, label_row: int) -> list[list[tuple[int, str]]]:
    """Kelompokkan kolom pendidikan per periode.

    Tabel matriks BPS punya dua blok periode berdampingan tanpa kolom kosong
    pemisah, sehingga batas blok dibaca dari baris judul periode (mis. kolom 1
    berisi '2008 Februari' dan kolom 10 berisi '2008 Agustus'). Label pendidikan
    lalu diambil dari baris di bawahnya, mulai dari kolom batas tersebut.

    Lebar blok bisa berbeda antar tabel: blok 2024 yang diulang BPS hanya punya
    6 kategori + Total (7 kolom), jadi lebar tidak boleh diasumsikan 9.
    """
    batas = [
        j for j in range(1, df.shape[1]) if not pd.isna(df.iloc[bounds_row, j])
    ]
    groups: list[list[tuple[int, str]]] = []
    for k, mulai in enumerate(batas):
        selesai = batas[k + 1] if k + 1 < len(batas) else df.shape[1]
        grup = [
            (j, str(df.iloc[label_row, j]).strip())
            for j in range(mulai, selesai)
            if not pd.isna(df.iloc[label_row, j])
        ]
        groups.append(grup)
    return groups


def parse_matrix(path_name: str, dim_name: str) -> pd.DataFrame:
    """Tabel matriks: baris = dimensi (status/lapangan usaha), kolom = pendidikan.

    Header dibaca per blok. BPS mengulang blok 2024 dengan 6 kategori
    (bentuk harmonisasi baru); blok duplikat tahun dilewati karena isinya
    agregasi dari blok 8 kategori yang sudah dipakai.
    """
    df = read_raw(path_name)
    rows = []
    seen_tahun: set[int] = set()
    for tahun, start, end, _per in find_blocks(df):
        if tahun in seen_tahun:
            CATATAN.append(
                {
                    "tabel": path_name,
                    "cek": f"blok {tahun} ganda dilewati",
                    "nilai": 1,
                    "status": "info",
                    "catatan": "BPS mengulang blok 2024 dengan 6 kategori; dipakai blok 8 kategori",
                }
            )
            continue
        seen_tahun.add(tahun)

        groups = _header_groups(df, start - 2, start - 1)
        for per, grup in zip(("Februari", "Agustus"), groups):
            for j, edu_raw in grup:
                for r in range(start, end):
                    label = df.iloc[r, 0]
                    if pd.isna(label):
                        continue
                    val = to_num(df.iloc[r, j])
                    if np.isnan(val):
                        continue
                    rows.append(
                        {
                            dim_name: str(label).strip(),
                            "pendidikan_bps": edu_raw,
                            "periode": periode_label(tahun, per),
                            "tahun": tahun,
                            "periode_survei": per,
                            "jumlah": val,
                            "sumber_file": path_name,
                        }
                    )
    out = pd.DataFrame(rows)
    out[["pendidikan", "kelompok_pendidikan"]] = out["pendidikan_bps"].apply(
        lambda s: pd.Series(std_pendidikan(s))
    )
    return out


def parse_snapshot(path_name: str, dimensi: str) -> pd.DataFrame:
    """Tabel snapshot 2 kolom (2023/2025): <kategori>, <nilai persen>."""
    df = read_raw(path_name)
    judul = str(df.iloc[1, 1]).strip()
    tahun = str(df.iloc[2, 1]).strip()
    rows = []
    for i in range(3, len(df)):
        kat = df.iloc[i, 0]
        val = to_num(df.iloc[i, 1])
        if pd.isna(kat) or np.isnan(val):
            continue
        rows.append(
            {
                "dimensi": dimensi,
                "kategori": str(kat).strip(),
                "tahun": int(tahun),
                "nilai": val,
                "satuan": "persen",
                "judul_tabel": judul,
                "sumber_file": path_name,
            }
        )
    return pd.DataFrame(rows)


def parse_triwulanan(path_name: str, tahun: int) -> pd.DataFrame:
    """Tabel TPT provinsi triwulanan (ID 2562): kolom Februari/Mei/Agustus/November."""
    df = read_raw(path_name)
    header = [str(x).strip() for x in df.iloc[3].tolist()]
    kolom = {i: h for i, h in enumerate(header) if h in PERIODE_KE_BULAN}
    rows = []
    for r in range(4, len(df)):
        prov = df.iloc[r, 0]
        if pd.isna(prov):
            continue
        for i, per in kolom.items():
            val = to_num(df.iloc[r, i])
            if np.isnan(val):
                continue  # '-' = belum tersedia, bukan nol
            kode, nama = std_provinsi(prov)
            rows.append(
                {
                    "kode_provinsi": kode,
                    "provinsi": nama,
                    "periode": periode_label(tahun, per),
                    "tpt": val,
                    "sumber_file": path_name,
                }
            )
    return pd.DataFrame(rows)


def parse_tpak_provinsi(path_name: str, tahun: int) -> pd.DataFrame:
    df = read_raw(path_name)
    header = [str(x).strip() for x in df.iloc[3].tolist()]
    kolom = {i: h for i, h in enumerate(header) if h in PERIODE_KE_BULAN}
    rows = []
    for r in range(4, len(df)):
        prov = df.iloc[r, 0]
        if pd.isna(prov):
            continue
        for i, per in kolom.items():
            val = to_num(df.iloc[r, i])
            if np.isnan(val):
                continue
            kode, nama = std_provinsi(prov)
            rows.append(
                {
                    "kode_provinsi": kode,
                    "provinsi": nama,
                    "periode": periode_label(tahun, per),
                    "tpak": val,
                    "sumber_file": path_name,
                }
            )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Bangun semua tabel turunan
# --------------------------------------------------------------------------
def build_nasional_pendidikan() -> pd.DataFrame:
    df = parse_kegiatan("bps_pendidikan_jenis_kegiatan_2008_2024.csv", "pendidikan_bps")
    df[["pendidikan", "kelompok_pendidikan"]] = df["pendidikan_bps"].apply(
        lambda s: pd.Series(std_pendidikan(s))
    )
    # 'Tak Terjawab' bernilai 0 pada seluruh periode (AK = 0) sehingga TPT tidak
    # terdefinisi. Baris ini dikeluarkan dari tabel analisis dan jumlahnya dicatat.
    n_drop = int((df["pendidikan"] == "Tak terjawab").sum())
    df = df[df["pendidikan"] != "Tak terjawab"].copy()
    df["catatan"] = ""
    CATATAN.append(
        {
            "tabel": "tpt_nasional_pendidikan",
            "cek": "baris 'Tak terjawab' dibuang (AK=0, TPT tidak terdefinisi)",
            "nilai": n_drop,
            "status": "info",
            "catatan": "kategori tetap ada di raw; hanya dihapus dari tabel analisis",
        }
    )
    return df[
        [
            "periode", "tahun", "periode_survei", "pendidikan_bps", "pendidikan",
            "kelompok_pendidikan", "bekerja", "pengangguran", "angkatan_kerja",
            "bukan_angkatan_kerja", "penduduk_usia_kerja", "tpak", "tpt",
            "sumber_tpt", "catatan", "sumber_file",
        ]
    ]


def build_provinsi() -> pd.DataFrame:
    df = parse_kegiatan("bps_provinsi_jenis_kegiatan_2008_2024.csv", "provinsi_bps")
    df[["kode_provinsi", "provinsi"]] = df["provinsi_bps"].apply(
        lambda s: pd.Series(std_provinsi(s))
    )
    # Kalimantan Utara (65) baru dimekarkan dari Kalimantan Timur pada 2012 dan
    # mulai disurvei terpisah pada Sakernas 2015 -> 2008-2014 AK = 0 (NA).
    # Provinsi Papua hasil pemekaran 2022/2023 tidak muncul sebelum 2023.
    df["catatan"] = ""
    df.loc[df["tpt"].isna(), "catatan"] = "AK = 0; provinsi belum disurvei terpisah"
    return df[
        [
            "periode", "tahun", "periode_survei", "kode_provinsi", "provinsi",
            "bekerja", "pengangguran", "angkatan_kerja", "bukan_angkatan_kerja",
            "penduduk_usia_kerja", "tpak", "tpt", "sumber_tpt", "catatan", "sumber_file",
        ]
    ]


def build_umur() -> pd.DataFrame:
    df = parse_kegiatan("bps_umur_jenis_kegiatan_2008_2024.csv", "kelompok_umur")
    return df[
        [
            "periode", "tahun", "periode_survei", "kelompok_umur",
            "bekerja", "pengangguran", "angkatan_kerja", "bukan_angkatan_kerja",
            "penduduk_usia_kerja", "tpak", "tpt", "sumber_tpt", "sumber_file",
        ]
    ]


def build_status_pekerjaan() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Status pekerjaan x pendidikan (orang) -> long + ringkasan formal/informal.

    Definisi BPS: formal = (3) berusaha dibantu buruh tetap + (4) buruh/karyawan;
    informal = (1), (2), (5), (6), (7).
    """
    df = parse_matrix("bps_status_pekerjaan_pendidikan_2008_2024.csv", "status_pekerjaan")
    df[["status_pekerjaan", "kelompok_status"]] = df["status_pekerjaan"].apply(
        lambda s: pd.Series(STATUS_MAP.get(s, (s, "Lainnya")))
    )
    long = df[
        [
            "periode", "tahun", "periode_survei", "status_pekerjaan",
            "kelompok_status", "pendidikan", "kelompok_pendidikan", "jumlah", "sumber_file",
        ]
    ].copy()

    # 'Tak terjawab' dan baris 'Total' status tidak dipakai untuk porsi formal/informal
    long = long[~long["pendidikan"].isin(["Tak terjawab"])].copy()

    # ringkasan: porsi informal per pendidikan
    pivot = (
        long[long["kelompok_status"].isin(["Formal", "Informal"])]
        .groupby(["periode", "tahun", "periode_survei", "pendidikan", "kelompok_pendidikan", "kelompok_status"])[
            "jumlah"
        ]
        .sum()
        .unstack("kelompok_status")
        .reset_index()
    )
    pivot["total_bekerja"] = pivot["Formal"] + pivot["Informal"]
    pivot["porsi_informal"] = (pivot["Informal"] / pivot["total_bekerja"] * 100).round(2)
    pivot["porsi_formal"] = (pivot["Formal"] / pivot["total_bekerja"] * 100).round(2)
    pivot["sumber_file"] = "bps_status_pekerjaan_pendidikan_2008_2024.csv (diolah)"
    return long, pivot


def build_snapshot_2025() -> pd.DataFrame:
    parts = [
        parse_snapshot("bps_tpt_pendidikan_2025.csv", "pendidikan"),
        parse_snapshot("bps_tpt_jenis_kelamin_2025.csv", "jenis_kelamin"),
        parse_snapshot("bps_tpt_kota_desa_2025.csv", "daerah"),
        parse_snapshot("bps_tpt_kelompok_umur_2025.csv", "kelompok_umur"),
    ]
    df = pd.concat(parts, ignore_index=True)
    df["kategori"] = df["kategori"].str.replace(r"\s*-\s*", "-", regex=True).str.strip()
    return df


def build_perbandingan_2024_2025(pend: pd.DataFrame, snap: pd.DataFrame) -> pd.DataFrame:
    """TPT per jenjang pada level 6 kategori: Feb 2024, Agu 2024, dan 2025.

    Tujuannya satu: membuat 2024 dan 2025 sebanding. Untuk 2024, TPT dihitung
    dari agregat pengangguran/angkatan kerja per kelompok (bukan rata-rata dari
    TPT tiap jenjang, karena rata-rata polos akan salah bobot).
    """
    rows = []
    for per in ("2024-02", "2024-08"):
        g = pend[(pend["periode"] == per) & (pend["pendidikan"] != "Indonesia")]
        agg = g.groupby("kelompok_pendidikan")[["pengangguran", "angkatan_kerja"]].sum()
        for kel, r in agg.iterrows():
            rows.append(
                {
                    "periode": per,
                    "tahun": 2024,
                    "kelompok_pendidikan": kel,
                    "pengangguran": r["pengangguran"],
                    "angkatan_kerja": r["angkatan_kerja"],
                    "tpt": round(r["pengangguran"] / r["angkatan_kerja"] * 100, 2),
                    "sumber_data": "seri 2008-2024 (dihitung)",
                    "sumber_file": "bps_pendidikan_jenis_kegiatan_2008_2024.csv (diolah)",
                }
            )

    s25 = snap[(snap["dimensi"] == "pendidikan")]
    for _, r in s25.iterrows():
        kel = std_pendidikan(r["kategori"])[1]
        if kel == "Indonesia":
            continue
        rows.append(
            {
                "periode": "2025-02",
                "tahun": 2025,
                "kelompok_pendidikan": kel,
                "pengangguran": np.nan,
                "angkatan_kerja": np.nan,
                "tpt": float(r["nilai"]),
                "sumber_data": "tabel 2025 (terbitan BPS)",
                "sumber_file": r["sumber_file"],
            }
        )
    return pd.DataFrame(rows)


def build_informal_2023() -> pd.DataFrame:
    df = parse_snapshot("bps_informal_pendidikan_2023.csv", "pendidikan")
    df[["pendidikan", "kelompok_pendidikan"]] = df["kategori"].apply(
        lambda s: pd.Series(std_pendidikan(s))
    )
    return df[["tahun", "kategori", "pendidikan", "kelompok_pendidikan", "nilai", "satuan", "sumber_file"]]


def build_setengah_pengangguran_2025() -> pd.DataFrame:
    df = parse_snapshot("bps_setengah_pengangguran_pendidikan_2025.csv", "pendidikan")
    df[["pendidikan", "kelompok_pendidikan"]] = df["kategori"].apply(
        lambda s: pd.Series(std_pendidikan(s))
    )
    return df[["tahun", "kategori", "pendidikan", "kelompok_pendidikan", "nilai", "satuan", "sumber_file"]]


# --------------------------------------------------------------------------
# Validasi
# --------------------------------------------------------------------------
def validate(df: pd.DataFrame, nama: str, kolom_nilai: str, kunci: list[str]) -> list[dict]:
    hasil = []
    n = len(df)
    dup = int(df.duplicated(subset=kunci).sum())
    nilai = df[kolom_nilai].dropna()
    out_of_range = int(((nilai < 0) | (nilai > 100)).sum())
    hasil.append(
        {"tabel": nama, "cek": "jumlah baris", "nilai": n, "status": "info", "catatan": ""}
    )
    hasil.append(
        {
            "tabel": nama,
            "cek": f"duplikat pada {kunci}",
            "nilai": dup,
            "status": "OK" if dup == 0 else "GAGAL",
            "catatan": "",
        }
    )
    hasil.append(
        {
            "tabel": nama,
            "cek": f"{kolom_nilai} di luar 0-100",
            "nilai": out_of_range,
            "status": "OK" if out_of_range == 0 else "GAGAL",
            "catatan": f"min={nilai.min():.2f}, max={nilai.max():.2f}",
        }
    )
    hasil.append(
        {
            "tabel": nama,
            "cek": f"{kolom_nilai} kosong (NaN)",
            "nilai": int(df[kolom_nilai].isna().sum()),
            "status": "info",
            "catatan": "kosong dibiarkan, tidak diimputasi",
        }
    )
    return hasil


def cek_konsistensi(df: pd.DataFrame, nama: str) -> list[dict]:
    """Cek aritmetika dasar: pengangguran <= AK, dan jumlah bagian = total."""
    hasil = []
    jml = df.dropna(subset=["pengangguran", "angkatan_kerja"])
    lebih = int((jml["pengangguran"] > jml["angkatan_kerja"] + 0.5).sum())
    hasil.append(
        {
            "tabel": nama,
            "cek": "pengangguran > angkatan kerja",
            "nilai": lebih,
            "status": "OK" if lebih == 0 else "GAGAL",
            "catatan": "",
        }
    )
    return hasil


def cek_jumlah_bagian(df: pd.DataFrame, nama: str, kolom_dim: str, label_total: str) -> list[dict]:
    """Bandingkan jumlah baris rincian dengan baris 'Indonesia' per periode."""
    hasil = []
    selisih_maks = 0.0
    periode_buruk = ""
    for per, grup in df.groupby("periode"):
        total = grup.loc[grup[kolom_dim] == label_total, "pengangguran"]
        if total.empty:
            continue
        rincian = grup.loc[grup[kolom_dim] != label_total, "pengangguran"].sum()
        selisih = abs(rincian - float(total.iloc[0]))
        if selisih > selisih_maks:
            selisih_maks, periode_buruk = selisih, per
    hasil.append(
        {
            "tabel": nama,
            "cek": "jumlah rincian vs baris Indonesia (orang)",
            "nilai": round(selisih_maks, 2),
            "status": "OK" if selisih_maks < 1 else "PERIKSA",
            "catatan": (
                "tidak ada selisih" if not periode_buruk
                else f"selisih terbesar pada {periode_buruk}"
            ),
        }
    )
    return hasil


def main() -> None:
    log: list[dict] = []

    # 1. TPT nasional menurut pendidikan (2008-2024)
    pend = build_nasional_pendidikan()
    pend.to_csv(PROC / "tpt_nasional_pendidikan.csv", index=False)
    log += validate(pend, "tpt_nasional_pendidikan", "tpt", ["periode", "pendidikan"])
    log += cek_konsistensi(pend, "tpt_nasional_pendidikan")
    log += cek_jumlah_bagian(pend, "tpt_nasional_pendidikan", "pendidikan", "Indonesia")

    # 2. TPT provinsi (2008-2024)
    prov = build_provinsi()
    prov.to_csv(PROC / "tpt_provinsi.csv", index=False)
    log += validate(prov, "tpt_provinsi", "tpt", ["periode", "kode_provinsi"])
    log += cek_konsistensi(prov, "tpt_provinsi")
    log += cek_jumlah_bagian(prov, "tpt_provinsi", "provinsi", "Indonesia")

    # 3. TPT nasional menurut kelompok umur
    umur = build_umur()
    umur.to_csv(PROC / "tpt_nasional_umur.csv", index=False)
    log += validate(umur, "tpt_nasional_umur", "tpt", ["periode", "kelompok_umur"])

    # 4. Status pekerjaan x pendidikan
    status_long, status_ringkas = build_status_pekerjaan()
    status_long.to_csv(PROC / "status_pekerjaan_pendidikan.csv", index=False)
    status_ringkas.to_csv(PROC / "formal_informal_pendidikan.csv", index=False)
    log += validate(status_ringkas, "formal_informal_pendidikan", "porsi_informal", ["periode", "pendidikan"])

    # 4b. Uji silang: total bekerja (status) vs bekerja (tabel pendidikan)
    beda_maks = 0.0
    for per, g in status_ringkas.groupby("periode"):
        tot = g.loc[g["pendidikan"] == "Indonesia", "total_bekerja"]
        ref = pend.loc[(pend["periode"] == per) & (pend["pendidikan"] == "Indonesia"), "bekerja"]
        if tot.empty or ref.empty:
            continue
        beda_maks = max(beda_maks, abs(float(tot.iloc[0]) - float(ref.iloc[0])))
    log.append(
        {
            "tabel": "silang",
            "cek": "total bekerja (status) vs bekerja (pendidikan), orang",
            "nilai": round(beda_maks, 2),
            "status": "OK" if beda_maks < 1 else "PERIKSA",
            "catatan": "selisih terbesar seluruh periode",
        }
    )

    # 5. Snapshot 2025 (pendidikan, gender, kota/desa, umur)
    snap = build_snapshot_2025()
    snap.to_csv(PROC / "snapshot_2025.csv", index=False)
    log += validate(snap, "snapshot_2025", "nilai", ["dimensi", "kategori"])

    # 6. Informal per pendidikan 2023
    inf = build_informal_2023()
    inf.to_csv(PROC / "informal_pendidikan_2023.csv", index=False)
    log += validate(inf, "informal_pendidikan_2023", "nilai", ["tahun", "kategori"])

    # 5b. Perbandingan TPT per jenjang 2024 vs 2025 (level 6 kategori)
    banding = build_perbandingan_2024_2025(pend, snap)
    banding.to_csv(PROC / "tpt_pendidikan_2024_2025.csv", index=False)
    log += validate(banding, "tpt_pendidikan_2024_2025", "tpt", ["periode", "kelompok_pendidikan"])
    log.append(
        {
            "tabel": "tpt_pendidikan_2024_2025",
            "cek": "jumlah jenjang per periode",
            "nilai": int(banding.groupby("periode").size().max()),
            "status": "OK" if banding.groupby("periode").size().eq(6).all() else "PERIKSA",
            "catatan": "harus 6 jenjang pada tiap periode",
        }
    )

    # 7. Setengah pengangguran per pendidikan 2025
    sp = build_setengah_pengangguran_2025()
    sp.to_csv(PROC / "setengah_pengangguran_pendidikan_2025.csv", index=False)
    log += validate(sp, "setengah_pengangguran_pendidikan_2025", "nilai", ["tahun", "kategori"])

    # 8. TPT provinsi triwulanan 2025-2026
    tri = pd.concat(
        [
            parse_triwulanan("bps_tpt_provinsi_triwulanan_2025.csv", 2025),
            parse_triwulanan("bps_tpt_provinsi_triwulanan_2026.csv", 2026),
        ],
        ignore_index=True,
    )
    tri.to_csv(PROC / "tpt_provinsi_triwulanan.csv", index=False)
    log += validate(tri, "tpt_provinsi_triwulanan", "tpt", ["periode", "kode_provinsi"])

    # 9. TPAK provinsi 2026
    tpak = parse_tpak_provinsi("bps_tpak_provinsi_2026.csv", 2026)
    tpak.to_csv(PROC / "tpak_provinsi.csv", index=False)
    log += validate(tpak, "tpak_provinsi", "tpak", ["periode", "kode_provinsi"])

    # 10. Uji konsistensi nasional vs jumlah provinsi
    for per in ["2024-02", "2024-08"]:
        nas = pend[(pend["periode"] == per) & (pend["pendidikan"] == "Indonesia")]
        pr = prov[(prov["periode"] == per) & (prov["provinsi"] == "Indonesia")]
        if len(nas) and len(pr):
            selisih = abs(nas["pengangguran"].iloc[0] - pr["pengangguran"].iloc[0])
            log.append(
                {
                    "tabel": "silang",
                    "cek": f"pengangguran nasional vs total provinsi {per}",
                    "nilai": round(selisih, 2),
                    "status": "OK" if selisih < 1 else "PERIKSA",
                    "catatan": f"pendidikan={nas['pengangguran'].iloc[0]:,.0f}, provinsi={pr['pengangguran'].iloc[0]:,.0f}",
                }
            )

    # 11. Uji terhadap angka terbitan BPS (2025)
    terbit = snap[(snap["dimensi"] == "pendidikan")]
    nas25 = terbit[terbit["kategori"].str.upper().str.contains("INDONESIA")]
    if len(nas25):
        log.append(
            {
                "tabel": "silang",
                "cek": "TPT nasional 2025 (tabel terbitan) vs 2024-08 (hitung)",
                "nilai": float(nas25["nilai"].iloc[0]),
                "status": "info",
                "catatan": "pembanding level, bukan uji identik (periode beda)",
            }
        )

    log_df = pd.DataFrame(log + CATATAN)
    log_df.to_csv(PROC / "_validasi.csv", index=False)

    print("Selesai. Tabel tersimpan di:", PROC)
    for f in sorted(PROC.glob("*.csv")):
        print(f"  - {f.name:45s} {len(pd.read_csv(f)):5d} baris")
    print("\nRingkasan validasi:")
    print(log_df.to_string(index=False))


if __name__ == "__main__":
    main()
