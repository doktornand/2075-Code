# █████████████████████████████████████████████████████████████████████████████
# █  CREONET vΩ.2 — GUI Multi-Villes                                         █
# █████████████████████████████████████████████████████████████████████████████

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from CreoNet4c import creonet_translate, get_emotion_tags, get_styles, get_city_profiles

class CreoNetGUIv2:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ CREONET vΩ.2 — RÉSEAU MULTI-VILLES")
        self.root.geometry("850x650")
        self.root.configure(bg="#0a0a0a")
        self.font_mono = ("Courier New", 11)
        self.font_title = ("Courier New", 14, "bold")

        # Titre
        title = tk.Label(root, text="🌍 CREONET vΩ.2 // RÉSEAUX LOCAUX ACTIFS", 
                         font=self.font_title, fg="#00ff41", bg="#0a0a0a")
        title.pack(pady=10)

        # Zone de texte source
        tk.Label(root, text="➤ TEXTE SOURCE (fr/en) :", fg="#00ccff", bg="#0a0a0a", font=self.font_mono).pack(anchor="w", padx=20)
        self.input_text = tk.Text(root, height=4, width=80, bg="#1a1a1a", fg="#ffffff", insertbackground="#00ff41", font=self.font_mono)
        self.input_text.pack(padx=20, pady=5)

        # Options avancées
        opts_frame = tk.Frame(root, bg="#0a0a0a")
        opts_frame.pack(pady=10)

        # Ligne 1: Mood, Style, Seed
        tk.Label(opts_frame, text="MOOD :", fg="#ff6600", bg="#0a0a0a", font=self.font_mono).grid(row=0, column=0, padx=5)
        self.mood_var = tk.StringVar(value="neutre")
        self.mood_menu = ttk.Combobox(opts_frame, textvariable=self.mood_var, values=list(get_emotion_tags().keys()), state="readonly", width=12)
        self.mood_menu.grid(row=0, column=1, padx=5)

        tk.Label(opts_frame, text="STYLE :", fg="#ff6600", bg="#0a0a0a", font=self.font_mono).grid(row=0, column=2, padx=5)
        self.style_var = tk.StringVar(value="street")
        self.style_menu = ttk.Combobox(opts_frame, textvariable=self.style_var, values=get_styles(), state="readonly", width=12)
        self.style_menu.grid(row=0, column=3, padx=5)

        tk.Label(opts_frame, text="SEED :", fg="#ff6600", bg="#0a0a0a", font=self.font_mono).grid(row=0, column=4, padx=5)
        self.seed_var = tk.StringVar(value="0")
        tk.Entry(opts_frame, textvariable=self.seed_var, width=8, font=self.font_mono, bg="#1a1a1a", fg="#ffffff").grid(row=0, column=5, padx=5)

        # Ligne 2: Ville et indicateurs de poids
        tk.Label(opts_frame, text="🌍 VILLE :", fg="#ff00ff", bg="#0a0a0a", font=self.font_mono).grid(row=1, column=0, padx=5, pady=(10,0))
        self.city_var = tk.StringVar(value="gwadar")
        city_opts = get_city_profiles()
        self.city_menu = ttk.Combobox(opts_frame, textvariable=self.city_var, values=city_opts, state="readonly", width=12)
        self.city_menu.grid(row=1, column=1, padx=5, pady=(10,0))
        self.city_menu.bind('<<ComboboxSelected>>', self.update_city_info)

        # Frame pour les indicateurs linguistiques
        lang_frame = tk.Frame(opts_frame, bg="#0a0a0a")
        lang_frame.grid(row=1, column=2, columnspan=4, padx=5, pady=(10,0))

        self.lang_labels = {}
        languages = [("créole", "#ff4444"), ("français", "#4444ff"), ("anglais", "#44ff44"), ("code", "#ff44ff")]
        
        for i, (lang, color) in enumerate(languages):
            label = tk.Label(lang_frame, text=f"{lang}: --", fg=color, bg="#0a0a0a", font=("Courier New", 8))
            label.grid(row=0, column=i, padx=3)
            self.lang_labels[lang] = label

        # Boutons
        btn_frame = tk.Frame(root, bg="#0a0a0a")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🌀 TRADUIRE", command=self.translate, bg="#003300", fg="#00ff41", font=self.font_mono).pack(side="left", padx=5)
        tk.Button(btn_frame, text="💾 SAUVEGARDER", command=self.save_output, bg="#330033", fg="#ff00ff", font=self.font_mono).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📡 TEST MULTI-VILLES", command=self.test_multi_city, bg="#003333", fg="#00ffff", font=self.font_mono).pack(side="left", padx=5)

        # Zone de résultat
        tk.Label(root, text="🌀 CRÉONEURAL (PROFIL ACTIF) :", fg="#00ff41", bg="#0a0a0a", font=self.font_mono).pack(anchor="w", padx=20, pady=(15,5))
        self.output_text = tk.Text(root, height=10, width=80, bg="#001100", fg="#00ff88", font=self.font_mono, state="disabled")
        self.output_text.pack(padx=20, pady=5)

        # Footer
        footer = tk.Label(root, text="🌍 SYSTÈME MULTI-VILLES — GWADAR | NAPLES | LAGOS | DJIBOUTI | ABIDJAN | PORT-AU-PRINCE", 
                          fg="#ff3333", bg="#0a0a0a", font=("Courier New", 9))
        footer.pack(side="bottom", pady=5)

        # Initialisation
        self.update_city_info()

    def update_city_info(self, event=None):
        """Met à jour les indicateurs de poids linguistique"""
        from CreoNet4c import CreoNetTranslator
        translator = CreoNetTranslator()
        weights = translator.get_language_weights(self.city_var.get())
        
        for lang, label in self.lang_labels.items():
            weight = weights.get(lang, 0)
            color = label.cget("fg")
            label.config(text=f"{lang}: {weight:.1f}")

    def translate(self):
        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("⚠️", "Veuillez entrer du texte.")
            return

        mood = self.mood_var.get()
        style = self.style_var.get()
        city = self.city_var.get()
        seed_str = self.seed_var.get()
        seed = int(seed_str) if seed_str.isdigit() and seed_str != "0" else None

        try:
            result = creonet_translate(text, mood=mood, style=style, city_profile=city, seed=seed)
        except Exception as e:
            result = f"<null> ERREUR : {str(e)}"

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.config(state="disabled")

    def save_output(self):
        content = self.output_text.get("1.0", "end-1c")
        if not content or content.startswith("<null>"):
            messagebox.showinfo("💾", "Rien à sauvegarder.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".creo",
            filetypes=[("Fichiers CréoNeural", "*.creo"), ("Texte", "*.txt")]
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"// CRÉONEURAL - {self.city_var.get().upper()}\n")
                f.write(content)
            messagebox.showinfo("💾", f"Sauvegardé depuis {self.city_var.get()}.")

    def test_multi_city(self):
        """Teste la même phrase sur plusieurs villes"""
        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("⚠️", "Veuillez entrer du texte à tester.")
            return

        cities = get_city_profiles()
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        
        self.output_text.insert("end", "🧪 TEST MULTI-VILLES :\n")
        self.output_text.insert("end", "=" * 50 + "\n")
        
        for city in cities[:6]:  # Limite à 6 villes pour la démo
            try:
                result = creonet_translate(text, city_profile=city, seed=42)
                self.output_text.insert("end", f"🌍 {city.upper():<12} → {result}\n")
            except Exception as e:
                self.output_text.insert("end", f"🌍 {city.upper():<12} → ERREUR: {str(e)}\n")
        
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CreoNetGUIv2(root)
    root.mainloop()
