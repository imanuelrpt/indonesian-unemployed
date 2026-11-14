"""
plots.py
========
Gaya dan fungsi grafik untuk seluruh proyek.

Aturan yang dipakai di semua grafik (supaya konsisten dan bisa dinilai):
1. Judul grafik adalah **kesimpulan**, bukan sekadar nama variabel.
2. Setiap sumbu punya label + satuan (mis. "TPT (%)").
3. Ada footer sumber data di bagian bawah gambar.
4. Angka desimal memakai koma (format Indonesia).
5. Warna dipakai konsisten: jenjang SMK selalu merah bata, SMA biru, Sarjana hijau.

Semua fungsi menerima DataFrame hasil `src.cleaning` (tidak membaca raw langsung)
dan mengembalikan objek `matplotlib.figure.Figure`.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# --- Palet ---------------------------------------------------------------
WARNA = {
    "utama": "#1f4e79",   # biru tua: seri utama
    "aksen": "#c0504d",   # merah bata: penekanan / SMK
    "netral": "#9e9e9e",  # abu: pembanding
    "kuning": "#ed7d31",
    "hijau": "#548235",
    "gelap": "#333333",
}

PALET_PENDIDIKAN = {
    "SD ke bawah": "#b3b3b3",
    "SMP": "#8fa9bf",
    "SMA": "#2e75b6",
    "SMK": "#c0504d",
    "Diploma": "#ed7d31",
    "Sarjana": "#548235",
}

URUTAN_PENDIDIKAN = ["SD ke bawah", "SMP", "SMA", "SMK", "Diploma", "Sarjana"]


def setup_style() -> None:
    """Setel gaya global. Panggil sekali di awal notebook."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10.5,
            "axes.titlesize": 13.5,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.labelsize": 10.5,
            "axes.labelcolor": "#3a3a3a",
            "axes.edgecolor": "#d5d5d5",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#e8e8e8",
            "grid.linewidth": 0.8,
            "xtick.color": "#5a5a5a",
            "ytick.color": "#5a5a5a",
            "legend.frameon": False,
            "figure.dpi": 110,
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
        }
    )


# --- Utilitas ------------------------------------------------------------
def pct(nilai: float, desimal: int = 1) -> str:
    """Format persen gaya Indonesia: 9.01 -> '9,0%'."""
    return f"{nilai:.{desimal}f}".replace(".", ",") + "%"


def angka(nilai: float, desimal: int = 0) -> str:
    """Format angka ribuan gaya Indonesia: 7465599 -> '7.465.599'."""
    return f"{nilai:,.{desimal}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def koma(nilai: float, desimal: int = 1) -> str:
    """Angka dengan koma desimal: 7.93 -> '7,9'."""
    return f"{nilai:.{desimal}f}".replace(".", ",")


def periode_ke_tanggal(periode):
    """'2024-08' -> Timestamp 2024-08-01. Menerima skalar maupun Series."""
    if isinstance(periode, pd.Series):
        return pd.to_datetime(periode + "-01", format="%Y-%m-%d")
    return pd.to_datetime(f"{periode}-01", format="%Y-%m-%d")


def sumbu_persen(ax, axis: str = "y", desimal: int = 0) -> None:
    fmt = FuncFormatter(lambda v, _pos: f"{v:.{desimal}f}".replace(".", ",") + "%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def judul(ax, teks: str, sub: str | None = None) -> None:
    ax.set_title(teks, loc="left", pad=24 if sub else 12, color="#1a1a1a")
    if sub:
        ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=9.5, color="#6b6b6b", va="bottom")


def simpan(fig, nama: str, sumber: str) -> Path:
    """Simpan PNG ke outputs/figures dengan footer sumber."""
    fig.text(0.005, -0.03, sumber, ha="left", va="top", fontsize=7.5, color="#7a7a7a", wrap=True)
    path = FIG_DIR / nama
    fig.savefig(path)
    return path


def _tpt_6level(pend: pd.DataFrame) -> pd.DataFrame:
    """TPT per kelompok pendidikan 6 level, dibobot dengan angkatan kerja."""
    d = pend[pend["pendidikan"] != "Indonesia"]
    g = d.groupby(["periode", "kelompok_pendidikan"])[["pengangguran", "angkatan_kerja"]].sum().reset_index()
    g["tpt"] = g["pengangguran"] / g["angkatan_kerja"] * 100
    return g


