"""
Estimasi pi dengan Monte Carlo memakai MPI (mpi4py)
Contoh paling sederhana "pemrograman paralel terdistribusi" ala HPC:
tiap proses (rank) menghitung bagiannya, lalu hasilnya digabung (reduce).

Instalasi (perlu library MPI di sistem, mis. OpenMPI):
  sudo apt install openmpi-bin libopenmpi-dev     # Ubuntu/WSL
  pip install mpi4py numpy

Jalankan di laptop dengan 4 proses:
  mpirun -n 4 python mpi_monte_carlo_pi.py

Jalankan di cluster HPC: lihat job.slurm
"""
import time
import numpy as np

TOTAL_TITIK = 40_000_000


def hitung_titik_dalam_lingkaran(n_titik, seed):
    """Lempar n_titik acak ke kotak 1x1, hitung yang jatuh di dalam seperempat lingkaran."""
    rng = np.random.default_rng(seed)
    x = rng.random(n_titik)
    y = rng.random(n_titik)
    return int(np.count_nonzero(x * x + y * y <= 1.0))


def main():
    from mpi4py import MPI  # import di sini agar fungsi di atas bisa diuji tanpa MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()   # nomor proses ini (0..size-1)
    size = comm.Get_size()   # jumlah seluruh proses

    # Bagi beban kerja rata; sisa pembagian diberikan ke rank-rank awal
    jatah = TOTAL_TITIK // size + (1 if rank < TOTAL_TITIK % size else 0)

    comm.Barrier()
    t0 = MPI.Wtime()

    # Seed berbeda per rank supaya angka acaknya tidak kembar
    dalam_lokal = hitung_titik_dalam_lingkaran(jatah, seed=1234 + rank)

    # Gabungkan hasil semua rank ke rank 0
    dalam_total = comm.reduce(dalam_lokal, op=MPI.SUM, root=0)

    comm.Barrier()
    waktu = MPI.Wtime() - t0

    if rank == 0:
        pi_estimasi = 4 * dalam_total / TOTAL_TITIK
        print(f"Jumlah proses : {size}")
        print(f"Total titik   : {TOTAL_TITIK:,}")
        print(f"Estimasi pi   : {pi_estimasi:.6f} (selisih {abs(pi_estimasi - np.pi):.6f})")
        print(f"Waktu         : {waktu:.3f} detik")


if __name__ == "__main__":
    main()
