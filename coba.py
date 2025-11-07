# ============================================================
# Project_Akhir_Dari_Pert_5_Contoh.py
# IMPLEMENTASI SIMULATOR PENJADWALAN CPU - perbaikan sintaks
# Untuk Python 3.11 di Windows 10
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class CPUSchedulerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Penjadwalan CPU - Perbaikan")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.process_entries = []
        self.processes = []

        # Judul Utama
        tk.Label(root, text="=== SIMULATOR PENJADWALAN CPU ===",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Frame input
        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)
        tk.Label(top_frame, text="Jumlah Proses: ").pack(side=tk.LEFT)
        self.num_entry = tk.Entry(top_frame, width=5)
        self.num_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Buat Input", command=self.create_input_fields).pack(side=tk.LEFT, padx=10)

        # Pilihan algoritma
        algo_frame = tk.Frame(root)
        algo_frame.pack(pady=5)
        tk.Label(algo_frame, text="Pilih Algoritma: ").pack(side=tk.LEFT)
        self.algo_var = tk.StringVar(value="FCFS")
        algo_choices = ["FCFS", "SJF", "Priority", "Round Robin"]
        ttk.Combobox(algo_frame, textvariable=self.algo_var, values=algo_choices, width=15, state="readonly").pack(side=tk.LEFT, padx=5)

        # Quantum untuk RR
        tk.Label(algo_frame, text="Quantum (untuk RR): ").pack(side=tk.LEFT)
        self.quantum_entry = tk.Entry(algo_frame, width=5)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side=tk.LEFT, padx=5)

        # Frame input proses
        self.process_frame = tk.Frame(root)
        self.process_frame.pack(pady=10)

        # Tombol Jalankan
        tk.Button(root, text="Jalankan Simulasi", bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"), command=self.run_scheduler).pack(pady=5)

        # Tabel hasil
        self.tree = ttk.Treeview(root, columns=("AT", "BT", "PR", "CT", "TAT", "WT"), show="headings", height=10)
        for col in ("AT", "BT", "PR", "CT", "TAT", "WT"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(pady=10)

        # Label evaluasi
        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)

        # Tombol Gantt Chart
        tk.Button(root, text="Tampilkan Gantt Chart", bg="#2196F3", fg="white",
                  font=("Arial", 11, "bold"), command=self.show_gantt).pack(pady=10)

    def create_input_fields(self):
        """Membuat kolom input proses sesuai jumlah yang diinginkan"""
        for w in self.process_frame.winfo_children():
            w.destroy()
        self.process_entries.clear()

        try:
            n = int(self.num_entry.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Masukkan jumlah proses yang valid (>=1)")
            return

        tk.Label(self.process_frame, text="Proses | Arrival Time | Burst Time | Prioritas").pack()
        for i in range(n):
            frame = tk.Frame(self.process_frame)
            frame.pack(pady=2)
            pname = f"P{i+1}"
            tk.Label(frame, text=pname, width=8).pack(side=tk.LEFT)
            at = tk.Entry(frame, width=10)
            at.pack(side=tk.LEFT, padx=5)
            bt = tk.Entry(frame, width=10)
            bt.pack(side=tk.LEFT, padx=5)
            pr = tk.Entry(frame, width=10)
            pr.pack(side=tk.LEFT, padx=5)
            self.process_entries.append((pname, at, bt, pr))

    def run_scheduler(self):
        """Menjalankan algoritma penjadwalan"""
        self.tree.delete(*self.tree.get_children())
        self.processes.clear()
        algo = self.algo_var.get()

        # Input data
        try:
            for pname, at_entry, bt_entry, pr_entry in self.process_entries:
                at_val = int(at_entry.get())
                bt_val = int(bt_entry.get())
                pr_val = int(pr_entry.get()) if pr_entry.get().strip() != "" else 0
                self.processes.append({
                    "Proses": pname,
                    "AT": at_val,
                    "BT": bt_val,
                    "PR": pr_val
                })
        except ValueError:
            messagebox.showerror("Error", "Pastikan semua nilai AT, BT, dan Prioritas valid (angka)!")
            return

        if len(self.processes) == 0:
            messagebox.showwarning("Peringatan", "Tidak ada proses untuk dijalankan.")
            return

        if algo == "FCFS":
            self.fcfs()
        elif algo == "SJF":
            self.sjf()
        elif algo == "Priority":
            self.priority()
        elif algo == "Round Robin":
            try:
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Quantum harus berupa bilangan bulat positif!")
                return
            self.round_robin(quantum)

    def fcfs(self):
        """Algoritma First Come First Serve"""
        self.processes.sort(key=lambda x: x['AT'])
        t = 0
        for p in self.processes:
            if t < p['AT']:
                t = p['AT']
            t += p['BT']
            p['CT'] = t
            p['TAT'] = p['CT'] - p['AT']
            p['WT'] = p['TAT'] - p['BT']
        self.display_result()

    def sjf(self):
        """Algoritma Shortest Job First (non-preemptive)"""
        processes = sorted(self.processes, key=lambda x: x['AT'])
        completed = []
        t = 0
        while len(completed) < len(processes):
            ready = [p for p in processes if p['AT'] <= t and p not in completed]
            if not ready:
                # jika belum ada proses siap, loncatkan waktu ke AT proses terawal yang belum selesai
                t = min([p['AT'] for p in processes if p not in completed])
                ready = [p for p in processes if p['AT'] <= t and p not in completed]
            shortest = min(ready, key=lambda x: x['BT'])
            t += shortest['BT']
            shortest['CT'] = t
            shortest['TAT'] = shortest['CT'] - shortest['AT']
            shortest['WT'] = shortest['TAT'] - shortest['BT']
            completed.append(shortest)
        # urutkan hasil berdasarkan waktu selesai agar Gantt rapi
        self.processes = sorted(completed, key=lambda x: x['CT'])
        self.display_result()

    def priority(self):
        """Algoritma Priority Scheduling (non-preemptive, prioritas kecil = prioritas tinggi)"""
        processes = sorted(self.processes, key=lambda x: x['AT'])
        completed = []
        t = 0
        while len(completed) < len(processes):
            ready = [p for p in processes if p['AT'] <= t and p not in completed]
            if not ready:
                t = min([p['AT'] for p in processes if p not in completed])
                ready = [p for p in processes if p['AT'] <= t and p not in completed]
            high = min(ready, key=lambda x: x['PR'])
            t += high['BT']
            high['CT'] = t
            high['TAT'] = high['CT'] - high['AT']
            high['WT'] = high['TAT'] - high['BT']
            completed.append(high)
        self.processes = sorted(completed, key=lambda x: x['CT'])
        self.display_result()

    def round_robin(self, quantum):
        """Algoritma Round Robin (preemptive)"""
        # copy dan urutkan proses awal berdasarkan AT
        arrival_sorted = sorted(self.processes, key=lambda x: x['AT'])
        t = 0
        ready_queue = []
        remaining = {p['Proses']: p['BT'] for p in arrival_sorted}
        finished = {}
        i = 0  # indeks untuk menambahkan proses ke ready_queue dari arrival_sorted

        # mulai dari waktu AT proses pertama (jika >0, loncat ke sana)
        if arrival_sorted:
            t = arrival_sorted[0]['AT']

        while True:
            # masukkan proses yang telah tiba ke ready_queue
            while i < len(arrival_sorted) and arrival_sorted[i]['AT'] <= t:
                ready_queue.append(arrival_sorted[i])
                i += 1

            if not ready_queue:
                # jika tidak ada proses siap dan masih ada yang belum tiba, loncat ke waktu tiba berikutnya
                if i < len(arrival_sorted):
                    t = arrival_sorted[i]['AT']
                    continue
                else:
                    break  # semua selesai

            # pop proses dari queue (FIFO)
            proc = ready_queue.pop(0)
            name = proc['Proses']
            execute = min(quantum, remaining[name])
            remaining[name] -= execute
            t += execute

            # tambahkan proses baru yang tiba selama eksekusi
            while i < len(arrival_sorted) and arrival_sorted[i]['AT'] <= t:
                ready_queue.append(arrival_sorted[i])
                i += 1

            if remaining[name] == 0:
                # proses selesai
                proc['CT'] = t
                proc['TAT'] = proc['CT'] - proc['AT']
                proc['WT'] = proc['TAT'] - proc['BT']
                finished[name] = proc
            else:
                # masih sisa, letakkan di akhir queue
                ready_queue.append(proc)

            # jika semua proses selesai, break
            if len(finished) == len(arrival_sorted):
                break

        # ambil hasil urut berdasarkan CT
        self.processes = sorted(list(finished.values()), key=lambda x: x['CT'])
        self.display_result()

    def display_result(self):
        """Menampilkan hasil ke tabel"""
        self.tree.delete(*self.tree.get_children())
        total_wt = 0
        total_tat = 0
        for p in self.processes:
            # Jika CT/TAT/WT belum terisi (kemungkinan pada input buruk), atur ke nilai default
            ct = p.get('CT', 0)
            tat = p.get('TAT', 0)
            wt = p.get('WT', 0)
            self.tree.insert("", tk.END, values=(p['AT'], p['BT'], p['PR'], ct, tat, wt))
            total_wt += wt
            total_tat += tat
        n = len(self.processes) if self.processes else 1
        avg_wt = total_wt / n
        avg_tat = total_tat / n
        self.result_label.config(text=f"Rata-rata WT: {avg_wt:.2f} | Rata-rata TAT: {avg_tat:.2f}")

    def show_gantt(self):
        """Menampilkan Gantt Chart"""
        if not self.processes:
            messagebox.showwarning("Peringatan", "Jalankan simulasi terlebih dahulu!")
            return
        fig, ax = plt.subplots(figsize=(9, 3))
        y = 10
        # gunakan segmen (start, durasi) -> hitung start dari CT - BT
        for p in self.processes:
            start = p.get('CT', 0) - p.get('BT', 0)
            dur = p.get('BT', 0)
            ax.broken_barh([(start, dur)], (y, 8), facecolors="tab:blue")
            ax.text(start + dur/2, y+4, p['Proses'], color="white", ha="center", va="center", fontsize=9)
            y += 12
        ax.set_ylim(5, y)
        ax.set_xlim(0, max(p.get('CT', 0) for p in self.processes) + 2)
        ax.set_xlabel("Waktu Eksekusi (unit waktu)")
        ax.set_yticks([])
        ax.set_title(f"Gantt Chart - Algoritma {self.algo_var.get()}")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerSimulator(root)
    root.mainloop()