# --- 1. Tren nasional ----------------------------------------------------
def plot_tren_nasional(pend: pd.DataFrame, tpt_2025: float):
    d = pend[pend["pendidikan"] == "Indonesia"].copy()
    d["tgl"] = periode_ke_tanggal(d["periode"])
    d = d.sort_values("tgl")

    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    ax.plot(d["tgl"], d["tpt"], color=WARNA["utama"], lw=2.2, marker="o", ms=3.6, zorder=3)

    # tandai puncak pandemi
    puncak = d.loc[d["tpt"].idxmax()]
    ax.scatter(puncak["tgl"], puncak["tpt"], s=70, color=WARNA["aksen"], zorder=4)
    ax.annotate(
        f"Puncak pandemi {puncak['periode'][:4]}: {pct(puncak['tpt'])}",
        xy=(puncak["tgl"], puncak["tpt"]),
        xytext=(-10, 18), textcoords="offset points", fontsize=9, color=WARNA["aksen"],
        ha="right",
    )

    # titik 2025 (seri baru, tidak disambung)
    tgl25 = pd.Timestamp("2025-02-01")
    ax.scatter(tgl25, tpt_2025, s=70, marker="D", color=WARNA["kuning"], zorder=5)
    ax.annotate(
        f"2025: {pct(tpt_2025)} (seri triwulanan baru)",
        xy=(tgl25, tpt_2025), xytext=(-6, -26), textcoords="offset points",
        fontsize=9, color="#8a4a10", ha="right",
    )

    awal15 = d[d["periode"] == "2015-02"]["tpt"].iloc[0]
    akhir = d.iloc[-1]
    judul(
        ax,
        f"TPT nasional turun {koma(awal15 - akhir['tpt'])} poin persen sejak 2015, "
        "tetapi naik lagi pada 2024",
        "Tingkat Pengangguran Terbuka, Indonesia, Februari 2008–Agustus 2024 "
        "(titik 2025 terpisah karena ganti metodologi survei)",
    )
    ax.set_xlabel("Periode survei")
    ax.set_ylabel("TPT (%)")
    ax.set_ylim(3.0, 9.2)
    sumbu_persen(ax, desimal=1)
    ax.axvline(pd.Timestamp("2020-03-01"), color="#cccccc", ls=":", lw=1)
    ax.text(pd.Timestamp("2020-04-01"), 8.9, "awal pandemi", fontsize=8.5, color="#8a8a8a")
    ax.margins(x=0.02)
    return fig


# --- 2. Tren per jenjang -------------------------------------------------
def plot_tren_pendidikan(pend: pd.DataFrame, mulai: str = "2015-02"):
    d = _tpt_6level(pend)
    d = d[d["periode"] >= mulai].copy()
    d["tgl"] = periode_ke_tanggal(d["periode"])

    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    sorot = {"SMK": 2.4, "SMA": 2.0, "Sarjana": 1.9}
    geser = {"Diploma": (6, -9), "Sarjana": (6, 5), "SMP": (6, -3), "SD ke bawah": (6, -2)}
    for jenjang in URUTAN_PENDIDIKAN:
        s = d[d["kelompok_pendidikan"] == jenjang].sort_values("tgl")
        lw = sorot.get(jenjang, 1.2)
        warna = PALET_PENDIDIKAN[jenjang]
        ax.plot(s["tgl"], s["tpt"], color=warna, lw=lw, label=jenjang,
                alpha=1 if jenjang in sorot else 0.55, zorder=3 if jenjang in sorot else 2)
        akhir = s.iloc[-1]
        ax.annotate(
            jenjang, xy=(akhir["tgl"], akhir["tpt"]),
            xytext=geser.get(jenjang, (6, 0)), textcoords="offset points",
            fontsize=9, color=warna, fontweight="bold" if jenjang in sorot else "normal",
            va="center",
        )

    smk = d[d["kelompok_pendidikan"] == "SMK"].sort_values("tgl").iloc[-1]
    sd = d[d["kelompok_pendidikan"] == "SD ke bawah"].sort_values("tgl").iloc[-1]
    judul(
        ax,
        f"Lulusan SMK paling sulit dapat kerja: {pct(smk['tpt'])} vs {pct(sd['tpt'])} "
        "pada lulusan SD ke bawah",
        "TPT menurut jenjang pendidikan (6 kategori harmonis), 2015–2024",
    )
    ax.set_xlabel("Periode survei")
    ax.set_ylabel("TPT (%)")
    ax.set_ylim(0, 16)
    ax.set_xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2025-07-01"))
    ax.set_xticks(pd.to_datetime([f"{y}-01-01" for y in range(2015, 2025)]))
    ax.set_xticklabels([str(y) for y in range(2015, 2025)])
    sumbu_persen(ax)
    return fig


