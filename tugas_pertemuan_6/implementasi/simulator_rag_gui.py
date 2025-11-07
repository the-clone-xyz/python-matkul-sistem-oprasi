import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import networkx as nx
import matplotlib.pyplot as plt


class RAGDiamondGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG – Diamond Layout (GeeksforGeeks Style)")
        self.root.geometry("850x650")

        frame_top = ttk.Frame(root, padding=10)
        frame_top.pack(fill="x")

        ttk.Label(frame_top, text="Jumlah Proses:").grid(row=0, column=0)
        self.in_proses = ttk.Entry(frame_top, width=10)
        self.in_proses.grid(row=0, column=1)

        ttk.Label(frame_top, text="Jumlah Resource:").grid(row=1, column=0)
        self.in_resource = ttk.Entry(frame_top, width=10)
        self.in_resource.grid(row=1, column=1)

        ttk.Button(frame_top, text="Buat Tabel", command=self.make_table).grid(row=2, column=0, pady=5)
        ttk.Button(frame_top, text="Generate RAG", command=self.generate_rag).grid(row=2, column=1, pady=5)
        ttk.Button(frame_top, text="Deteksi Deadlock", command=self.detect_deadlock).grid(row=2, column=2, pady=5)

        self.table_frame = ttk.Frame(root, padding=10)
        self.table_frame.pack(fill="both", expand=True)

        self.alloc_entries = []
        self.req_entries = []

        self.output = tk.Text(root, height=8)
        self.output.pack(fill="x", padx=10, pady=10)

    def make_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        try:
            self.n = int(self.in_proses.get())
            self.m = int(self.in_resource.get())
        except:
            messagebox.showerror("Error", "Masukkan angka valid!")
            return

        self.alloc_entries = []
        self.req_entries = []

        ttk.Label(self.table_frame, text="Allocation (R → P)").grid(row=0, column=0)
        ttk.Label(self.table_frame, text="Request (P → R)").grid(row=0, column=1)

        for i in range(self.n):
            row_a, row_r = [], []

            frame_a = ttk.Frame(self.table_frame)
            frame_a.grid(row=i + 1, column=0, padx=5)

            frame_r = ttk.Frame(self.table_frame)
            frame_r.grid(row=i + 1, column=1, padx=5)

            for j in range(self.m):
                e1 = ttk.Entry(frame_a, width=4)
                e1.grid(row=0, column=j)
                row_a.append(e1)

                e2 = ttk.Entry(frame_r, width=4)
                e2.grid(row=0, column=j)
                row_r.append(e2)

            self.alloc_entries.append(row_a)
            self.req_entries.append(row_r)

    def read_data(self):
        processes = [f"P{i+1}" for i in range(self.n)]
        resources = [f"R{j+1}" for j in range(self.m)]

        alloc, req = [], []

        for i in range(self.n):
            for j in range(self.m):
                a = int(self.alloc_entries[i][j].get() or 0)
                r = int(self.req_entries[i][j].get() or 0)

                if a == 1:
                    alloc.append((f"R{j+1}", f"P{i+1}"))

                if r == 1:
                    req.append((f"P{i+1}", f"R{j+1}"))

        return processes, resources, alloc, req

    # ✅ LAYOUT DIAGONAL / DIAMOND
    def diamond_layout(self, processes, resources):
        pos = {}

        # Proses ditaruh diagonal kiri atas → kiri bawah
        for i, p in enumerate(processes):
            pos[p] = (-1, i * -1)

        # Resource diagonal kanan bawah → kanan atas
        for j, r in enumerate(resources):
            pos[r] = (1, j)

        return pos

    def generate_rag(self):
        p, r, alloc, req = self.read_data()
        self.output.delete("1.0")
        self.output.insert("1.0", "✅ RAG (Diamond Layout) berhasil dibuat.\n")
        self.draw_diamond(p, r, alloc, req)

    def draw_diamond(self, processes, resources, allocation_edges, request_edges):
        pos = self.diamond_layout(processes, resources)
        G = nx.DiGraph()

        for p in processes:
            G.add_node(p, shape='o', color='lightblue')
        for r in resources:
            G.add_node(r, shape='s', color='lightgreen')

        G.add_edges_from(allocation_edges, type="alloc")
        G.add_edges_from(request_edges, type="req")

        plt.figure(figsize=(10, 7))

        # Node drawing
        for n in G.nodes():
            shape = "o" if n.startswith("P") else "s"
            color = G.nodes[n]["color"]
            nx.draw_networkx_nodes(G, pos, nodelist=[n], node_shape=shape,
                                   node_color=color, node_size=1800)

        # Edges
        alloc_edges = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == "alloc"]
        req_edges   = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == "req"]

        nx.draw_networkx_edges(G, pos, edgelist=req_edges, arrows=True, style="dashed", width=2)
        nx.draw_networkx_edges(G, pos, edgelist=alloc_edges, arrows=True, width=2)

        nx.draw_networkx_labels(G, pos, font_size=12)

        plt.title("Resource Allocation Graph (RAG) – Diamond Layout")
        plt.axis("off")
        plt.show()

    def detect_deadlock(self):
        p, r, alloc, req = self.read_data()
        G = nx.DiGraph()
        G.add_edges_from(alloc)
        G.add_edges_from(req)

        self.output.delete("1.0")

        try:
            cycle = nx.find_cycle(G, orientation="original")
            dead = set([u for u, v, _ in cycle])
            self.output.insert("1.0", f"⚠️ DEADLOCK TERDETEKSI: {dead}\n")
        except:
            self.output.insert("1.0", "✅ Tidak ada deadlock.\n")


# MAIN
app = tb.Window(themename="superhero")
RAGDiamondGUI(app)
app.mainloop()
