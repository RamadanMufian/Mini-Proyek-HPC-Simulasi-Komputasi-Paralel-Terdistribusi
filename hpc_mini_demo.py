"""
Mini Demo HPC untuk Tantangan Lokal (versi laptop)
Berdasarkan materi: Infrastruktur Komputasi Global untuk Mengatasi Tantangan Lokal (HPC)

Isi:
  Bagian 1 - Ukur kecepatan komputasi dalam GFLOPS (float32 vs float64)
  Bagian 2 - Simulasi epidemi SIR dengan parameter sweep, dijalankan paralel
             (contoh tantangan lokal: pelacakan penyebaran epidemi)
  Bagian 3 - Hitung speedup & efisiensi paralel (dasar performance tuning)

Cara pakai:
  pip install numpy matplotlib
  python hpc_mini_demo.py
"""
import os
import time
from multiprocessing import Pool

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ------------------------------------------------------------------
# BAGIAN 1: BENCHMARK FLOPS
# FLOPS = Floating Point Operations Per Second.
# Perkalian matriks n x n butuh sekitar 2 * n^3 operasi floating point.
# Catatan: numpy memakai BLAS yang bisa multi-thread, jadi hasilnya
# mencerminkan seluruh core CPU Anda.
# ------------------------------------------------------------------
def benchmark_flops(n=1500, repeat=3):
    print("=== BAGIAN 1: Benchmark GFLOPS ===")
    hasil = {}
    for dtype in (np.float32, np.float64):
        a = np.random.rand(n, n).astype(dtype)
        b = np.random.rand(n, n).astype(dtype)
        a @ b  # pemanasan
        waktu = []
        for _ in range(repeat):
            t0 = time.perf_counter()
            a @ b
            waktu.append(time.perf_counter() - t0)
        terbaik = min(waktu)
        gflops = 2 * n**3 / terbaik / 1e9
        hasil[np.dtype(dtype).name] = gflops
        print(f"{np.dtype(dtype).name:>8}: {terbaik:.3f} detik -> {gflops:8.1f} GFLOPS")
    rasio = hasil["float32"] / hasil["float64"]
    print(f"float32 sekitar {rasio:.1f}x lebih cepat dari float64 "
          f"(tapi presisinya lebih rendah)\n")
    return hasil


# ------------------------------------------------------------------
# BAGIAN 2: SIMULASI EPIDEMI SIR (parameter sweep)
# S' = -beta*S*I ; I' = beta*S*I - gamma*I ; R' = gamma*I
# Tiap kombinasi (beta, gamma) independen -> "embarrassingly parallel",
# sehingga cocok dibagi ke banyak core / node.
# ------------------------------------------------------------------
HARI = 200
DT = 0.01


def simulasi_sir(params):
    """Satu simulasi. Mengembalikan (puncak infeksi, hari puncak)."""
    beta, gamma = params
    s, i, r = 0.999, 0.001, 0.0
    puncak, hari_puncak = i, 0.0
    langkah = int(HARI / DT)
    for k in range(langkah):
        infeksi_baru = beta * s * i * DT
        sembuh = gamma * i * DT
        s -= infeksi_baru
        i += infeksi_baru - sembuh
        r += sembuh
        if i > puncak:
            puncak, hari_puncak = i, k * DT
    return puncak, hari_puncak


def jalankan_sweep(daftar_param, n_pekerja):
    t0 = time.perf_counter()
    if n_pekerja == 1:
        hasil = [simulasi_sir(p) for p in daftar_param]
    else:
        with Pool(n_pekerja) as pool:
            hasil = pool.map(simulasi_sir, daftar_param, chunksize=8)
    return hasil, time.perf_counter() - t0


def sweep_paralel(ukuran_grid=20):
    print("=== BAGIAN 2: Simulasi epidemi SIR (parameter sweep) ===")
    betas = np.linspace(0.2, 1.0, ukuran_grid)
    gammas = np.linspace(0.05, 0.5, ukuran_grid)
    daftar = [(b, g) for b in betas for g in gammas]
    print(f"Jumlah simulasi: {len(daftar)} (grid {ukuran_grid}x{ukuran_grid})")

    n_core = os.cpu_count() or 1
    kandidat = sorted({1, 2, 4, 8, n_core})
    kandidat = [k for k in kandidat if k <= max(n_core, 2)]
    print(f"Core terdeteksi: {n_core} | Uji jumlah pekerja: {kandidat}")

    # ---------------- BAGIAN 3: speedup & efisiensi ----------------
    print("\n=== BAGIAN 3: Speedup & Efisiensi ===")
    print(f"{'pekerja':>8} {'waktu (s)':>10} {'speedup':>9} {'efisiensi':>10}")
    waktu_serial, hasil_terakhir, baris = None, None, []
    for n in kandidat:
        hasil, waktu = jalankan_sweep(daftar, n)
        if n == 1:
            waktu_serial = waktu
        speedup = waktu_serial / waktu
        efisiensi = speedup / n
        baris.append((n, waktu, speedup, efisiensi))
        hasil_terakhir = hasil
        print(f"{n:>8} {waktu:>10.2f} {speedup:>9.2f} {efisiensi:>9.0%}")

    puncak = np.array([h[0] for h in hasil_terakhir]).reshape(ukuran_grid, ukuran_grid)
    return betas, gammas, puncak, baris


def buat_grafik(betas, gammas, puncak, baris, nama_file="hasil_hpc.png"):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))

    im = ax[0].imshow(puncak, origin="lower", aspect="auto",
                      extent=[gammas[0], gammas[-1], betas[0], betas[-1]])
    ax[0].set(xlabel="gamma (laju sembuh)", ylabel="beta (laju menular)",
              title="Puncak proporsi terinfeksi")
    fig.colorbar(im, ax=ax[0])

    n = [b[0] for b in baris]
    sp = [b[2] for b in baris]
    ax[1].plot(n, sp, "o-", label="speedup terukur")
    ax[1].plot(n, n, "--", color="gray", label="ideal (linear)")
    ax[1].set(xlabel="Jumlah pekerja", ylabel="Speedup", title="Skalabilitas paralel")
    ax[1].legend()

    plt.tight_layout()
    plt.savefig(nama_file, dpi=120)
    print(f"\nGrafik disimpan: {nama_file}")


if __name__ == "__main__":
    benchmark_flops()
    betas, gammas, puncak, baris = sweep_paralel(ukuran_grid=20)
    buat_grafik(betas, gammas, puncak, baris)
