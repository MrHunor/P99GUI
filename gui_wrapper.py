import os
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- Configuration ---
EXE_NAME = "main.exe"
CPP_SOURCE = "main.cpp"

# Set Apple-like modern theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def get_exe_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), EXE_NAME)

def auto_compile():
    exe_path = get_exe_path()
    if os.path.exists(exe_path):
        return True

    if os.path.exists(CPP_SOURCE):
        print(f"[{EXE_NAME}] not found. Attempting auto-compilation with g++...")
        try:
            result = subprocess.run(
                ["g++", "-O3", CPP_SOURCE, "-o", EXE_NAME], 
                capture_output=True, text=True
            )
            if result.returncode == 0 and os.path.exists(exe_path):
                return True
        except FileNotFoundError:
            pass
    return False

class SteganoGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Steganography Studio")
        self.geometry("700x580")
        self.resizable(False, False)

        if not auto_compile():
            messagebox.showwarning(
                "Missing Executable", 
                f"Could not find or compile '{EXE_NAME}'.\n\nPlease place your 'main.exe' in this directory."
            )

        self.create_widgets()

    def create_widgets(self):
        # --- Main Layout Padding ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- 1. Mode Selection ---
        mode_frame = ctk.CTkFrame(self, corner_radius=10)
        mode_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        mode_label = ctk.CTkLabel(mode_frame, text="1. Select Operation", font=ctk.CTkFont(size=14, weight="bold"))
        mode_label.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")

        self.mode_var = ctk.StringVar(value="encode")
        
        radio_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        radio_frame.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        
        ctk.CTkRadioButton(radio_frame, text="Encode (Hide Data)", variable=self.mode_var, value="encode", command=self.update_labels).pack(side="left", padx=(0, 30))
        ctk.CTkRadioButton(radio_frame, text="Decode (Extract Data)", variable=self.mode_var, value="decode", command=self.update_labels).pack(side="left")

        # --- 2. Target Selection (with fixed File/Folder logic) ---
        path_frame = ctk.CTkFrame(self, corner_radius=10)
        path_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        path_label = ctk.CTkLabel(path_frame, text="2. Select Targets", font=ctk.CTkFont(size=14, weight="bold"))
        path_label.grid(row=0, column=0, columnspan=4, padx=15, pady=(10, 5), sticky="w")

        # Target 1
        self.lbl_target1 = ctk.CTkLabel(path_frame, text="Target Image/Folder:", width=140, anchor="w")
        self.lbl_target1.grid(row=1, column=0, padx=(15, 5), pady=10)
        
        self.entry_target1 = ctk.CTkEntry(path_frame, width=320, placeholder_text="Path to target...")
        self.entry_target1.grid(row=1, column=1, padx=5, pady=10)
        
        ctk.CTkButton(path_frame, text="📄 File", width=60, command=lambda: self.browse_file(self.entry_target1)).grid(row=1, column=2, padx=5, pady=10)
        ctk.CTkButton(path_frame, text="📁 Folder", width=60, command=lambda: self.browse_folder(self.entry_target1)).grid(row=1, column=3, padx=(5, 15), pady=10)

        # Target 2
        self.lbl_target2 = ctk.CTkLabel(path_frame, text="Data Source to Hide:", width=140, anchor="w")
        self.lbl_target2.grid(row=2, column=0, padx=(15, 5), pady=(0, 15))
        
        self.entry_target2 = ctk.CTkEntry(path_frame, width=320, placeholder_text="Path to data...")
        self.entry_target2.grid(row=2, column=1, padx=5, pady=(0, 15))
        
        ctk.CTkButton(path_frame, text="📄 File", width=60, command=lambda: self.browse_file(self.entry_target2)).grid(row=2, column=2, padx=5, pady=(0, 15))
        ctk.CTkButton(path_frame, text="📁 Folder", width=60, command=lambda: self.browse_folder(self.entry_target2)).grid(row=2, column=3, padx=(5, 15), pady=(0, 15))

        # --- 3. Output Console ---
        out_frame = ctk.CTkFrame(self, corner_radius=10)
        out_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        out_frame.grid_columnconfigure(0, weight=1)
        out_frame.grid_rowconfigure(0, weight=1)

        self.txt_output = ctk.CTkTextbox(out_frame, font=ctk.CTkFont(family="Consolas", size=12), corner_radius=10)
        self.txt_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.txt_output.insert("0.0", "System ready.\n")

        # --- 4. Action Buttons ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        ctk.CTkButton(btn_frame, text="Launch Interactive Terminal", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.run_interactive).pack(side="left")
        ctk.CTkButton(btn_frame, text="Execute Action", font=ctk.CTkFont(weight="bold"), command=self.run_backend_cmd).pack(side="right")

    def update_labels(self):
        if self.mode_var.get() == "encode":
            self.lbl_target1.configure(text="Target Image/Folder:")
            self.lbl_target2.configure(text="Data Source to Hide:")
        else:
            self.lbl_target1.configure(text="Original Image/Folder:")
            self.lbl_target2.configure(text="Encoded Image/Folder:")

    # --- Fixed Browse Logic ---
    def browse_file(self, entry_widget):
        path = filedialog.askopenfilename(title="Select File")
        if path:
            path = os.path.normpath(path)
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, path)

    def browse_folder(self, entry_widget):
        path = filedialog.askdirectory(title="Select Folder")
        if path:
            path = os.path.normpath(path)
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, path)

    def append_output(self, text):
        self.txt_output.insert(ctk.END, text)
        self.txt_output.see(ctk.END)

    def run_backend_cmd(self):
        exe_path = get_exe_path()
        if not os.path.exists(exe_path):
            messagebox.showerror("Error", f"Executable '{EXE_NAME}' not found.")
            return

        action = self.mode_var.get()
        t1 = self.entry_target1.get().strip()
        t2 = self.entry_target2.get().strip()

        if not t1 or not t2:
            messagebox.showwarning("Warning", "Please provide paths for both fields.")
            return

        cmd = [exe_path, action, t1, t2]
        
        self.txt_output.delete("0.0", ctk.END)
        self.append_output(f"> {' '.join(cmd)}\n\n")
        
        def execute():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                if result.stdout:
                    self.append_output(result.stdout)
                if result.stderr:
                    self.append_output(f"\nERROR:\n{result.stderr}")
            except Exception as e:
                self.append_output(f"Execution failed: {str(e)}")
            self.append_output("\n[Process Finished]\n")

        # Run in a thread so the UI doesn't freeze during large file encoding
        threading.Thread(target=execute, daemon=True).start()

    def run_interactive(self):
        exe_path = get_exe_path()
        if os.path.exists(exe_path):
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/c", exe_path])
        else:
            messagebox.showerror("Error", f"Executable '{EXE_NAME}' not found.")

if __name__ == "__main__":
    app = SteganoGUI()
    app.mainloop()