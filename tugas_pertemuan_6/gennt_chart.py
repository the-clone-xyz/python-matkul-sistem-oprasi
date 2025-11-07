# ------------------------------------------------------
# SIMULATOR MANAJEMEN RESOURCE & DEADLOCK (BANKER'S ALGORITHM)
# VERSI TERMINAL + GANTT CHART
# ------------------------------------------------------
# Dibuat oleh: Yogi Irwan Syahputra
# Praktikum Sistem Operasi
# ------------------------------------------------------

import matplotlib.pyplot as plt

# ---------------------------------
# Fungsi untuk Banker's Algorithm
# ---------------------------------
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

# ---------------------------------
# Fungsi menampilkan Gantt Chart
# ---------------------------------
def show_gantt_chart(safe_sequence):
    print("\nMembuat Gantt Chart...")
    fig, ax = plt.subplots(figsize=(8, 3))
    start_time = 0
    height = 0.4

    for i, p in enumerate(safe_sequence):
        ax.barh(0, width=1, left=start_time, height=height, label=f"P{p}")
        ax.text(start_time + 0.5, 0, f"P{p}", ha='center', va='center', color='white', fontsize=12)
        start_time += 1  # misal tiap proses butuh 1 unit waktu

    ax.set_xlim(0, start_time)
    ax.set_xlabel("Waktu Eksekusi (unit)")
    ax.set_yticks([])
    ax.set_title("Gantt Chart - Safe Sequence Eksekusi Proses")
    ax.legend(loc="upper center", ncol=len(safe_sequence))
    plt.tight_layout()
    plt.show()

# ---------------------------------
# MAIN PROGRAM
# ---------------------------------
def main():
    print("=== SIMULATOR MANAJEMEN RESOURCE & DEADLOCK ===")
    print("Versi Terminal + Visualisasi Gantt Chart\n")

    n = int(input("Masukkan jumlah proses: "))
    m = int(input("Masukkan jumlah resource: "))

    print("\nMasukkan matriks ALLOCATION (alokasi saat ini):")
    alloc = []
    for i in range(n):
        row = list(map(int, input(f"Proses P{i}: ").split()))
        alloc.append(row)

    print("\nMasukkan matriks MAX (kebutuhan maksimum):")
    max_need = []
    for i in range(n):
        row = list(map(int, input(f"Proses P{i}: ").split()))
        max_need.append(row)

    print("\nMasukkan vector AVAILABLE (resource tersedia):")
    avail = list(map(int, input("Available: ").split()))

    safe, seq = is_safe(alloc, max_need, avail)

    print("\n=== HASIL SIMULASI ===")
    if safe:
        print("✅ SISTEM TIDAK DEADLOCK.")
        print("Urutan aman (Safe Sequence):", " -> ".join(f"P{i}" for i in seq))
        show_gantt_chart(seq)
    else:
        print("❌ SISTEM DEADLOCK! Tidak ada urutan aman.")

# ---------------------------------
# Jalankan program
# ---------------------------------
if __name__ == "__main__":
    main()
