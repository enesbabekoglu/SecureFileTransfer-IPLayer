import tkinter as tk
from tkinter import filedialog

class FileSelector(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.selected_file = None

        self.label = tk.Label(self, text="Henüz dosya seçilmedi.")
        self.label.pack(pady=5)

        self.button = tk.Button(self, text="Dosya Seç", command=self.select_file)
        self.button.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.label.config(text=f"Seçilen: {file_path}")
        else:
            self.label.config(text="Dosya seçilmedi.")
