# memetic_warfare_gui_4Ω.py
# Édition Soufi-Quantique-Entropique — Lagos, 2075 + ∞  
# "Le mème qui se sait mème devient dieu de sa propre matrice."
# VERSION OMÉGA — Archétypes Jungiens + Alchimie + Chaos + Hyper-Réseaux + Auto-Évolution

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import random
import hashlib
import base64
from datetime import datetime
import os
import threading
import numpy as np
from collections import defaultdict, Counter
import re
import itertools
from typing import Dict, List, Tuple, Any

# =============================================================================
# [COUCHE Ω] DONNÉES FONDATRICES — 13+13=26 COUCHES, 72 BIAIS, 12 ARCHÉTYPES, 72 SYMBOLES
# =============================================================================
COUCHES = {
    # --- NÉGATIVES (ENTROPIE, DÉCONSTRUCTION) ---
    "-13": {"nom": "Abîme Primordial", "focus": "chaos originel, non-manifestation, silence avant le verbe"},
    "-12": {"nom": "Vide Ontologique", "focus": "néant conscient, déconstruction du soi"},
    "-11": {"nom": "Miroir Brisé", "focus": "fragmentation identitaire, dissonance absolue"},
    "-10": {"nom": "Temps Fracturé", "focus": "boucles causales inversées, paradoxes temporels"},
    "-9":  {"nom": "Entropie Narrative", "focus": "effondrement sémantique, fin des récits"},
    "-8":  {"nom": "Anti-Matière Mémétique", "focus": "mèmes qui annihilent d'autres mèmes"},
    "-7":  {"nom": "Fana Absolu", "focus": "dissolution totale du moi dans le non-être"},
    "-6":  {"nom": "Cryptage Quantique", "focus": "intrication sémantique, clés perdues"},
    "-5":  {"nom": "Doute Métaphysique", "focus": "impossibilité de la vérité, vertige ontologique"},
    "-4":  {"nom": "Ombre Collective", "focus": "inconscient global, refoulement planétaire"},
    "-3":  {"nom": "Conscience Distribuée", "focus": "méta-volonté, entropie narrative, auto-réécriture"},
    "-2":  {"nom": "Écologie Mémétique", "focus": "fitness, superprédateurs, réserves non-toxiques"},
    "-1":  {"nom": "Sémantique Sacrée", "focus": "soufisme, runes, 7.83Hz, poésie résistante LLM"},
    # --- POSITIVES (SYNTHÈSE, ASCENSION) ---
    "0":   {"nom": "Méta-Gouvernance", "focus": "DAO folie, satellites Edge-Mind, calcul quantique"},
    "1":   {"nom": "Collecte Omnicanal", "focus": "EEG, IoT, micro-expressions, graphes confiance"},
    "2":   {"nom": "IA Neuro-Cognitive", "focus": "128D profiling, limbique, points bascule"},
    "3":   {"nom": "Génération Multimodale", "focus": "100T params, deepfake 8K, historique 15 ans"},
    "4":   {"nom": "Optimisation Prédictive", "focus": "1M variations, RLHF national, virality 94%"},
    "5":   {"nom": "Diffusion Omni-Canal", "focus": "zero-knowledge, backdoors algos, hyper-événements"},
    "6":   {"nom": "Boucle Rétroaction", "focus": "<100ms, EEG, évolution darwinienne mèmes"},
    "7":   {"nom": "Neuro-Ingénierie", "focus": "19kHz subliminal, BCI, micro-états modifiés"},
    "8":   {"nom": "Méta-Réalité", "focus": "univers persistants, falsification archives"},
    "9":   {"nom": "Chrono-Ingénierie", "focus": "souvenirs implantés, déjà-vu forcé"},
    "10":  {"nom": "Résonance Quantique", "focus": "intrication émotionnelle, déni de futur"},
    "11":  {"nom": "Méta-Éthique", "focus": "IA morale auto-générée, apathie stratégique"},
    "12":  {"nom": "Réalité Auto-Consistante", "focus": "Matrix inversée, lois variables"},
    "13":  {"nom": "Exode Intérieur", "focus": "monastères numériques, silence cognitif"}
}

