import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisasi Penjadwalan CPU (FCFS) - Hitung Waktu Tunggu")
        self.root.geometry("900x800") # Memberi ruang lebih untuk tabel hasil

        self.processes = []
        self.gantt_canvas = None

        # Konfigurasi layout utama
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Frame Input ---
        input_frame = ttk.LabelFrame(main_frame, text="Input Proses", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="ID Proses:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.pid_entry = ttk.Entry(input_frame, width=10)
        self.pid_entry.grid(row=0, column=1, padx=5, pady=5)
        self.pid_entry.insert(0, "P0") # Default PID

        ttk.Label(input_frame, text="Waktu Tiba (AT):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.arrival_entry = ttk.Entry(input_frame, width=10)
        self.arrival_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Waktu Eksekusi (BT):").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.burst_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=0, column=5, padx=5, pady=5)

        self.add_button = ttk.Button(input_frame, text="Tambah Proses", command=self.add_process)
        self.add_button.grid(row=0, column=6, padx=10, pady=5)

        # --- Frame Tabel Proses ---
        table_frame = ttk.LabelFrame(main_frame, text="Daftar Proses", padding="10")
        table_frame.pack(fill=tk.X, pady=5)

        columns = ("pid", "arrival", "burst")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("pid", text="ID Proses")
        self.tree.heading("arrival", text="Waktu Tiba (AT)")
        self.tree.heading("burst", text="Waktu Eksekusi (BT)")
        self.tree.column("pid", width=100, anchor=tk.CENTER)
        self.tree.column("arrival", width=100, anchor=tk.CENTER)
        self.tree.column("burst", width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.X)

        # --- Tombol Aksi ---
        action_frame = ttk.Frame(main_frame, padding="5")
        action_frame.pack(fill=tk.X)

        self.run_button = ttk.Button(action_frame, text="Jalankan Penjadwalan (FCFS)", command=self.run_fcfs)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(action_frame, text="Reset", command=self.reset_all)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # --- Frame Hasil (Gantt Chart dan Tabel Hasil) ---
        self.result_frame = ttk.LabelFrame(main_frame, text="Hasil Visualisasi dan Kalkulasi", padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 1. Frame untuk Gantt Chart
        self.gantt_frame = ttk.Frame(self.result_frame)
        self.gantt_frame.pack(fill=tk.X, pady=5)
        # (Canvas akan ditambahkan di sini oleh draw_gantt_chart)

        # 2. Frame untuk Tabel Hasil Kalkulasi
        results_table_frame = ttk.LabelFrame(self.result_frame, text="Tabel Hasil Kalkulasi", padding="10")
        results_table_frame.pack(fill=tk.X, pady=10)
        
        results_columns = ("pid", "at", "bt", "ct", "tat", "wt")
        self.results_tree = ttk.Treeview(results_table_frame, columns=results_columns, show="headings")
        
        self.results_tree.heading("pid", text="ID Proses")
        self.results_tree.heading("at", text="AT")
        self.results_tree.heading("bt", text="BT")
        self.results_tree.heading("ct", text="Waktu Selesai (CT)")
        self.results_tree.heading("tat", text="Turnaround Time (TAT)")
        self.results_tree.heading("wt", text="Waktu Tunggu (WT)")

        # Mengatur lebar kolom
        for col in results_columns:
             self.results_tree.column(col, width=120, anchor=tk.CENTER)

        self.results_tree.pack(fill=tk.X)

        # 3. Frame untuk Rata-rata
        avg_frame = ttk.Frame(self.result_frame, padding="5")
        avg_frame.pack(fill=tk.X)

        self.avg_wt_label = ttk.Label(avg_frame, text="Rata-rata Waktu Tunggu (AVG WT): -", font=("Arial", 12, "bold"))
        self.avg_wt_label.pack(anchor="w")

        self.avg_tat_label = ttk.Label(avg_frame, text="Rata-rata Turnaround Time (AVG TAT): -", font=("Arial", 12))
        self.avg_tat_label.pack(anchor="w")


    def add_process(self):
        """Menambahkan proses dari input user ke tabel Treeview."""
        try:
            pid = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())

            if pid.strip() == "":
                messagebox.showerror("Error", "ID Proses tidak boleh kosong")
                return
            if burst <= 0:
                messagebox.showerror("Error", "Waktu Eksekusi harus lebih dari 0")
                return
            if arrival < 0:
                messagebox.showerror("Error", "Waktu Tiba tidak boleh negatif")
                return

            self.tree.insert("", tk.END, values=(pid, arrival, burst))

            # Siapkan PID untuk proses selanjutnya
            try:
                # Coba auto-increment P0, P1, ...
                num = int(pid[1:]) + 1
                self.pid_entry.delete(0, tk.END)
                self.pid_entry.insert(0, f"P{num}")
            except:
                # Jika format PID aneh, kosongkan saja
                self.pid_entry.delete(0, tk.END)

            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.pid_entry.focus() # Fokus kembali ke PID

        except ValueError:
            messagebox.showerror("Error", "Input Waktu Tiba dan Eksekusi harus berupa angka!")

    def run_fcfs(self):
        """Menjalankan algoritma FCFS dan menampilkan hasil."""
        
        # Bersihkan hasil sebelumnya
        self.clear_results()
        
        self.get_processes_from_tree()
        
        if not self.processes:
            messagebox.showwarning("Warning", "Tidak ada proses untuk dijadwalkan!")
            return

        # 1. Sortir proses berdasarkan Waktu Tiba (Kunci FCFS)
        sorted_processes = sorted(self.processes, key=lambda x: x[1])

        gantt_data = []  # (PID, start_time, duration)
        results_data = [] # (PID, AT, BT, CT, TAT, WT)

        current_time = 0
        total_wait_time = 0
        total_turnaround_time = 0

        for proc in sorted_processes:
            pid, arrival, burst = proc

            # Jika CPU idle, geser current_time ke waktu tiba proses
            if current_time < arrival:
                current_time = arrival
            
            start_time = current_time
            
            # Kalkulasi inti
            completion_time = start_time + burst
            turnaround_time = completion_time - arrival
            wait_time = turnaround_time - burst # Atau wait_time = start_time - arrival

            # Kumpulkan data untuk Gantt Chart
            gantt_data.append((pid, start_time, burst))
            
            # Kumpulkan data untuk tabel hasil
            results_data.append((pid, arrival, burst, completion_time, turnaround_time, wait_time))

            # Update waktu saat ini
            current_time = completion_time

            # Akumulasi total
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time
        
        # 2. Tampilkan Gantt Chart
        self.draw_gantt_chart(gantt_data)
        
        # 3. Tampilkan Tabel Hasil
        for data in results_data:
            self.results_tree.insert("", tk.END, values=data)
            
        # 4. Tampilkan Rata-rata (AVG)
        avg_wait_time = total_wait_time / len(self.processes)
        avg_turnaround_time = total_turnaround_time / len(self.processes)

        self.avg_wt_label.config(text=f"Rata-rata Waktu Tunggu (AVG WT): {avg_wait_time:.2f}")
        self.avg_tat_label.config(text=f"Rata-rata Turnaround Time (AVG TAT): {avg_turnaround_time:.2f}")


    def draw_gantt_chart(self, gantt_data):
        """Menggambar Gantt Chart menggunakan Matplotlib di frame Tkinter."""
        
        # Hapus chart sebelumnya (jika ada)
        if self.gantt_canvas:
            self.gantt_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(8, 2.5)) # Dibuat lebih pendek

        pids = [data[0] for data in gantt_data]
        start_times = [data[1] for data in gantt_data]
        durations = [data[2] for data in gantt_data]
        
        colors = plt.cm.get_cmap('Set3', len(pids))

        for i, pid in enumerate(pids):
            ax.barh(pid, durations[i], left=start_times[i], color=colors(i), edgecolor='black', height=0.6)
            # Teks durasi
            ax.text(start_times[i] + durations[i]/2, i, str(durations[i]), 
                    va='center', ha='center', color='black', fontweight='bold')

        ax.set_xlabel("Waktu")
        ax.set_ylabel("Proses")
        ax.set_title("Gantt Chart (FCFS)")
        
        max_time = max(s + d for s, d in zip(start_times, durations))
        
        # Membuat tick/penanda di sumbu X agar lebih jelas
        ax.set_xticks(range(0, int(max_time) + 2, 1))
        
        # Menambahkan garis grid
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_ylim(-0.5, len(pids) - 0.5) # Rapikan batas Y
        
        plt.tight_layout()

        self.gantt_canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        self.gantt_canvas.draw()
        self.gantt_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_processes_from_tree(self):
        """Mengambil data dari Treeview dan menyimpannya di self.processes."""
        self.processes = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            self.processes.append((values[0], int(values[1]), int(values[2])))

    def clear_results(self):
        """Membersihkan Gantt Chart, Tabel Hasil, dan Label AVG."""
        if self.gantt_canvas:
            self.gantt_canvas.get_tk_widget().destroy()
            self.gantt_canvas = None
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        self.avg_wt_label.config(text="Rata-rata Waktu Tunggu (AVG WT): -")
        self.avg_tat_label.config(text="Rata-rata Turnaround Time (AVG TAT): -")

    def reset_all(self):
        """Membersihkan semua input dan hasil."""
        # Hapus tabel input
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.processes = []
        
        # Hapus hasil
        self.clear_results()
            
        # Reset entri
        self.pid_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.pid_entry.insert(0, "P0")

# --- Main Program ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()