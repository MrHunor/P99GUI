import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Resolve path relative to the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXE_PATH = os.path.join(BASE_DIR, "main.exe")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class P99Gui(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("P99 Image Encoder/Decoder")
        self.geometry("720x680")
        self.minsize(650, 580)

        self.verbose_var = ctk.BooleanVar(value=False)

        self.create_layout()
        self.verify_backend()

    def verify_backend(self):
        if not os.path.exists(EXE_PATH):
            self.log_output(f"Warning: Executable not found at {EXE_PATH}\n\n")

    def create_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))

        title = ctk.CTkLabel(
            header, text="P99 Engine", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        )
        title.pack(side="left")

        verbose_switch = ctk.CTkSwitch(
            header,
            text="Verbose Logs",
            variable=self.verbose_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        verbose_switch.pack(side="right", pady=5)

        self.tabs = ctk.CTkTabview(self, corner_radius=12)
        self.tabs.pack(fill="both", expand=True, padx=25, pady=10)

        self.tab_encode = self.tabs.add("Encode")
        self.tab_decode = self.tabs.add("Decode")

        self.setup_encode_ui()
        self.setup_decode_ui()

        # Console Log Panel
        console_frame = ctk.CTkFrame(self, corner_radius=12)
        console_frame.pack(fill="both", expand=True, padx=25, pady=(10, 25))

        console_label = ctk.CTkLabel(
            console_frame,
            text="CONSOLE OUTPUT",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#8a8a8f",
        )
        console_label.pack(anchor="w", padx=15, pady=(10, 2))

        self.console_text = ctk.CTkTextbox(
            console_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=("#f2f2f7", "#1c1c1e"),
            text_color=("#1c1c1e", "#e5e5ea"),
            border_width=0,
        )
        self.console_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_encode_ui(self):
        self.enc_from = tk.StringVar()
        self.enc_into = tk.StringVar()

        container = ctk.CTkFrame(self.tab_encode, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.add_input_row(container, "Source File (--from)", self.enc_from, is_folder=False, row=0)
        self.add_input_row(container, "Destination Image/Folder (--into)", self.enc_into, is_folder=True, row=1)

        btn = ctk.CTkButton(
            container,
            text="Run Encoder",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40,
            corner_radius=8,
            command=self.process_encode,
        )
        btn.grid(row=2, column=0, columnspan=2, pady=(35, 0), sticky="ew")
        container.columnconfigure(0, weight=1)

    def setup_decode_ui(self):
        self.dec_orig = tk.StringVar()
        self.dec_mod = tk.StringVar()

        container = ctk.CTkFrame(self.tab_decode, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.add_input_row(container, "Original Image/Folder (--original)", self.dec_orig, is_folder=True, row=0)
        self.add_input_row(container, "Modified Image/Folder (--modified)", self.dec_mod, is_folder=True, row=1)

        btn = ctk.CTkButton(
            container,
            text="Run Decoder",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40,
            corner_radius=8,
            command=self.process_decode,
        )
        btn.grid(row=2, column=0, columnspan=2, pady=(35, 0), sticky="ew")
        container.columnconfigure(0, weight=1)

    def add_input_row(self, master, label_text, variable, is_folder, row):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        frame.columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(
            frame, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        lbl.pack(anchor="w", pady=(0, 4))

        entry = ctk.CTkEntry(
            frame, textvariable=variable, height=35, corner_radius=8, border_width=1
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        if is_folder:
            btn_dir = ctk.CTkButton(
                frame,
                text="Folder",
                width=65,
                height=35,
                corner_radius=6,
                fg_color=("#e5e5ea", "#2c2c2e"),
                text_color=("#000000", "#ffffff"),
                hover_color=("#d1d1d6", "#3a3a3c"),
                command=lambda: self.browse(variable, browse_dir=True),
            )
            btn_dir.pack(side="right", padx=2)

        btn_file = ctk.CTkButton(
            frame,
            text="File",
            width=65,
            height=35,
            corner_radius=6,
            fg_color=("#e5e5ea", "#2c2c2e"),
            text_color=("#000000", "#ffffff"),
            hover_color=("#d1d1d6", "#3a3a3c"),
            command=lambda: self.browse(variable, browse_dir=False),
        )
        btn_file.pack(side="right", padx=2)

    def browse(self, variable, browse_dir):
        path = filedialog.askdirectory() if browse_dir else filedialog.askopenfilename()
        if path:
            variable.set(os.path.normpath(path))

    def log_output(self, text):
        self.console_text.insert(tk.END, text)
        self.console_text.see(tk.END)

    def execute_command(self, args):
        if not os.path.exists(EXE_PATH):
            messagebox.showerror("Error", f"Backend executable not found at: {EXE_PATH}")
            return

        cmd = [EXE_PATH] + args
        self.log_output(f"> {' '.join(cmd)}\n")
        self.update_idletasks()

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if res.stdout:
                self.log_output(res.stdout)
            if res.stderr:
                self.log_output(f"[stderr]\n{res.stderr}\n")

            self.log_output(f"Process exited with code: {res.returncode}\n\n")

            if res.returncode == 0:
                messagebox.showinfo("Success", "Task completed successfully.")
            else:
                messagebox.showerror("Error", f"Execution failed with code {res.returncode}")

        except Exception as e:
            self.log_output(f"System Error: {str(e)}\n")

    def process_encode(self):
        f = self.enc_from.get().strip()
        i = self.enc_into.get().strip()

        if not f or not i:
            messagebox.showwarning("Warning", "All fields are required.")
            return

        args = ["encode", "-f", f, "-i", i]
        if self.verbose_var.get():
            args.insert(0, "-v")
        self.execute_command(args)

    def process_decode(self):
        o = self.dec_orig.get().strip()
        m = self.dec_mod.get().strip()

        if not o or not m:
            messagebox.showwarning("Warning", "All fields are required.")
            return

        args = ["decode", "-o", o, "-m", m]
        if self.verbose_var.get():
            args.insert(0, "-v")
        self.execute_command(args)


if __name__ == "__main__":
    app = P99Gui()
    app.mainloop()