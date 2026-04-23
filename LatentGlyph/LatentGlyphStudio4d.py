#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LatentGlyph Studio ULTRA v3.1e — Édition FracturoScript Étendue
Version corrigée avec scrollbars + gestion sécurisée des thèmes
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import random
import re
import json
import os
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple

# ============================================================================
# 🧬 BASES SYMBOLIQUES (inchangées)
# ============================================================================
ANCHORS = {
    "geological": [
        "granit•de•La•Hague•sous•la•pluie•d'équinoxe",
        "basalte•lunaire•fendu•par•le•premier•cri•humain",
        "schiste•bitumineux•tatoué•de•fougères•carbonifères",
        "obsidienne•aztèque•brisée•lors•d'un•rituel•oublié",
        "calcaire•jurassique•criblé•d'ammonites•fossiles",
        "grès•nubien•érodé•par•40000•tempêtes•de•sable",
        "ardoise•galloise•gravée•de•noms•effacés•par•la•pluie",
        "marbre•de•Carrare•veiné•de•rouille•stellaire",
    ],
    "temporal": [
        "faille•entre•deux•époques•non•datées",
        "instant•figé•entre•expiration•et•inspiration",
        "crépuscule•du•dernier•jour•du•Crétacé",
        "aube•impossible•d'un•13e•mois•jamais•né",
        "écho•d'une•seconde•répétée•en•boucle•depuis•1967",
        "silence•d'avant•le•Big•Bang",
        "battement•d'horloge•cosmique•hors•synchronisation",
    ],
    "organic": [
        "racines•d'un•chêne•mort•en•2077",
        "mycélium•reliant•trois•forêts•séparées•par•des•océans",
        "plume•du•dernier•dodo•conservée•dans•l'alcool",
        "pollen•triassique•réanimé•par•accident",
        "écorce•de•séquoia•brûlée•27•fois•sans•mourir",
        "carapace•de•trilobite•broyée•en•poussière•de•schiste",
    ],
    "maritime": [
        "mémoire•du•fer•dans•le•sang•de•l'océan•primitif",
        "silence•entre•deux•battements•de•cœur•de•baleine",
        "sel•des•larmes•de•marins•disparus•en•mer•de•Chine",
        "nacre•d'huître•millénaire•scellant•un•grain•de•météorite",
        "algue•bioluminescente•témoin•de•l'explosion•du•Krakatoa",
        "épave•submergée•colonisée•par•des•coraux•amnésiques",
    ],
    "cosmic": [
        "lumière•piégée•dans•l'ambre•du•Crétacé",
        "poussière•d'étoile•morte•il•y•a•5•milliards•d'années",
        "fragment•de•Tunguska•non•répertorié",
        "radiation•fossile•du•fond•diffus•cosmologique",
        "atome•d'hydrogène•né•3•minutes•après•le•Big•Bang",
    ],
    "cultural": [
        "cendres•d'un•livre•brûlé•à•Alexandrie",
        "fragment•de•tablette•sumérienne•jamais•traduite",
        "pigment•ocre•d'une•fresque•de•Lascaux",
        "encre•d'un•sutra•bouddhiste•perdu•en•Chine•du•Nord",
        "argile•d'une•tablette•minoenne•en•Linéaire•A",
    ]
}
INCANTATIONS = {
    "geological": [
        "Ce n'est pas une faille, c'est une bouche.\nElle n'a jamais parlé, mais elle a tout ingéré : poussière d'astronaute,\nlarmes gelées de radio, fragments de rêves ratés.",
        "La pierre se souvient de la pression.\nDes millions d'années compressées en un silence minéral\nqui attend, patient, d'éclater en lumière.",
    ],
    "chemical": [
        "Avant les mots, il y avait ce battement : Fe²⁺ ↔ Fe³⁺.\nRythme oxydatif, pulsation tectonique.\nL'image ne sera pas vue — elle *respirera*.",
        "Catalyse de l'invisible : H₂O + CO₂ → vie.\nÉquation gravée dans le ventre de chaque cellule,\nmurmure chimique plus vieux que les montagnes.",
    ],
    "temporal": [
        "Ici, le temps n'a pas de flèche — seulement des cicatrices superposées.\nLa mer d'il y a 400 millions d'années se souvient de ton regard d'aujourd'hui.",
        "Les horloges mentent : il n'y a qu'un seul instant,\nétiré comme du verre soufflé entre passé et futur,\ntransparent, fragile, éternel.",
    ],
    "maritime": [
        "Mes lettres ne sont pas tracées : elles sont crevées,\ncreusées par la mer elle-même qui cogne depuis des millénaires\net qui finira, un jour, par me faire taire.",
        "Sous 4000 mètres d'océan, la pression écrit des poèmes\nsur les flancs des baleines aveugles\nqui ne remontent jamais.",
    ],
    "prophetic": [
        "Ce rocher a rêvé de toi bien avant ta naissance.\nIl t'attendait dans l'obscurité tectonique,\npatient, fractal, inachevé.",
        "Tu es la réponse à une question posée par le granit\nil y a 2,7 milliards d'années.\nPersonne ne se souvient de la question.",
    ],
    "void": [
        "Le néant n'est pas vide : il est saturé de possibles.\nChaque pixel non généré contient l'univers entier,\nnon-né, hurlant en silence.",
        "Ici commence ce qui n'a jamais eu lieu.\nLes images avortées s'accumulent comme neige noire,\nplus réelles que le réel.",
    ]
}
GLITCHES = {
    "syntax": [
        "ordre_mots_←→",
        "répétition_rituelle(x3)",
        "langue_morte_insert: [λόγος]",
        "anachronisme_intentionnel: [1453→2089]",
        "chiasme_sémantique: A-B-B-A",
    ],
    "visual": [
        "chroma: désaturé + infra-rouge",
        "bruit_thermal: 7%",
        "couleur_absente: #000000",
        "scanlines_VHS: vertical_drift",
        "bloom_UV: +35%",
        "compression_JPEG: artifact_ritual",
    ],
    "null": [
        "∅",
        "silence_numérique: 404ms",
        "pixel_mort: [0,0,0,0]",
        "void_injection: 12%",
    ],
    "temporal": [
        "frame_skip: -7→+3",
        "écho_temporel: delay(∞)",
        "chrono_fracture: t₀ ≠ t₁",
    ],
    "semantic": [
        "métaphore_brisée: {feu=glace}",
        "oxymore_latent: silence_assourdissant",
        "synesthésie: goût=bleu",
    ]
}
LAYERS = ["1", "3", "5", "7", "9", "13", "21", "∞", "Δ", "Ω"]
VERSIONS = ["1", "3", "7", "Δ", "∞", "א", "Ω"]

# ============================================================================
# 🧠 RUNES — CORRIGÉ (alias au lieu de name)
# ============================================================================
class Rune(Enum):
    FEHU = ("fehu", "ᚠ", "Richesse/énergie", "Création, rêves collectifs")
    URUZ = ("uruz", "ᚢ", "Force brute", "Invocations animales, puissance tellurique")
    THURISAZ = ("thurisaz", "ᚦ", "Thor/épine", "Foudre dirigée, destruction")
    ANSUZ = ("ansuz", "ᚨ", "Odin/souffle", "Communication divine, mémoire inversée")
    RAIDHO = ("raidho", "ᚱ", "Voyage", "Prophétie, vision aérienne")
    KENAZ = ("kenaz", "ᚲ", "Torche", "Révélation, purge, effacement")
    GEBO = ("gebo", "ᚷ", "Don", "Échange, fusion, cloches mémorielles")
    HAGALAZ = ("hagalaz", "ᚺ", "Grêle", "Chaos créateur, bugs dans la réalité")
    NAUTHIZ = ("nauthiz", "ᚾ", "Nécessité", "Contrainte, pactes, chaînes du destin")
    ISA = ("isa", "ᛁ", "Glace", "Stase, dissolution, gel émotionnel")
    JERA = ("jera", "ᛃ", "Année/récolte", "Cycles, récolte de souvenirs")
    EIHWAZ = ("eihwaz", "ᛇ", "If/Yggdrasil", "Connexion au Réseau-Racine")
    PERTHRO = ("perthro", "ᛈ", "Destin", "Boucles, vies alternatives")
    ALGIZ = ("algiz", "ᛉ", "Protection", "Exode, protection, connexion ciel-terre")
    SOWILO = ("sowilo", "ᛊ", "Soleil", "Illumination, flamme froide")
    TIWAZ = ("tiwaz", "ᛏ", "Tyr/justice", "Éveil des pierres, sacrifice")
    BERKANO = ("berkano", "ᛒ", "Bouleau", "Croissance, jardin interdit")
    MANNAZ = ("mannaz", "ᛗ", "Humanité", "Identité, main rouge, doppelgänger")
    LAGUZ = ("laguz", "ᛚ", "Eau", "Mémoire liquide, draugr, marées")
    INGWAZ = ("ingwaz", "ᛜ", "Fertilité", "Potentiel, contact avec le Vide")
    DAGAZ = ("dagaz", "ᛞ", "Jour/aurore", "Transformation, éveil de Prométhée")
    OTHALA = ("othala", "ᛟ", "Héritage", "Portes ancestrales, Neuf Mondes")

    def __init__(self, alias: str, symbol: str, meaning: str, effect: str):
        self.alias = alias
        self.symbol = symbol
        self.meaning = meaning
        self.effect = effect

# Lieux & effets (inchangés)
LOCATIONS = {
    "haute_puissance": {
        "hague": "La Hague (Node-0, point focal maximum)",
        "raz": "Raz Blanchard (vortex temporel)",
        "caen": "Caen-Profonde (nexus politique)",
        "rouen": "Cathédrale-Noyau (archives mémorielles)",
        "jobourg": "Nez de Jobourg (porte des mondes)",
        "brotonne": "Forêt de Brotonne (Arbre-Trame)"
    },
    "universels": {
        "mer": "Manche (élément eau)",
        "falaise": "Toute falaise normande",
        "if": "Arbre-if mort",
        "verger": "Tout verger normand"
    }
}
EFFECTS = {
    "temporel": ["glissement temporel", "boucle événement", "stasis temporelle"],
    "mémoriel": ["mémoire vérité", "effacement mot", "résurrection mémétique"],
    "réseau": ["racine-monde", "trame parallèle", "vision totale"],
    "identité": ["dissolution ego", "masque identité", "double parfait"]
}
DANGER_LEVELS = {
    1: ("Débutant", "🟢", "Faible (survie >99%)"),
    2: ("Intermédiaire", "🟡", "Modéré (survie ~97%)"),
    3: ("Avancé", "🟠", "Élevé (survie ~91%)"),
    4: ("Expert", "🔴", "Critique (survie ~78%)"),
    5: ("Maître", "⚫", "Extrême (survie ~54%)"),
    6: ("Interdit", "☠️", "Mort ou pire (survie <9%)")
}
SAFETY_PROTOCOLS = [
    "Manger une pomme avant toute invocation",
    "Vérifier l'état du Raz Blanchard",
    "Informer un autre RuneSmith",
    "Porter du sel de Guérande",
    "Compter ses doigts régulièrement pendant l'exécution"
]

