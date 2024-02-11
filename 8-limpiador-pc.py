import os
import hashlib
import tempfile
import platform
import shutil
import tkinter as tk 
from tkinter import messagebox

class PC_Cleaner_App:
    def __init__(self, master):
        self.master = master
        master.title("PC Cleaner")

        self.label = tk.Label(master, text="Bienvenido al Limpiador de PC")
        self.label.pack()

        self.duplicate_btn = tk.Button(master, text="Buscar archivos duplicados", command=self.find_duplicates)
        self.duplicate_btn.pack()

        self.cache_btn = tk.Button(master, text="Limpiar caché", command=self.clean_cache)
        self.cache_btn.pack()

        self.space_btn = tk.Button(master, text="Liberar espacio", command=self.free_space)
        self.space_btn.pack()

    def find_duplicates(self):
        duplicates = self._find_duplicates()
        messagebox.showinfo("Archivos duplicados", f"Se encontraron {len(duplicates)} archivos duplicados.")

    def find_duplicates(self):
        hash_dict = {}
        duplicates = []
        for root, _, files in os.walk(os.path.expanduser("~")):
            for filename in files:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as f:
                        filehash = hashlib.md5(f.read()).hexdigest()
                    if filehash in hash_dict:
                        duplicates.append(filepath)
                    else:
                        hash_dict[filehash] = filepath
        return duplicates

    def clean_cache(self):
        if platform.system() == "Windows":
            temp_dir = os.path.join(os.environ["TEMP"], "temp_folder")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                messagebox.showinfo("Limpiar caché", "Caché limpiada correctamente.")
            else:
                messagebox.showinfo("Limpiar caché", "No se encontró caché para limpiar.")
        elif platform.system() == "Linux":
            temp_dir = tempfile.gettempdir()
            if os.path.exists(temp_dir):
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            os.remove(filepath)
                        except Exception as e:
                            print(f"No se pudo eliminar {filepath}: {e}")
                messagebox.showinfo("Limpiar caché", "Caché limpiada correctamente.")
            else:
                messagebox.showinfo("Limpiar caché", "No se encontró caché para limpiar.")

    def free_space(self):
        if platform.system() == "Windows":
            messagebox.showinfo("Liberar espacio", "Funcionalidad no disponible en Windows.")
        elif platform.system() == "Linux":
            root_dir = '/'
            total, used, free = shutil.disk_usage(root_dir)
            messagebox.showinfo("Liberar espacio", f"Espacio total: {total / (2**30):.2f} GB\nEspacio usado: {used / (2**30):.2f} GB\nEspacio libre: {free / (2**30):.2f} GB")

def main():
    root = tk.Tk()
    PC_Cleaner_App(root)
    root.mainloop()

if __name__ == "__main__":
    main()