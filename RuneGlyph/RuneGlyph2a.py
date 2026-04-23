#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RuneGlyph Tk — Interface Runique pour Glyphe Mémétique
Beaumont-Hague, 2075 | Pour les RuneSmiths de Caen-Profonde
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import random
import hashlib
import os
from datetime import datetime

# === Symboles ===
RUNIC_SIGILS = ["ᚠ", "ᚢ", "ᚦ", "ᚩ", "ᚱ", "ᚳ", "ᚷ", "ᚹ", "ᚺ", "ᚾ", "ᛁ", "ᛃ", "ᛇ", "ᛈ", "ᛉ", "ᛋ", "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛝ", "ᛟ", "ᛞ", "ᚪ", "ᚫ", "ᚣ", "ᛡ", "ᛠ"]
VON_PETZINGER = ["△", "○", "||", "///", "▫", "⚡", "🌀", "✧", "⧖", "⚯"]
ARCHETYPES = ["Le Gardien Fracturé", "L’Écho Enchaîné", "La Mère Salée", "Le Codificateur Sombre", "Le Rêveur Atomique"]
DEFAULT_LEXICON = "paleo_mnemos_lexicon.json"

class RuneGlyphApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" runesight ∞ glyphe — Beaumont-Hague 2075 ")
        self.root.geometry("900x700")
        self.lexicon = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # === Frame principal ===
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # === Prompt ===
        ttk.Label(main_frame, text="Prompt mémétique :").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.prompt_var = tk.StringVar()
        prompt_entry = ttk.Entry(main_frame, textvariable=self.prompt_var, width=60)
        prompt_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # === Options ===
        self.echo_var = tk.BooleanVar()
        self.lexicon_var = tk.BooleanVar()
        
        ttk.Checkbutton(main_frame, text="Mode Echo-Guillaume", variable=self.echo_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Charger lexique", variable=self.lexicon_var, command=self.load_lexicon_if_needed).grid(row=1, column=1, sticky=tk.W)
        
        # === Palette Runique ===
        palette_frame = ttk.LabelFrame(main_frame, text=" Palette Runique ", padding="10")
        palette_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Runes
        ttk.Label(palette_frame, text="Futhark :").grid(row=0, column=0, sticky=tk.W)
        rune_text = scrolledtext.ScrolledText(palette_frame, height=2, width=40, wrap=tk.WORD, font=("Courier", 12))
        rune_text.insert(tk.END, " ".join(RUNIC_SIGILS))
        rune_text.config(state=tk.DISABLED)
        rune_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # von Petzinger
        ttk.Label(palette_frame, text="Symboles Paleo :").grid(row=2, column=0, sticky=tk.W, pady=(10,0))
        petz_text = scrolledtext.ScrolledText(palette_frame, height=2, width=40, wrap=tk.WORD, font=("Courier", 12))
        petz_text.insert(tk.END, " ".join(VON_PETZINGER))
        petz_text.config(state=tk.DISABLED)
        petz_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Archétypes
        ttk.Label(palette_frame, text="Archétypes :").grid(row=4, column=0, sticky=tk.W, pady=(10,0))
        arch_text = scrolledtext.ScrolledText(palette_frame, height=2, width=40, wrap=tk.WORD, font=("Courier", 12))
        arch_text.insert(tk.END, " • ".join(ARCHETYPES))
        arch_text.config(state=tk.DISABLED)
        arch_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # === Boutons ===
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Générer Glyphe", command=self.generate_glyph).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exporter TXT", command=self.export_txt).pack(side=tk.LEFT, padx=5)
        
        # === Canvas de glyphe ===
        view_frame = ttk.LabelFrame(main_frame, text=" Aperçu du Glyphe ", padding="10")
        view_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        view_frame.rowconfigure(0, weight=1)
        view_frame.columnconfigure(0, weight=1)
        
        self.glyph_display = scrolledtext.ScrolledText(view_frame, wrap=tk.NONE, font=("Courier", 14), bg="#0d0d0d", fg="#00ffcc")
        self.glyph_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Code FracturoScript ===
        code_frame = ttk.LabelFrame(main_frame, text=" FracturoScript ", padding="10")
        code_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        code_frame.rowconfigure(0, weight=1)
        code_frame.columnconfigure(0, weight=1)
        
        self.code_display = scrolledtext.ScrolledText(code_frame, wrap=tk.NONE, font=("Courier", 10), bg="#1a1a1a", fg="#ff66ff")
        self.code_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurer poids pour redimensionnement
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def load_lexicon_if_needed(self):
        if self.lexicon_var.get():
            if os.path.exists(DEFAULT_LEXICON):
                with open(DEFAULT_LEXICON, 'r', encoding='utf-8') as f:
                    self.lexicon = json.load(f)
            else:
                messagebox.showwarning("Lexique manquant", f"Fichier {DEFAULT_LEXICON} non trouvé. Génération basique activée.")
                self.lexicon_var.set(False)
                self.lexicon = None
                
    def fracturo_hash(self, seed):
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
        
    def generate_glyph(self):
        prompt = self.prompt_var.get().strip() or "Beaumont-Hague"
        random.seed(self.fracturo_hash(prompt + str(datetime.now())))
        
        rune = random.choice(RUNIC_SIGILS)
        petz = random.choice(VON_PETZINGER)
        arch = random.choice(ARCHETYPES)
        
        # ASCII glyphe
        ascii_glyph = f"""
      {petz}
    {rune} {rune}
      {petz}
    ——{arch}——
        """
        
        # FracturoScript
        semantic = f"⟦⌇:{prompt.upper()}:⌇⟧"
        if self.lexicon and "entries" in self.lexicon:
            seed_entry = random.choice(self.lexicon["entries"])
            semantic += f" ⊕ {seed_entry.get('symbol', '?')}({seed_entry.get('archetype', 'VOID')})"
        if self.echo_var.get():
            semantic += " ↻ ECHO-GUILLAUME.ACTIVE"
            
        fracturo_code = f"""// FracturoGlyph — Beaumont-Hague 2075
glyph {{
    core_rune = "{rune}";
    archetype = "{arch}";
    petzinger = "{petz}";
    semantic = "{semantic}";
    zone = "Beaumont-Hague";
    echo_mode = {"true" if self.echo_var.get() else "false"};
}}"""
        
        self.glyph_display.delete(1.0, tk.END)
        self.glyph_display.insert(tk.END, ascii_glyph)
        
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(tk.END, fracturo_code)
        
        self.last_glyph = {
            "ascii": ascii_glyph,
            "code": fracturo_code,
            "prompt": prompt
        }
        
    def export_txt(self):
        if not hasattr(self, 'last_glyph'):
            messagebox.showwarning("Rien à exporter", "Génère d’abord un glyphe !")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texte", "*.txt"), ("Tous fichiers", "*.*")],
            title="Exporter le glyphe"
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("=== FracturoGlyph (ASCII) ===\n")
                f.write(self.last_glyph["ascii"])
                f.write("\n=== FracturoScript ===\n")
                f.write(self.last_glyph["code"])
            messagebox.showinfo("Exporté", f"Glyphe sauvegardé : {os.path.basename(filepath)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuneGlyphApp(root)
    root.mainloop()
