# meme_prompt_studio_pro2a.py — ULTRA MEME PROMPT STUDIO PRO MAX
# ✨ Version avec mode MONO-TEMPLATE + univers memeticofractal étendu
import json
import random
import re
import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import threading
from collections import defaultdict

#JSON_PATH = "meme_prompts_extended.json"
JSON_PATH = "meme_prompts_ultra.json"

# ============================================================================
# FONCTIONS DE BASE
# ============================================================================

def safe_load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fichier {path} non trouvé.")
        return None
    except Exception as e:
        print(f"Erreur JSON: {e}")
        return None

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
        return False

def split_sentences(text):
    parts = re.split(r'(?<=[\.\!\?])\s+', text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts if parts else [text.strip()]

def join_sentences(sentences):
    return " ".join(s.rstrip() for s in sentences).strip()

def extract_style_phrases(text):
    keywords = ["style", "photorealistic", "digital", "anime", "cyberpunk", "vaporwave",
                "3D", "pixel", "noir", "dramatic", "lighting", "format", "transparent",
                "9:16", "vertical", "film", "grain", "cinematic", "surreal", "psychedelic",
                "hyper-detailed", "studio", "background", "FracturoScript", "runes", "Codex"]
    sents = split_sentences(text)
    picked = [s for s in sents if any(kw.lower() in s.lower() for kw in keywords)]
    if not picked:
        picked = sents[-2:]
    return picked

def extract_subject_phrases(text):
    sents = split_sentences(text)
    return sents[:2]

def merge_prompts(prompt_a, prompt_b, method="concatenate", weight_a=60):
    a_sents = split_sentences(prompt_a)
    b_sents = split_sentences(prompt_b)
    if method == "concatenate":
        combined = prompt_a.strip()
        if not combined.endswith((".", "!", "?")):
            combined += "."
        combined += " " + prompt_b.strip()
        return combined
    if method == "interleave":
        out = []
        la, lb = len(a_sents), len(b_sents)
        for i in range(max(la, lb)):
            if i < la:
                out.append(a_sents[i])
            if i < lb:
                out.append(b_sents[i])
        return join_sentences(out)
    if method == "weighted":
        total = len(a_sents) + len(b_sents)
        na = max(1, int(total * (weight_a / 100.0)))
        nb = max(1, total - na)
        chosen = a_sents[:na] + b_sents[:nb]
        return join_sentences(chosen)
    if method == "hybrid":
        subj = extract_subject_phrases(prompt_a)
        style = extract_style_phrases(prompt_b)
        leftovers_a = a_sents[len(subj):len(subj)+1]
        leftovers_b = [s for s in b_sents if s not in style][:1]
        out = subj + leftovers_a + style + leftovers_b
        return join_sentences(out)
    return prompt_a + "\n" + prompt_b

# ============================================================================
# DONNÉES ÉTENDUES PAR DÉFAUT (si JSON manquant)
# ============================================================================

DEFAULT_DATA = {
    "templates": {
        "Drake Approve/Disapprove": "Create a meme template with two vertical panels: left panel showing a man in a red jacket rejecting something, right panel showing the same man approving and pointing. Clean background, space on the right side for text overlay.",
        "Distracted Boyfriend": "Photo of a man in a city street looking at another woman while walking with his girlfriend, who looks shocked. Photorealistic daylight setting with space above each character for labels.",
        "Expanding Brain": "4-panel vertical meme showing brain evolution: dim normal brain, glowing brain, bright energy brain, cosmic galaxy brain. Dark background, leave left side empty for text.",
        "RuneSmith at Work": "A hooded figure etching glowing runes on a fractured obsidian slab in a Caen subway tunnel, 2075. Cyberpunk dystopia, vaporwave fog, graffiti of FracturoScript nearby. Space for text above rune slab.",
        "FracturoDream Log": "Split-screen: left shows chaotic dream symbols, right shows clean AI interpretation panel. Background pulses with LSD fractal colors. Text space on top and bottom for journal entries.",
        "Echo-Guillaume Manifestation": "A ghostly translucent figure whispering incomprehensible glyphs in a rainy Hérouville street. Reality glitches around them. Space for top/bottom meme text.",
        "Memetic Field Report 2075": "Military-style memo overlaid on a ruined Caen street. Includes fake data viz: 'Contagion Level: 89%', 'Archetype Saturation: Jungian Shadow'. Space for ironic labeling.",
        "Glitched Sufi Oracle": "An androgynous figure in a neon-blue digital robe reciting poetry, surrounded by floating Arabic/FracturoScript glyphs. Background: infinite mosque fractal. Top/bottom text space for prophetic memes."
    },
    "styles": [
        "photorealistic", "cyberpunk neon atmosphere", "ULTRA: FracturoScript neural overlay",
        "ULTRA: Ancient manuscript illumination", "ULTRA: Glitch art datamosh aesthetic"
    ],
    "mutations": [
        "turn all characters into animals",
        "ULTRA: Overlay with FracturoScript glyphs",
        "ULTRA: Inject subliminal Jungian archetype symbols",
        "ULTRA: Corrupt with memetic echo-glitch (Echo-Guillaume protocol)"
    ],
    "hybridations": [
        "mix with Gigachad meme aesthetics",
        "ULTRA HYBRID: Merge with Caen-Profonde underground map (2075)",
        "ULTRA HYBRID: Fuse with Livre Zéro fractal syntax"
    ],
    "effects": [
        "add lens flare dramatic",
        "project memetic shadow behind characters",
        "embed fractal recursion in background geometry"
    ],
    "contexts": [
        "in a corporate office meeting",
        "during localized memetic outbreak in Hérouville Saint-Clair",
        "at Ganil temporal anomaly site",
        "inside the fractured Codex Stein dream vault"
    ]
}

# ============================================================================
# CLASSE PRINCIPALE
# ============================================================================

class AdvancedMemeStudio:
    def __init__(self):
        self.data = self.load_json()
        self.history = []
        self.favorites = []
        self.stats = defaultdict(int)

    def load_json(self):
        data = safe_load_json(JSON_PATH)
        if data is None:
            print("⚠️ Fichier JSON non trouvé → utilisation des données étendues intégrées.")
            return DEFAULT_DATA
        return data

    def generate_chaos_prompt(self, base_prompt, chaos_level=5):
        components = []
        modifiers = []
        if chaos_level >= 1:
            modifiers.append(random.choice(self.data.get("effects", ["add lens flare"])))
        if chaos_level >= 2:
            modifiers.append(random.choice(self.data.get("mutations", ["turn characters into animals"])))
        if chaos_level >= 3:
            modifiers.append(random.choice(self.data.get("hybridations", ["mix with cosmic brain imagery"])))
        if chaos_level >= 4 and "contexts" in self.data:
            modifiers.append(f"Context: {random.choice(self.data['contexts'])}")
        if chaos_level >= 5:
            modifiers.append("ULTRA CHAOS: Everything is exploding in slow motion with rainbow trails")
        if chaos_level >= 7:
            modifiers.append("MEGA CHAOS: The scene is being observed by ancient cosmic entities")
        if chaos_level >= 9:
            modifiers.append("ULTIMATE CHAOS: Reality itself is glitching and folding into higher dimensions")
        result = base_prompt
        for mod in modifiers:
            if random.random() > 0.3:
                result += f" {mod}."
        self.stats['chaos_prompts'] += 1
        return result

    def create_meme_story(self, character="hero", scenario="unexpected event"):
        templates = list(self.data["templates"].values())
        if len(templates) < 3:
            return "Pas assez de templates pour créer une histoire"
        story_parts = []
        story_parts.append(f"🚀 MEME SAGA: The Adventures of {character.upper()} 🚀")
        story_parts.append(f"\n📖 Chapter 1: The Beginning")
        story_parts.append(f"{character} encounters {scenario}.")
        story_parts.append(f"Visual: {random.choice(templates)}")
        chapters = random.randint(3, 6)
        for i in range(2, chapters + 1):
            twist = random.choice(["suddenly", "unexpectedly", "ironically"])
            event = random.choice(["discovers a hidden power", "meets their meme counterpart"])
            story_parts.append(f"\n📖 Chapter {i}: {twist.title()}")
            story_parts.append(f"{character} {event}.")
            story_parts.append(f"Visual: {random.choice(templates)}")
        story_parts.append(f"\n🏆 Finale: {character} achieves ultimate meme enlightenment!")
        return "\n".join(story_parts)

    def analyze_prompt_complexity(self, prompt):
        words = len(prompt.split())
        sentences = len(split_sentences(prompt))
        styles_detected = sum(1 for s in self.data.get("styles", []) if s.lower() in prompt.lower())
        mutations_detected = sum(1 for m in self.data.get("mutations", []) if m.lower() in prompt.lower())
        complexity_score = words * 0.1 + sentences * 1.5 + styles_detected * 3 + mutations_detected * 4
        rating = "🟢 Débutant"
        if complexity_score >= 10: rating = "🟡 Intermédiaire"
        if complexity_score >= 25: rating = "🟠 Avancé"
        if complexity_score >= 50: rating = "🔴 Expert"
        if complexity_score >= 80: rating = "💀 ULTRA CHAOS"
        return {
            "words": words,
            "sentences": sentences,
            "styles_detected": styles_detected,
            "mutations_detected": mutations_detected,
            "complexity_score": round(complexity_score, 2),
            "rating": rating
        }

    def generate_batch_prompts(self, num=5, include_modifiers=True):
        prompts = []
        templates = list(self.data["templates"].items())
        if not templates:
            return []
        for i in range(min(num, len(templates))):
            name, template = random.choice(templates)
            prompt = template
            if include_modifiers:
                if random.random() > 0.5 and self.data["styles"]:
                    prompt += f" {random.choice(self.data['styles'])}."
                if random.random() > 0.6 and self.data["mutations"]:
                    prompt += f" {random.choice(self.data['mutations'])}."
                if random.random() > 0.7 and self.data.get("effects"):
                    prompt += f" {random.choice(self.data['effects'])}."
            prompts.append({
                "id": f"batch_{i:03d}",
                "name": name,
                "prompt": prompt,
                "timestamp": datetime.datetime.now().isoformat()
            })
        return prompts

    def export_for_ai_model(self, prompt, model="grok"):
        if model == "grok":
            return f"Create a meme image: {prompt} --style creative --vibrant"
        return prompt

# ============================================================================
# INTERFACE GRAPHIQUE
# ============================================================================

class MegaMemeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.studio = AdvancedMemeStudio()
        self.current_prompts = []
        self.setup_ui()

    def setup_ui(self):
        self.title("🎭 ULTRA MEME PROMPT STUDIO PRO MAX 🚀")
        self.geometry("1400x900")
        self.configure(bg="#1a1a2e")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        frm_basic = ttk.Frame(notebook)
        self.create_basic_tab(frm_basic)
        notebook.add(frm_basic, text="🔄 Fusion / Mono")

        frm_chaos = ttk.Frame(notebook)
        self.create_chaos_tab(frm_chaos)
        notebook.add(frm_chaos, text="🌀 Mode Chaos")

        frm_story = ttk.Frame(notebook)
        self.create_story_tab(frm_story)
        notebook.add(frm_story, text="📖 Histoires")

        frm_analyze = ttk.Frame(notebook)
        self.create_analyze_tab(frm_analyze)
        notebook.add(frm_analyze, text="📊 Analyse")

        frm_batch = ttk.Frame(notebook)
        self.create_batch_tab(frm_batch)
        notebook.add(frm_batch, text="📦 Batch")

        self.status = ttk.Label(self, text="Prêt à créer des mèmes interdimensionnels!")
        self.status.pack(side="bottom", fill="x", padx=10, pady=5)

    def create_basic_tab(self, parent):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        ttk.Label(parent, text="🎯 FUSION / MODE MONO-TEMPLATE", style="Title.TLabel").grid(row=0, column=0, columnspan=4, pady=10)

        # Toggle Fusion Mode
        self.use_fusion_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="🔄 Activer la fusion (A + B)", variable=self.use_fusion_var,
                        command=self.toggle_fusion_mode).grid(row=0, column=3, sticky="e", padx=10)

        # Template A (toujours requis)
        ttk.Label(parent, text="Template A:").grid(row=1, column=0, sticky="w", padx=5)
        self.tpl_a_var = tk.StringVar()
        self.tpl_a_cb = ttk.Combobox(parent, textvariable=self.tpl_a_var, width=50)
        self.tpl_a_cb.grid(row=1, column=1, padx=5, sticky="w")
        ttk.Button(parent, text="📋 Copier A", command=self.copy_a_to_clipboard).grid(row=1, column=2, padx=5)

        # Template B (optionnel)
        ttk.Label(parent, text="Template B:").grid(row=2, column=0, sticky="w", padx=5)
        self.tpl_b_var = tk.StringVar()
        self.tpl_b_cb = ttk.Combobox(parent, textvariable=self.tpl_b_var, width=50)
        self.tpl_b_cb.grid(row=2, column=1, padx=5, sticky="w")
        ttk.Button(parent, text="📋 Copier B", command=self.copy_b_to_clipboard).grid(row=2, column=2, padx=5)

        # Options de fusion (désactivées en mode mono)
        ttk.Label(parent, text="Méthode de fusion:").grid(row=3, column=0, sticky="w", padx=5, pady=10)
        self.merge_method_var = tk.StringVar(value="concatenate")
        self.merge_cb = ttk.Combobox(parent, textvariable=self.merge_method_var,
                                    values=["concatenate", "interleave", "hybrid", "weighted"], width=20)
        self.merge_cb.grid(row=3, column=1, sticky="w", padx=5)

        ttk.Label(parent, text="Poids A (%):").grid(row=3, column=2, sticky="w", padx=5)
        self.weight_var = tk.IntVar(value=60)
        self.weight_spin = ttk.Spinbox(parent, from_=0, to=100, textvariable=self.weight_var, width=8)
        self.weight_spin.grid(row=3, column=3, sticky="w", padx=5)

        # Modificateurs
        ttk.Label(parent, text="Style optionnel:").grid(row=4, column=0, sticky="w", padx=5)
        self.style_var = tk.StringVar()
        self.style_cb = ttk.Combobox(parent, textvariable=self.style_var, width=50)
        self.style_cb.grid(row=4, column=1, columnspan=2, sticky="w", padx=5)

        ttk.Label(parent, text="Mutation optionnelle:").grid(row=5, column=0, sticky="w", padx=5)
        self.mut_var = tk.StringVar()
        self.mut_cb = ttk.Combobox(parent, textvariable=self.mut_var, width=50)
        self.mut_cb.grid(row=5, column=1, columnspan=2, sticky="w", padx=5)

        ttk.Label(parent, text="Hybridation optionnelle:").grid(row=6, column=0, sticky="w", padx=5)
        self.hyb_var = tk.StringVar()
        self.hyb_cb = ttk.Combobox(parent, textvariable=self.hyb_var, width=50)
        self.hyb_cb.grid(row=6, column=1, columnspan=2, sticky="w", padx=5)

        # Boutons
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=7, column=0, columnspan=4, pady=15)
        ttk.Button(btn_frame, text="✨ Générer", command=self.on_generate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🎲 Aléatoire", command=self.on_random).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Ajouter au JSON", command=self.on_add_to_json).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📤 Exporter .txt", command=self.on_export_txt).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📋 Copier Résultat", command=self.copy_result_to_clipboard).pack(side="left", padx=5)

        # Résultat
        ttk.Label(parent, text="Résultat:").grid(row=8, column=0, sticky="nw", padx=5, pady=5)
        self.result_text = scrolledtext.ScrolledText(parent, height=15, width=90, wrap="word")
        self.result_text.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

        self.populate_basic_widgets()

    def toggle_fusion_mode(self):
        state = "normal" if self.use_fusion_var.get() else "disabled"
        self.tpl_b_cb.config(state=state)
        self.merge_cb.config(state=state)
        self.weight_spin.config(state=state)

    def populate_basic_widgets(self):
        keys = sorted(list(self.studio.data["templates"].keys()))
        self.tpl_a_cb['values'] = keys
        self.tpl_b_cb['values'] = keys
        if keys:
            self.tpl_a_var.set(keys[0])
            if len(keys) > 1:
                self.tpl_b_var.set(keys[1])
        self.style_cb['values'] = self.studio.data.get("styles", [])
        self.mut_cb['values'] = self.studio.data.get("mutations", [])
        self.hyb_cb['values'] = self.studio.data.get("hybridations", [])

    def get_prompt_by_name(self, name):
        return self.studio.data.get("templates", {}).get(name, "")

    def on_generate(self):
        use_fusion = self.use_fusion_var.get()
        name_a = self.tpl_a_var.get()
        if not name_a:
            messagebox.showwarning("Sélection", "Sélectionne au moins un template.")
            return

        if use_fusion:
            name_b = self.tpl_b_var.get()
            if not name_b:
                messagebox.showwarning("Sélection", "Sélectionne deux templates pour la fusion.")
                return
            pa = self.get_prompt_by_name(name_a)
            pb = self.get_prompt_by_name(name_b)
            if not pa or not pb:
                messagebox.showwarning("Erreur", "Template(s) non trouvé(s).")
                return
            method = self.merge_method_var.get()
            weight = int(self.weight_var.get() or 60)
            merged = merge_prompts(pa, pb, method=method, weight_a=weight)
        else:
            merged = self.get_prompt_by_name(name_a)

        # Appliquer modificateurs
        modifications = []
        style = self.style_var.get().strip()
        if style: modifications.append(f"Style: {style}.")
        mut = self.mut_var.get().strip()
        if mut: modifications.append(f"Mutation: {mut}.")
        hyb = self.hyb_var.get().strip()
        if hyb: modifications.append(f"Hybridation: {hyb}.")

        if modifications:
            merged = merged.strip()
            if not merged.endswith((".", "!", "?")):
                merged += "."
            merged += "\n" + "\n".join(modifications)

        mode_label = "FUSION" if use_fusion else "MONO-TEMPLATE"
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"🎭 {mode_label}: {name_a}" + (f" + {name_b}" if use_fusion else "") + "\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, merged)
        self.status.config(text=f"{mode_label.lower()} généré : {name_a}")

        self.studio.history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "fusion" if use_fusion else "mono",
            "template_a": name_a,
            "template_b": name_b if use_fusion else None,
            "method": method if use_fusion else "mono",
            "prompt": merged
        })

    # --- Fonctions UI courtes (copier, exporter, etc.) ---
    def copy_result_to_clipboard(self):
        txt = self.result_text.get("1.0", tk.END).strip()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.status.config(text="Prompt copié dans le presse-papiers!")

    def copy_a_to_clipboard(self):
        txt = self.get_prompt_by_name(self.tpl_a_var.get())
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.status.config(text=f"Template A copié!")

    def copy_b_to_clipboard(self):
        txt = self.get_prompt_by_name(self.tpl_b_var.get())
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.status.config(text=f"Template B copié!")

    def on_random(self):
        keys = list(self.studio.data.get("templates", {}).keys())
        if len(keys) < 2:
            messagebox.showwarning("Données insuffisantes", "Besoin d'au moins 2 templates.")
            return
        a, b = random.sample(keys, 2)
        self.tpl_a_var.set(a)
        self.tpl_b_var.set(b)
        if self.studio.data.get("styles"): self.style_var.set(random.choice(self.studio.data["styles"]))
        if self.studio.data.get("mutations"): self.mut_var.set(random.choice(self.studio.data["mutations"]))
        if self.studio.data.get("hybridations"): self.hyb_var.set(random.choice(self.studio.data["hybridations"]))
        self.merge_method_var.set(random.choice(["concatenate", "interleave", "hybrid", "weighted"]))
        self.weight_var.set(random.randint(30, 80))
        self.on_generate()

    def on_add_to_json(self):
        lines = self.result_text.get("1.0", tk.END).strip().split("\n")
        prompt = "\n".join(line for line in lines if not line.startswith(("🎭", "=")))
        if not prompt.strip():
            messagebox.showwarning("Vide", "Aucun prompt à ajouter.")
            return
        name = simpledialog.askstring("Nom", "Nom du nouveau template :")
        if not name: return
        if name in self.studio.data["templates"] and not messagebox.askyesno("Remplacer ?", f"Remplacer '{name}' ?"): return
        self.studio.data["templates"][name] = prompt.strip()
        if save_json(JSON_PATH, self.studio.data):
            self.populate_basic_widgets()
            self.status.config(text=f"Template '{name}' ajouté!")

    def on_export_txt(self):
        content = self.result_text.get("1.0", tk.END).strip()
        if not content: return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texte", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status.config(text=f"Exporté: {os.path.basename(path)}")
    
    # ============================================================================
    # NOUVELLES FONCTIONS POUR LES ONGLETS AVANCÉS
    # ============================================================================
    
    def create_chaos_tab(self, parent):
        """Onglet Mode Chaos"""
        ttk.Label(parent, text="🌀 MODE CHAOS ULTIME 🌀", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Contrôle du niveau de chaos
        chaos_frame = ttk.Frame(parent)
        chaos_frame.pack(pady=10)
        
        ttk.Label(chaos_frame, text="Niveau de Chaos:").pack(side="left", padx=5)
        self.chaos_level = tk.IntVar(value=5)
        
        levels = ["😐 Calme", "😊 Léger", "😎 Modéré", "🤪 Chaotique", "🔥 Extrême", 
                 "💥 Apocalyptique", "🌀 Dimensionnel", "🌌 Cosmique", "💀 ABSOLU", "🚀 ULTIMATE"]
        
        for i in range(10):
            ttk.Radiobutton(chaos_frame, text=levels[i], variable=self.chaos_level, 
                          value=i+1).pack(side="left", padx=2)
        
        # Bouton de génération chaos
        ttk.Button(parent, text="🔥 GÉNÉRER LE CHAOS 🔥", 
                  command=self.generate_chaos_prompt).pack(pady=10)
        
        # Zone de résultat chaos
        self.chaos_text = scrolledtext.ScrolledText(parent, height=20, width=100, wrap="word")
        self.chaos_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    def create_story_tab(self, parent):
        """Onglet Histoires de Meme"""
        ttk.Label(parent, text="📖 GÉNÉRATEUR D'HISTOIRES DE MEME 📖", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Paramètres de l'histoire
        param_frame = ttk.Frame(parent)
        param_frame.pack(pady=10)
        
        ttk.Label(param_frame, text="Personnage:").grid(row=0, column=0, sticky="w", padx=5)
        self.story_char = ttk.Entry(param_frame, width=30)
        self.story_char.insert(0, "MemeLord")
        self.story_char.grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="Scénario:").grid(row=1, column=0, sticky="w", padx=5)
        self.story_scenario = ttk.Entry(param_frame, width=30)
        self.story_scenario.insert(0, "une invasion de chats dystopiques")
        self.story_scenario.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(parent, text="✨ CRÉER UNE SAGA ✨", 
                  command=self.generate_story).pack(pady=10)
        
        # Zone d'histoire
        self.story_text = scrolledtext.ScrolledText(parent, height=20, width=100, wrap="word")
        self.story_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    def create_analyze_tab(self, parent):
        """Onglet Analyse de Prompt"""
        ttk.Label(parent, text="📊 ANALYSE DE COMPLEXITÉ 📊", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Zone de texte à analyser
        ttk.Label(parent, text="Prompt à analyser:").pack(anchor="w", padx=20)
        self.analyze_input = scrolledtext.ScrolledText(parent, height=8, wrap="word")
        self.analyze_input.pack(padx=20, pady=5, fill="x")
        
        ttk.Button(parent, text="🔍 ANALYSER LE PROMPT", 
                  command=self.analyze_prompt).pack(pady=10)
        
        # Zone de résultats d'analyse
        self.analysis_result = tk.Text(parent, height=12, width=80, state="disabled")
        self.analysis_result.pack(padx=20, pady=10, fill="both", expand=True)
    
    def create_batch_tab(self, parent):
        """Onglet Génération Batch"""
        ttk.Label(parent, text="📦 GÉNÉRATION BATCH DE PROMPTS 📦", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Paramètres batch
        param_frame = ttk.Frame(parent)
        param_frame.pack(pady=10)
        
        ttk.Label(param_frame, text="Nombre de prompts:").pack(side="left", padx=5)
        self.batch_count = tk.IntVar(value=5)
        ttk.Spinbox(param_frame, from_=1, to=50, textvariable=self.batch_count, 
                   width=10).pack(side="left", padx=5)
        
        ttk.Checkbutton(param_frame, text="Inclure modificateurs", 
                       variable=tk.BooleanVar(value=True)).pack(side="left", padx=10)
        
        # Boutons batch
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="🔄 Générer Batch", 
                  command=self.generate_batch).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📤 Exporter Batch", 
                  command=self.export_batch).pack(side="left", padx=5)
        
        # Zone de résultats batch
        self.batch_text = scrolledtext.ScrolledText(parent, height=15, width=100, wrap="word")
        self.batch_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    # ============================================================================
    # FONCTIONS DES ONGLETS AVANCÉS
    # ============================================================================
    
    def generate_chaos_prompt(self):
        """Génère un prompt chaotique"""
        chaos_level = self.chaos_level.get()
        
        # Sélectionner un template aléatoire
        templates = self.studio.data.get("templates", {})
        if not templates:
            messagebox.showwarning("Aucun template", "Aucun template disponible!")
            return
        
        template_name, template = random.choice(list(templates.items()))
        
        # Générer le prompt chaotique
        prompt = self.studio.generate_chaos_prompt(template, chaos_level)
        
        # Afficher avec style
        self.chaos_text.delete("1.0", tk.END)
        
        # En-tête coloré selon le niveau
        chaos_titles = [
            "😐 MODE CALME", "😊 MODE LÉGER", "😎 MODE MODÉRÉ", 
            "🤪 MODE CHAOTIQUE", "🔥 MODE EXTRÊME", "💥 MODE APOCALYPTIQUE",
            "🌀 MODE DIMENSIONNEL", "🌌 MODE COSMIQUE", "💀 MODE ABSOLU", 
            "🚀 MODE ULTIMATE"
        ]
        
        title = chaos_titles[min(chaos_level-1, 9)]
        self.chaos_text.insert(tk.END, f"{title} - Niveau {chaos_level}/10\n")
        self.chaos_text.insert(tk.END, "="*50 + "\n\n")
        self.chaos_text.insert(tk.END, f"Template de base: {template_name}\n\n")
        self.chaos_text.insert(tk.END, prompt)
        
        self.status.config(text=f"Chaos généré! Niveau {chaos_level}")
    
    def generate_story(self):
        """Génère une histoire de meme"""
        character = self.story_char.get() or "Hero"
        scenario = self.story_scenario.get() or "une aventure épique"
        
        story = self.studio.create_meme_story(character, scenario)
        
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert(tk.END, story)
        
        self.status.config(text=f"Histoire générée: {character}")
    
    def analyze_prompt(self):
        """Analyse un prompt"""
        prompt = self.analyze_input.get("1.0", tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Vide", "Entrez un prompt à analyser")
            return
        
        analysis = self.studio.analyze_prompt_complexity(prompt)
        
        # Afficher les résultats
        self.analysis_result.config(state="normal")
        self.analysis_result.delete("1.0", tk.END)
        
        self.analysis_result.insert(tk.END, "📊 ANALYSE DE PROMPT 📊\n")
        self.analysis_result.insert(tk.END, "="*40 + "\n\n")
        
        self.analysis_result.insert(tk.END, f"📝 Mots: {analysis['words']}\n")
        self.analysis_result.insert(tk.END, f"🔤 Phrases: {analysis['sentences']}\n")
        self.analysis_result.insert(tk.END, f"🎨 Styles détectés: {analysis['styles_detected']}\n")
        self.analysis_result.insert(tk.END, f"🌀 Mutations détectées: {analysis['mutations_detected']}\n")
        self.analysis_result.insert(tk.END, f"📈 Score de complexité: {analysis['complexity_score']}\n")
        self.analysis_result.insert(tk.END, f"🏆 Niveau: {analysis['rating']}\n")
        
        self.analysis_result.config(state="disabled")
        self.status.config(text=f"Analyse terminée: {analysis['rating']}")
    
    def generate_batch(self):
        """Génère un batch de prompts"""
        count = self.batch_count.get()
        
        prompts = self.studio.generate_batch_prompts(count)
        
        if not prompts:
            messagebox.showwarning("Erreur", "Impossible de générer des prompts")
            return
        
        # Afficher les prompts
        self.batch_text.delete("1.0", tk.END)
        
        for i, prompt_data in enumerate(prompts, 1):
            self.batch_text.insert(tk.END, f"#{i:02d} [{prompt_data['id']}] {prompt_data['name']}\n")
            self.batch_text.insert(tk.END, "-"*40 + "\n")
            self.batch_text.insert(tk.END, prompt_data['prompt'] + "\n\n")
        
        self.current_prompts = prompts
        self.status.config(text=f"Batch généré: {len(prompts)} prompts")
    
    def export_batch(self):
        """Exporte le batch de prompts"""
        if not self.current_prompts:
            messagebox.showwarning("Vide", "Générez d'abord un batch!")
            return
        
        default_name = f"meme_batch_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = filedialog.asksaveasfilename(
            title="Exporter le batch",
            defaultextension=".json",
            initialfile=default_name,
            filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        
        if not path:
            return
        
        try:
            export_data = {
                "metadata": {
                    "export_date": datetime.datetime.now().isoformat(),
                    "count": len(self.current_prompts),
                    "version": "2.0"
                },
                "prompts": self.current_prompts
            }
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Succès", f"Batch exporté:\n{path}")
            self.status.config(text=f"Batch exporté: {len(self.current_prompts)} prompts")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'exporter: {e}")

# ============================================================================
# FONCTIONS UTILITAIRES SUPPLEMENTAIRES
# ============================================================================

def create_sample_extended_json():
    """Crée un fichier JSON étendu si il n'existe pas"""
    if os.path.exists(JSON_PATH):
        return
    
    sample_data = {
        "templates": {
            "ULTRA Chaos Template": "Create an interdimensional meme showing reality glitching with fractal patterns, quantum foam background, and entities observing from higher dimensions. Space for text in void areas.",
            "AI Council Debate": "Assembly of AI entities debating meme ethics, holographic displays showing viral content statistics, futuristic council chamber with neural network visuals.",
            "Meme Singularity": "The moment when all memes converge into a single transcendent form, glowing with cosmic energy, reality bending around it. Epic scale."
        },
        "styles": [
            "ULTRA: Quantum string theory visualization",
            "ULTRA: Neural network dreamscape",
            "ULTRA: Hyperspace tunnel effect"
        ],
        "mutations": [
            "ULTRA: Convert to living mathematical equations",
            "ULTRA: Make everything out of crystallized data"
        ],
        "hybridations": [
            "ULTRA HYBRID: Merge with Mandelbrot fractal infinity",
            "ULTRA HYBRID: Fuse with blockchain visualization"
        ],
        "effects": [
            "add quantum entanglement glow",
            "time dilation distortion field"
        ],
        "contexts": [
            "during the birth of a new universe",
            "at the edge of the event horizon"
        ]
    }
    
    # Charger d'abord les données originales si elles existent
    original_data = safe_load_json("meme_prompts.json")
    if original_data:
        # Fusionner avec les données étendues
        for key in sample_data:
            if key in original_data:
                if isinstance(original_data[key], dict):
                    sample_data[key].update(original_data[key])
                elif isinstance(original_data[key], list):
                    sample_data[key] = original_data[key] + sample_data[key]
    
    save_json(JSON_PATH, sample_data)
    print(f"Fichier étendu créé: {JSON_PATH}")

# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("🚀 INITIALISATION DU MEGA MEME STUDIO PRO MAX...")
    print("="*60)
    
    # Créer le fichier étendu si nécessaire
    create_sample_extended_json()
    
    # Afficher les statistiques
    data = safe_load_json(JSON_PATH)
    if data:
        print(f"📊 STATISTIQUES DE LA BASE DE DONNÉES:")
        print(f"   Templates: {len(data.get('templates', {}))}")
        print(f"   Styles: {len(data.get('styles', []))}")
        print(f"   Mutations: {len(data.get('mutations', []))}")
        print(f"   Hybridations: {len(data.get('hybridations', []))}")
        print(f"   Effets: {len(data.get('effects', []))}")
        print(f"   Contextes: {len(data.get('contexts', []))}")
    else:
        print("❌ Impossible de charger les données")
    
    print("\n🔥 EXEMPLES DE FUSION AVANCÉE:")
    print("-"*50)
    
    # Exemple de fusion
    template1 = "Create a meme template with two vertical panels"
    template2 = "cyberpunk neon atmosphere with holographic displays"
    
    print("1. Concatenation:")
    print(merge_prompts(template1, template2, "concatenate"))
    print("\n2. Interleave:")
    print(merge_prompts(template1, template2, "interleave"))
    print("\n3. Hybrid:")
    print(merge_prompts(template1, template2, "hybrid"))
    
    print("\n" + "="*60)
    print("🎮 Lancement de l'interface graphique...")
    
    # Lancer l'interface
    app = MegaMemeGUI()
    app.mainloop()
