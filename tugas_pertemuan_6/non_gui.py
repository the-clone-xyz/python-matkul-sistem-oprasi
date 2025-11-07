# --------------------------------------------
# SIMULATOR MANAJEMEN RESOURCE & DEADLOCK (BANKER'S ALGORITHM)
# --------------------------------------------
# Dibuat oleh: Yogi Irwan Syahputra
# Untuk praktikum Sistem Operasi - versi terminal (CLI)
# --------------------------------------------

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


# --------------------------------------------
# MAIN PROGRAM
# --------------------------------------------
def main():
    print("=== SIMULATOR MANAJEMEN RESOURCE & DEADLOCK ===")
    print("Versi Terminal - Algoritma Banker's Algorithm\n")

    # Input jumlah proses dan resource
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

    # Periksa kondisi sistem
    safe, seq = is_safe(alloc, max_need, avail)

    print("\n=== HASIL SIMULASI ===")
    if safe:
        print("✅ SISTEM TIDAK DEADLOCK.")
        print("Urutan aman (Safe Sequence):", " -> ".join(f"P{i}" for i in seq))
    else:
        print("❌ SISTEM DALAM KEADAAN DEADLOCK!")


if __name__ == "__main__":
    main()
