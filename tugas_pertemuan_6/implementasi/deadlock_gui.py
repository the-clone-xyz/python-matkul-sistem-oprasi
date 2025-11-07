import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb


class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Manajemen Resource & Deadlock")
        self.root.geometry("700x500")

        # Frame Input
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Jumlah Proses:").grid(row=0, column=0, sticky="w")
        self.entry_proses = ttk.Entry(frame, width=10)
        self.entry_proses.grid(row=0, column=1)

        ttk.Label(frame, text="Jumlah Resource:").grid(row=1, column=0, sticky="w")
        self.entry_resource = ttk.Entry(frame, width=10)
        self.entry_resource.grid(row=1, column=1)

        ttk.Button(frame, text="Buat Tabel", command=self.make_table).grid(row=2, column=0, pady=5)
        ttk.Button(frame, text="Cek Deadlock", command=self.check_deadlock).grid(row=2, column=1, pady=5)

        # Frame Table
        self.table_frame = ttk.Frame(root, padding=10)
        self.table_frame.pack(fill="both", expand=True)

        # Result Output
        self.output = tk.Text(root, height=8)
        self.output.pack(fill="x", padx=10, pady=10)

    def make_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        try:
            self.n = int(self.entry_proses.get())
            self.m = int(self.entry_resource.get())
        except:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
            return

        self.entries_alloc = []
        self.entries_req = []

        ttk.Label(self.table_frame, text="Allocation").grid(row=0, column=0)
        ttk.Label(self.table_frame, text="Request").grid(row=0, column=1)

        for i in range(self.n):
            row_alloc = []
            row_req = []

            frame_alloc = ttk.Frame(self.table_frame)
            frame_alloc.grid(row=i+1, column=0, padx=5)

            frame_req = ttk.Frame(self.table_frame)
            frame_req.grid(row=i+1, column=1, padx=5)

            for j in range(self.m):
                e1 = ttk.Entry(frame_alloc, width=4)
                e1.grid(row=0, column=j)
                row_alloc.append(e1)

                e2 = ttk.Entry(frame_req, width=4)
                e2.grid(row=0, column=j)
                row_req.append(e2)

            self.entries_alloc.append(row_alloc)
            self.entries_req.append(row_req)

    def check_deadlock(self):
        alloc = []
        req = []

        # baca data input
        for i in range(self.n):
            alloc_row = []
            req_row = []
            for j in range(self.m):
                a = int(self.entries_alloc[i][j].get() or 0)
                r = int(self.entries_req[i][j].get() or 0)
                alloc_row.append(a)
                req_row.append(r)
            alloc.append(alloc_row)
            req.append(req_row)

        # Deadlock detection sederhana
        unfinished = set(range(self.n))
        change = True

        while change:
            change = False
            for p in list(unfinished):
                # jika proses tidak meminta resource apapun → aman
                if all(x == 0 for x in req[p]):
                    unfinished.remove(p)
                    change = True

        self.output.delete("1.0", tk.END)

        if len(unfinished) == 0:
            self.output.insert(tk.END, "✅ Sistem Aman, Tidak Ada Deadlock.\n")
        else:
            self.output.insert(tk.END, "⚠️ DEADLOCK Terdeteksi!\n")
            self.output.insert(tk.END, f"Proses yang mengalami deadlock: {list(unfinished)}\n")


# Main Program
app = tb.Window(themename="superhero")
DeadlockSimulator(app)
app.mainloop()