# --- 3. Perbandingan 2024 vs 2025 ---------------------------------------
def plot_perbandingan_2025(banding: pd.DataFrame):
    warna_per = {"2024-02": "#9dc3e6", "2024-08": "#2e75b6", "2025-02": "#c0504d"}
    label_per = {"2024-02": "Feb 2024", "2024-08": "Agu 2024", "2025-02": "2025"}

    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    x = np.arange(len(URUTAN_PENDIDIKAN))
    lebar = 0.26
    for i, per in enumerate(["2024-02", "2024-08", "2025-02"]):
        s = banding[banding["periode"] == per].set_index("kelompok_pendidikan").reindex(URUTAN_PENDIDIKAN)
        ax.bar(x + (i - 1) * lebar, s["tpt"], width=lebar, color=warna_per[per],
               label=label_per[per], edgecolor="white", linewidth=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels(URUTAN_PENDIDIKAN)
    ax.set_xlabel("Jenjang pendidikan tertinggi yang ditamatkan")
    ax.set_ylabel("TPT (%)")
    ax.set_ylim(0, 10.5)
    sumbu_persen(ax)
    ax.legend(ncol=3, loc="upper right")
    ax.grid(axis="x", visible=False)

    t24 = banding[banding["periode"] == "2024-08"].set_index("kelompok_pendidikan")["tpt"]
    t25 = banding[banding["periode"] == "2025-02"].set_index("kelompok_pendidikan")["tpt"]
    judul(
        ax,
        "SMK masih paling sulit dapat kerja pada 2025; hanya lulusan Sarjana yang TPT-nya naik",
        f"TPT per jenjang, 2024 (Feb & Agu) dan 2025 — "
        f"SMK {pct(t24['SMK'])} → {pct(t25['SMK'])}, Sarjana {pct(t24['Sarjana'])} → {pct(t25['Sarjana'])}",
    )
    return fig


# --- 4. Kelompok umur ----------------------------------------------------
def plot_umur(umur: pd.DataFrame, periode: str = "2024-08"):
    d = umur[(umur["periode"] == periode) & (umur["kelompok_umur"] != "Total")].copy()
    d = d.sort_values("tpt", ascending=True)

    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    warna = [WARNA["aksen"] if g in ("15 - 19", "20 - 24") else WARNA["netral"] for g in d["kelompok_umur"]]
    ax.barh(d["kelompok_umur"], d["tpt"], color=warna, height=0.7)
    for _, r in d.iterrows():
        ax.text(r["tpt"] + 0.3, r["kelompok_umur"], pct(r["tpt"]), va="center", fontsize=9,
                color="#333333")

    muda = d[d["kelompok_umur"] == "15 - 19"]["tpt"].iloc[0]
    tua = d[d["kelompok_umur"] == "60 +"]["tpt"].iloc[0]
    judul(
        ax,
        f"Pemuda 15–19 tahun {muda / tua:.0f} kali lebih berisiko menganggur dibanding usia 60+",
        f"TPT menurut kelompok umur, Agustus 2024",
    )
    ax.set_xlabel("TPT (%)")
    ax.set_ylabel("Kelompok umur (tahun)")
    ax.set_xlim(0, max(d["tpt"]) * 1.18)
    sumbu_persen(ax, "x")
    ax.grid(axis="y", visible=False)
    return fig


# --- 5. Gender & kota-desa (2025) ---------------------------------------
def plot_gender_daerah(snap: pd.DataFrame):
    gender = snap[(snap["dimensi"] == "jenis_kelamin")].set_index("kategori")["nilai"]
    daerah = snap[(snap["dimensi"] == "daerah")].set_index("kategori")["nilai"]
    total = float(daerah.get("Perkotaan + Perdesaan", np.nan))

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.9))
    ax = axes[0]
    ax.bar(["Laki-laki", "Perempuan"], [gender.get("Laki-Laki"), gender.get("Perempuan")],
           color=[WARNA["utama"], WARNA["kuning"]], width=0.55)
    for i, v in enumerate([gender.get("Laki-Laki"), gender.get("Perempuan")]):
        ax.text(i, v + 0.06, pct(v, 2), ha="center", fontsize=10)
    ax.set_ylim(0, 6.2)
    ax.set_ylabel("TPT (%)")
    ax.set_title("Gender: hampir tidak ada celah", loc="left", fontsize=11, pad=8)
    sumbu_persen(ax, "y", 1)
    ax.grid(axis="x", visible=False)

    ax = axes[1]
    ax.bar(["Perkotaan", "Perdesaan"], [daerah.get("Perkotaan"), daerah.get("Perdesaan")],
           color=[WARNA["utama"], WARNA["hijau"]], width=0.55)
    for i, v in enumerate([daerah.get("Perkotaan"), daerah.get("Perdesaan")]):
        ax.text(i, v + 0.06, pct(v, 2), ha="center", fontsize=10)
    ax.set_ylim(0, 6.2)
    ax.set_ylabel("TPT (%)")
    ax.set_title("Kota vs desa: pengangguran lebih tinggi di kota", loc="left", fontsize=11, pad=8)
    sumbu_persen(ax, "y", 1)
    ax.grid(axis="x", visible=False)

    fig.suptitle(
        f"TPT 2025 ({pct(total, 2)}): gender seimbang, kesenjangan justru kota–desa",
        x=0.005, ha="left", fontsize=13.5, fontweight="bold", color="#1a1a1a",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return fig


# --- 6. Provinsi ---------------------------------------------------------
def plot_provinsi(prov: pd.DataFrame, periode: str = "2024-08"):
    d = prov[(prov["periode"] == periode) & (prov["provinsi"] != "Indonesia")].copy()
    nasional = prov[(prov["periode"] == periode) & (prov["provinsi"] == "Indonesia")]["tpt"].iloc[0]
    d = d.sort_values("tpt")

    fig, ax = plt.subplots(figsize=(9.2, 10.2))
    warna = []
    for _, r in d.iterrows():
        if r["tpt"] >= d["tpt"].quantile(0.75):
            warna.append(WARNA["aksen"])
        elif r["tpt"] <= d["tpt"].quantile(0.25):
            warna.append(WARNA["hijau"])
        else:
            warna.append("#9db7cd")
    ax.barh(d["provinsi"], d["tpt"], color=warna, height=0.72)
    ax.axvline(nasional, color=WARNA["gelap"], ls="--", lw=1.1)
    ax.text(nasional + 0.05, 0.2, f"nasional {pct(nasional)}", fontsize=8.5, color=WARNA["gelap"])

    for nama in d.nlargest(3, "tpt")["provinsi"].tolist() + d.nsmallest(2, "tpt")["provinsi"].tolist():
        row = d[d["provinsi"] == nama].iloc[0]
        ax.text(row["tpt"] + 0.05, nama, pct(row["tpt"]), va="center", fontsize=8.5)

    judul(
        ax,
        f"Jawa Barat paling sulit ({pct(d['tpt'].max())}), Papua Pegunungan paling mudah ({pct(d['tpt'].min())})",
        f"TPT 38 provinsi, Agustus 2024 (garis putus-putus = rata-rata nasional)",
    )
    ax.set_xlabel("TPT (%)")
    ax.set_ylabel("Provinsi")
    ax.set_xlim(0, d["tpt"].max() * 1.16)
    ax.tick_params(axis="y", labelsize=8)
    sumbu_persen(ax, "x")
    ax.grid(axis="y", visible=False)
    return fig


# --- 7. Heatmap provinsi -------------------------------------------------
def plot_heatmap_provinsi(prov: pd.DataFrame, mulai: str = "2015-02"):
    d = prov[(prov["provinsi"] != "Indonesia") & (prov["periode"] >= mulai)]
    pivot = d.pivot_table(index="provinsi", columns="periode", values="tpt", aggfunc="first")
    pivot = pivot.reindex(pivot.mean(axis=1).sort_values(ascending=False).index)

    fig, ax = plt.subplots(figsize=(10.8, 10.4))
    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_bad("#f2f2f2")
    im = ax.imshow(pivot.values, aspect="auto", cmap=cmap, vmin=0, vmax=np.nanmax(pivot.values))
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([c.replace("-02", " Feb").replace("-08", " Agu") for c in pivot.columns],
                       rotation=90, fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8)
    ax.grid(False)

    # label sel ekstrem
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            v = pivot.values[i, j]
            if np.isnan(v):
                continue
            if v >= 7.5:
                ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=6.5, color="white")
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label("TPT (%)", fontsize=9)
    cb.ax.tick_params(labelsize=8)

    judul(
        ax,
        "Hanya segelintir provinsi pernah menembus TPT 7,5% — dan itu berulang di provinsi yang sama",
        f"Peta panas TPT 38 provinsi, {mulai[:4]}–2024 (sel abu-abu = data belum tersedia)",
    )
    ax.set_xlabel("Periode survei")
    ax.set_ylabel("Provinsi")
    return fig


