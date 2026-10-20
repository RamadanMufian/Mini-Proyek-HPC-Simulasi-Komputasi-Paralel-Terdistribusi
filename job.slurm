#!/bin/bash
# =====================================================================
# Template job Slurm untuk menjalankan skrip MPI di cluster HPC
# Alur kerja (sesuai materi):
#   1. Login ke superkomputer lewat SSH (kunci publik/privat)
#   2. Salin kode  -> scp / git clone
#   3. Kirim job   -> sbatch job.slurm
#   4. Pantau job  -> squeue -u $USER
#   5. Unduh hasil -> scp, lalu visualisasi di laptop
#
# Catatan: nama partition, module, dan batas sumber daya berbeda tiap
# cluster. Sesuaikan dengan dokumentasi cluster yang dipakai.
# =====================================================================

#SBATCH --job-name=mpi_pi
#SBATCH --partition=compute        # SESUAIKAN dengan cluster Anda
#SBATCH --nodes=2                  # jumlah node
#SBATCH --ntasks-per-node=8        # proses per node (total 16 rank)
#SBATCH --time=00:05:00            # batas waktu
#SBATCH --output=hasil_%j.out      # %j = nomor job

module load python openmpi         # SESUAIKAN: cek dengan `module avail`

echo "Job $SLURM_JOB_ID jalan di node: $SLURM_JOB_NODELIST"
srun python mpi_monte_carlo_pi.py

# ---------------------------------------------------------------------
# Perintah dari laptop (jalankan di terminal lokal, bukan di dalam file ini):
#
#   ssh-keygen -t ed25519                     # buat kunci publik/privat
#   ssh-copy-id user@alamat-cluster           # daftarkan kunci publik
#   ssh user@alamat-cluster                   # login
#   scp mpi_monte_carlo_pi.py job.slurm user@alamat-cluster:~/proyek/
#   sbatch job.slurm
#   scp user@alamat-cluster:~/proyek/hasil_*.out .
# ---------------------------------------------------------------------