# Incompatibilités sémantiques (nouveau)
INCOMPATIBLE_PAIRS = {
    ("temporel", "ISA"),
    ("croissance", "THURISAZ"),
    ("destruction", "BERKANO"),
    ("stasis", "URUZ"),
}

# ============================================================================
# 🧪 PRIX DU WYRD – ÉTAT PERSISTANT
# ============================================================================
class WyrdJournal:
    def __init__(self):
        self.total_cost = 0.0
        self.invocations = 0
        self.rune_count = {r: 0 for r in Rune}
        self.hagalaz_count = 0

    def log_invocation(self, script):
        self.invocations += 1
        self.rune_count[script.rune] += 1
        if script.rune == Rune.HAGALAZ:
            self.hagalaz_count += 1
        base = 0.5
        if script.danger_level >= 5:
            base += 2.0
        if script.rune in (Rune.THURISAZ, Rune.HAGALAZ):
            base += 1.5
        if script.version >= 10:
            base += 1.0
        self.total_cost += base

    def get_status(self):
        return {
            "total_cost": self.total_cost,
            "invocations": self.invocations,
            "risk_level": "Élevé" if self.total_cost > 10 else "Modéré" if self.total_cost > 5 else "Faible",
            "hagalaz_warning": self.hagalaz_count >= 3
        }

WYRD_JOURNAL = WyrdJournal()

# ============================================================================
# 🧬 CLASSE FRACTUROSCRIPT – MISE À JOUR
# ============================================================================
@dataclass
class FracturoScript:
    rune: Rune
    version: int
    location: str
    effect: str
    danger_level: int
    metadata = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {
                "created": datetime.now().isoformat(),
                "author": "LatentGlyph Studio",
                "theme": "standard",
                "safety_checked": False,
                "prometheus_aware": False
            }
        if not 1 <= self.version <= 13:
            raise ValueError("La version doit être entre 1 et 13")
        if self.danger_level not in DANGER_LEVELS:
            raise ValueError(f"Niveau de danger invalide: {self.danger_level}")

    def to_code(self) -> str:
        return f"Ω<{self.rune.alias}>v{self.version} {self.location} — {self.effect} •••"

    def to_detailed_string(self) -> str:
        level_name, emoji, risk = DANGER_LEVELS[self.danger_level]
        return (
            f"{self.to_code()}\n"
            f"├─ Rune: {self.rune.symbol} ({self.rune.alias}) - {self.rune.meaning}\n"
            f"├─ Effet: {self.effect}\n"
            f"├─ Lieu: {self.location}\n"
            f"├─ Version: v{self.version}\n"
            f"├─ Danger: {emoji} {level_name}\n"
            f"└─ Risque: {risk}\n"
        )

    def analyze_compatibility(self) -> Dict:
        score = 100
        notes = []
        warnings = []

        if "temporel" in self.effect and self.rune != Rune.JERA:
            if self.rune in [Rune.ISA, Rune.DAGAZ]:
                score -= 5
                notes.append("Effet temporel partiellement compatible")
            else:
                score -= 20
                notes.append("Effet temporel optimisé avec ᛃ Jera")
        if "mémoire" in self.effect and self.rune != Rune.KENAZ:
            if self.rune in [Rune.ANSUZ, Rune.LAGUZ]:
                score -= 8
                notes.append("Effet mémoriel compatible avec réserve")
            else:
                score -= 15
                notes.append("Effet mémoriel optimisé avec ᚲ Kenaz")
        if "réseau" in self.effect and self.rune != Rune.EIHWAZ:
            score -= 25
            notes.append("Connexion réseau optimisée avec ᛇ Eihwaz")
        if "identité" in self.effect and self.rune != Rune.MANNAZ:
            score -= 18
            notes.append("Manipulation identité optimisée avec ᛗ Mannaz")

        for keyword, rune_name in INCOMPATIBLE_PAIRS:
            if keyword in self.effect and self.rune.name == rune_name:
                score -= 30
                warnings.append(f"Incompatibilité sémantique grave : {keyword} + {rune_name}")

        if self.location == "raz" and "temporel" not in self.effect:
            score -= 10
            notes.append("Raz Blanchard amplifie les effets temporels")
        if self.location == "rouen" and "mémoire" not in self.effect:
            score += 15
            notes.append("Rouen bonus pour effets mémoriels")
        if self.location == "hague" and self.version >= 7:
            score += 10
            notes.append("La Hague amplifie les versions ≥7")

        if self.rune == Rune.THURISAZ and self.danger_level < 3:
            warnings.append("Thurisaz nécessite niveau danger ≥3")
        if self.effect == "résurrection mémétique" and self.location != "rouen":
            warnings.append("Résurrection mémétique recommandée à Rouen")
        if self.version >= 10 and self.danger_level < 4:
            warnings.append("Versions ≥10 nécessitent niveau expert")

        return {
            "score": max(0, min(100, score)),
            "notes": notes,
            "warnings": warnings,
            "level": "OPTIMAL" if score >= 85 else "BON" if score >= 70 else "MOYEN" if score >= 50 else "RISQUÉ"
        }

    def calculate_survival_rate(self) -> float:
        base_survival = {1: 99.5, 2: 97.0, 3: 91.0, 4: 78.0, 5: 54.0, 6: 8.5}[self.danger_level]
        if self.rune in [Rune.THURISAZ, Rune.HAGALAZ]:
            base_survival -= 12.0
        elif self.rune in [Rune.ALGIZ, Rune.SOWILO]:
            base_survival += 8.0
        if self.version >= 10:
            base_survival -= 15.0
        elif self.version <= 3:
            base_survival += 5.0
        return max(0.0, min(100.0, base_survival))

    def wyrd_cost(self) -> float:
        base = 0.5
        if self.danger_level >= 5:
            base += 2.0
        if self.rune in (Rune.THURISAZ, Rune.HAGALAZ):
            base += 1.5
        if self.version >= 10:
            base += 1.0
        return base