# --- 8. TPT vs informalitas ---------------------------------------------
def plot_tpt_vs_informal(fi: pd.DataFrame, pend: pd.DataFrame, periode: str = "2024-08"):
    informal = fi[fi["periode"] == periode].set_index("pendidikan")
    tpt = pend[(pend["periode"] == periode) & (pend["pendidikan"] != "Indonesia")].set_index("pendidikan")
    d = pd.DataFrame({"tpt": tpt["tpt"], "informal": informal["porsi_informal"],
                      "pekerja": informal["total_bekerja"]}).dropna()

    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    for nama, r in d.iterrows():
        ax.scatter(r["informal"], r["tpt"], s=max(60, r["pekerja"] / 350_000),
                   color=WARNA["utama"], alpha=0.75, edgecolor="white", linewidth=1.2, zorder=3)
        ax.annotate(nama, xy=(r["informal"], r["tpt"]), xytext=(0, 12),
                    textcoords="offset points", ha="center", fontsize=8.5, color="#333333")

    x = d["informal"].values
    y = d["tpt"].values
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min() - 3, x.max() + 3, 50)
    ax.plot(xs, m * xs + b, color=WARNA["aksen"], ls="--", lw=1.2, zorder=2)
    r = np.corrcoef(x, y)[0, 1]

    judul(
        ax,
        "Semakin rendah pendidikan, semakin kecil risiko menganggur — tapi semakin besar peluang kerja informal",
        f"TPT vs porsi pekerja informal per jenjang, Agustus 2024 (r = {r:.2f}; ukuran gelembung = jumlah pekerja)",
    )
    ax.set_xlabel("Porsi pekerja informal (%)")
    ax.set_ylabel("TPT (%)")
    ax.set_xlim(10, 100)
    ax.set_ylim(0, 7)
    sumbu_persen(ax, "x")
    sumbu_persen(ax, "y")
    return fig