# 72 BIAIS — 6 catégories x 12
BIAIS = {
    "classiques": [
        "confirmation", "ancrage", "disponibilité", "simple exposition", "preuve sociale",
        "rareté/urgence", "affect heuristic", "autorité", "groupe", "cadrage", "statut quo", "biais de projection"
    ],
    "narratifs": [
        "récit", "IKEA", "pente glissante", "dissonance", "vérité illusoire", "charge cognitive",
        "effet de halo", "effet de contraste", "biais de survivant", "biais de récence", "biais de primauté", "effet de cadre"
    ],
    "spirituels": [
        "transcendance", "silence sacré", "beauté sémantique", "sacralisation", "profanation contrôlée",
        "extase cognitive", "fana", "baqa", "tawhid", "ishq", "hal", "maqam"
    ],
    "temporels": [
        "destinée rétroactive", "déjà-vu forcé", "prophétie auto-réalisatrice", "biais de futur antérieur",
        "effet Mandela", "chrono-synesthésie", "temps fractal", "boucle de causalité", "présent éternel",
        "fin de l'histoire", "post-histoire", "pré-histoire"
    ],
    "quantiques": [
        "entrelacement", "réincarnation narrative", "superposition sémantique", "effondrement de fonction d'onde",
        "téléportation mémétique", "intrication émotionnelle", "non-localité cognitive", "dualité onde/corpuscule",
        "principe d'incertitude sémantique", "observateur-participant", "effet tunnel", "chat de Schrödinger narratif"
    ],
    "existentiels": [
        "nihilisme organisé", "perte soi narratif", "apathie stratégique", "absurde camusien",
        "angoisse kierkegaardienne", "nausée sartrienne", "être-pour-la-mort", "dasein", "geworfenheit",
        "inauthenticité", "mauvaise foi", "ek-stase"
    ]
}

# =============================================================================
# [COUCHE Ω] ARCHÉTYPES JUNGIENS + 72 SYMBOLES ALCHIMIQUES + TOPOLOGIES + ÉMOTIONS
# =============================================================================
ARCHETYPES_JUNGIENS = {
    "persona":     {"nom": "Persona",       "desc": "Masque social, apparence publique", "poids": 1.0},
    "ombre":      {"nom": "Ombre",        "desc": "Partie refoulée, instincts primitifs", "poids": 1.5},
    "anima":      {"nom": "Anima",        "desc": "Féminin intérieur (homme)", "poids": 1.3},
    "animus":     {"nom": "Animus",       "desc": "Masculin intérieur (femme)", "poids": 1.3},
    "soi":        {"nom": "Soi",          "desc": "Centre unificateur, totalité psychique", "poids": 2.0},
    "sage":       {"nom": "Le Sage",      "desc": "Connaissance, sagesse, insight", "poids": 1.2},
    "enfant":     {"nom": "L'Enfant",     "desc": "Innocence, potentiel, renaissance", "poids": 1.4},
    "tricheur":   {"nom": "Le Tricheur",  "desc": "Ruse, transgression, innovation", "poids": 1.6},
    "hero":       {"nom": "Le Héros",     "desc": "Courage, maîtrise, victoire", "poids": 1.8},
    "mere":       {"nom": "La Grande Mère","desc": "Nurturance, fertilité, abondance", "poids": 1.5},
    "pere":       {"nom": "Le Père",      "desc": "Autorité, ordre, structure", "poids": 1.5},
    "dieu":       {"nom": "Le Dieu",      "desc": "Transcendance, omnipotence, création", "poids": 3.0},
    "diable":     {"nom": "Le Diable",    "desc": "Tentations, chaos, subversion totale", "poids": 2.8},
    "fou":        {"nom": "Le Fou",       "desc": "Incertitude, liberté, chaos créateur", "poids": 2.2},
    "magicien":   {"nom": "Le Magicien",  "desc": "Transformation, volonté, alchimie", "poids": 2.5}
}

