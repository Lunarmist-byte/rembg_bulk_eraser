import os
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox
from processor import BackgroundRemover

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bulk Background Remover")
        self.geometry("600x450")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.input_folder = ""
        self.output_folder = ""
        self.remover = None

        self.setup_ui()

    def setup_ui(self):
        title_font = ctk.CTkFont(size=24, weight="bold")
        self.title_label = ctk.CTkLabel(self, text="Bulk Background Remover", font=title_font)
        self.title_label.pack(pady=(30, 20))
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=40, pady=10)

        self.input_btn = ctk.CTkButton(self.input_frame, text="Select Input Folder", command=self.select_input_folder, width=150)
        self.input_btn.pack(side="left")

        self.input_label = ctk.CTkLabel(self.input_frame, text="No folder selected", text_color="gray")
        self.input_label.pack(side="left", padx=15)

        self.output_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.output_frame.pack(fill="x", padx=40, pady=10)

        self.output_btn = ctk.CTkButton(self.output_frame, text="Select Output Folder", command=self.select_output_folder, width=150)
        self.output_btn.pack(side="left")

        self.output_label = ctk.CTkLabel(self.output_frame, text="No folder selected", text_color="gray")
        self.output_label.pack(side="left", padx=15)
        self.progress_bar = ctk.CTkProgressBar(self, width=520)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(30, 10))

        self.status_label = ctk.CTkLabel(self, text="Ready", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)

        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.controls_frame, text="Start Processing", command=self.start_processing, width=200, height=40, font=ctk.CTkFont(size=15, weight="bold"))
        self.start_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(self.controls_frame, text="Cancel", command=self.cancel_processing, width=100, height=40, fg_color="#D32F2F", hover_color="#B71C1C", state="disabled")
        self.cancel_btn.pack(side="left", padx=10)

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(side="bottom", pady=20)

        credit_label = ctk.CTkLabel(self.footer_frame, text="Made by Lunarmist-byte", font=ctk.CTkFont(size=12, weight="bold"))
        credit_label.pack(side="top", pady=(0, 5))

        links_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        links_frame.pack(side="top")

        github_link = ctk.CTkLabel(links_frame, text="GitHub", font=ctk.CTkFont(size=12, underline=True), text_color="#1f6aa5", cursor="hand2")
        github_link.pack(side="left", padx=10)
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Lunarmist-byte"))

        linkedin_link = ctk.CTkLabel(links_frame, text="LinkedIn", font=ctk.CTkFont(size=12, underline=True), text_color="#1f6aa5", cursor="hand2")
        linkedin_link.pack(side="left", padx=10)
        linkedin_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.linkedin.com/in/amal-s-kumar-ba69a1290/"))


    def select_input_folder(self):
        if folder := filedialog.askdirectory(title="Select Input Folder"):
            self.input_folder = folder
            self.input_label.configure(text=f"...{folder[-37:]}" if len(folder) > 40 else folder, text_color="white")

    def select_output_folder(self):
        if folder := filedialog.askdirectory(title="Select Output Folder"):
            self.output_folder = folder
            self.output_label.configure(text=f"...{folder[-37:]}" if len(folder) > 40 else folder, text_color="white")

    def start_processing(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return

        for btn in (self.start_btn, self.input_btn, self.output_btn):
            btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")

        self.progress_bar.set(0)
        self.status_label.configure(text="Loading model and starting...")

        self.remover = BackgroundRemover(
            self.input_folder,
            self.output_folder,
            lambda c, t, p: self.after(0, lambda: self._update_progress(c, t, p)),
            lambda t: self.after(0, lambda: self._on_complete(t)),
            lambda e: self.after(0, lambda: self._on_error(e))
        )
        self.remover.start()

    def cancel_processing(self):
        if self.remover:
            self.remover.cancel()
        self.status_label.configure(text="Cancelling...")
        self.cancel_btn.configure(state="disabled")

    def _update_progress(self, current, total, progress):
        self.progress_bar.set(progress)
        self.status_label.configure(text=f"Processing: {current}/{total}")

    def _on_complete(self, total):
        for btn in (self.start_btn, self.input_btn, self.output_btn):
            btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

        if self.remover and self.remover.is_cancelled:
            self.status_label.configure(text="Cancelled.")
        else:
            self.progress_bar.set(1)
            self.status_label.configure(text=f"Done! {total} images processed.")
            messagebox.showinfo("Success", f"Processed {total} images.")

    def _on_error(self, err):
        for btn in (self.start_btn, self.input_btn, self.output_btn):
            btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.status_label.configure(text="Error occurred.")
        messagebox.showerror("Error", str(err))

if __name__ == "__main__":
    app = App()
    app.mainloop()