# --- 9. Setengah pengangguran -------------------------------------------
def plot_setengah_pengangguran(sp: pd.DataFrame):
    d = sp.copy()
    if "kelompok_pendidikan" in d.columns:
        d = d.groupby("kelompok_pendidikan", as_index=False)["nilai"].first()
    d = d.sort_values("nilai", ascending=True)

    fig, ax = plt.subplots(figsize=(9.4, 4.9))
    warna = [PALET_PENDIDIKAN.get(k, WARNA["netral"]) for k in d["kelompok_pendidikan"]]
    ax.barh(d["kelompok_pendidikan"], d["nilai"], color=warna, height=0.65)
    for _, r in d.iterrows():
        ax.text(r["nilai"] + 0.12, r["kelompok_pendidikan"], pct(r["nilai"]), va="center", fontsize=9)

    judul(
        ax,
        "Lulusan SD ke bawah paling banyak 'setengah menganggur': bekerja, tapi jam kerjanya kurang",
        "Tingkat setengah pengangguran menurut jenjang pendidikan, 2025 (bekerja < 35 jam/minggu)",
    )
    ax.set_xlabel("Setengah pengangguran (%)")
    ax.set_ylabel("Jenjang pendidikan")
    ax.set_xlim(0, d["nilai"].max() * 1.2)
    sumbu_persen(ax, "x")
    ax.grid(axis="y", visible=False)
    return fig


