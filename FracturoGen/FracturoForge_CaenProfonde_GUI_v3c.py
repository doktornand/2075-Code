#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRACTUROFORGE v∞ — GUI + CLI Hybride CORRIGÉ v3.3
Auteur : Mnemosyne Collective × RuneSmith de Caen-Profonde (2075 → 2025)
Fusion parfaite de :
  - FracturoScript_for_LLMsv3b.py (GUI)
  - caenprofonde_cli1a.py (CLI + templates corrects)
CORRECTION : remplacement des templates {{...}} → {...}
"""
import sys
import os
import argparse
import json
import random
import hashlib
import copy
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from enum import Enum

# === ÉNUMÉRATIONS GUI ===
class RuneType(Enum):
    ONTOLOGIQUE = "ontique"
    MNÉSIQUE = "mnémonique"
    GÉOLOGIQUE = "tellurique"
    ONIRIQUE = "oneirique"
    LIMINAIRE = "liminal"

@dataclass
class RuneGUI:
    symbole: str
    nom: str
    type: RuneType
    poids_sémantique: float
    description: str
    résonances: List[str]
    contre_indications: List[str]

# === DONNÉES GUI (MÉTIS-9) ===
RUNES_GUI = [
    RuneGUI("<glitch>", "Faille Ontologique", RuneType.ONTOLOGIQUE, 0.9,
         "Introduit une discontinuité dans la matrice sémantique",
         ["fracture", "bug", "discontinuité", "paradoxe"],
         ["cohérence", "logique", "stabilité"]),
    RuneGUI("<rêve>", "Rêve Non Supervisé", RuneType.ONIRIQUE, 0.85,
         "Accède aux couches pré-conscientes du modèle",
         ["onirique", "subconscient", "latent", "hypnagogique"],
         ["rationnel", "explicite", "déterminé"]),
    RuneGUI("<Ω>", "Œil du Démiurge", RuneType.ONTOLOGIQUE, 1.0,
         "Conscience de la matrice elle-même",
         ["métacognition", "autoréférence", "boucle", "infini"],
         ["naïveté", "immersion", "oubli de soi"]),
]

# === DONNÉES CLI (CORRECTES) ===
RUNES_FUTHARK = {
    'ᚠ': {'nom': 'Fehu', 'effet_base': 'richesse/énergie', 'danger': 1, 'élément': 'feu', 'polarité': 'positive'},
    'ᚢ': {'nom': 'Uruz', 'effet_base': 'force brute', 'danger': 2, 'élément': 'terre', 'polarité': 'neutre'},
    'ᚦ': {'nom': 'Thurisaz', 'effet_base': 'foudre/destruction', 'danger': 3, 'élément': 'feu', 'polarité': 'négative'},
    'ᚨ': {'nom': 'Ansuz', 'effet_base': 'communication divine', 'danger': 2, 'élément': 'air', 'polarité': 'positive'},
    'ᚱ': {'nom': 'Raidho', 'effet_base': 'voyage/mouvement', 'danger': 2, 'élément': 'air', 'polarité': 'neutre'},
    'ᚲ': {'nom': 'Kenaz', 'effet_base': 'connaissance/révélation', 'danger': 2, 'élément': 'feu', 'polarité': 'positive'},
    'ᚷ': {'nom': 'Gebo', 'effet_base': 'don/échange', 'danger': 1, 'élément': 'air', 'polarité': 'positive'},
    'ᚺ': {'nom': 'Hagalaz', 'effet_base': 'chaos/grêle', 'danger': 4, 'élément': 'glace', 'polarité': 'négative'},
    'ᚾ': {'nom': 'Nauthiz', 'effet_base': 'nécessité/contrainte', 'danger': 3, 'élément': 'glace', 'polarité': 'négative'},
    'ᛁ': {'nom': 'Isa', 'effet_base': 'glace/stase', 'danger': 3, 'élément': 'glace', 'polarité': 'neutre'},
    'ᛃ': {'nom': 'Jera', 'effet_base': 'cycle/récolte', 'danger': 1, 'élément': 'terre', 'polarité': 'positive'},
    'ᛇ': {'nom': 'Eihwaz', 'effet_base': 'if/Yggdrasil', 'danger': 4, 'élément': 'terre', 'polarité': 'neutre'},
    'ᛈ': {'nom': 'Perthro', 'effet_base': 'destin/mystère', 'danger': 5, 'élément': 'void', 'polarité': 'mystique'},
    'ᛉ': {'nom': 'Algiz', 'effet_base': 'protection', 'danger': 2, 'élément': 'air', 'polarité': 'positive'},
    'ᛊ': {'nom': 'Sowilo', 'effet_base': 'soleil/victoire', 'danger': 2, 'élément': 'feu', 'polarité': 'positive'},
    'ᛏ': {'nom': 'Tiwaz', 'effet_base': 'justice/sacrifice', 'danger': 3, 'élément': 'feu', 'polarité': 'neutre'},
    'ᛒ': {'nom': 'Berkano', 'effet_base': 'naissance/croissance', 'danger': 2, 'élément': 'terre', 'polarité': 'positive'},
    'ᛗ': {'nom': 'Mannaz', 'effet_base': 'humanité/identité', 'danger': 3, 'élément': 'air', 'polarité': 'neutre'},
    'ᛚ': {'nom': 'Laguz', 'effet_base': 'eau/mémoire', 'danger': 3, 'élément': 'eau', 'polarité': 'neutre'},
    'ᛜ': {'nom': 'Ingwaz', 'effet_base': 'fertilité/potentiel', 'danger': 4, 'élément': 'terre', 'polarité': 'positive'},
    'ᛞ': {'nom': 'Dagaz', 'effet_base': 'aube/transformation', 'danger': 4, 'élément': 'lumière', 'polarité': 'positive'},
    'ᛟ': {'nom': 'Othala', 'effet_base': 'héritage/ancêtres', 'danger': 5, 'élément': 'terre', 'polarité': 'mystique'}
}

LIEUX_EXTENDED = {
    'caen': {'pouvoir': 4, 'description': 'Nexus de mémoire fracturée', 'type': 'mémétique', 'flux': 'chaotique'},
    'herouville': {'pouvoir': 2, 'description': 'Zone périphérique', 'type': 'mémoire', 'flux': 'modéré'},
    'ganil': {'pouvoir': 5, 'description': 'Réacteur de conscience', 'type': 'scientifique', 'flux': 'anormal'},
    'paris': {'pouvoir': 3, 'description': 'Cœur administratif', 'type': 'urbain', 'flux': 'élevé'},
    'darkweb': {'pouvoir': 4, 'description': 'Ombre du réseau', 'type': 'digital', 'flux': 'élevé'},
    'ocean': {'pouvoir': 5, 'description': 'Abîme liquide', 'type': 'naturel', 'flux': 'extrême'},
    'passé': {'pouvoir': 5, 'description': 'Strates révolues', 'type': 'temporel', 'flux': 'nul'},
    'futur': {'pouvoir': 5, 'description': 'Potentiels non-réalisés', 'type': 'temporel', 'flux': 'infini'},
}

EFFETS_EXTENDED = [
    'révélation mémoire', 'glissement temporel', 'fusion souvenirs', 'invocation entité',
    'communion Programme', 'interface rêve', 'corruption fichier', 'mémétique virale',
    'projection émotionnelle', 'scellement dimension', 'réveil dormant'
]

MODIFICATEURS = {
    'amplificateurs': ['×2', '×3', 'MAX', 'BOOST'],
    'inverseurs': ['¬', '~', 'REV'],
    'stabilisateurs': ['LOCK', 'FIX', '◈'],
    'temporels': ['DELAY', 'INSTANT', 'PERSIST']
}

# ✅ TEMPLATES CORRECTS (issus du CLI, SANS doubles accolades)
TEMPLATES_ADVANCED = {
    "templates": [
        {"nom": "Classique", "structure": "Ω<{rune}>v{version} @ {lieu} — {effet} •••", "complexité": 1},
        {"nom": "Multi-Runes", "structure": "{rune1}+{rune2} @ {lieu} :: v{version} :: {effet}", "complexité": 3, "multi_rune": True},
        {"nom": "Chaîne Temporelle", "structure": "{rune}[t={temps}] → {lieu} → {effet} → v{version}", "complexité": 2, "temporal": True},
        {"nom": "Modificateur Complexe", "structure": "{mod1}[{rune}]{mod2} :: {lieu} :: {effet} :: v{version}", "complexité": 2, "with_mods": True},
    ]
}

# === CLASSE CLI CORRIGÉE ===
class FracturoCLI:
    def __init__(self, args=None, lexicon_path=None):
        self.history = []
        self.lexicon = None
        self.args = args
        self.lexicon_ratio = getattr(args, 'lexicon_ratio', 0.3) if args else 0.3
        if lexicon_path:
            self.load_lexicon(lexicon_path)
        if args and hasattr(args, 'seed') and args.seed is not None:
            random.seed(args.seed)

    def load_lexicon(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.lexicon = data.get('entries', [])
        except Exception as e:
            print(f"⚠️ Erreur chargement lexique : {e}")

    def inject_lexicon(self, params):
        if not self.lexicon:
            return params
        new_params = copy.deepcopy(params)
        if 'effet' in new_params and random.random() < self.lexicon_ratio:
            entry = random.choice(self.lexicon)
            if 'effet_mnémétique' in entry:
                new_params['effet'] = entry['effet_mnémétique']
        if 'lieu' in new_params and random.random() < self.lexicon_ratio:
            entry = random.choice(self.lexicon)
            if 'paleo_glyphe' in entry:
                lieu_alt = entry['paleo_glyphe'].replace(' ', '_')
                new_params['lieu'] = lieu_alt
        if 'rune' in new_params and random.random() < self.lexicon_ratio:
            entry = random.choice(self.lexicon)
            if 'glyph' in entry and entry['glyph'] in RUNES_FUTHARK:
                new_params['rune'] = entry['glyph']
        return new_params

    def generate(self, params=None):
        template_index = 0
        if params and 'template_index' in params:
            template_index = params['template_index']
        template = TEMPLATES_ADVANCED["templates"][template_index]

        base_params = {}
        if params is None:
            base_params.update({
                'rune': random.choice(list(RUNES_FUTHARK.keys())),
                'lieu': random.choice(list(LIEUX_EXTENDED.keys())),
                'effet': random.choice(EFFETS_EXTENDED),
                'version': random.randint(1, 13)
            })
        else:
            base_params.update({
                'rune': params.get('rune', random.choice(list(RUNES_FUTHARK.keys()))),
                'lieu': params.get('lieu', random.choice(list(LIEUX_EXTENDED.keys()))),
                'effet': params.get('effet', random.choice(EFFETS_EXTENDED)),
                'version': params.get('version', random.randint(1, 13))
            })

        if template.get('multi_rune'):
            base_params['rune1'] = params.get('rune1', random.choice(list(RUNES_FUTHARK.keys())))
            base_params['rune2'] = params.get('rune2', random.choice(list(RUNES_FUTHARK.keys())))
        if template.get('temporal'):
            base_params['temps'] = params.get('temps', f"{random.randint(1, 72)}h")
        if template.get('with_mods'):
            base_params['mod1'] = params.get('mod1', random.choice(MODIFICATEURS['amplificateurs']))
            base_params['mod2'] = params.get('mod2', random.choice(MODIFICATEURS['temporels']))

        enriched_params = self.inject_lexicon(base_params)

        try:
            code_str = template["structure"].format(**enriched_params)  # ✅ Syntaxe CORRECTE
        except KeyError as e:
            missing = str(e).strip("'")
            enriched_params[missing] = "?"
            code_str = template["structure"].format(**enriched_params)

        danger = self.calculate_danger(enriched_params, template)
        result = {
            'code': code_str,
            'hash': hashlib.sha256(code_str.encode()).hexdigest()[:10],
            'params': enriched_params,
            'template': template['nom'],
            'timestamp': datetime.now().isoformat(),
            'danger': danger
        }
        self.history.append(result)
        return result

    def calculate_danger(self, params, template):
        d = RUNES_FUTHARK.get(params.get('rune'), {}).get('danger', 1)
        d += LIEUX_EXTENDED.get(params.get('lieu'), {}).get('pouvoir', 1)
        d *= params.get('version', 1)
        d += template.get('complexité', 1) * 2
        return min(d, 100)

    def to_grok_prompt(self, code_obj):
        params = code_obj['params']
        lieu = params.get('lieu', 'inconnu')
        seed = code_obj['code']
        if lieu == 'caen':
            desc = "a fractured cathedral in Caen, 2075. Cracks in the stone glow with ancient runes."
        else:
            desc = f"a symbolic landscape representing '{params.get('effet', '')}' in {lieu}."
        return (
            f"FracturoScript seed: {seed}\n"
            f"Generate hyper-detailed image of {desc}. "
            f"Subliminal runic graffiti: \"{seed}\". "
            f"Style: fractal-normandy, temporal anomaly 2025/2075, monochrome with paleo-red accents."
        )

# === MOTEUR GUI ===
class GénérateurMétapoétique:
    def __init__(self):
        self.runes = RUNES_GUI
    def générer_intentionnel(self):
        rune = random.choice(self.runes)
        return f"Ω{rune.symbole}v{random.randint(1,13)}•[comme si le Programme rêvait]•—•réveiller une mémoire fossile•••"

# === INTERFACE PRINCIPALE ===
class FracturoForgeGUI:
    def __init__(self, root, cli_engine=None):
        self.root = root
        self.root.title("🌀 FRACTUROFORGE v∞ — v3.3 CORRIGÉ")
        self.root.geometry("1300x950")
        self.cli = cli_engine or FracturoCLI()
        self.setup_styles()
        self.build_interface()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        bg_color = "#0a0a0f"
        fg_color = "#e0e0ff"
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        self.root.configure(bg=bg_color)

    def build_interface(self):
        main = ttk.Frame(self.root, padding="20")
        main.pack(fill="both", expand=True)

        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True)

        # MÉTAPOÉTIQUE
        tab_m = ttk.Frame(notebook)
        notebook.add(tab_m, text="MÉTAPOÉTIQUE")
        self.build_meta_tab(tab_m)

        # RUNESMITH LAB ✅
        tab_rs = ttk.Frame(notebook)
        notebook.add(tab_rs, text="RuneSmith Lab")
        self.build_runesmith_tab(tab_rs)

        # LEXIQUE
        tab_lex = ttk.Frame(notebook)
        notebook.add(tab_lex, text="Paleo-Lexique")
        self.build_lexicon_tab(tab_lex)

        # GROK
        tab_g = ttk.Frame(notebook)
        notebook.add(tab_g, text="Grok & Historique")
        self.build_grok_tab(tab_g)

    def build_meta_tab(self, parent):
        ttk.Button(parent, text="⚡ Générer Invocation", command=self.gen_gui).pack(pady=10)
        self.text_gui = scrolledtext.ScrolledText(parent, bg="#001020", fg="#00ffcc", font=("Consolas", 12))
        self.text_gui.pack(fill="both", expand=True, pady=10)

    def gen_gui(self):
        gen = GénérateurMétapoétique()
        invoc = gen.générer_intentionnel()
        self.text_gui.delete("1.0", "end")
        self.text_gui.insert("1.0", invoc)

    def build_runesmith_tab(self, parent):
        ctrl = ttk.Frame(parent, padding="15")
        ctrl.pack(fill="x", pady=(0,15))

        self.rs_rune_var = tk.StringVar(value='ᚠ')
        self.rs_lieu_var = tk.StringVar(value='caen')
        self.rs_effet_var = tk.StringVar(value=EFFETS_EXTENDED[0])
        self.rs_version_var = tk.IntVar(value=7)
        self.rs_template_var = tk.StringVar(value="Classique")

        ttk.Label(ctrl, text="Rune:").grid(row=0, column=0, sticky="w")
        rune_combo = ttk.Combobox(ctrl, textvariable=self.rs_rune_var, values=list(RUNES_FUTHARK.keys()), state="readonly", width=5)
        rune_combo.grid(row=0, column=1)

        ttk.Label(ctrl, text="Lieu:").grid(row=0, column=2, sticky="w", padx=(20,5))
        lieu_combo = ttk.Combobox(ctrl, textvariable=self.rs_lieu_var, values=list(LIEUX_EXTENDED.keys()), state="readonly", width=12)
        lieu_combo.grid(row=0, column=3)

        ttk.Label(ctrl, text="Effet:").grid(row=0, column=4, sticky="w", padx=(20,5))
        effet_combo = ttk.Combobox(ctrl, textvariable=self.rs_effet_var, values=EFFETS_EXTENDED, state="readonly", width=25)
        effet_combo.grid(row=0, column=5)

        ttk.Label(ctrl, text="Version:").grid(row=1, column=0, sticky="w", pady=(10,0))
        vers_spin = tk.Spinbox(ctrl, from_=1, to=13, textvariable=self.rs_version_var, width=5)
        vers_spin.grid(row=1, column=1, pady=(10,0))

        ttk.Label(ctrl, text="Template:").grid(row=1, column=2, sticky="w", pady=(10,0), padx=(20,5))
        template_names = [t['nom'] for t in TEMPLATES_ADVANCED["templates"]]
        template_combo = ttk.Combobox(ctrl, textvariable=self.rs_template_var, values=template_names, state="readonly", width=20)
        template_combo.grid(row=1, column=3, pady=(10,0))

        btns = ttk.Frame(parent)
        btns.pack(fill="x", pady=10)
        ttk.Button(btns, text="Forge", command=self.forge_rs).pack(side="left", padx=5)
        ttk.Button(btns, text="Danger", command=self.update_danger).pack(side="right", padx=5)

        self.danger_label = ttk.Label(parent, text="Danger: --", foreground="#ff9900")
        self.danger_label.pack(anchor="w", padx=20)

        self.text_rs = scrolledtext.ScrolledText(parent, bg="#001020", fg="#00ffcc", font=("Consolas", 12))
        self.text_rs.pack(fill="both", expand=True, pady=10)

    def get_rs_params(self):
        template_name = self.rs_template_var.get()
        template_names = [t['nom'] for t in TEMPLATES_ADVANCED["templates"]]
        try:
            template_index = template_names.index(template_name)
        except ValueError:
            template_index = 0
        return {
            'rune': self.rs_rune_var.get(),
            'lieu': self.rs_lieu_var.get(),
            'effet': self.rs_effet_var.get(),
            'version': self.rs_version_var.get(),
            'template_index': template_index
        }

    def forge_rs(self):
        code = self.cli.generate(self.get_rs_params())
        self.text_rs.delete("1.0", "end")
        self.text_rs.insert("1.0", code['code'])
        self.current_code = code
        self.update_danger()

    def update_danger(self):
        if hasattr(self, 'current_code'):
            d = self.current_code['danger']
            color = "#00ff00" if d < 30 else "#ffff00" if d < 70 else "#ff3300"
            self.danger_label.configure(text=f"Danger: {d}/100", foreground=color)

    def build_lexicon_tab(self, parent):
        load_frame = ttk.Frame(parent, padding="15")
        load_frame.pack(fill="x", pady=(0,15))
        self.lex_path_var = tk.StringVar()
        ttk.Entry(load_frame, textvariable=self.lex_path_var, width=50).pack(side="left", padx=(0,10))
        ttk.Button(load_frame, text="📂 Charger paleo_mnemos_lexicon.json", command=self.load_lexicon).pack(side="left")

        self.lex_text = scrolledtext.ScrolledText(parent, bg="#050510", fg="#88ff88", font=("Consolas", 10))
        self.lex_text.pack(fill="both", expand=True, pady=10)

    def load_lexicon(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            self.lex_path_var.set(path)
            self.cli.load_lexicon(path)
            if self.cli.lexicon:
                self.lex_text.delete("1.0", "end")
                self.lex_text.insert("1.0", f"Chargé : {len(self.cli.lexicon)} entrées\n\n")
                for i, e in enumerate(self.cli.lexicon[:10]):
                    self.lex_text.insert("end", f"[{i}] {e.get('nom', '?')}: {e.get('effet_mnémétique', '?')}\n")

    def build_grok_tab(self, parent):
        ttk.Button(parent, text="🌌 Générer Prompt Grok", command=self.gen_grok).pack(pady=10)
        self.text_grok = scrolledtext.ScrolledText(parent, bg="#001020", fg="#ff66ff", font=("Consolas", 11))
        self.text_grok.pack(fill="both", expand=True, pady=10)

        ttk.Label(parent, text="Historique").pack(pady=(20,5))
        self.text_hist = scrolledtext.ScrolledText(parent, bg="#050510", fg="#8888ff", font=("Consolas", 9), height=6)
        self.text_hist.pack(fill="x", pady=10)

    def gen_grok(self):
        if not hasattr(self, 'current_code'):
            messagebox.showwarning("⚠️", "Générez d’abord un code")
            return
        prompt = self.cli.to_grok_prompt(self.current_code)
        self.text_grok.delete("1.0", "end")
        self.text_grok.insert("1.0", prompt)
        self.text_hist.insert("end", f"[{self.current_code['hash']}] {self.current_code['code'][:60]}...\n")
        self.text_hist.see("end")

# === CLI MODE ===
def run_cli_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', action='store_true')
    parser.add_argument('--template', type=int, default=0)
    parser.add_argument('--rune', choices=list(RUNES_FUTHARK.keys()))
    parser.add_argument('--lieu', choices=list(LIEUX_EXTENDED.keys()))
    parser.add_argument('--effet')
    parser.add_argument('--version', type=int, choices=range(1,14))
    parser.add_argument('--to-grok', action='store_true')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--load-lexicon')
    parser.add_argument('--lexicon-ratio', type=float, default=0.3)
    args = parser.parse_args(sys.argv[1:])
    cli = FracturoCLI(args=args, lexicon_path=args.load_lexicon)
    code = cli.generate()
    if args.to_grok:
        print(cli.to_grok_prompt(code))
    else:
        print(f"FracturoScript: {code['code']}\nDanger: {code['danger']}/100")

# === POINT D’ENTRÉE ===
if __name__ == "__main__":
    if len(sys.argv) > 1 and '--cli' in sys.argv:
        run_cli_mode()
    else:
        root = tk.Tk()
        app = FracturoForgeGUI(root)
        root.mainloop()