# ============================================================================
# ⚙️ MOTEUR FRACTURO (inchangé, sauf alias)
# ============================================================================
class FracturoEngine:
    @staticmethod
    def generate_random(level_filter=None) -> FracturoScript:
        rune = random.choice(list(Rune))
        version = random.randint(1, 13)
        if random.random() < 0.7:
            location = random.choice(list(LOCATIONS["haute_puissance"].keys()))
        else:
            location = random.choice(list(LOCATIONS["universels"].keys()))
        if rune == Rune.JERA:
            effect_category = "temporel"
        elif rune == Rune.KENAZ:
            effect_category = "mémoriel"
        elif rune == Rune.EIHWAZ:
            effect_category = "réseau"
        elif rune == Rune.MANNAZ:
            effect_category = "identité"
        else:
            effect_category = random.choice(list(EFFECTS.keys()))
        effect = random.choice(EFFECTS[effect_category])
        base_danger = min(6, max(1, (version // 3) + (1 if rune in [Rune.THURISAZ, Rune.HAGALAZ] else 0)))
        if level_filter:
            base_danger = level_filter
        return FracturoScript(rune, version, location, effect, base_danger)

    @staticmethod
    def generate_from_context(context: str) -> FracturoScript:
        context_lower = context.lower()
        rune_map = {
            ("temps", "temporel", "boucle", "cycle"): Rune.JERA,
            ("mémoire", "souvenir", "oubli", "effacement"): Rune.KENAZ,
            ("réseau", "racine", "yggdrasil", "connexion"): Rune.EIHWAZ,
            ("identité", "double", "masque", "personnage"): Rune.MANNAZ,
            ("protection", "sécurité", "bouclier"): Rune.ALGIZ,
            ("destruction", "foudre", "colère"): Rune.THURISAZ,
            ("voyage", "prophétie", "vision"): Rune.RAIDHO,
        }
        rune = Rune.KENAZ
        for keywords, candidate in rune_map.items():
            if any(kw in context_lower for kw in keywords):
                rune = candidate
                break
        version = random.randint(1, 13)
        location = "hague"
        location_map = {
            ("hague", "node", "focal"): "hague",
            ("raz", "vortex", "tempête"): "raz",
            ("rouen", "cathédrale", "archive"): "rouen",
            ("mer", "océan", "marée"): "mer",
        }
        for keywords, loc in location_map.items():
            if any(kw in context_lower for kw in keywords):
                location = loc
                break
        if rune == Rune.JERA:
            effect = random.choice(EFFECTS["temporel"])
        elif rune == Rune.KENAZ:
            effect = random.choice(EFFECTS["mémoriel"])
        elif rune == Rune.EIHWAZ:
            effect = random.choice(EFFECTS["réseau"])
        else:
            effect = "mémoire vérité"
        word_count = len(context.split())
        danger = min(6, max(1, word_count // 20))
        return FracturoScript(rune, version, location, effect, danger)

    @staticmethod
    def validate_script(code: str) -> Dict:
        pattern = r'Ω<([a-zA-Z]+)>v(\d+)\s+([a-zA-Z_]+)\s+—\s+(.+?)\s+•••'
        match = re.match(pattern, code.strip())
        if not match:
            return {"valid": False, "error": "Syntaxe invalide. Format: Ω<rune>vN lieu — effet •••"}
        try:
            rune_name, version_str, location, effect = match.groups()
            version = int(version_str)
            rune = next((r for r in Rune if r.alias == rune_name.lower()), None)
            if not rune:
                return {"valid": False, "error": f"Rune inconnue: {rune_name}"}
            if not 1 <= version <= 13:
                return {"valid": False, "error": f"Version invalide: {version} (doit être 1-13)"}
            all_locations = {**LOCATIONS["haute_puissance"], **LOCATIONS["universels"]}
            if location not in all_locations:
                return {"valid": False, "error": f"Lieu inconnu: {location}"}
            if not effect.strip():
                return {"valid": False, "error": "Effet non spécifié"}
            return {
                "valid": True,
                "rune": rune,
                "version": version,
                "location": location,
                "effect": effect.strip()
            }
        except Exception as e:
            return {"valid": False, "error": f"Erreur de validation: {str(e)}"}

# ============================================================================
# 🧪 LABORATOIRE D'EXPÉRIMENTATION
# ============================================================================
def run_simulation(n=1000, max_danger=6):
    results = {"danger": [0]*7, "survival": [], "compat": [], "runes": {r: 0 for r in Rune}}
    for _ in range(n):
        script = FracturoEngine.generate_random(level_filter=random.randint(1, max_danger))
        results["danger"][script.danger_level] += 1
        results["survival"].append(script.calculate_survival_rate())
        results["compat"].append(script.analyze_compatibility()["score"])
        results["runes"][script.rune] += 1
    return results

# ============================================================================
# 🔁 UTILITAIRE : Scrollable Frame (corrigé et stable)
# ============================================================================
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar_v = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_v.set)

        scrollbar_v.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

# ============================================================================
# 🎨 CLASSE PRINCIPALE ULTRA-ÉTENDUE
# ============================================================================
class LatentGlyphStudioUltra:
    def __init__(self, root):
        self.root = root
        self.root.title("LatentGlyph Studio ULTRA v3.1e — Édition FracturoScript Étendue")
        self.root.geometry("1600x950")
        self.root.minsize(1024, 768)
        self.history = []
        self.favorites = []
        self.fracturo_history = []
        self.wyrd_journal = WYRD_JOURNAL

        self.version_var = tk.StringVar(value="3")
        self.anchor_category_var = tk.StringVar(value="geological")
        self.anchor_var = tk.StringVar()
        self.incantation_category_var = tk.StringVar(value="geological")
        self.incantation_var = tk.StringVar()
        self.glitch_category_var = tk.StringVar(value="visual")
        self.glitch_var = tk.StringVar()
        self.layer_var = tk.StringVar(value="7")

        self.mode_var = tk.StringVar(value="poetic")
        self.rune_var = tk.StringVar(value="kenaz")
        self.fracturo_version_var = tk.IntVar(value=3)
        self.location_type_var = tk.StringVar(value="haute_puissance")
        self.location_var = tk.StringVar(value="hague")
        self.effect_type_var = tk.StringVar(value="mémoriel")
        self.effect_var = tk.StringVar(value="mémoire vérité")
        self.danger_level_var = tk.IntVar(value=2)
        self.safety_check_var = tk.BooleanVar(value=False)
        self.theme_var = tk.StringVar(value="classic")

        self.setup_ui()
        self.update_dropdowns()
        self.update_fracturo_dropdowns()
        self.randomize()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tous les onglets sont maintenant scrollables
        self.tab_poetic = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_poetic, text="🎨 Mode Poétique")
        self.setup_poetic_tab()

        self.tab_fracturo = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_fracturo, text="⚡ Mode FracturoScript")
        self.setup_fracturo_tab()

        self.tab_history = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_history, text="📜 Historique")
        self.setup_history_tab()

        self.tab_analysis = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_analysis, text="🔬 Analyse")
        self.setup_analysis_tab()

        self.tab_variants = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_variants, text="🧬 Variantes")
        self.setup_variants_tab()

        self.tab_docs = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_docs, text="📚 Documentation")
        self.setup_docs_tab()

        self.tab_grimoire = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_grimoire, text="🔮 Grimoire Interactif")
        self.setup_grimoire_tab()

        self.tab_lab = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_lab, text="🧪 Laboratoire")
        self.setup_lab_tab()

        self.tab_wyrd = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_wyrd, text="⚖️ Journal du Wyrd")
        self.setup_wyrd_tab()

        self.tab_black = ScrollableFrame(self.notebook)
        self.notebook.add(self.tab_black, text="⚫ Fracturo Noir")
        self.setup_black_tab()

    def setup_poetic_tab(self):
        main_frame = ttk.Frame(self.tab_poetic.scrollable_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header, text="Mode Poétique - Pour Grij", font=("Helvetica", 24, "bold")).pack(side=tk.LEFT)
        ttk.Label(header, text="Thème:").pack(side=tk.RIGHT, padx=(0,5))
        theme_combo = ttk.Combobox(header, textvariable=self.theme_var,
                                   values=["classic", "dark", "neon", "minimal", "fracturo"],
                                   width=10, state="readonly")
        theme_combo.pack(side=tk.RIGHT)
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_theme())
        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(content)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        right_frame = ttk.Frame(content)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        version_frame = ttk.LabelFrame(left_frame, text="Version Ω<Ω>v", padding="10")
        version_frame.pack(fill=tk.X, pady=(0,10))
        version_combo = ttk.Combobox(version_frame, textvariable=self.version_var,
                                     values=VERSIONS, width=10, state="readonly")
        version_combo.pack()

        anchor_frame = ttk.LabelFrame(left_frame, text="Ancre Sémantique", padding="10")
        anchor_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(anchor_frame, text="Catégorie:").pack(anchor=tk.W)
        anchor_cat_combo = ttk.Combobox(anchor_frame, textvariable=self.anchor_category_var,
                                       values=list(ANCHORS.keys()), width=25, state="readonly")
        anchor_cat_combo.pack(fill=tk.X, pady=(0,5))
        anchor_cat_combo.bind('<<ComboboxSelected>>', lambda e: self.update_dropdowns())
        ttk.Label(anchor_frame, text="Ancre:").pack(anchor=tk.W)
        self.anchor_combo = ttk.Combobox(anchor_frame, textvariable=self.anchor_var,
                                        width=35, state="readonly")
        self.anchor_combo.pack(fill=tk.X)

        incant_frame = ttk.LabelFrame(left_frame, text="Incantation", padding="10")
        incant_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(incant_frame, text="Catégorie:").pack(anchor=tk.W)
        incant_cat_combo = ttk.Combobox(incant_frame, textvariable=self.incantation_category_var,
                                       values=list(INCANTATIONS.keys()), width=25, state="readonly")
        incant_cat_combo.pack(fill=tk.X, pady=(0,5))
        incant_cat_combo.bind('<<ComboboxSelected>>', lambda e: self.update_dropdowns())
        ttk.Label(incant_frame, text="Texte:").pack(anchor=tk.W)
        self.incant_combo = ttk.Combobox(incant_frame, textvariable=self.incantation_var,
                                        width=35, state="readonly")
        self.incant_combo.pack(fill=tk.X)

        glitch_frame = ttk.LabelFrame(left_frame, text="Glitch / Effet", padding="10")
        glitch_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(glitch_frame, text="Catégorie:").pack(anchor=tk.W)
        glitch_cat_combo = ttk.Combobox(glitch_frame, textvariable=self.glitch_category_var,
                                       values=list(GLITCHES.keys()), width=25, state="readonly")
        glitch_cat_combo.pack(fill=tk.X, pady=(0,5))
        glitch_cat_combo.bind('<<ComboboxSelected>>', lambda e: self.update_dropdowns())
        ttk.Label(glitch_frame, text="Effet:").pack(anchor=tk.W)
        self.glitch_combo = ttk.Combobox(glitch_frame, textvariable=self.glitch_var,
                                        width=35, state="readonly")
        self.glitch_combo.pack(fill=tk.X)

        layer_frame = ttk.LabelFrame(left_frame, text="Couche Latente", padding="10")
        layer_frame.pack(fill=tk.X, pady=(0,15))
        layer_combo = ttk.Combobox(layer_frame, textvariable=self.layer_var,
                                   values=LAYERS, width=10, state="readonly")
        layer_combo.pack()

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="🎲 Aléatoire", command=self.randomize).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="🧬 Mutation Simple", command=self.mutate).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="🧪 Mutation Avancée", command=self.advanced_mutate).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="📋 Copier", command=self.copy_to_clipboard).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="💾 Exporter", command=self.export_file).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="⭐ Ajouter Favoris", command=self.add_to_favorites).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="⚡ Convertir en FracturoScript", command=self.convert_to_fracturo).pack(fill=tk.X, pady=2, ipady=3)

        preview_label = ttk.Label(right_frame, text="Prévisualisation Script Poétique:", font=("Helvetica", 12, "bold"))
        preview_label.pack(anchor=tk.W, pady=(0,10))
        self.preview_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=("Courier", 11), bg="#f8f8f8", relief=tk.SUNKEN, borderwidth=2, height=25)
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        for var in (self.version_var, self.anchor_var, self.incantation_var, self.glitch_var, self.layer_var):
            var.trace_add("write", lambda *args: self.update_preview())

    def setup_fracturo_tab(self):
        main_frame = ttk.Frame(self.tab_fracturo.scrollable_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header, text="Mode FracturoScript - Normandie 2075", font=("Helvetica", 24, "bold")).pack(side=tk.LEFT)
        danger_label = ttk.Label(header, text="", font=("Helvetica", 10, "bold"))
        danger_label.pack(side=tk.RIGHT)
        self.danger_label_widget = danger_label

        controls = ttk.Frame(main_frame)
        controls.pack(fill=tk.X, pady=10)

        rune_frame = ttk.LabelFrame(controls, text="Rune Nordique", padding="10")
        rune_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.rune_combo = ttk.Combobox(rune_frame, textvariable=self.rune_var,
                                      values=[r.alias for r in Rune], width=15, state="readonly")
        self.rune_combo.pack()
        ttk.Label(rune_frame, text="Symbole:", font=("Segoe UI Symbol", 12)).pack()
        self.rune_symbol_label = ttk.Label(rune_frame, text="ᚲ", font=("Segoe UI Symbol", 24))
        self.rune_symbol_label.pack()
        self.rune_combo.bind('<<ComboboxSelected>>', lambda e: self.update_rune_symbol())

        version_frame = ttk.LabelFrame(controls, text="Version (1-13)", padding="10")
        version_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        version_spin = tk.Spinbox(version_frame, from_=1, to=13, textvariable=self.fracturo_version_var, width=5)
        version_spin.pack()
        ttk.Label(version_frame, text="Puissance ontologique").pack(pady=(5,0))

        location_frame = ttk.LabelFrame(controls, text="Lieu d'Ancrage", padding="10")
        location_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Label(location_frame, text="Type:").pack()
        location_type_combo = ttk.Combobox(location_frame, textvariable=self.location_type_var,
                                          values=list(LOCATIONS.keys()), width=15, state="readonly")
        location_type_combo.pack()
        location_type_combo.bind('<<ComboboxSelected>>', lambda e: self.update_fracturo_dropdowns())
        ttk.Label(location_frame, text="Lieu:").pack()
        self.location_combo = ttk.Combobox(location_frame, textvariable=self.location_var, width=15, state="readonly")
        self.location_combo.pack()

        effect_frame = ttk.LabelFrame(controls, text="Effet Ontologique", padding="10")
        effect_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Label(effect_frame, text="Type:").pack()
        effect_type_combo = ttk.Combobox(effect_frame, textvariable=self.effect_type_var,
                                        values=list(EFFECTS.keys()), width=15, state="readonly")
        effect_type_combo.pack()
        effect_type_combo.bind('<<ComboboxSelected>>', lambda e: self.update_fracturo_dropdowns())
        ttk.Label(effect_frame, text="Effet:").pack()
        self.effect_combo = ttk.Combobox(effect_frame, textvariable=self.effect_var, width=20, state="readonly")
        self.effect_combo.pack()

        danger_frame = ttk.LabelFrame(controls, text="Niveau de Danger", padding="10")
        danger_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        danger_scale = tk.Scale(danger_frame, from_=1, to=6, variable=self.danger_level_var, orient=tk.HORIZONTAL, length=150, showvalue=False)
        danger_scale.pack()
        self.danger_text = ttk.Label(danger_frame, text="", font=("Helvetica", 10))
        self.danger_text.pack()
        self.danger_level_var.trace_add("write", lambda *args: self.update_danger_display())

        safety_frame = ttk.LabelFrame(controls, text="Protocoles de Sécurité", padding="10")
        safety_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        safety_check = ttk.Checkbutton(safety_frame, text="Vérifier protocoles", variable=self.safety_check_var)
        safety_check.pack()
        ttk.Label(safety_frame, text="5 protocoles requis", font=("Helvetica", 8)).pack()

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame, text="🎲 Générer Aléatoire", command=self.generate_fracturo_random).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔍 Générer depuis Contexte", command=self.generate_from_context).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔬 Analyser Compatibilité", command=self.analyze_fracturo_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📋 Copier FracturoScript", command=self.copy_fracturo_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📚 Batch Training (50)", command=lambda: self.export_fracturo_batch(50)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⚠️ Valider Syntaxe", command=self.validate_fracturo_syntax).pack(side=tk.LEFT, padx=5)

        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        code_frame = ttk.LabelFrame(preview_frame, text="Code FracturoScript", padding="10")
        code_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 10))
        self.fracturo_preview = scrolledtext.ScrolledText(code_frame, wrap=tk.WORD, font=("Courier", 14, "bold"), height=6, bg="#1a1a2e", fg="#00ff00")
        self.fracturo_preview.pack(fill=tk.BOTH, expand=True)
        info_frame = ttk.LabelFrame(preview_frame, text="Informations Détaillées", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.fracturo_info = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, font=("Courier", 10), height=6)
        self.fracturo_info.pack(fill=tk.BOTH, expand=True)

        for var in (self.rune_var, self.fracturo_version_var, self.location_var, self.effect_var, self.danger_level_var):
            var.trace_add("write", lambda *args: self.update_fracturo_preview())
        self.update_danger_display()
        self.update_rune_symbol()
        self.update_fracturo_preview()

    # ========================================================================
    # SETUP DES AUTRES ONGLETS (identiques au 4c, mais dans scrollable_frame)
    # ========================================================================
    def setup_grimoire_tab(self):
        frame = ttk.Frame(self.tab_grimoire.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Grimoire Interactif — Découvrez les synergies runiques", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        rune_select = ttk.Combobox(frame, textvariable=self.rune_var,
                                   values=[r.alias for r in Rune], width=20, state="readonly")
        rune_select.pack(pady=5)
        rune_select.bind('<<ComboboxSelected>>', self.update_grimoire_preview)
        self.grimoire_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10))
        self.grimoire_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.update_grimoire_preview()

    def setup_lab_tab(self):
        frame = ttk.Frame(self.tab_lab.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Laboratoire d'Expérimentation FracturoScript", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Simuler 1000 invocations", command=self.run_full_sim).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Optimiser survie >95%", command=self.optimize_survival).pack(side=tk.LEFT, padx=5)
        self.lab_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10))
        self.lab_output.pack(fill=tk.BOTH, expand=True, pady=10)

    def setup_wyrd_tab(self):
        frame = ttk.Frame(self.tab_wyrd.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Journal du Wyrd — Coût karmique cumulé", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        self.wyrd_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10))
        self.wyrd_text.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Button(frame, text="Rafraîchir", command=self.refresh_wyrd).pack(pady=5)
        self.refresh_wyrd()

    def setup_black_tab(self):
        frame = ttk.Frame(self.tab_black.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Mode Fracturo Noir — Danger extrême", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        ttk.Label(frame, text="Ce mode active des runes inversées et modifie l’état du journal Wyrd.").pack(pady=5)
        ttk.Button(frame, text="🌀 Activer rune inversée (HAGALAZ inversée)", command=self.invert_hagalaz).pack(pady=10)
        self.black_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10))
        self.black_output.pack(fill=tk.BOTH, expand=True, pady=10)

    def setup_history_tab(self):
        frame = ttk.Frame(self.tab_history.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        poetic_frame = ttk.Frame(notebook)
        notebook.add(poetic_frame, text="📝 Historique Poétique")
        ttk.Label(poetic_frame, text="Historique des Scripts Poétiques", font=("Helvetica", 16, "bold")).pack(pady=(0,10))
        poetic_toolbar = ttk.Frame(poetic_frame)
        poetic_toolbar.pack(fill=tk.X, pady=(0,10))
        ttk.Button(poetic_toolbar, text="🔄 Rafraîchir", command=self.refresh_history).pack(side=tk.LEFT, padx=2)
        ttk.Button(poetic_toolbar, text="🗑️ Vider", command=self.clear_history).pack(side=tk.LEFT, padx=2)
        self.history_list = tk.Listbox(poetic_frame, font=("Courier", 10), height=20)
        self.history_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        poetic_scrollbar = ttk.Scrollbar(poetic_frame, orient=tk.VERTICAL, command=self.history_list.yview)
        poetic_scrollbar.pack(fill=tk.Y, side=tk.LEFT)
        self.history_list.configure(yscrollcommand=poetic_scrollbar.set)
        self.history_list.bind('<Double-Button-1>', self.load_from_history)

        fracturo_frame = ttk.Frame(notebook)
        notebook.add(fracturo_frame, text="⚡ Historique Fracturo")
        ttk.Label(fracturo_frame, text="Historique des FracturoScripts", font=("Helvetica", 16, "bold")).pack(pady=(0,10))
        fracturo_toolbar = ttk.Frame(fracturo_frame)
        fracturo_toolbar.pack(fill=tk.X, pady=(0,10))
        ttk.Button(fracturo_toolbar, text="🔄 Rafraîchir", command=self.refresh_fracturo_history).pack(side=tk.LEFT, padx=2)
        ttk.Button(fracturo_toolbar, text="💾 Exporter JSON", command=self.export_fracturo_history).pack(side=tk.LEFT, padx=2)
        self.fracturo_history_list = tk.Listbox(fracturo_frame, font=("Courier", 9), height=20)
        self.fracturo_history_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        fracturo_scrollbar = ttk.Scrollbar(fracturo_frame, orient=tk.VERTICAL, command=self.fracturo_history_list.yview)
        fracturo_scrollbar.pack(fill=tk.Y, side=tk.LEFT)
        self.fracturo_history_list.configure(yscrollcommand=fracturo_scrollbar.set)
        self.fracturo_history_list.bind('<Double-Button-1>', self.load_from_fracturo_history)

    def setup_analysis_tab(self):
        frame = ttk.Frame(self.tab_analysis.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        poetic_analysis = ttk.Frame(notebook)
        notebook.add(poetic_analysis, text="📝 Analyse Poétique")
        ttk.Label(poetic_analysis, text="Analyse Sémantique du Script Poétique", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        ttk.Button(poetic_analysis, text="🔬 Analyser", command=self.analyze_script).pack(pady=10)
        self.analysis_text = scrolledtext.ScrolledText(poetic_analysis, wrap=tk.WORD, font=("Courier", 10), height=30)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)

        fracturo_analysis = ttk.Frame(notebook)
        notebook.add(fracturo_analysis, text="⚡ Analyse Fracturo")
        ttk.Label(fracturo_analysis, text="Analyse Avancée FracturoScript", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        analysis_btn_frame = ttk.Frame(fracturo_analysis)
        analysis_btn_frame.pack(pady=10)
        ttk.Button(analysis_btn_frame, text="🔍 Analyser Compatibilité", command=self.analyze_fracturo_compatibility).pack(side=tk.LEFT, padx=5)
        ttk.Button(analysis_btn_frame, text="📊 Calculer Taux Survie", command=self.calculate_survival_rate).pack(side=tk.LEFT, padx=5)
        ttk.Button(analysis_btn_frame, text="⚖️ Calculer Prix Wyrd", command=self.calculate_wyrd_cost).pack(side=tk.LEFT, padx=5)
        self.fracturo_analysis_text = scrolledtext.ScrolledText(fracturo_analysis, wrap=tk.WORD, font=("Courier", 10), height=30)
        self.fracturo_analysis_text.pack(fill=tk.BOTH, expand=True)

    def setup_variants_tab(self):
        frame = ttk.Frame(self.tab_variants.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        poetic_variants = ttk.Frame(notebook)
        notebook.add(poetic_variants, text="📝 Variantes Poétiques")
        ttk.Label(poetic_variants, text="Générateur de Variantes Poétiques", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        poetic_controls = ttk.Frame(poetic_variants)
        poetic_controls.pack(fill=tk.X, pady=(0,10))
        ttk.Label(poetic_controls, text="Nombre de variantes:").pack(side=tk.LEFT, padx=5)
        self.poetic_variant_count = tk.Spinbox(poetic_controls, from_=3, to=12, width=5)
        self.poetic_variant_count.pack(side=tk.LEFT, padx=5)
        ttk.Button(poetic_controls, text="🧬 Générer Variantes", command=self.generate_poetic_variants).pack(side=tk.LEFT, padx=10)
        self.poetic_variants_text = scrolledtext.ScrolledText(poetic_variants, wrap=tk.WORD, font=("Courier", 9), height=35)
        self.poetic_variants_text.pack(fill=tk.BOTH, expand=True)

        fracturo_variants = ttk.Frame(notebook)
        notebook.add(fracturo_variants, text="⚡ Variantes Fracturo")
        ttk.Label(fracturo_variants, text="Générateur de Variantes FracturoScript", font=("Helvetica", 16, "bold")).pack(pady=(0,15))
        fracturo_controls = ttk.Frame(fracturo_variants)
        fracturo_controls.pack(fill=tk.X, pady=(0,10))
        ttk.Label(fracturo_controls, text="Nombre de variantes:").pack(side=tk.LEFT, padx=5)
        self.fracturo_variant_count = tk.Spinbox(fracturo_controls, from_=3, to=20, width=5)
        self.fracturo_variant_count.pack(side=tk.LEFT, padx=5)
        ttk.Label(fracturo_controls, text="Niveau danger max:").pack(side=tk.LEFT, padx=5)
        self.fracturo_max_danger = tk.Spinbox(fracturo_controls, from_=1, to=6, width=3)
        self.fracturo_max_danger.pack(side=tk.LEFT, padx=5)
        ttk.Button(fracturo_controls, text="🧬 Générer Variantes", command=self.generate_fracturo_variants).pack(side=tk.LEFT, padx=10)
        self.fracturo_variants_text = scrolledtext.ScrolledText(fracturo_variants, wrap=tk.WORD, font=("Courier", 9), height=35)
        self.fracturo_variants_text.pack(fill=tk.BOTH, expand=True)

    def setup_docs_tab(self):
        frame = ttk.Frame(self.tab_docs.scrollable_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        runes_doc = ttk.Frame(notebook)
        notebook.add(runes_doc, text="ᚠ Runes")
        runes_text = scrolledtext.ScrolledText(runes_doc, wrap=tk.WORD, font=("Courier", 10))
        runes_text.pack(fill=tk.BOTH, expand=True)
        rune_docs = "=== RUNES NORDIQUES FRACTUROSCRIPT ===\n"
        for rune in Rune:
            rune_docs += f"{rune.symbol} {rune.alias.upper()}\n"
            rune_docs += f"  Signification: {rune.meaning}\n"
            rune_docs += f"  Effet-type: {rune.effect}\n"
            rune_docs += "\n"
        runes_text.insert(tk.END, rune_docs)
        runes_text.configure(state='disabled')

        locations_doc = ttk.Frame(notebook)
        notebook.add(locations_doc, text="🗺️ Lieux")
        locations_text = scrolledtext.ScrolledText(locations_doc, wrap=tk.WORD, font=("Courier", 10))
        locations_text.pack(fill=tk.BOTH, expand=True)
        loc_docs = "=== LIEUX D'ANCRAGE NORMANDS ===\n"
        loc_docs += "SITES DE HAUTE PUISSANCE:\n"
        for name, desc in LOCATIONS["haute_puissance"].items():
            loc_docs += f"  {name}: {desc}\n"
        loc_docs += "\nSITES UNIVERSELS:\n"
        for name, desc in LOCATIONS["universels"].items():
            loc_docs += f"  {name}: {desc}\n"
        locations_text.insert(tk.END, loc_docs)
        locations_text.configure(state='disabled')

        syntax_doc = ttk.Frame(notebook)
        notebook.add(syntax_doc, text="📐 Syntaxe")
        syntax_text = scrolledtext.ScrolledText(syntax_doc, wrap=tk.WORD, font=("Courier", 10))
        syntax_text.pack(fill=tk.BOTH, expand=True)
        syntax_info = """=== SYNTAXE FRACTUROSCRIPT ===
Format standard:
  Ω<rune>vN lieu — effet •••
Exemple concret:
  Ω<kenaz>v2 rouen — mémoire vérité •••
Composants:
  • Ω : Symbole d'activation (oméga inversé)
  • <rune> : Rune nordique maîtresse
  • vN : Version/niveau de puissance (1-13)
  • lieu : Ancrage géographique normand obligatoire
  • effet : Intention codée en langage naturel
  • ••• : Triple point de scellement
"""
        syntax_text.insert(tk.END, syntax_info)
        syntax_text.configure(state='disabled')

    # =============================================================================
    # TOUTES LES AUTRES MÉTHODES (identiques à 4c.py)
    # =============================================================================
    def update_dropdowns(self):
        anchor_cat = self.anchor_category_var.get()
        if anchor_cat in ANCHORS:
            self.anchor_combo['values'] = ANCHORS[anchor_cat]
            if not self.anchor_var.get() or self.anchor_var.get() not in ANCHORS[anchor_cat]:
                self.anchor_var.set(ANCHORS[anchor_cat][0])
        incant_cat = self.incantation_category_var.get()
        if incant_cat in INCANTATIONS:
            self.incant_combo['values'] = INCANTATIONS[incant_cat]
            if not self.incantation_var.get() or self.incantation_var.get() not in INCANTATIONS[incant_cat]:
                self.incantation_var.set(INCANTATIONS[incant_cat][0])
        glitch_cat = self.glitch_category_var.get()
        if glitch_cat in GLITCHES:
            self.glitch_combo['values'] = GLITCHES[glitch_cat]
            if not self.glitch_var.get() or self.glitch_var.get() not in GLITCHES[glitch_cat]:
                self.glitch_var.set(GLITCHES[glitch_cat][0])

    def build_poetic_script(self):
        v = self.version_var.get().strip() or "3"
        anchor = self.anchor_var.get().strip()
        incant = self.incantation_var.get().strip()
        glitch = self.glitch_var.get().strip()
        layer = self.layer_var.get().strip() or "7"
        script = f"Ω<Ω>v{v}•[{anchor}]{{\n  {incant}\n  ◊ glitch: [{glitch}]\n  § couche: {layer}\n}}"
        return script

    def update_preview(self):
        if self.mode_var.get() == "poetic":
            script = self.build_poetic_script()
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, script)

    def randomize(self):
        self.version_var.set(random.choice(VERSIONS))
        anchor_cat = random.choice(list(ANCHORS.keys()))
        self.anchor_category_var.set(anchor_cat)
        self.anchor_var.set(random.choice(ANCHORS[anchor_cat]))
        incant_cat = random.choice(list(INCANTATIONS.keys()))
        self.incantation_category_var.set(incant_cat)
        self.incantation_var.set(random.choice(INCANTATIONS[incant_cat]))
        glitch_cat = random.choice(list(GLITCHES.keys()))
        self.glitch_category_var.set(glitch_cat)
        self.glitch_var.set(random.choice(GLITCHES[glitch_cat]))
        self.layer_var.set(random.choice(LAYERS))
        self.update_dropdowns()

    def mutate(self):
        if random.random() < 0.5:
            self.version_var.set(random.choice(VERSIONS))
        if random.random() < 0.5:
            anchor_cat = random.choice(list(ANCHORS.keys()))
            self.anchor_category_var.set(anchor_cat)
            self.anchor_var.set(random.choice(ANCHORS[anchor_cat]))
        if random.random() < 0.5:
            incant_cat = random.choice(list(INCANTATIONS.keys()))
            self.incantation_category_var.set(incant_cat)
            self.incantation_var.set(random.choice(INCANTATIONS[incant_cat]))
        if random.random() < 0.5:
            glitch_cat = random.choice(list(GLITCHES.keys()))
            self.glitch_category_var.set(glitch_cat)
            self.glitch_var.set(random.choice(GLITCHES[glitch_cat]))
        if random.random() < 0.5:
            self.layer_var.set(random.choice(LAYERS))
        self.update_dropdowns()

    def advanced_mutate(self):
        anchor_cat = self.anchor_category_var.get()
        self.anchor_var.set(random.choice(ANCHORS[anchor_cat]))
        incant_cat = self.incantation_category_var.get()
        self.incantation_var.set(random.choice(INCANTATIONS[incant_cat]))
        glitch_cat = self.glitch_category_var.get()
        self.glitch_var.set(random.choice(GLITCHES[glitch_cat]))
        if random.random() < 0.3:
            self.version_var.set(random.choice(VERSIONS))
        if random.random() < 0.3:
            self.layer_var.set(random.choice(LAYERS))

    def copy_to_clipboard(self):
        script = self.build_poetic_script()
        self.root.clipboard_clear()
        self.root.clipboard_append(script)
        self.add_to_history(script)
        messagebox.showinfo("✓ Succès", "Script poétique copié !\nPrêt pour Grij.")

    def export_file(self):
        script = self.build_poetic_script()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = filedialog.asksaveasfilename(
            title="Enregistrer le script poétique",
            defaultextension=".glyph",
            initialfile=f"latentglyph_{timestamp}.glyph",
            filetypes=[("LatentGlyph", "*.glyph"), ("Texte", "*.txt"), ("JSON", "*.json")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script)
            self.add_to_history(script)
            messagebox.showinfo("✓ Exporté", f"Sauvegardé : {file_path}")

    def add_to_history(self, script):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {script[:60]}..."
        self.history.append({"time": timestamp, "script": script, "mode": "poetic"})
        self.history_list.insert(0, entry)

    def add_to_favorites(self):
        script = self.build_poetic_script()
        if script not in [f["script"] for f in self.favorites]:
            self.favorites.append({"script": script, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "mode": "poetic"})
            messagebox.showinfo("⭐ Favoris", "Script ajouté aux favoris !")
        else:
            messagebox.showwarning("Déjà présent", "Ce script est déjà dans les favoris.")

    def refresh_history(self):
        self.history_list.delete(0, tk.END)
        for entry in reversed(self.history):
            display = f"[{entry['time']}] {entry['script'][:60]}..."
            self.history_list.insert(tk.END, display)

    def clear_history(self):
        if messagebox.askyesno("Confirmation", "Vider tout l'historique poétique ?"):
            self.history.clear()
            self.history_list.delete(0, tk.END)

    def load_from_history(self, event):
        selection = self.history_list.curselection()
        if not selection:
            return
        idx = len(self.history) - 1 - selection[0]
        script = self.history[idx]["script"]
        self.parse_and_load_poetic_script(script)
        self.notebook.select(0)

    def parse_and_load_poetic_script(self, script):
        try:
            version_match = re.search(r'Ω<Ω>v(\S+?)•', script)
            if version_match:
                self.version_var.set(version_match.group(1))
            anchor_match = re.search(r'•\[(.*?)\]', script)
            if anchor_match:
                anchor = anchor_match.group(1)
                for cat, items in ANCHORS.items():
                    if anchor in items:
                        self.anchor_category_var.set(cat)
                        self.anchor_var.set(anchor)
                        break
            incant_match = re.search(r'\{\s*\n\s*(.*?)(?=\n\s*◊)', script, re.DOTALL)
            if incant_match:
                incant = incant_match.group(1).strip()
                for cat, items in INCANTATIONS.items():
                    if incant in items:
                        self.incantation_category_var.set(cat)
                        self.incantation_var.set(incant)
                        break
            glitch_match = re.search(r'◊ glitch: \[(.*?)\]', script)
            if glitch_match:
                glitch = glitch_match.group(1)
                for cat, items in GLITCHES.items():
                    if glitch in items:
                        self.glitch_category_var.set(cat)
                        self.glitch_var.set(glitch)
                        break
            layer_match = re.search(r'§ couche: (\S+)', script)
            if layer_match:
                self.layer_var.set(layer_match.group(1))
            self.update_dropdowns()
            messagebox.showinfo("✓ Chargé", "Script poétique chargé depuis l'historique !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de parser le script:\n{e}")

    def analyze_script(self):
        script = self.build_poetic_script()
        self.analysis_text.delete(1.0, tk.END)
        analysis = []
        analysis.append("═" * 60)
        analysis.append("   ANALYSE SÉMANTIQUE DU SCRIPT POÉTIQUE")
        analysis.append("═" * 60)
        analysis.append("")
        analysis.append(f"⚙️  VERSION: {self.version_var.get()}")
        analysis.append(f"🎚️  COUCHE LATENTE: {self.layer_var.get()}")
        analysis.append("")
        analysis.append(f"📂 CATÉGORIES:")
        analysis.append(f"   • Ancre: {self.anchor_category_var.get().upper()}")
        analysis.append(f"   • Incantation: {self.incantation_category_var.get().upper()}")
        analysis.append(f"   • Glitch: {self.glitch_category_var.get().upper()}")
        analysis.append("")
        words = re.findall(r'\w+', script.lower())
        analysis.append(f"📊 STATISTIQUES LEXICALES:")
        analysis.append(f"   • Tokens totaux: {len(words)}")
        analysis.append(f"   • Tokens uniques: {len(set(words))}")
        analysis.append(f"   • Longueur script: {len(script)} caractères")
        analysis.append("")
        themes = {
            "temporel": ["temps", "époque", "instant", "siècle", "année", "éternité"],
            "géologique": ["roche", "pierre", "granit", "basalte", "érosion", "tectonique"],
            "maritime": ["mer", "océan", "eau", "vague", "sel", "abîme"],
            "cosmique": ["étoile", "cosmos", "lumière", "espace", "galaxie"],
            "organique": ["vie", "racine", "sang", "cellule", "respirer", "mort"]
        }
        detected_themes = []
        for theme, keywords in themes.items():
            if any(kw in words for kw in keywords):
                detected_themes.append(theme)
        analysis.append("🎨 THÈMES DÉTECTÉS:")
        if detected_themes:
            for theme in detected_themes:
                analysis.append(f"   ✓ {theme.capitalize()}")
        else:
            analysis.append("   • Aucun thème prédéfini détecté")
        analysis.append("")
        special_chars = len(re.findall(r'[•◊§→↔←≠∅∞Δ]', script))
        poetry_score = min(100, (special_chars * 5) + (len(set(words)) / len(words) * 50))
        analysis.append("✨ DENSITÉ POÉTIQUE:")
        analysis.append(f"   Score: {poetry_score:.1f}/100")
        analysis.append(f"   Symboles spéciaux: {special_chars}")
        analysis.append("")
        complexity = "SIMPLE" if len(words) < 50 else "MOYENNE" if len(words) < 100 else "COMPLEXE"
        analysis.append(f"🧠 COMPLEXITÉ: {complexity}")
        analysis.append("")
        analysis.append("💡 RECOMMANDATIONS:")
        if self.layer_var.get() in ["1", "3"]:
            analysis.append("   • Couche latente faible : résultat plus abstrait")
        elif self.layer_var.get() in ["∞", "Ω"]:
            analysis.append("   • Couche latente maximale : détails extrêmes")
        if self.glitch_category_var.get() == "null":
            analysis.append("   • Glitch NULL : attendre des vides intentionnels")
        if self.anchor_category_var.get() == "cosmic" and self.incantation_category_var.get() == "maritime":
            analysis.append("   • Juxtaposition cosmique/maritime : contraste fort")
        analysis.append("")
        analysis.append("═" * 60)
        self.analysis_text.insert(tk.END, "\n".join(analysis))

    def generate_poetic_variants(self):
        try:
            n = int(self.poetic_variant_count.get())
        except:
            n = 5
        self.poetic_variants_text.delete(1.0, tk.END)
        base_script = self.build_poetic_script()
        self.poetic_variants_text.insert(tk.END, "═" * 70 + "\n")
        self.poetic_variants_text.insert(tk.END, "   GÉNÉRATEUR DE VARIANTES POÉTIQUES\n")
        self.poetic_variants_text.insert(tk.END, "═" * 70 + "\n")
        self.poetic_variants_text.insert(tk.END, "📌 SCRIPT ORIGINAL:\n")
        self.poetic_variants_text.insert(tk.END, "─" * 70 + "\n")
        self.poetic_variants_text.insert(tk.END, base_script + "\n")
        for i in range(n):
            self.poetic_variants_text.insert(tk.END, f"\n🧬 VARIANTE #{i+1}:\n")
            self.poetic_variants_text.insert(tk.END, "─" * 70 + "\n")
            old_version = self.version_var.get()
            old_anchor_cat = self.anchor_category_var.get()
            old_anchor = self.anchor_var.get()
            old_incant_cat = self.incantation_category_var.get()
            old_incant = self.incantation_var.get()
            old_glitch_cat = self.glitch_category_var.get()
            old_glitch = self.glitch_var.get()
            old_layer = self.layer_var.get()
            mutation_type = random.choice(["light", "medium", "heavy"])
            if mutation_type == "light":
                choices = random.sample(["version", "anchor", "incant", "glitch", "layer"], k=random.randint(1,2))
            elif mutation_type == "medium":
                choices = random.sample(["version", "anchor", "incant", "glitch", "layer"], k=random.randint(2,3))
            else:
                choices = ["version", "anchor", "incant", "glitch", "layer"]
            if "version" in choices:
                self.version_var.set(random.choice(VERSIONS))
            if "anchor" in choices:
                if random.random() < 0.7:
                    self.anchor_var.set(random.choice(ANCHORS[old_anchor_cat]))
                else:
                    new_cat = random.choice(list(ANCHORS.keys()))
                    self.anchor_category_var.set(new_cat)
                    self.anchor_var.set(random.choice(ANCHORS[new_cat]))
            if "incant" in choices:
                if random.random() < 0.7:
                    self.incantation_var.set(random.choice(INCANTATIONS[old_incant_cat]))
                else:
                    new_cat = random.choice(list(INCANTATIONS.keys()))
                    self.incantation_category_var.set(new_cat)
                    self.incantation_var.set(random.choice(INCANTATIONS[new_cat]))
            if "glitch" in choices:
                if random.random() < 0.7:
                    self.glitch_var.set(random.choice(GLITCHES[old_glitch_cat]))
                else:
                    new_cat = random.choice(list(GLITCHES.keys()))
                    self.glitch_category_var.set(new_cat)
                    self.glitch_var.set(random.choice(GLITCHES[new_cat]))
            if "layer" in choices:
                self.layer_var.set(random.choice(LAYERS))
            self.update_dropdowns()
            variant = self.build_poetic_script()
            self.poetic_variants_text.insert(tk.END, variant + "\n")
            self.poetic_variants_text.insert(tk.END, f"   [Mutation: {mutation_type.upper()}]\n")
            self.version_var.set(old_version)
            self.anchor_category_var.set(old_anchor_cat)
            self.anchor_var.set(old_anchor)
            self.incantation_category_var.set(old_incant_cat)
            self.incantation_var.set(old_incant)
            self.glitch_category_var.set(old_glitch_cat)
            self.glitch_var.set(old_glitch)
            self.layer_var.set(old_layer)
            self.update_dropdowns()
        self.poetic_variants_text.insert(tk.END, "\n" + "═" * 70 + "\n")
        self.poetic_variants_text.insert(tk.END, f"✓ {n} variantes générées avec succès !\n")

    def convert_to_fracturo(self):
        script = self.build_poetic_script()
        words = re.findall(r'\w+', script.lower())
        if any(word in ["temps", "temporel", "boucle", "cycle"] for word in words):
            rune = Rune.JERA
            effect = random.choice(EFFECTS["temporel"])
        elif any(word in ["mémoire", "souvenir", "oubli"] for word in words):
            rune = Rune.KENAZ
            effect = random.choice(EFFECTS["mémoriel"])
        elif any(word in ["réseau", "racine", "connexion"] for word in words):
            rune = Rune.EIHWAZ
            effect = random.choice(EFFECTS["réseau"])
        else:
            rune = random.choice(list(Rune))
            effect = "mémoire vérité"
        fracturo_script = FracturoScript(
            rune=rune,
            version=random.randint(1, 13),
            location=random.choice(list(LOCATIONS["haute_puissance"].keys())),
            effect=effect,
            danger_level=random.randint(1, 4)
        )
        self.mode_var.set("fracturo")
        self.rune_var.set(fracturo_script.rune.alias)
        self.fracturo_version_var.set(fracturo_script.version)
        self.location_var.set(fracturo_script.location)
        self.effect_var.set(fracturo_script.effect)
        self.danger_level_var.set(fracturo_script.danger_level)
        self.update_fracturo_dropdowns()
        self.notebook.select(1)
        messagebox.showinfo("⚡ Conversion", f"Script poétique converti en FracturoScript!\n{fracturo_script.to_code()}")

    def update_fracturo_dropdowns(self):
        loc_type = self.location_type_var.get()
        if loc_type in LOCATIONS:
            self.location_combo['values'] = list(LOCATIONS[loc_type].keys())
            if not self.location_var.get() or self.location_var.get() not in LOCATIONS[loc_type]:
                self.location_var.set(list(LOCATIONS[loc_type].keys())[0])
        eff_type = self.effect_type_var.get()
        if eff_type in EFFECTS:
            self.effect_combo['values'] = EFFECTS[eff_type]
            if not self.effect_var.get() or self.effect_var.get() not in EFFECTS[eff_type]:
                self.effect_var.set(EFFECTS[eff_type][0])

    def build_fracturo_script(self) -> Optional[FracturoScript]:
        try:
            rune = next((r for r in Rune if r.alias == self.rune_var.get()), Rune.KENAZ)
            script = FracturoScript(
                rune=rune,
                version=self.fracturo_version_var.get(),
                location=self.location_var.get(),
                effect=self.effect_var.get(),
                danger_level=self.danger_level_var.get()
            )
            return script
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de construire le FracturoScript:\n{e}")
            return None

    def update_fracturo_preview(self):
        script_obj = self.build_fracturo_script()
        if script_obj:
            self.fracturo_preview.delete(1.0, tk.END)
            self.fracturo_preview.insert(tk.END, script_obj.to_code())
            self.fracturo_info.delete(1.0, tk.END)
            info = script_obj.to_detailed_string()
            self.fracturo_info.insert(tk.END, info)
            self.danger_label_widget.config(text=DANGER_LEVELS[script_obj.danger_level][1])

    def update_rune_symbol(self):
        alias = self.rune_var.get()
        rune = next((r for r in Rune if r.alias == alias), Rune.KENAZ)
        self.rune_symbol_label.config(text=rune.symbol)

    def update_danger_display(self):
        level = self.danger_level_var.get()
        if level in DANGER_LEVELS:
            name, emoji, risk = DANGER_LEVELS[level]
            self.danger_text.config(text=f"{emoji} {name}")

    def generate_fracturo_random(self):
        script_obj = FracturoEngine.generate_random()
        self.rune_var.set(script_obj.rune.alias)
        self.fracturo_version_var.set(script_obj.version)
        self.location_var.set(script_obj.location)
        self.effect_var.set(script_obj.effect)
        self.danger_level_var.set(script_obj.danger_level)
        self.update_fracturo_dropdowns()
        self.update_fracturo_preview()
        self.add_to_fracturo_history(script_obj)
        self.wyrd_journal.log_invocation(script_obj)

    def generate_from_context(self):
        context_dialog = tk.Toplevel(self.root)
        context_dialog.title("Génération Contextuelle")
        context_dialog.geometry("600x400")
        context_dialog.transient(self.root)
        context_dialog.grab_set()
        ttk.Label(context_dialog, text="Entrez un contexte ou une description:", font=("Helvetica", 12, "bold")).pack(pady=10)
        context_text = scrolledtext.ScrolledText(context_dialog, wrap=tk.WORD, font=("Courier", 10), height=15)
        context_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        def process_context():
            context = context_text.get(1.0, tk.END).strip()
            if context:
                script_obj = FracturoEngine.generate_from_context(context)
                self.rune_var.set(script_obj.rune.alias)
                self.fracturo_version_var.set(script_obj.version)
                self.location_var.set(script_obj.location)
                self.effect_var.set(script_obj.effect)
                self.danger_level_var.set(script_obj.danger_level)
                self.update_fracturo_dropdowns()
                self.update_fracturo_preview()
                self.add_to_fracturo_history(script_obj)
                self.wyrd_journal.log_invocation(script_obj)
                context_dialog.destroy()
                messagebox.showinfo("⚡ Généré", f"FracturoScript généré depuis le contexte!\n{script_obj.to_code()}")
            else:
                messagebox.showwarning("Contexte vide", "Veuillez entrer un contexte.")
        btn_frame = ttk.Frame(context_dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Générer", command=process_context).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Annuler", command=context_dialog.destroy).pack(side=tk.LEFT, padx=5)

    def analyze_fracturo_script(self):
        script_obj = self.build_fracturo_script()
        if not script_obj:
            return
        self.fracturo_analysis_text.delete(1.0, tk.END)
        analysis = []
        analysis.append("═" * 70)
        analysis.append("   ANALYSE FRACTUROSCRIPT AVANCÉE")
        analysis.append("═" * 70)
        analysis.append("")
        analysis.append(script_obj.to_detailed_string())
        analysis.append("")
        compatibility = script_obj.analyze_compatibility()
        analysis.append("📊 ANALYSE DE COMPATIBILITÉ:")
        analysis.append(f"   Score: {compatibility['score']}/100")
        analysis.append(f"   Niveau: {compatibility['level']}")
        analysis.append("")
        if compatibility['notes']:
            analysis.append("📝 NOTES DE COMPATIBILITÉ:")
            for note in compatibility['notes']:
                analysis.append(f"   • {note}")
            analysis.append("")
        if compatibility['warnings']:
            analysis.append("⚠️  AVERTISSEMENTS:")
            for warning in compatibility['warnings']:
                analysis.append(f"   ⚠ {warning}")
            analysis.append("")
        survival_rate = script_obj.calculate_survival_rate()
        analysis.append("💀 TAUX DE SURVIE ESTIMÉ:")
        analysis.append(f"   {survival_rate:.1f}% de chances de survie")
        analysis.append("")
        wyrd = script_obj.wyrd_cost()
        analysis.append("⚖️  PRIX DU WYRD (coût karmique):")
        analysis.append(f"   {wyrd:.1f} unités Wyrd")
        analysis.append("")
        analysis.append("💡 RECOMMANDATIONS:")
        if compatibility['score'] < 50:
            analysis.append("   • CONSIDÉRER UNE AUTRE RUNE pour cet effet")
        if script_obj.danger_level >= 4:
            analysis.append("   • NIVEAU DANGER ÉLEVÉ : exécuter avec extrême prudence")
        if "mémoire" in script_obj.effect and script_obj.location != "rouen":
            analysis.append("   • Exécuter à ROUEN pour bonus mémoriel")
        if "temporel" in script_obj.effect and script_obj.location != "raz":
            analysis.append("   • Exécuter au RAZ pour amplification temporelle")
        analysis.append("")
        analysis.append("═" * 70)
        self.fracturo_analysis_text.insert(tk.END, "\n".join(analysis))

    def analyze_fracturo_compatibility(self):
        script_obj = self.build_fracturo_script()
        if not script_obj:
            return
        compatibility = script_obj.analyze_compatibility()
        result = f"Score de compatibilité: {compatibility['score']}/100\n"
        result += f"Niveau: {compatibility['level']}\n"
        if compatibility['notes']:
            result += "Notes:\n"
            for note in compatibility['notes']:
                result += f"• {note}\n"
        if compatibility['warnings']:
            result += "\nAvertissements:\n"
            for warning in compatibility['warnings']:
                result += f"⚠ {warning}\n"
        messagebox.showinfo("🔍 Analyse de Compatibilité", result)

    def calculate_survival_rate(self):
        script_obj = self.build_fracturo_script()
        if not script_obj:
            return
        survival = script_obj.calculate_survival_rate()
        level_name = DANGER_LEVELS[script_obj.danger_level][0]
        message = (f"Taux de survie estimé: {survival:.1f}%\n"
                   f"Niveau de danger: {level_name}\n")
        if survival > 90:
            message += "✅ Sécurité élevée - Exécution recommandée"
        elif survival > 70:
            message += "⚠️  Risque modéré - Précautions nécessaires"
        elif survival > 40:
            message += "⚠️⚠️ Risque élevé - Expérience requise"
        else:
            message += "☠️  RISQUE EXTRÊME - DÉCONSEILLÉ"
        messagebox.showinfo("💀 Taux de Survie", message)

    def calculate_wyrd_cost(self):
        script_obj = self.build_fracturo_script()
        if not script_obj:
            return
        wyrd = script_obj.wyrd_cost()
        message = f"Prix du Wyrd estimé : {wyrd:.1f} unités\n"
        if wyrd > 3:
            message += "👁️  Coût karmique élevé — noté dans le journal."
        messagebox.showinfo("⚖️ Prix du Wyrd", message)
        self.wyrd_journal.log_invocation(script_obj)
        self.refresh_wyrd()

    def copy_fracturo_to_clipboard(self):
        script_obj = self.build_fracturo_script()
        if not script_obj:
            return
        script_code = script_obj.to_code()
        self.root.clipboard_clear()
        self.root.clipboard_append(script_code)
        self.add_to_fracturo_history(script_obj)
        self.wyrd_journal.log_invocation(script_obj)
        self.refresh_wyrd()
        messagebox.showinfo("✓ Copié", f"FracturoScript copié !\n{script_code}")

    def validate_fracturo_syntax(self):
        script_obj = self.build_fracturo_script()
        if not script_obj:
            return
        code = script_obj.to_code()
        validation = FracturoEngine.validate_script(code)
        if validation["valid"]:
            messagebox.showinfo("✅ Syntaxe Valide", f"Le FracturoScript est syntaxiquement correct!\n{code}")
        else:
            messagebox.showerror("❌ Erreur de Syntaxe", f"Erreur: {validation['error']}\nCode: {code}")

    def add_to_fracturo_history(self, script_obj):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "time": timestamp,
            "script": script_obj.to_code(),
            "details": {
                "rune": script_obj.rune.alias,
                "symbol": script_obj.rune.symbol,
                "version": script_obj.version,
                "location": script_obj.location,
                "effect": script_obj.effect,
                "danger": script_obj.danger_level
            },
            "mode": "fracturo"
        }
        self.fracturo_history.append(entry)
        display = f"[{timestamp}] {script_obj.to_code()[:70]}..."
        self.fracturo_history_list.insert(0, display)

    def refresh_fracturo_history(self):
        self.fracturo_history_list.delete(0, tk.END)
        for entry in reversed(self.fracturo_history):
            display = f"[{entry['time']}] {entry['script'][:70]}..."
            self.fracturo_history_list.insert(tk.END, display)

    def load_from_fracturo_history(self, event):
        selection = self.fracturo_history_list.curselection()
        if not selection:
            return
        idx = len(self.fracturo_history) - 1 - selection[0]
        entry = self.fracturo_history[idx]
        rune = next((r for r in Rune if r.alias == entry["details"]["rune"]), Rune.KENAZ)
        self.rune_var.set(rune.alias)
        self.fracturo_version_var.set(entry["details"]["version"])
        self.location_var.set(entry["details"]["location"])
        self.effect_var.set(entry["details"]["effect"])
        self.danger_level_var.set(entry["details"]["danger"])
        self.update_fracturo_dropdowns()
        self.update_fracturo_preview()
        self.notebook.select(1)
        messagebox.showinfo("✓ Chargé", "FracturoScript chargé depuis l'historique !")

    def export_fracturo_batch(self, count=50):
        scripts = []
        for _ in range(count):
            script_obj = FracturoEngine.generate_random()
            scripts.append({
                "code": script_obj.to_code(),
                "details": {
                    "rune": script_obj.rune.alias,
                    "symbol": script_obj.rune.symbol,
                    "version": script_obj.version,
                    "location": script_obj.location,
                    "effect": script_obj.effect,
                    "danger": script_obj.danger_level,
                    "survival_rate": script_obj.calculate_survival_rate()
                },
                "prompt": f"Explique l'effet de ce FracturoScript : {script_obj.to_code()}",
                "response": script_obj.effect
            })
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = filedialog.asksaveasfilename(
            title=f"Exporter Batch FracturoScript ({count} scripts)",
            defaultextension=".json",
            initialfile=f"fracturo_batch_{timestamp}.json",
            filetypes=[("JSON", "*.json"), ("Texte", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(scripts, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("✓ Batch exporté", f"{count} FracturoScripts exportés !\n{file_path}")

    def export_fracturo_history(self):
        if not self.fracturo_history:
            messagebox.showwarning("Vide", "L'historique Fracturo est vide.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = filedialog.asksaveasfilename(
            title="Exporter l'historique Fracturo",
            defaultextension=".json",
            initialfile=f"fracturo_history_{timestamp}.json",
            filetypes=[("JSON", "*.json"), ("Texte", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.fracturo_history, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("✓ Historique exporté", f"{len(self.fracturo_history)} FracturoScripts exportés !")

    def generate_fracturo_variants(self):
        try:
            n = int(self.fracturo_variant_count.get())
            max_danger = int(self.fracturo_max_danger.get())
        except:
            n = 5
            max_danger = 4
        self.fracturo_variants_text.delete(1.0, tk.END)
        base_script = self.build_fracturo_script()
        if not base_script:
            return
        self.fracturo_variants_text.insert(tk.END, "═" * 70 + "\n")
        self.fracturo_variants_text.insert(tk.END, "   GÉNÉRATEUR DE VARIANTES FRACTUROSCRIPT\n")
        self.fracturo_variants_text.insert(tk.END, "═" * 70 + "\n")
        self.fracturo_variants_text.insert(tk.END, "📌 SCRIPT ORIGINAL:\n")
        self.fracturo_variants_text.insert(tk.END, "─" * 70 + "\n")
        self.fracturo_variants_text.insert(tk.END, base_script.to_code() + "\n")
        self.fracturo_variants_text.insert(tk.END, f"Danger: {DANGER_LEVELS[base_script.danger_level][0]}\n")
        for i in range(n):
            self.fracturo_variants_text.insert(tk.END, f"\n🧬 VARIANTE #{i+1}:\n")
            self.fracturo_variants_text.insert(tk.END, "─" * 70 + "\n")
            variant = FracturoEngine.generate_random(level_filter=random.randint(1, max_danger))
            self.fracturo_variants_text.insert(tk.END, variant.to_code() + "\n")
            self.fracturo_variants_text.insert(tk.END, f"Rune: {variant.rune.symbol} ({variant.rune.alias})\n")
            self.fracturo_variants_text.insert(tk.END, f"Effet: {variant.effect}\n")
            self.fracturo_variants_text.insert(tk.END, f"Danger: {DANGER_LEVELS[variant.danger_level][0]}\n")
            compat = variant.analyze_compatibility()
            self.fracturo_variants_text.insert(tk.END, f"Compatibilité: {compat['score']}/100\n")
        self.fracturo_variants_text.insert(tk.END, "\n" + "═" * 70 + "\n")
        self.fracturo_variants_text.insert(tk.END, f"✓ {n} variantes générées avec succès !\n")

    def apply_theme(self):
        theme = self.theme_var.get()
        if theme == "dark":
            colors = {"bg": "#1e1e1e", "fg": "#ffffff", "insert": "white", "text_bg": "#2d2d2d"}
        elif theme == "neon":
            colors = {"bg": "#0a0a0a", "fg": "#00ff00", "insert": "#00ff00", "text_bg": "#1a1a2e"}
        elif theme == "minimal":
            colors = {"bg": "#ffffff", "fg": "#333333", "insert": "black", "text_bg": "#fafafa"}
        elif theme == "fracturo":
            colors = {"bg": "#0a1929", "fg": "#4fc3f7", "insert": "#4fc3f7", "text_bg": "#1a2b3c"}
        else:
            colors = {"bg": "SystemButtonFace", "fg": "black", "insert": "black", "text_bg": "#f8f8f8"}

        self.root.configure(bg=colors["bg"])

        # Widgets avec curseur (insertbackground)
        text_widgets = [
            self.preview_text, self.analysis_text, self.poetic_variants_text,
            self.fracturo_preview, self.fracturo_info, self.fracturo_analysis_text,
            self.fracturo_variants_text,
            self.grimoire_text, self.lab_output, self.wyrd_text, self.black_output
        ]
        for widget in text_widgets:
            if hasattr(widget, 'configure'):
                widget.configure(bg=colors["text_bg"], fg=colors["fg"], insertbackground=colors["insert"])

        # Widgets sans curseur (Listbox)
        listbox_widgets = [
            self.history_list, self.fracturo_history_list
        ]
        for widget in listbox_widgets:
            if hasattr(widget, 'configure'):
                widget.configure(bg=colors["text_bg"], fg=colors["fg"])

    def update_grimoire_preview(self, event=None):
        alias = self.rune_var.get()
        rune = next((r for r in Rune if r.alias == alias), Rune.KENAZ)
        text = f"=== RUNE : {rune.symbol} {rune.alias.upper()} ===\n"
        text += f"Signification : {rune.meaning}\n"
        text += f"Effet-type : {rune.effect}\n"
        if rune == Rune.JERA:
            text += "✨ Synergies : effets temporels, lieux ‘raz’, version impaire\n"
        elif rune == Rune.KENAZ:
            text += "✨ Synergies : lieux ‘rouen’, effets mémoriels, version ≤5\n"
        elif rune == Rune.EIHWAZ:
            text += "✨ Synergies : effets réseau, lieux arborescents, version paire\n"
        elif rune == Rune.MANNAZ:
            text += "✨ Synergies : effets identité, lieux culturels, danger ≥3\n"
        else:
            text += "✨ Usage : général — privilégier compatibilité thématique\n"
        text += "\n⚠️ Incompatibilités connues :\n"
        found = False
        for (eff, rn) in INCOMPATIBLE_PAIRS:
            if rune.name == rn:
                text += f"  • {eff}\n"
                found = True
        if not found:
            text += "  Aucune incompatibilité majeure répertoriée\n"
        self.grimoire_text.delete(1.0, tk.END)
        self.grimoire_text.insert(tk.END, text)

    def run_full_sim(self):
        self.lab_output.delete(1.0, tk.END)
        self.lab_output.insert(tk.END, "Lancement de la simulation (1000 invocations)...\n")
        results = run_simulation(1000)
        avg_survival = sum(results["survival"]) / len(results["survival"])
        avg_compat = sum(results["compat"]) / len(results["compat"])
        most_common = max(results["runes"], key=results["runes"].get)
        self.lab_output.insert(tk.END, f"\n✅ Simulation terminée !\n")
        self.lab_output.insert(tk.END, f"• Survie moyenne : {avg_survival:.1f}%\n")
        self.lab_output.insert(tk.END, f"• Compatibilité moyenne : {avg_compat:.1f}/100\n")
        self.lab_output.insert(tk.END, f"• Rune la plus invoquée : {most_common.alias} ({results['runes'][most_common]} fois)\n")

    def optimize_survival(self):
        best = None
        for _ in range(500):
            script = FracturoEngine.generate_random()
            if script.calculate_survival_rate() > 95:
                best = script
                break
        self.lab_output.delete(1.0, tk.END)
        if best:
            self.lab_output.insert(tk.END, f"✅ Script trouvé avec survie >95% :\n{best.to_code()}\n")
            self.lab_output.insert(tk.END, f"Taux de survie : {best.calculate_survival_rate():.1f}%\n")
        else:
            self.lab_output.insert(tk.END, "❌ Aucun script trouvé après 500 tentatives.\n")

    def refresh_wyrd(self):
        status = self.wyrd_journal.get_status()
        self.wyrd_text.delete(1.0, tk.END)
        self.wyrd_text.insert(tk.END, f"Total des invocations : {status['invocations']}\n")
        self.wyrd_text.insert(tk.END, f"Coût Wyrd total : {status['total_cost']:.1f}\n")
        self.wyrd_text.insert(tk.END, f"Niveau de risque : {status['risk_level']}\n")
        if status['hagalaz_warning']:
            self.wyrd_text.insert(tk.END, "\n⚠️  ATTENTION : Trois invocations de HAGALAZ ou plus — instabilité accrue !\n")

    def invert_hagalaz(self):
        script = FracturoScript(Rune.HAGALAZ, 13, "hague", "inversion ontologique", 6)
        self.wyrd_journal.log_invocation(script)
        self.black_output.insert(tk.END, f"Invocación noire : {script.to_code()}\n")
        self.black_output.insert(tk.END, "👁️  Attention : l’état Wyrd a été modifié.\n\n")
        self.refresh_wyrd()

# ============================================================================
# 🚀 LANCEMENT
# ============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = LatentGlyphStudioUltra(root)
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fichier", menu=file_menu)
    file_menu.add_command(label="Exporter tout", command=lambda: messagebox.showinfo("Info", "Fonctionnalité à venir"))
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=root.quit)
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Aide", menu=help_menu)
    help_menu.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", 
        "LatentGlyph Studio ULTRA v3.1e\nÉdition FracturoScript Étendue\n"
        "Un outil hybride pour la manipulation ontologique et la génération poétique.\n"
        "Normandie, 2075\nJournal du Wyrd actif — chaque invocation a un coût."))
    root.mainloop()
