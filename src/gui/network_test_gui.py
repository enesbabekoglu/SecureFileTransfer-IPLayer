import tkinter as tk
from tkinter import ttk, messagebox
from ..utils.network_test_utils import run_ping, run_iperf

def run_network_test_gui():
    class NetworkTestGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Ağ Karşılaştırması")
            self.root.geometry("700x400")
            
            # Ana menüye dönüş butonu
            self.back_button = tk.Button(root, text="Ana Menüye Dön", command=self.return_to_main_menu)
            self.back_button.pack(pady=5)

            frame = tk.Frame(root)
            frame.pack(pady=10)

            tk.Label(frame, text="Ping Host:").grid(row=0, column=0, sticky="e")
            self.ping_entry = tk.Entry(frame, width=20)
            self.ping_entry.insert(0, "8.8.8.8")
            self.ping_entry.grid(row=0, column=1, padx=5)

            tk.Label(frame, text="iperf3 Sunucu:").grid(row=1, column=0, sticky="e")
            self.iperf_entry = tk.Entry(frame, width=20)
            self.iperf_entry.insert(0, "127.0.0.1")
            self.iperf_entry.grid(row=1, column=1, padx=5)

            tk.Button(root, text="Test Et", command=self.run_tests).pack(pady=5)

            columns = ("environment", "rtt_ms", "packet_loss", "bandwidth")
            self.tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
            self.tree.heading("environment", text="Ortam")
            self.tree.heading("rtt_ms", text="RTT (ms)")
            self.tree.heading("packet_loss", text="Packet Loss (%)")
            self.tree.heading("bandwidth", text="Band Genişliği")
            for col in columns:
                self.tree.column(col, anchor="center", width=150)
            self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        def return_to_main_menu(self):
            """Ana menüye geri dön"""
            self.root.destroy()
            from src.gui.app import main
            main()
            
        def run_tests(self):
            # Test konfigürasyonları
            ping_host = self.ping_entry.get()
            iperf_host = self.iperf_entry.get()
            self.tree.delete(*self.tree.get_children())

            tests = [
                ("Google DNS", ping_host),
                ("Loopback", "127.0.0.1"),
                ("iperf Sunucu", iperf_host)
            ]

            for env, host in tests:
                rtt, loss = run_ping(host)
                bw = run_iperf(iperf_host)
                self.tree.insert("", tk.END, values=(env, rtt, loss, bw))

    root = tk.Tk()
    NetworkTestGUI(root)
    root.mainloop()