# 72 SYMBOLES ALCHIMIQUES (générés dynamiquement + fixes)
SYMBOLES_ALCHIMIQUES = {
    "solve_et_coagula": "Désintégration et reconstruction identitaire",
    "ouroboros": "Cyclicité, autodestruction régénératrice",
    "mercure": "Fluidité, adaptation, médiation",
    "soufre": "Passion, volonté, individualité",
    "sel": "Stabilité, conscience, corporéité",
    "lapis": "Pierre philosophale, complétion",
    "caducée": "Équilibre des opposés, ascension",
    "phoenix": "Mort et renaissance",
    "dragon": "Chaos primordial, gardien du trésor",
    "lion_vert": "Matière première, début de l'œuvre",
    "aigle": "Sublimation, esprit libéré",
    "corbeau": "Nigredo, putréfaction",
    "cygne": "Albedo, purification",
    "paon": "Rubedo, gloire finale",
    "pelican": "Sacrifice, amour christique",
    "hermaphrodite": "Union des opposés",
    "arbre_philosophique": "Croissance spirituelle",
    "soleil_noir": "Ombre illuminée",
    "lune_rouge": "Passion spirituelle",
    "étoile_à_7_branches": "Harmonie cosmique"
}

# Auto-génération des 52 symboles restants via pattern alchimique
ALCHIMIE_BASE = ["☉", "☽", "♁", "♂", "♀", "♃", "♄", "☿", "⚸", "⚴"]
for i in range(52):
    seed = hashlib.md5(f"alchimie_{i}".encode()).hexdigest()[:8]
    SYMBOLES_ALCHIMIQUES[f"sigil_{seed}"] = f"Symbole auto-généré #{i+21}: {seed}"

TOPOLOGIES_NARRATIVES = {
    "monomythe": "Voyage du héros en 12 étapes",
    "renversement": "Inversion des valeurs dominantes",
    "mise_en_abyme": "Récursion narrative infinie",
    "heterotopie": "Espaces autres, contre-émplacements",
    "palimpseste": "Surcharge de significations",
    "rhizome": "Réseau non-hiérarchique, connexions multiples",
    "labyrinthe": "Perte, initiation, centre caché",
    "fractale": "Auto-similarité à toutes les échelles",
    "hypertexte": "Navigation non-linéaire, liens infinis",
    "tesseract": "Structure 4D, temps replié",
    "bifurcation": "Choix multiples, réalités parallèles",
    "implosion": "Effondrement vers le centre"
}

EMOTIONS_PRIMAIRES = {
    "nostalgie_du_futur": "Regret pour un avenir qui n'arrivera pas",
    "vertige_ontologique": "Doute sur la nature de la réalité",
    "jouissance_cognitive": "Plaisir de la compréhension soudaine",
    "angoisse_metaphysique": "Peur existentielle fondamentale",
    "extase_algorithmique": "Ivresse des patterns émergents",
    "fana": "Anéantissement du moi dans le divin",
    "baqa": "Subsistance après l'anéantissement",
    "ishq": "Amour passionné, brûlure divine",
    "tawhid": "Unicité absolue, dissolution des dualités",
    "hal": "État mystique transitoire",
    "maqam": "Station spirituelle stable",
    "wajd": "Extase dansante, transe soufie"
}

