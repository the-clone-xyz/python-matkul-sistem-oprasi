import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import networkx as nx
import matplotlib.pyplot as plt
import time


class RAGSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator RAG – Clean Layout + ANIMASI")
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
        ttk.Button(frame_top, text="Animasi RAG", command=self.animate_rag).grid(row=2, column=2, pady=5)
        ttk.Button(frame_top, text="Deteksi Deadlock", command=self.detect_deadlock).grid(row=2, column=3, pady=5)

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

        self.alloc_entries, self.req_entries = [], []

        ttk.Label(self.table_frame, text="Allocation (R → P)").grid(row=0, column=0)
        ttk.Label(self.table_frame, text="Request (P → R)").grid(row=0, column=1)

        for i in range(self.n):
            row_a, row_r = [], []

            frame_a = ttk.Frame(self.table_frame)
            frame_a.grid(row=i+1, column=0, padx=5)

            frame_r = ttk.Frame(self.table_frame)
            frame_r.grid(row=i+1, column=1, padx=5)

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

    # NORMAL RAG (tanpa animasi)
    def generate_rag(self):
        p, r, alloc, req = self.read_data()
        self.output.delete("1.0")
        self.output.insert("1.0", "✅ RAG berhasil dibuat.\n")
        self.draw_clean(p, r, alloc, req)

    # CLEAN LAYOUT (dipakai animasi juga)
    def prepare_layout(self, processes, resources):
        pos = {}
        for i, p in enumerate(processes):
            pos[p] = (-1, i)
        for j, r in enumerate(resources):
            pos[r] = (1, j)
        return pos

    def draw_clean(self, processes, resources, allocation_edges, request_edges):
        pos = self.prepare_layout(processes, resources)
        G = nx.DiGraph()

        for p in processes:
            G.add_node(p, shape='o', color='lightblue')

        for r in resources:
            G.add_node(r, shape='s', color='lightgreen')

        G.add_edges_from(allocation_edges, type="alloc")
        G.add_edges_from(request_edges, type="req")

        plt.figure(figsize=(10, 6))

        # draw nodes
        for n in G.nodes():
            s = G.nodes[n]["shape"]
            c = G.nodes[n]["color"]
            nx.draw_networkx_nodes(G, pos, nodelist=[n], node_shape=s, node_color=c, node_size=1500)

        # draw edges
        alloc_edges = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == "alloc"]
        req_edges   = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == "req"]

        nx.draw_networkx_edges(G, pos, edgelist=alloc_edges, arrows=True, width=2)
        nx.draw_networkx_edges(G, pos, edgelist=req_edges, arrows=True, style="dashed", width=2)

        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.title("RAG – Clean Layout")
        plt.axis("off")
        plt.show()

    # ✅ ANIMASI
    def animate_rag(self):
        p, r, alloc_edges, req_edges = self.read_data()
        pos = self.prepare_layout(p, r)

        G = nx.DiGraph()
        G.add_edges_from(alloc_edges, type="alloc")
        G.add_edges_from(req_edges, type="req")

        plt.ion()  # MODE INTERAKTIF
        fig = plt.figure("Animasi RAG", figsize=(10, 6))

        # langkah animasi
        steps = []

        # 1. highlight semua request (P → R)
        for edge in req_edges:
            steps.append(("request", edge))

        # 2. highlight semua allocation (R → P)
        for edge in alloc_edges:
            steps.append(("alloc", edge))

        # JALANKAN ANIMASI
        for step_type, (u, v) in steps:
            plt.clf()

            # gambar node
            for n in p + r:
                shape = 'o' if n.startswith("P") else 's'
                color = "yellow" if n == u or n == v else ("lightblue" if n.startswith("P") else "lightgreen")
                nx.draw_networkx_nodes(G, pos, nodelist=[n], node_shape=shape,
                                       node_color=color, node_size=1500)

            # gambar edge
            for e in req_edges:
                style = "dashed"
                color = "orange" if e == (u, v) and step_type == "request" else "black"
                nx.draw_networkx_edges(G, pos, edgelist=[e], arrows=True,
                                       style=style, width=2, edge_color=color)

            for e in alloc_edges:
                style = "solid"
                color = "red" if e == (u, v) and step_type == "alloc" else "black"
                nx.draw_networkx_edges(G, pos, edgelist=[e], arrows=True,
                                       width=2, edge_color=color)

            nx.draw_networkx_labels(G, pos, font_size=12)

            title = "Animasi Request (P → R)" if step_type == "request" else "Animasi Allocation (R → P)"
            plt.title(title)
            plt.axis("off")

            plt.pause(1.0)  # jeda per langkah

        plt.ioff()
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
            self.output.insert("1.0", f"⚠️ DEADLOCK: {dead}\n")
        except:
            self.output.insert("1.0", "✅ Tidak ada deadlock.\n")


# MAIN
app = tb.Window(themename="superhero")
RAGSimulatorGUI(app)
app.mainloop()
