import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import ttkbootstrap as tb

# ----------------------------
# BANKER'S ALGORITHM FUNCTION
# ----------------------------
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

# ----------------------------
# GUI PROGRAM
# ----------------------------
class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Manajemen Resource & Deadlock")
        self.root.geometry("850x600")
        self.style = tb.Style("flatly")

        frame = ttk.LabelFrame(root, text="Input Data Resource dan Proses", padding=15)
        frame.pack(fill="x", padx=10, pady=10)

        # Input jumlah proses dan resource
        ttk.Label(frame, text="Jumlah Proses:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_p = ttk.Entry(frame, width=10)
        self.entry_p.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Jumlah Resource:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_r = ttk.Entry(frame, width=10)
        self.entry_r.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame, text="Buat Tabel", command=self.create_tables).grid(row=0, column=4, padx=10, pady=5)

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.btn_check = ttk.Button(root, text="Cek Deadlock", command=self.check_deadlock, bootstyle="success")
        self.btn_check.pack(pady=10)

    def create_tables(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        try:
            self.p = int(self.entry_p.get())
            self.r = int(self.entry_r.get())
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
            return

        self.entries_alloc = []
        self.entries_max = []
        self.entries_avail = []

        ttk.Label(self.table_frame, text="Allocation Matrix").grid(row=0, column=0)
        ttk.Label(self.table_frame, text="Max Matrix").grid(row=0, column=1)

        alloc_frame = ttk.Frame(self.table_frame)
        alloc_frame.grid(row=1, column=0)
        max_frame = ttk.Frame(self.table_frame)
        max_frame.grid(row=1, column=1)

        for i in range(self.p):
            row_alloc = []
            row_max = []
            for j in range(self.r):
                e1 = ttk.Entry(alloc_frame, width=5)
                e2 = ttk.Entry(max_frame, width=5)
                e1.grid(row=i, column=j, padx=2, pady=2)
                e2.grid(row=i, column=j, padx=2, pady=2)
                row_alloc.append(e1)
                row_max.append(e2)
            self.entries_alloc.append(row_alloc)
            self.entries_max.append(row_max)

        ttk.Label(self.table_frame, text="Available:").grid(row=2, column=0, sticky="e", pady=10)
        avail_frame = ttk.Frame(self.table_frame)
        avail_frame.grid(row=2, column=1)
        for j in range(self.r):
            e = ttk.Entry(avail_frame, width=5)
            e.grid(row=0, column=j, padx=2)
            self.entries_avail.append(e)

    def check_deadlock(self):
        try:
            alloc = [[int(e.get()) for e in row] for row in self.entries_alloc]
            max_need = [[int(e.get()) for e in row] for row in self.entries_max]
            avail = [int(e.get()) for e in self.entries_avail]
        except ValueError:
            messagebox.showerror("Error", "Semua nilai harus angka!")
            return

        safe, seq = is_safe(alloc, max_need, avail)

        if safe:
            messagebox.showinfo("Status Sistem", f"TIDAK DEADLOCK.\nUrutan aman: {seq}")
        else:
            messagebox.showwarning("Status Sistem", "SISTEM DEADLOCK!")

# ----------------------------
# MAIN PROGRAM
# ----------------------------
if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = DeadlockSimulator(root)
    root.mainloop()