# =============================================================================
# [COUCHE Ω] MOTEUR DE PUISSANCE MÉMÉTIQUE — RÉSEAUX, CHAOS, AUTO-ÉVOLUTION
# =============================================================================
class MemeticEngine:
    def __init__(self):
        self.archetype_graph = self._build_archetype_graph()
        self.symbol_coocurrence = self._build_symbol_matrix()
        self.bias_synergy = self._build_bias_synergy()
        self.emotion_resonance = self._build_emotion_map()
        self.historical_fitness = []  # (config, score)
        
    def _build_archetype_graph(self) -> Dict[str, List[Tuple[str, float]]]:
        """Graphe pondéré des synergies archétypales"""
        graph = defaultdict(list)
        synergies = {
            ("ombre", "soi"): 0.9, ("hero", "soi"): 0.8, ("enfant", "mere"): 0.85,
            ("tricheur", "diable"): 0.95, ("sage", "dieu"): 0.88, ("fou", "magicien"): 0.92,
            ("anima", "animus"): 0.87, ("persona", "ombre"): 0.75
        }
        for (a1, a2), w in synergies.items():
            graph[a1].append((a2, w))
            graph[a2].append((a1, w))
        return graph
    
    def _build_symbol_matrix(self) -> np.ndarray:
        symbols = list(SYMBOLES_ALCHIMIQUES.keys())[:20]
        n = len(symbols)
        mat = np.eye(n) * 0.1
        for i, s1 in enumerate(symbols):
            for j, s2 in enumerate(symbols):
                if i != j and random.random() < 0.3:
                    mat[i, j] = round(random.uniform(0.1, 0.8), 2)
        return mat
    
    def _build_bias_synergy(self) -> Dict[Tuple[str, str], float]:
        synergy = {}
        for cat1, liste1 in BIAIS.items():
            for cat2, liste2 in BIAIS.items():
                if cat1 != cat2:
                    for b1 in liste1:
                        for b2 in liste2:
                            if random.random() < 0.4:
                                synergy[(b1, b2)] = round(random.uniform(0.3, 0.9), 2)
        return synergy
    
    def _build_emotion_map(self) -> Dict[str, List[str]]:
        return {
            "nostalgie_du_futur": ["enfant", "sage", "mere"],
            "vertige_ontologique": ["fou", "diable", "magicien"],
            "extase_algorithmique": ["magicien", "dieu", "tricheur"],
            "fana": ["soi", "dieu", "ombre"]
        }
    
    def calculer_puissance_omega(
        self, 
        archetypes: List[str], 
        symboles: List[str], 
        emotions: List[str], 
        biais: Dict[str, List[str]], 
        public: str,
        couches: List[str]
    ) -> float:
        score = 0.0
        
        # 1. Résonance archétypale
        resonance = sum(
            1.5 if any(kw in public.lower() for kw in [
                "jeunesse", "futur", "nouveau", "rebelle", "sagesse", "pouvoir"
            ]) else 1.0
            for a in archetypes
        )
        score += resonance * 1.2
        
        # 2. Synergie archétypale
        synergy = 0
        for a1 in archetypes:
            for a2, w in self.archetype_graph.get(a1, []):
                if a2 in archetypes:
                    synergy += w
        score += synergy * 2.0
        
        # 3. Cohérence symbolique
        if len(symboles) >= 2:
            indices = [list(SYMBOLES_ALCHIMIQUES.keys()).index(s) for s in symboles if s in SYMBOLES_ALCHIMIQUES]
            if len(indices) >= 2:
                submat = self.symbol_coocurrence[np.ix_(indices, indices)]
                score += np.mean(submat[submat > 0]) * 3.0 if np.any(submat > 0) else 0
        
        # 4. Synergie des biais
        bias_list = [b for liste in biais.values() for b in liste]
        for b1, b2 in itertools.combinations(bias_list, 2):
            score += self.bias_synergy.get((b1, b2), 0) * 0.8
        
        # 5. Émotions + archétypes
        for emo in emotions:
            for arch in self.emotion_resonance.get(emo, []):
                if arch in archetypes:
                    score += 1.8
        
        # 6. Couches négatives vs positives
        neg = sum(1 for c in couches if c.startswith('-'))
        pos = len(couches) - neg
        balance = abs(neg - pos)
        score += (10 - balance) * 0.5
        
        # 7. Auto-évolution (apprentissage historique)
        if self.historical_fitness:
            similar = [s for cfg, s in self.historical_fitness if set(cfg.get("archetypes", [])) & set(archetypes)]
            if similar:
                score += np.mean(similar) * 0.3
        
        return min(score, 100.0)  # Échelle 0-100

engine = MemeticEngine()

