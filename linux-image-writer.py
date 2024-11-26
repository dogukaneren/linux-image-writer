import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def select_iso():
    file_path = filedialog.askopenfilename(filetypes=[("ISO Files", "*.iso")])
    if file_path:
        iso_path_entry.delete(0, tk.END)
        iso_path_entry.insert(0, file_path)

def select_usb():
    directory = filedialog.askdirectory()
    if directory:
        usb_path_entry.delete(0, tk.END)
        usb_path_entry.insert(0, directory)

def write_iso():
    iso_path = iso_path_entry.get()
    usb_path = usb_path_entry.get()

    if not iso_path or not os.path.exists(iso_path):
        messagebox.showerror("Error", "Please select a valid ISO file!")
        return

    if not usb_path or not os.path.exists(usb_path):
        messagebox.showerror("Error", "Please select a valid USB path!")
        return

    result = messagebox.askyesno("Warning", "This process will erase all data on the USB drive! Do you want to continue?")
    if not result:
        return

    try:
        command = f"sudo dd if={iso_path} of={usb_path} bs=4M status=progress conv=fsync"
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", "ISO successfully written to USB!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

window = tk.Tk()
window.title("ISO Writer")
window.geometry("500x300")

tk.Label(window, text="ISO File:").pack(pady=5)
iso_path_entry = tk.Entry(window, width=50)
iso_path_entry.pack(pady=5)
tk.Button(window, text="Select ISO", command=select_iso).pack(pady=5)

tk.Label(window, text="USB Drive Path:").pack(pady=5)
usb_path_entry = tk.Entry(window, width=50)
usb_path_entry.pack(pady=5)
tk.Button(window, text="Select USB", command=select_usb).pack(pady=5)

tk.Button(window, text="Write ISO", command=write_iso, bg="green", fg="white").pack(pady=20)

window.mainloop()
