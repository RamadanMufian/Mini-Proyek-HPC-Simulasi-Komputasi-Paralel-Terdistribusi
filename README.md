# 🚀 Mini Proyek HPC: Simulasi & Komputasi Paralel Terdistribusi

Repositori ini berisi serangkaian modul praktikum dan demonstrasi **High Performance Computing (HPC)** berbasis Python. Repositori ini dirancang untuk menjembatani konsep teoretis komputasi performa tinggi dengan penerapannya di dunia nyata—mulai dari lingkungan lokal (laptop/PC) hingga lingkungan klaster superkomputer (*multi-node cluster*) berbasis **Slurm**.

---

## 📌 Daftar Isi
1. [Tentang Sistem](#-tentang-sistem)
2. [Struktur File](#-struktur-file)
3. [Prasyarat & Kebutuhan Sistem](#-prasyarat--kebutuhan-sistem)
4. [Instalasi & Persiapan Lingkungan](#-instalasi--persiapan-lingkungan)
5. [Panduan Penggunaan Program](#-panduan-penggunaan-program)
   - [1. HPC Mini Demo (`hpc_mini_demo.py`)](#1-hpc-mini-demo-hpc_mini_demopy)
   - [2. MPI Monte Carlo $\pi$ (`mpi_monte_carlo_pi.py`)](#2-mpi-monte-carlo--mpi_monte_carlo_pipy)
   - [3. Job Script Cluster HPC (`job.slurm`)](#3-job-script-cluster-hpc-jobslurm)
6. [Konsep Inti HPC yang Diterapkan](#-konsep-inti-hpc-yang-diterapkan)
7. [Panduan Troubleshooting](#-panduan-troubleshooting)

---

## 📖 Tentang Sistem

Sistem ini memodelkan tiga pilar utama dalam High Performance Computing:
1. **CPU Benchmark & Presisi Floating Point:** Mengukur kapasitas komputasi murni prosesor dalam satuan GFLOPS (*Giga Floating-Point Operations per Second*) serta perbandingan efisiensi `float32` vs `float64`.
2. **Shared-Memory Parallelism (Multiprocessing):** Menyelesaikan permasalahan simulasi epidemi SIR (*Susceptible-Infectious-Recovered*) dengan metode *parameter sweep* (pencarian ruang parameter) secara paralel di seluruh core CPU lokal.
3. **Distributed-Memory Parallelism (MPI & Slurm):** Menghitung aproksimasi nilai Pi ($\pi$) dengan metode Monte Carlo menggunakan *Message Passing Interface* (MPI) yang dapat diskalakan ke banyak node komputasi melalui Slurm Workload Manager.

---

## 📂 Struktur File

| Berkas | Jenis Lingkungan | Deskripsi |
| :--- | :--- | :--- |
| [`hpc_mini_demo.py`](file:///c:/Users/ASUS/Downloads/hpc/hpc_mini_demo.py) | Komputer Lokal (Laptop/PC) | Mengukur GFLOPS, menjalankan simulasi epidemi SIR secara paralel (`multiprocessing.Pool`), mengukur *speedup* & efisiensi, dan menghasilkan grafik `hasil_hpc.png`. |
| [`mpi_monte_carlo_pi.py`](file:///c:/Users/ASUS/Downloads/hpc/mpi_monte_carlo_pi.py) | Lokal / Cluster Terdistribusi | Estimasi nilai $\pi$ menggunakan 40 juta titik acak terdistribusi antar-proses via `mpi4py` (`MPI.COMM_WORLD` & `reduce`). |
| [`job.slurm`](file:///c:/Users/ASUS/Downloads/hpc/job.slurm) | Cluster HPC / Superkomputer | Skrip *batch submission* Slurm untuk mengorkestrasi eksekusi `mpi_monte_carlo_pi.py` pada 2 node komputasi dengan total 16 proses. |

---

## 🛠 Prasyarat & Kebutuhan Sistem

- **Sistem Operasi:** Windows (PowerShell/CMD), Linux (Ubuntu/Debian), atau macOS.
- **Python:** Versi 3.8 ke atas.
- **Paket Python:**
  - `numpy`
  - `matplotlib`
  - `mpi4py` *(khusus untuk modul MPI)*
- **MPI Runtime (Opsional untuk MPI):**
  - **Linux / WSL:** `OpenMPI` (`openmpi-bin`, `libopenmpi-dev`) atau `MPICH`.
  - **Windows:** Microsoft MPI (MS-MPI) v10+ (jika ingin menjalankan MPI langsung di Windows).

---

## ⚙️ Instalasi & Persiapan Lingkungan

### 1. Di Komputer Lokal (Windows / macOS / Linux)

Buka terminal atau PowerShell, arahkan ke direktori proyek, lalu instal paket dasar:

```bash
pip install numpy matplotlib
```

### 2. Persiapan untuk Eksekusi MPI (Modul 2)

#### Pada Linux / WSL (Sangat Direkomendasikan untuk MPI):
```bash
# Update repository paket
sudo apt update

# Instal pustaka MPI
sudo apt install -y openmpi-bin libopenmpi-dev

# Instal mpi4py
pip install mpi4py
```

#### Pada Windows Native:
1. Unduh dan instal **MS-MPI v10+** (keduanya: `msmpisetup.exe` dan `msmpisdk.msi`) dari situs resmi Microsoft.
2. Jalankan perintah instalasi pustaka Python:
   ```bash
   pip install mpi4py
   ```

---

## 🚀 Panduan Penggunaan Program

### 1. HPC Mini Demo (`hpc_mini_demo.py`)

Skrip ini berdiri sendiri (*standalone*) dan tidak membutuhkan MPI. Skrip ini memanfaatkan CPU multi-core komputer Anda.

#### Cara Menjalankan:
```bash
python hpc_mini_demo.py
```

#### Apa yang Dilakukan Skrip Ini?
1. **Bagian 1 - Benchmark GFLOPS:**
   - Melakukan perkalian matriks $1500 \times 1500$ sebanyak 3 iterasi.
   - Membandingkan performa antara `float32` (single precision) dan `float64` (double precision).
2. **Bagian 2 - Simulasi Epidemi SIR (Parameter Sweep):**
   - Mensimulasikan model dinamika penyebaran penyakit $S \to I \to R$ sepanjang 200 hari.
   - Menyapu (*sweep*) parameter $\beta$ (laju penularan: 0.2 hingga 1.0) dan $\gamma$ (laju kesembuhan: 0.05 hingga 0.5) dalam grid $20 \times 20$ (total 400 skenario).
   - Karena tiap skenario bersifat independen (*embarrassingly parallel*), pembagian beban kerja dialokasikan ke sejumlah *worker* menggunakan `multiprocessing.Pool`.
3. **Bagian 3 - Analisis Skalabilitas:**
   - Menguji kombinasi jumlah pekerja (misal: 1, 2, 4, 8 core).
   - Menghitung nilai **Speedup** dan **Efisiensi Paralel**.
4. **Visualisasi Output:**
   - Menyimpan visualisasi ke berkas gambar **`hasil_hpc.png`**:
     - *Heatmap*: Puncak proporsi infeksi terhadap variasi parameter $\beta$ dan $\gamma$.
     - *Grafik Garis*: Skalabilitas speedup terukur dibandingkan garis ideal (linear).

---

### 2. MPI Monte Carlo $\pi$ (`mpi_monte_carlo_pi.py`)

Skrip ini mendemonstrasikan komputasi paralel memori terdistribusi (*distributed-memory parallelism*). 

#### Cara Menjalankan di Laptop/PC Lokal:
Gunakan `mpirun` dengan menentukan jumlah proses (flag `-n`):

```bash
# Menjalankan dengan 4 proses
mpirun -n 4 python mpi_monte_carlo_pi.py
```

*(Catatan: Anda dapat mengubah angka `4` sesuai jumlah core fisik atau thread CPU Anda, misalnya 2, 8, atau 16).*

#### Alur Kerja Algoritma:
1. Total beban kerja adalah **40.000.000 titik**.
2. Setiap proses (rank) menerima porsi titik yang dibagi rata: $\text{jatah} = \frac{\text{TOTAL\_TITIK}}{\text{size}}$.
3. Setiap rank menggunakan generator angka acak mandiri (`seed = 1234 + rank`) agar distribusi titik tidak identik.
4. Setiap rank menghitung titik yang masuk ke kuadran lingkaran ($x^2 + y^2 \le 1.0$).
5. Menggunakan operasi kolektif **`comm.reduce(..., op=MPI.SUM, root=0)`**, seluruh hasil parsial dijumlahkan dan diserahkan ke **Rank 0**.
6. Rank 0 menghitung estimasi Pi dengan rumus:
   $$\pi \approx 4 \times \frac{\text{Jumlah Titik di Dalam Lingkaran}}{\text{Total Titik}}$$
   dan mencetak selisih akurasi terhadap konstanta `numpy.pi` serta waktu komputasi.

---

### 3. Job Script Cluster HPC (`job.slurm`)

Berkas ini adalah templat *batch submission* untuk klaster superkomputer yang menggunakan **Slurm Workload Manager**.

#### Konfigurasi Slurm Header:
```bash
#SBATCH --job-name=mpi_pi          # Nama pekerjaan di antrean Slurm
#SBATCH --partition=compute       # Nama partisi node komputasi (sesuaikan dengan klaster)
#SBATCH --nodes=2                 # Menggunakan 2 unit komputer fisik (node)
#SBATCH --ntasks-per-node=8       # Menjalankan 8 proses MPI di setiap node (total 16 rank)
#SBATCH --time=00:05:00           # Batas waktu maksimal (wall-clock limit) 5 menit
#SBATCH --output=hasil_%j.out     # Berkas log keluaran (%j otomatis diganti ID job)
```

#### Alur Kerja Penuh dari Laptop ke Superkomputer:

```mermaid
flowchart LR
    A[Laptop Lokal] -- 1. Buat Kunci SSH & Login --> B(Login Node HPC)
    A -- 2. Salin Berkas scp --> B
    B -- 3. Submit Job sbatch --> C{Slurm Scheduler}
    C -- 4. Eksekusi srun --> D[Compute Node 1 (8 rank)]
    C -- 4. Eksekusi srun --> E[Compute Node 2 (8 rank)]
    D & E -- 5. Tulis Hasil --> F[hasil_JOBID.out]
    F -- 6. Unduh Hasil scp --> A
```

#### Langkah Perintah Terminal:
1. **Otentikasi SSH Kunci Publik:**
   ```bash
   ssh-keygen -t ed25519
   ssh-copy-id user@alamat-cluster-hpc.ac.id
   ```
2. **Transfer Berkas Kode ke Klaster:**
   ```bash
   scp mpi_monte_carlo_pi.py job.slurm user@alamat-cluster-hpc.ac.id:~/proyek_hpc/
   ```
3. **Login ke Klaster:**
   ```bash
   ssh user@alamat-cluster-hpc.ac.id
   cd ~/proyek_hpc/
   ```
4. **Kirim Pekerjaan ke Antrean Slurm:**
   ```bash
   sbatch job.slurm
   ```
5. **Memantau Status Antrean:**
   ```bash
   squeue -u $USER
   ```
6. **Melihat Hasil Eksekusi:**
   ```bash
   cat hasil_*.out
   ```
7. **Mengunduh Hasil Kembali ke Laptop (dari terminal lokal):**
   ```bash
   scp user@alamat-cluster-hpc.ac.id:~/proyek_hpc/hasil_*.out .
   ```

---

## 🧠 Konsep Inti HPC yang Diterapkan

### 1. FLOPS & Presisi Floating Point
- **FLOPS (Floating-Point Operations per Second):** Standar internasional untuk mengukur kemampuan perangkat keras dalam melakukan operasi matematika desimal.
- **Presisi Tunggal (`float32`) vs Ganda (`float64`):** Matriks berukuran besar pada `float32` memerlukan bandwidth memori dan siklus aritmetika lebih sedikit, sehingga umumnya menghasilkan GFLOPS hingga 2× lebih tinggi dibanding `float64`, dengan kompromi berkurangnya digit ketelitian numerik.

### 2. Karakteristik "Embarrassingly Parallel"
- Masalah seperti simulasi Monte Carlo atau pencarian parameter (*parameter sweep*) SIR tidak memerlukan koordinasi yang intens antartugas saat perhitungan berlangsung. Karakteristik ini memberikan efisiensi paralelisasi yang sangat tinggi (*near-linear scalability*).

### 3. Metrik Kinerja Paralel
- **Speedup ($S_p$):** Rasio waktu komputasi serial dibandingkan komputasi paralel:
  $$S_p = \frac{T_1}{T_p}$$
- **Efisiensi Paralel ($E_p$):** Seberapa optimal tiap pekerja/prosesor dimanfaatkan:
  $$E_p = \frac{S_p}{p} \times 100\%$$
  *(Di mana $p$ adalah jumlah pekerja. Efisiensi ideal adalah 100%).*

### 4. MPI vs Multiprocessing
| Aspek | Multiprocessing (`Pool`) | MPI (`mpi4py` & `srun`) |
| :--- | :--- | :--- |
| **Model Memori** | *Shared Memory* (Satu RAM bersama) | *Distributed Memory* (Masing-masing proses punya ruang RAM sendiri) |
| **Batas Skalabilitas** | Terbatas pada jumlah core dalam 1 mesin fisik | Dapat diperluas ke ratusan/ribuan node komputasi yang terhubung jaringan *high-speed interconnect* (InfiniBand) |
| **Komunikasi Data** | Salin memori lokal / antrean OS | Pengiriman pesan eksplisit (`send`, `recv`, `reduce`, `broadcast`) |

---

## ❓ Panduan Troubleshooting

| Gejala Masalah | Penyebab Umum | Solusi |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'mpi4py'` | Paket `mpi4py` belum terpasang di environment Python aktif. | Jalankan `pip install mpi4py`. Pastikan compiler C dan library OpenMPI sudah ada di sistem. |
| `mpirun: command not found` | Pustaka runtime MPI belum terinstal pada sistem operasi. | Di Ubuntu/WSL: `sudo apt install openmpi-bin`. Di Windows: instal MS-MPI runtime. |
| `sbatch: command not found` | Anda menjalankan perintah Slurm di komputer lokal / laptop, bukan di *login node* klaster HPC. | `sbatch` hanya dapat dijalankan di lingkungan klaster/superkomputer yang memiliki Slurm scheduler. |
| `Invalid partition specified` pada Slurm | Nama partisi `#SBATCH --partition=compute` tidak cocok dengan arsitektur klaster Anda. | Periksa nama partisi yang tersedia di klaster Anda menggunakan perintah `sinfo`, lalu sesuaikan baris tersebut di `job.slurm`. |
| Nilai estimasi Pi tidak berubah atau kembar | Seluruh rank menggunakan nilai acak yang identik karena seed sama. | Pastikan seed diatur berbeda per rank, misalnya: `seed = 1234 + rank` (sudah diimplementasikan pada kode). |

---

## 👨‍💻 Kontribusi & Lisensi
Proyek ini dibuat untuk tujuan edukasi, demonstrasi komputasi performa tinggi, dan referensi implementasi HPC tingkat dasar hingga menengah. Bebas dikembangkan dan dimodifikasi untuk riset maupun pembelajaran.
