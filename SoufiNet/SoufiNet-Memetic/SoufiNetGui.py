import tkinter as tk
from tkinter import ttk, messagebox
from SoufiGen4a import GenerateurGhazalCyberSoufi
import json

class SoufiNetGui:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ SoufiNet – GUI Mystique")
        self.root.geometry("700x600")
        self.root.configure(bg="#0d0b1a")

        # Palette mystique
        self.bg = "#0d0b1a"
        self.fg = "#e0d6ff"
        self.accent = "#8a2be2"  # violet mystique
        self.entry_bg = "#1a162d"

        self.gen = GenerateurGhazalCyberSoufi()

        self.creer_widgets()

    def creer_widgets(self):
        # Titre
        tk.Label(self.root, text="Générateur de Ghazal Cyber-Soufi", 
                 font=("Courier", 16, "bold"), bg=self.bg, fg="#c7a2ff").pack(pady=15)

        # Thème
        tk.Label(self.root, text="Thème spirituel :", bg=self.bg, fg=self.fg).pack()
        self.theme_var = tk.StringVar(value="amour_divin")
        themes = list(json.load(open("lexiques.json", encoding="utf-8"))["thèmes"].keys())
        ttk.Combobox(self.root, textvariable=self.theme_var, values=themes, 
                     state="readonly", width=30).pack(pady=5)

        # Options avancées
        self.balise_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Inclure balises oniriques (<burn>, <still>, etc.)",
                       variable=self.balise_var, bg=self.bg, fg=self.fg,
                       selectcolor=self.entry_bg, activebackground=self.bg).pack(pady=5)

        self.nb_var = tk.IntVar(value=6)
        tk.Label(self.root, text="Nombre de vers :", bg=self.bg, fg=self.fg).pack()
        tk.Spinbox(self.root, from_=1, to=20, textvariable=self.nb_var, 
                   bg=self.entry_bg, fg=self.fg, width=8).pack(pady=5)

        # Bouton
        tk.Button(self.root, text="✨ Générer le Ghazal", command=self.generer,
                  bg=self.accent, fg="white", font=("Courier", 12, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=20)

        # Zone de résultat
        self.texte = tk.Text(self.root, height=12, width=70, 
                             bg=self.entry_bg, fg=self.fg, 
                             font=("Courier", 11), wrap="word", 
                             insertbackground="#c7a2ff")
        self.texte.pack(padx=20, pady=10)

    def generer(self):
        self.texte.delete(1.0, tk.END)
        try:
            ghazal = self.gen.generer_ghazal(
                nb_vers=self.nb_var.get(),
                theme=self.theme_var.get()
            )
            for vers in ghazal:
                self.texte.insert(tk.END, "- " + vers + "\n\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer :\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SoufiNetGui(root)
    root.mainloop()