# --- 10. Rasio pemuda vs dewasa -----------------------------------------
def plot_rasio_umur(umur: pd.DataFrame, mulai: str = "2015-02"):
    d = umur[umur["periode"] >= mulai].pivot_table(index="periode", columns="kelompok_umur", values="tpt")
    dewasa = ["25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59"]
    d["dewasa"] = d[dewasa].mean(axis=1)
    d["rasio_15_19"] = d["15 - 19"] / d["dewasa"]
    d["rasio_20_24"] = d["20 - 24"] / d["dewasa"]
    d = d.reset_index()
    d["tgl"] = periode_ke_tanggal(d["periode"])

    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    ax.plot(d["tgl"], d["rasio_15_19"], color=WARNA["aksen"], lw=2.4, marker="o", ms=3.5,
            label="Umur 15–19 vs 25–59")
    ax.plot(d["tgl"], d["rasio_20_24"], color=WARNA["utama"], lw=2.2, marker="s", ms=3.2,
            label="Umur 20–24 vs 25–59")
    ax.axhline(1, color="#bbbbbb", ls=":", lw=1)
    ax.text(d["tgl"].min(), 1.05, "garis 1x = setara orang dewasa", fontsize=8.5, color="#8a8a8a")

    akhir_besar = d["rasio_15_19"].iloc[-1]
    akhir_kecil = d["rasio_20_24"].iloc[-1]
    judul(
        ax,
        f"Peluang menganggur pemuda 15–19 tahun sekitar {akhir_besar:.1f}x orang dewasa, dan tidak membaik",
        "Rasio TPT kelompok muda terhadap rata-rata TPT umur 25–59, 2015–2024",
    )
    ax.set_xlabel("Periode survei")
    ax.set_ylabel("Kali lipat (x)")
    ax.set_ylim(0, 6)
    ax.legend(loc="upper right")
    ax.margins(x=0.02)
    return fig


# --- 11. TPAK vs TPT provinsi -------------------------------------------
def plot_tpak_tpt(prov: pd.DataFrame, tpak: pd.DataFrame, periode: str = "2026-02"):
    a = prov[(prov["periode"] == periode) & (prov["provinsi"] != "Indonesia")][["provinsi", "tpt"]]
    b = tpak[(tpak["periode"] == periode) & (tpak["provinsi"] != "Indonesia")][["provinsi", "tpak"]]
    d = a.merge(b, on="provinsi")

    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    ax.scatter(d["tpak"], d["tpt"], s=55, color=WARNA["utama"], alpha=0.8,
               edgecolor="white", linewidth=1, zorder=3)
    r = np.corrcoef(d["tpak"], d["tpt"])[0, 1]

    for nama in d.nlargest(3, "tpt")["provinsi"].tolist() + d.nsmallest(2, "tpt")["provinsi"].tolist():
        row = d[d["provinsi"] == nama].iloc[0]
        ax.annotate(nama, xy=(row["tpak"], row["tpt"]), xytext=(0, 9), textcoords="offset points",
                    ha="center", fontsize=8.5, color="#333333")

    judul(
        ax,
        f"Partisipasi kerja tinggi tidak menjamin pengangguran rendah (r = {r:.2f})",
        "TPAK vs TPT 38 provinsi, Februari 2026",
    )
    ax.set_xlabel("TPAK — Tingkat Partisipasi Angkatan Kerja (%)")
    ax.set_ylabel("TPT (%)")
    sumbu_persen(ax, "x")
    sumbu_persen(ax, "y")
    return fig