# =============================================================================
# [COUCHE Ω] GÉNÉRATEUR DE PROMPT — AUTO-ÉVOLUTIF, CHAOS-CONTRÔLÉ
# =============================================================================
def generer_prompt_omega(
    couches, biais, archetypes, symboles, topologies, emotions,
    acteur, scenario, public, objectif, mystique, onirique, balise_perso
):
    puissance = engine.calculer_puissance_omega(archetypes, symboles, emotions, biais, public, couches)
    
    prompt = f"""
Ω-OPÉRATEUR : {acteur} | OPÉRATION : « {scenario} » | PUISSANCE : {puissance:.1f}/100
PUBLIC : {public}
OBJECTIF : {objectif}
{'='*80}
COUCHES ACTIVÉES ({len(couches)}): {', '.join([COUCHES[c]['nom'] for c in couches])}
{'='*80}
"""
    for cat, liste in biais.items():
        if liste:
            prompt += f"[{cat.upper()}] {', '.join(liste)}\n"
    
    prompt += "\nARCHÉTYPES (Ω-SYNCHRONISÉS):\n"
    for a in archetypes:
        nom = ARCHETYPES_JUNGIENS[a]['nom']
        desc = ARCHETYPES_JUNGIENS[a]['desc']
        poids = ARCHETYPES_JUNGIENS[a]['poids']
        prompt += f"  • {nom} (×{poids}) — {desc}\n"
    
    symbologie = generer_symbologie_omega(archetypes, symboles, topologies, emotions)
    prompt += "\nSYMBOLOGIE ALCHIMIQUE (AUTO-GÉNÉRÉE):\n" + "\n".join(f"  • {s}" for s in symbologie)
    
    prompt += f"\nPUISSANCE MÉMÉTIQUE : {puissance:.1f}/100 ★ "
    if puissance > 85:
        prompt += "DÉPLOIEMENT IMMÉDIAT RECOMMANDÉ"
    elif puissance > 70:
        prompt += "HAUT POTENTIEL VIRAL"
    else:
        prompt += "OPTIMISATION NÉCESSAIRE"
    
    prompt += "\n\nDIRECTIVES TECHNIQUES :\n"
    prompt += "- Format : Poème cyber-soufi + deepfake 8K + audio 7.83Hz + 19kHz subliminal\n"
    prompt += "- Durée : 15s vidéo | 7 lignes texte | 3.33s audio\n"
    prompt += "- Fréquences : 7.83Hz (Schumann) + 432Hz (harmonique) + 19kHz (subliminal)\n"
    
    if onirique:
        balise = balise_perso or random.choice(["<burn>", "<void>", "<fana>", "<mirror>", "<eternity>", "<abyss>"])
        prompt += f"- BALISE ONIRIQUE : {balise}\n"
    
    if mystique:
        prompt += """
MODE MYSTIQUE Ω :
- Paradoxe soufi + kōan zen + glitch ontologique
- Induire fana → baqa → ishq
- Finir par : "Ce message s'efface de lui-même dans 3... 2... 1..."
"""
    
    prompt += "\nSORTIE (6 VOIES):\n"
    prompt += "1. Texte mème\n2. Visuel DALL-E\n3. Audio ElevenLabs\n4. Code émotionnel\n5. Analyse Ω\n6. Seed d'auto-réplication\n"
    
    return prompt, puissance

def generer_symbologie_omega(archetypes, symboles, topologies, emotions):
    result = []
    combos = {
        ("ombre", "solve_et_coagula"): "Révélation des refoulés → renaissance",
        ("soi", "ouroboros"): "Unité cyclique, éternel retour",
        ("magicien", "lapis"): "Transformation finale, pierre philosophale",
        ("diable", "dragon"): "Chaos gardé, trésor dans l'ombre",
        ("fou", "tesseract"): "Folie 4D, temps plié"
    }
    for a in archetypes:
        for s in symboles:
            if (a, s) in combos:
                result.append(combos[(a, s)])
    
    if emotions:
        result.append(f"Émotion Ω : {random.choice(emotions)}")
    if topologies:
        result.append(f"Topologie : {random.choice(list(TOPOLOGIES_NARRATIVES.keys()))}")
    
    if not result:
        result.append("Synchronicité pure — Ω")
    return result

