# ================================================================
# SIMULATOR MANAJEMEN RESOURCE & DEADLOCK
# Algoritma: Banker's Algorithm
# Fitur: Input manual + Gantt Chart Visualisasi Safe Sequence
# ---------------------------------------------------------------
# Dibuat oleh: Yogi Irwan Syahputra
# Praktikum Sistem Operasi - Python 3.11 (Windows 10)
# ================================================================

import matplotlib.pyplot as plt

# -----------------------------
# Fungsi Banker's Algorithm
# -----------------------------
def is_safe(alloc, max_need, avail):
    n = len(alloc)
    m = len(avail)
    finish = [False] * n
    safe_seq = []
    work = avail.copy()

    while len(safe_seq) < n:
        allocated = False
        for i in range(n):
            if not finish[i]:
                need = [max_need[i][j] - alloc[i][j] for j in range(m)]
                if all(need[j] <= work[j] for j in range(m)):
                    for j in range(m):
                        work[j] += alloc[i][j]
                    finish[i] = True
                    safe_seq.append(i)
                    allocated = True
        if not allocated:
            return False, []
    return True, safe_seq


# -----------------------------
# Fungsi Gantt Chart
# -----------------------------
def show_gantt_chart(safe_sequence, execution_time=None):
    print("\n📊 Membuat Gantt Chart Visualisasi Safe Sequence...")

    if execution_time is None:
        # Default tiap proses butuh 1 unit waktu
        execution_time = [1 for _ in safe_sequence]

    fig, ax = plt.subplots(figsize=(9, 3))
    start_time = 0
    height = 0.4

    for i, p in enumerate(safe_sequence):
        durasi = execution_time[i]
        ax.barh(0, width=durasi, left=start_time, height=height, label=f"P{p}")
        ax.text(start_time + durasi / 2, 0, f"P{p}", ha='center', va='center', color='white', fontsize=12)
        start_time += durasi

    ax.set_xlim(0, start_time)
    ax.set_xlabel("Waktu Eksekusi (unit waktu)")
    ax.set_yticks([])
    ax.set_title("Gantt Chart - Urutan Aman (Safe Sequence)")
    ax.legend(loc="upper center", ncol=len(safe_sequence))
    plt.tight_layout()
    plt.show()


# -----------------------------
# Fungsi Input Manual
# -----------------------------
def input_matrix(prompt, n, m):
    print(f"\n{prompt}")
    matrix = []
    for i in range(n):
        row = list(map(int, input(f"Proses P{i}: ").split()))
        while len(row) != m:
            print(f"⚠️  Harus ada {m} nilai per baris.")
            row = list(map(int, input(f"Proses P{i}: ").split()))
        matrix.append(row)
    return matrix


# -----------------------------
# MAIN PROGRAM
# -----------------------------
def main():
    print("="*65)
    print("💻  SIMULATOR MANAJEMEN RESOURCE & DEADLOCK")
    print("🔹 Menggunakan Algoritma Banker's Algorithm")
    print("🔹 Versi Terminal + Visualisasi Gantt Chart")
    print("="*65)

    # Input jumlah proses & resource
    n = int(input("Masukkan jumlah proses: "))
    m = int(input("Masukkan jumlah resource: "))

    # Input matrix
    alloc = input_matrix("Masukkan matriks ALLOCATION (alokasi saat ini):", n, m)
    max_need = input_matrix("Masukkan matriks MAX (kebutuhan maksimum):", n, m)

    print("\nMasukkan vector AVAILABLE (resource tersedia):")
    avail = list(map(int, input("Available: ").split()))
    while len(avail) != m:
        print(f"⚠️  Harus ada {m} nilai.")
        avail = list(map(int, input("Available: ").split()))

    # Jalankan algoritma Banker
    safe, seq = is_safe(alloc, max_need, avail)

    print("\n=== HASIL SIMULASI ===")
    if safe:
        print("✅ SISTEM TIDAK DEADLOCK.")
        print("Urutan aman (Safe Sequence):", " -> ".join(f"P{i}" for i in seq))

        # (Opsional) Input durasi eksekusi per proses
        ans = input("\nIngin masukkan waktu eksekusi tiap proses? (y/n): ").lower()
        if ans == 'y':
            waktu = []
            for i in seq:
                t = int(input(f"Durasi eksekusi P{i} (dalam unit waktu): "))
                waktu.append(t)
        else:
            waktu = [1 for _ in seq]

        # Tampilkan Gantt Chart
        show_gantt_chart(seq, waktu)
    else:
        print("❌ SISTEM DEADLOCK! Tidak ada urutan aman.")


# -----------------------------
# Jalankan program
# -----------------------------
if __name__ == "__main__":
    main()