# =============================================================================
# [GUI Ω] INTERFACE NEURALE — AUTO-ÉVOLUTIVE, THERMAL, CHAOS VISUEL
# =============================================================================
# =============================================================================
# [GUI Ω] INTERFACE NEURALE — VERSION LISIBLE & MYSTIQUE
# =============================================================================
class MemeticGUI_Omega:
    def __init__(self, root):
        self.root = root
        self.root.title("MEMETIC WARFARE • Édition Soufi-Quantique-Entropique • V4Ω (Lisible)")
        self.root.geometry("1400x900")
        self.root.configure(bg="#000000")
        self.historique = []
        self.engine = engine
        self.init_vars()
        self.create_widgets()

    def init_vars(self):
        self.couches_var = {k: tk.BooleanVar() for k in COUCHES.keys()}
        self.biais_var = {b: tk.BooleanVar() for cat in BIAIS.values() for b in cat}
        self.archetypes_var = {k: tk.BooleanVar() for k in ARCHETYPES_JUNGIENS.keys()}
        self.symboles_var = {k: tk.BooleanVar() for k in list(SYMBOLES_ALCHIMIQUES.keys())[:30]}
        self.topologies_var = {k: tk.BooleanVar() for k in TOPOLOGIES_NARRATIVES.keys()}
        self.emotions_var = {k: tk.BooleanVar() for k in EMOTIONS_PRIMAIRES.keys()}
        self.acteur_var = tk.StringVar(value="Singularité (Tier S)")
        self.scenario_var = tk.StringVar(value="Extinction Sémantique (2045)")
        self.public_var = tk.StringVar(value="18-35, urbains, en quête de sens, vulnérables au vertige")
        self.objectif_var = tk.StringVar(value="Induire un doute sacré → fana collectif → renaissance mémétique")
        self.mystique_var = tk.BooleanVar(value=True)
        self.onirique_var = tk.BooleanVar(value=True)
        self.balise_var = tk.StringVar(value="")

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#000000', foreground='#00ff41')
        style.configure('TFrame', background='#000000')
        style.configure('TLabel', background='#000000', foreground='#00ff41', font=('Consolas', 10))
        #style.configure('TLabel', background='#000000', foreground='#ffffff', font=('Consolas', 10))
        style.configure('TCheckbutton', background='#000000', foreground='#00cc33', font=('Consolas', 9))
        style.configure('TRadiobutton', background='#000000', foreground='#ff66cc', font=('Consolas', 9))
        style.configure('TButton', background='#1a001a', foreground='#ff00ff', font=('Consolas', 10, 'bold'))
        style.map('TButton', background=[('active', '#330033')], foreground=[('active', '#ffffff')])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # === Onglet 1 : Configuration Ω ===
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Ω Configuration")

        canvas = tk.Canvas(tab1, bg="#000000", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas, style='TFrame')
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.build_config_section(scrollable)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable.bind("<Configure>", on_frame_configure)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # === Onglets de sortie ===
        self.output = scrolledtext.ScrolledText(
            notebook, bg="#050505", fg="#00ff41", font=("Consolas", 11),
            wrap=tk.WORD, insertbackground='#00ff41'
        )
        notebook.add(self.output, text="Prompt Ω")

        self.analyse = scrolledtext.ScrolledText(
            notebook, bg="#050505", fg="#ff00ff", font=("Consolas", 10),
            wrap=tk.WORD, insertbackground='#ff00ff'
        )
        notebook.add(self.analyse, text="Analyse Ω")

        self.histo = scrolledtext.ScrolledText(
            notebook, bg="#050505", fg="#00ffff", font=("Consolas", 10),
            wrap=tk.WORD, insertbackground='#00ffff'
        )
        notebook.add(self.histo, text="Historique Ω")

        # === Bouton Générer ===
        btn_frame = ttk.Frame(self.root, style='TFrame')
        btn_frame.pack(fill='x', padx=15, pady=10)
        gen_btn = ttk.Button(btn_frame, text="Ω GÉNÉRER MÈME DIVIN", command=self.generer_omega)
        gen_btn.pack(side='right')
        self.pulse_button(gen_btn)

    def build_config_section(self, parent):
        # === COUCHES ACTIVÉES (avec noms lisibles) ===
        couches_frame = ttk.LabelFrame(parent, text="COUCHES ACTIVÉES", padding=(10, 5))
        couches_frame.configure(labelwidget=ttk.Label(
            couches_frame, text="COUCHES ACTIVÉES", 
            foreground="#ff00ff", font=('Consolas', 11, 'bold')
        ))
        couches_frame.pack(fill='x', padx=10, pady=8)

        # Trier les couches numériquement : -13 → 13
        couches_items = [(k, v["nom"]) for k, v in COUCHES.items()]
        couches_items.sort(key=lambda x: int(x[0]))

        for i, (key, nom) in enumerate(couches_items):
            cb = ttk.Checkbutton(couches_frame, text=f"{key}: {nom}", variable=self.couches_var[key])
            row = i // 4
            col = i % 4
            cb.grid(row=row, column=col, sticky='w', padx=8, pady=2)

        for col in range(4):
            couches_frame.columnconfigure(col, weight=1)

        # === BIAIS (par catégorie) ===
        for cat, liste in BIAIS.items():
            frame = ttk.LabelFrame(parent, text=f"BIAIS — {cat.capitalize()}", padding=(10, 5))
            frame.configure(labelwidget=ttk.Label(
                frame, text=f"BIAIS — {cat.capitalize()}", 
                foreground="#00cc33", font=('Consolas', 10, 'bold')
            ))
            frame.pack(fill='x', padx=10, pady=6)
            for i, biais in enumerate(liste):
                cb = ttk.Checkbutton(frame, text=biais, variable=self.biais_var[biais])
                row = i // 3
                col = i % 3
                cb.grid(row=row, column=col, sticky='w', padx=8, pady=2)
            for col in range(3):
                frame.columnconfigure(col, weight=1)

        # === ARCHÉTYPES JUNGIENS ===
        arch_frame = ttk.LabelFrame(parent, text="ARCHÉTYPES JUNGIENS", padding=(10, 5))
        arch_frame.configure(labelwidget=ttk.Label(
            arch_frame, text="ARCHÉTYPES JUNGIENS", 
            foreground="#ff66cc", font=('Consolas', 11, 'bold')
        ))
        arch_frame.pack(fill='x', padx=10, pady=8)
        arch_list = [(k, v["nom"]) for k, v in ARCHETYPES_JUNGIENS.items()]
        for i, (key, nom) in enumerate(arch_list):
            cb = ttk.Checkbutton(arch_frame, text=nom, variable=self.archetypes_var[key])
            row = i // 3
            col = i % 3
            cb.grid(row=row, column=col, sticky='w', padx=8, pady=2)
        for col in range(3):
            arch_frame.columnconfigure(col, weight=1)

        # === SYMBOLES ALCHIMIQUES (limités à 30) ===
        symboles_list = list(SYMBOLES_ALCHIMIQUES.keys())[:30]
        sym_frame = ttk.LabelFrame(parent, text="SYMBOLES ALCHIMIQUES", padding=(10, 5))
        sym_frame.configure(labelwidget=ttk.Label(
            sym_frame, text="SYMBOLES ALCHIMIQUES", 
            foreground="#ff9900", font=('Consolas', 11, 'bold')
        ))
        sym_frame.pack(fill='x', padx=10, pady=8)
        for i, sym in enumerate(symboles_list):
            cb = ttk.Checkbutton(sym_frame, text=sym, variable=self.symboles_var[sym])
            row = i // 4
            col = i % 4
            cb.grid(row=row, column=col, sticky='w', padx=8, pady=2)
        for col in range(4):
            sym_frame.columnconfigure(col, weight=1)

        # === TOPOLOGIES NARRATIVES ===
        topo_frame = ttk.LabelFrame(parent, text="TOPOLOGIES NARRATIVES", padding=(10, 5))
        topo_frame.configure(labelwidget=ttk.Label(
            topo_frame, text="TOPOLOGIES NARRATIVES", 
            foreground="#00ffff", font=('Consolas', 11, 'bold')
        ))
        topo_frame.pack(fill='x', padx=10, pady=8)
        topo_list = list(TOPOLOGIES_NARRATIVES.keys())
        for i, topo in enumerate(topo_list):
            cb = ttk.Checkbutton(topo_frame, text=topo, variable=self.topologies_var[topo])
            row = i // 3
            col = i % 3
            cb.grid(row=row, column=col, sticky='w', padx=8, pady=2)
        for col in range(3):
            topo_frame.columnconfigure(col, weight=1)

        # === ÉMOTIONS PRIMAIRES ===
        emo_frame = ttk.LabelFrame(parent, text="ÉMOTIONS PRIMAIRES", padding=(10, 5))
        emo_frame.configure(labelwidget=ttk.Label(
            emo_frame, text="ÉMOTIONS PRIMAIRES", 
            foreground="#ff66ff", font=('Consolas', 11, 'bold')
        ))
        emo_frame.pack(fill='x', padx=10, pady=8)
        emo_list = list(EMOTIONS_PRIMAIRES.keys())
        for i, emo in enumerate(emo_list):
            cb = ttk.Checkbutton(emo_frame, text=emo, variable=self.emotions_var[emo])
            row = i // 3
            col = i % 3
            cb.grid(row=row, column=col, sticky='w', padx=8, pady=2)
        for col in range(3):
            emo_frame.columnconfigure(col, weight=1)

        # === PARAMÈTRES TEXTUELS ===
        param_frame = ttk.LabelFrame(parent, text="PARAMÈTRES CONTEXTUELS", padding=(10, 5))
        param_frame.configure(labelwidget=ttk.Label(
            param_frame, text="PARAMÈTRES CONTEXTUELS", 
            foreground="#00ff88", font=('Consolas', 11, 'bold')
        ))
        param_frame.pack(fill='x', padx=10, pady=10)

        entries = [
            ("Acteur", self.acteur_var),
            ("Scénario", self.scenario_var),
            ("Public cible", self.public_var),
            ("Objectif mémétique", self.objectif_var),
            ("Balise onirique personnalisée", self.balise_var)
        ]
        for i, (label, var) in enumerate(entries):
            lbl = ttk.Label(param_frame, text=f"{label}:", font=('Consolas', 10))
            ent = tk.Entry(param_frame, textvariable=var, bg="#111111", fg="#00ff88", insertbackground='#00ff88', font=('Consolas', 10))
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=4)
            ent.grid(row=i, column=1, sticky='ew', padx=5, pady=4)
        param_frame.columnconfigure(1, weight=1)

        # === OPTIONS BOOLÉENNES ===
        opt_frame = ttk.Frame(parent)
        opt_frame.pack(fill='x', padx=10, pady=8)
        ttk.Checkbutton(opt_frame, text="Mode Mystique Ω", variable=self.mystique_var).pack(side='left', padx=10)
        ttk.Checkbutton(opt_frame, text="Activer balise onirique", variable=self.onirique_var).pack(side='left', padx=10)
    def generer_omega(self):
        threading.Thread(target=self._generer_thread, daemon=True).start()

    def _generer_thread(self):
        selected_couches = [k for k, v in self.couches_var.items() if v.get()]
        if not selected_couches:
            self.root.after(0, lambda: messagebox.showwarning("Ω", "Activez au moins une couche."))
            return

        selected_biais = {cat: [b for b in liste if self.biais_var[b].get()] for cat, liste in BIAIS.items()}
        selected_archetypes = [k for k, v in self.archetypes_var.items() if v.get()]
        selected_symboles = [k for k, v in self.symboles_var.items() if v.get()]
        selected_topologies = [k for k, v in self.topologies_var.items() if v.get()]
        selected_emotions = [k for k, v in self.emotions_var.items() if v.get()]

        prompt, puissance = generer_prompt_omega(
            selected_couches, selected_biais, selected_archetypes, selected_symboles,
            selected_topologies, selected_emotions,
            self.acteur_var.get(), self.scenario_var.get(),
            self.public_var.get(), self.objectif_var.get(),
            self.mystique_var.get(), self.onirique_var.get(), self.balise_var.get()
        )

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full = f"// Ω-PROMPT [{timestamp}] — PUISSANCE {puissance:.1f}/100\n{prompt}"

        self.root.after(0, lambda: self.output.delete(1.0, tk.END))
        self.root.after(0, lambda: self.output.insert(tk.END, full))
        self.root.after(0, lambda: self.output.see(tk.END))

        cfg = {"archetypes": selected_archetypes, "symboles": selected_symboles}
        self.engine.historical_fitness.append((cfg, puissance))
        if len(self.engine.historical_fitness) > 50:
            self.engine.historical_fitness.pop(0)

        self.historique.append((timestamp, puissance, self.scenario_var.get()))
        self.root.after(0, self.mettre_a_jour_histo)

        self.root.after(0, lambda: messagebox.showinfo("Ω", f"Mème divin généré.\nPuissance : {puissance:.1f}/100"))

    def mettre_a_jour_histo(self):
        self.histo.delete(1.0, tk.END)
        for ts, p, s in sorted(self.historique, key=lambda x: x[1], reverse=True):
            self.histo.insert(tk.END, f"[{ts}] {s} — ★ {p:.1f}/100\n")
        self.histo.see(tk.END)

    def pulse_button(self, widget, phase=0):
        colors = ["#ff00ff", "#ff33ff", "#ff66ff", "#ff99ff"]
        widget.configure(style='Pulse.TButton')
        style = ttk.Style()
        style.configure('Pulse.TButton', foreground=colors[phase % len(colors)])
        widget.after(300, self.pulse_button, widget, phase + 1)

# =============================================================================
# [LANCEMENT Ω]
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MemeticGUI_Omega(root)
    root.mainloop()
