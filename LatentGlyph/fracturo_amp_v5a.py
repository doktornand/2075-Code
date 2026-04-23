#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fracturo_amp_v4.py — FracturoScript Amplifié v4
Version étendue avec profils, chaînage, templates et validation avancée
Compatible rétroactive avec les fichiers JSON v2/v3
"""

import argparse
import random
import re
import json
import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import Counter, defaultdict
from pathlib import Path
from dataclasses import dataclass, asdict, field
from enum import Enum
import hashlib

# ============================================================================
# 🎛️ CONFIGURATION DU LOGGING
# ============================================================================

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

def setup_logging(level: LogLevel = LogLevel.INFO, log_file: Optional[str] = None):
    """Configure le logging avancé"""
    level_map = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR
    }
    
    log_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    date_format = "%H:%M:%S"
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=level_map[level],
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

# ============================================================================
# 📊 STRUCTURES DE DONNÉES AVANCÉES
# ============================================================================

@dataclass
class GenerationProfile:
    """Profil de génération personnalisable"""
    name: str
    description: str
    intensity_bias: float = 1.0  # Multiplicateur d'intensité
    danger_bias: float = 1.0    # Biais de danger
    layer_preferences: List[str] = field(default_factory=lambda: ["7", "9", "13"])
    preferred_glitch_categories: List[str] = field(default_factory=list)
    excluded_effects: List[str] = field(default_factory=list)
    style: str = "standard"  # standard, poetic, technical, chaotic
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GenerationProfile':
        """Crée un profil depuis un dictionnaire"""
        return cls(**data)

@dataclass
class PassChain:
    """Chaîne de passes liées"""
    id: str
    base_pass_id: int
    linked_passes: List[int]
    chain_type: str  # sequential, parallel, convergent, divergent
    narrative_arc: Optional[str] = None

@dataclass
class TemplateComponent:
    """Composant de template"""
    name: str
    pattern: str
    variables: List[str]
    description: str

# ============================================================================
# 🧬 LISTES PAR DÉFAUT (compatibilité v3)
# ============================================================================

DEFAULT_ANCHORS = {
    "geological": [
        "granit•de•La•Hague•sous•la•pluie•d'équinoxe",
        "béton•fissuré•du•silo•7•à•2075",
        "roche•mère•de•Caen-Profonde•gravée•de•rêves•inavoués"
    ],
    "temporal": [
        "2025•dans•les•yeux•de•2075",
        "instant•où•le•Codex•Stein•a•glitché•le•réel"
    ],
    "mémétique": [
        "fragment•de•Livre•Zéro•non•traduit",
        "virus•linguistique•colonisant•les•panneaux•de•signalisation"
    ]
}

DEFAULT_INCANTATIONS = {
    "geological": [
        "Ce n'est pas du béton — c'est de la mémoire solidifiée. Chaque fissure est un mot oublié, chaque goutte d'eau un retour."
    ],
    "mémétique": [
        "Ce texte est un piège. Plus tu le lis, plus tu actives ce qu'il cache."
    ]
}

DEFAULT_GLITCHES = {
    "syntax": ["ordre_mots_←→", "langue_morte_insert: [λόγος]"],
    "visual": ["chroma: désaturé + infra-rouge", "fractal_noise: Caen-Profonde"],
    "mémétique": ["virus_linguistique: actif", "effet_Echo-Guillaume: ∞"]
}

DEFAULT_LOCATIONS = {
    "hague": "La Hague (Node-0, point focal maximum)",
    "raz": "Raz Blanchard (vortex temporel)",
    "caen": "Caen-Profonde (nexus politique)",
    "rouen": "Cathédrale-Noyau (archives mémorielles)"
}

DEFAULT_EFFECTS = {
    "temporel": ["glissement temporel", "boucle événement"],
    "mémoriel": ["mémoire vérité", "résurrection mémétique"],
    "réseau": ["racine-monde", "mycélium mémoriel"],
    "identité": ["double parfait", "main rouge"],
    "mémétique": ["paleo-mème activation", "virus linguistique"]
}

DEFAULT_INCOMPATIBLE_PAIRS = {
    ("temporel", "ISA"),
    ("croissance", "THURISAZ"),
    ("destruction", "BERKANO"),
    ("virus", "ALGIZ")
}

DEFAULT_GENERATION_PROFILES = {
    "narrative": {
        "name": "narrative",
        "description": "Génération orientée narration",
        "intensity_bias": 1.2,
        "danger_bias": 0.8,
        "layer_preferences": ["7", "9"],
        "style": "poetic"
    },
    "technical": {
        "name": "technical", 
        "description": "Génération technique détaillée",
        "intensity_bias": 0.9,
        "danger_bias": 1.0,
        "layer_preferences": ["13", "Δ"],
        "preferred_glitch_categories": ["syntax", "visual"],
        "style": "technical"
    },
    "chaotic": {
        "name": "chaotic",
        "description": "Génération chaotique et imprévisible",
        "intensity_bias": 1.5,
        "danger_bias": 1.3,
        "layer_preferences": ["∞", "Δ"],
        "style": "chaotic"
    }
}

# ============================================================================
# 🎭 TEMPLATES DE SORTIE
# ============================================================================

DEFAULT_TEMPLATES = {
    "standard": {
        "header": "// FracturoScript Amplifié v4 — Contexte: «{context}»\n"
                  "// Base: Ω<{rune}> @ {location} → {effect}\n"
                  "// Intensité: {intensity}/10 • Mode: {variation}\n"
                  "// Passes: {passes_count} • Généré: {timestamp}\n"
                  "="*80 + "\n\n",
        "pass_template": "Ω<{rune}>v{version} {location} — {effect} •••\n"
                        "  [P{pass_id:02d}] Ancrage: {anchor}\n"
                        "  [P{pass_id:02d}] Incantation: «{incantation}»\n"
                        "  [P{pass_id:02d}] Glitch: {glitch}\n"
                        "  [P{pass_id:02d}] Couche: {layer} • Danger: {danger}/6\n",
        "footer": ""
    },
    "poetic": {
        "header": "╔═══════════════════════════════════════════════════════════════╗\n"
                  "║                     FRACTURO POETICA v4                       ║\n"
                  "║  Contexte: «{context}»                                        ║\n"
                  "║  Rune: {rune} • Lieu: {location}                              ║\n"
                  "╚═══════════════════════════════════════════════════════════════╝\n\n",
        "pass_template": "§ {rune} // v{version}\n"
                        "  où: {location}\n"
                        "  quand: {anchor}\n"
                        "  dire: «{incantation}»\n"
                        "  glitch: {glitch}\n"
                        "  couche {layer} • péril {danger}/6\n"
                        "  ——\n",
        "footer": "\n═ fin de transmission ═"
    },
    "technical": {
        "header": "## FRACTURO TECHNICAL LOG v4\n"
                  "### CONTEXT: {context}\n"
                  "### PARAMETERS:\n"
                  "- Base rune: {rune}\n"  
                  "- Location: {location}\n"
                  "- Effect: {effect}\n"
                  "- Intensity: {intensity}/10\n"
                  "- Generation mode: {variation}\n"
                  "- Timestamp: {timestamp}\n\n"
                  "---\n",
        "pass_template": "### PASS {pass_id:02d}\n"
                        "```fracturo\n"
                        "RUNE:      Ω<{rune}>v{version}\n"
                        "LOCATION:  {location}\n" 
                        "EFFECT:    {effect}\n"
                        "ANCHOR:    {anchor}\n"
                        "INCANT:    {incantation}\n"
                        "GLITCH:    {glitch}\n"
                        "LAYER:     {layer}\n"
                        "DANGER:    {danger}/6\n"
                        "```\n\n",
        "footer": "## END OF LOG"
    }
}

# ============================================================================
# 📥 UTILITAIRES DE CHARGEMENT ET VALIDATION ÉTENDUS
# ============================================================================

class DataValidator:
    """Validateur étendu pour les structures de données"""
    
    @staticmethod
    def validate_anchors(data: dict) -> Tuple[bool, List[str]]:
        """Valide la structure des anchors avec diagnostics"""
        issues = []
        if not isinstance(data, dict):
            issues.append("Anchors must be a dictionary")
            return False, issues
        
        for key, value in data.items():
            if not isinstance(value, list):
                issues.append(f"Anchor category '{key}' must be a list")
            elif not all(isinstance(v, str) for v in value):
                issues.append(f"Anchor category '{key}' contains non-string values")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_incompatible_pairs(data: list) -> Tuple[bool, List[str]]:
        """Valide la structure des paires incompatibles"""
        issues = []
        if not isinstance(data, list):
            issues.append("Incompatible pairs must be a list")
            return False, issues
        
        for i, item in enumerate(data):
            if not isinstance(item, list):
                issues.append(f"Item {i} must be a list")
            elif len(item) != 2:
                issues.append(f"Item {i} must have exactly 2 elements")
            elif not all(isinstance(x, str) for x in item):
                issues.append(f"Item {i} contains non-string values")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_profile(data: dict) -> Tuple[bool, List[str]]:
        """Valide un profil de génération"""
        issues = []
        required_fields = ["name", "description"]
        
        for field in required_fields:
            if field not in data:
                issues.append(f"Missing required field: {field}")
        
        if "intensity_bias" in data and not isinstance(data["intensity_bias"], (int, float)):
            issues.append("intensity_bias must be a number")
        
        if "danger_bias" in data and not isinstance(data["danger_bias"], (int, float)):
            issues.append("danger_bias must be a number")
        
        return len(issues) == 0, issues

class ResourceManager:
    """Gestionnaire de ressources avec cache"""
    
    def __init__(self):
        self.cache = {}
        self.loaded_files = {}
    
    def load_json(self, filename: str, default: Any, desc: str = "", 
                  validate_func=None) -> Any:
        """Charge un fichier JSON avec cache et validation"""
        
        # Vérifier le cache
        cache_key = f"{filename}_{os.path.getmtime(filename) if os.path.exists(filename) else 0}"
        if cache_key in self.cache:
            logging.debug(f"Cache hit for {filename}")
            return self.cache[cache_key]
        
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                if validate_func:
                    if callable(validate_func):
                        is_valid, issues = validate_func(data)
                        if not is_valid:
                            logging.warning(f"Invalid structure in {filename}: {issues}")
                            return default
                    elif not validate_func(data):
                        logging.warning(f"Invalid structure in {filename}")
                        return default
                
                logging.info(f"Loaded: {filename}")
                self.loaded_files[filename] = datetime.now()
                self.cache[cache_key] = data
                return data
                
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in {filename}: {e}")
            except Exception as e:
                logging.error(f"Error loading {filename}: {e}")
        else:
            logging.info(f"{filename} not found → using internal {desc}")
        
        self.cache[cache_key] = default
        return default
    
    def load_profiles(self, filename: str) -> Dict[str, GenerationProfile]:
        """Charge les profils de génération"""
        default_profiles = {
            name: GenerationProfile.from_dict(data) 
            for name, data in DEFAULT_GENERATION_PROFILES.items()
        }
        
        if not os.path.exists(filename):
            return default_profiles
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            profiles = {}
            for name, profile_data in data.items():
                is_valid, issues = DataValidator.validate_profile(profile_data)
                if is_valid:
                    profiles[name] = GenerationProfile.from_dict(profile_data)
                else:
                    logging.warning(f"Invalid profile '{name}': {issues}")
            
            # Fusionner avec les profils par défaut
            profiles = {**default_profiles, **profiles}
            logging.info(f"Loaded {len(profiles)} profiles from {filename}")
            return profiles
            
        except Exception as e:
            logging.error(f"Error loading profiles: {e}")
            return default_profiles
    
    def load_templates(self, filename: str) -> Dict[str, Dict]:
        """Charge les templates personnalisés"""
        if not os.path.exists(filename):
            return DEFAULT_TEMPLATES
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                custom_templates = json.load(f)
            
            # Fusionner avec les templates par défaut
            templates = {**DEFAULT_TEMPLATES, **custom_templates}
            logging.info(f"Loaded templates from {filename}")
            return templates
            
        except Exception as e:
            logging.error(f"Error loading templates: {e}")
            return DEFAULT_TEMPLATES

# ============================================================================
# 🧠 LOGIQUE FRACTURO ÉTENDUE
# ============================================================================

RUNE_ORDER = [
    "fehu", "uruz", "thurisaz", "ansuz", "raidho", "kenaz", "gebo", "hagalaz",
    "nauthiz", "isa", "jera", "eihwaz", "perthro", "algiz", "sowilo", "tiwaz",
    "berkano", "mannaz", "laguz", "ingwaz", "dagaz", "othala"
]

RUNE_MEANINGS = {
    "fehu": "richesse, croissance",
    "uruz": "force brute, vitalité",
    "thurisaz": "destruction, chaos",
    "ansuz": "connaissance, communication",
    "raidho": "voyage, mouvement",
    "kenaz": "lumière, révélation",
    "gebo": "don, échange",
    "hagalaz": "rupture, transformation",
    "nauthiz": "nécessité, contrainte",
    "isa": "stasis, gel",
    "jera": "cycle, récolte",
    "eihwaz": "connexion, endurance",
    "perthro": "mystère, destin",
    "algiz": "protection, refuge",
    "sowilo": "victoire, soleil",
    "tiwaz": "justice, sacrifice",
    "berkano": "croissance, nouveau départ",
    "mannaz": "humanité, identité",
    "laguz": "flux, intuition",
    "ingwaz": "potentiel, gestation",
    "dagaz": "éveil, transformation",
    "othala": "héritage, ancêtres"
}

class RuneAnalyzer:
    """Analyse avancée des runes avec historique"""
    
    def __init__(self):
        self.history = []
    
    def get_rune_intensity(self, rune: str, context: str, profile: Optional[GenerationProfile] = None) -> int:
        """Calcule l'intensité d'une rune avec biais de profil"""
        context_lower = context.lower()
        meaning = RUNE_MEANINGS.get(rune, "")
        keywords = meaning.split(", ")
        
        intensity = 5  # base
        
        # Score basé sur les mots-clés
        for keyword in keywords:
            if keyword in context_lower:
                intensity += 2
        
        # Ajustements contextuels
        if rune in ["thurisaz", "hagalaz"] and ("danger" in context_lower or "destruction" in context_lower):
            intensity += 2
        if rune in ["algiz", "berkano"] and ("protection" in context_lower or "sécurité" in context_lower):
            intensity += 2
        
        # Appliquer le biais du profil
        if profile:
            intensity = int(intensity * profile.intensity_bias)
        
        # Enregistrer dans l'historique
        self.history.append({
            "rune": rune,
            "context": context,
            "intensity": intensity,
            "timestamp": datetime.now()
        })
        
        return min(10, max(1, intensity))
    
    def get_compatibility_score(self, rune1: str, rune2: str, incompatible_pairs: Set) -> float:
        """Calcule un score de compatibilité entre deux runes"""
        if (rune1.upper(), rune2.upper()) in incompatible_pairs:
            return 0.0
        if (rune2.upper(), rune1.upper()) in incompatible_pairs:
            return 0.0
        
        # Calcul basique : runes adjacentes sont plus compatibles
        try:
            idx1 = RUNE_ORDER.index(rune1)
            idx2 = RUNE_ORDER.index(rune2)
            distance = abs(idx1 - idx2)
            return max(0.0, 1.0 - (distance / len(RUNE_ORDER)))
        except ValueError:
            return 0.5

class ContextProcessor:
    """Processeur de contexte avancé"""
    
    @staticmethod
    def extract_keywords(context: str) -> List[str]:
        """Extrait les mots-clés significatifs du contexte"""
        # Mots vides à ignorer
        stop_words = {"de", "du", "la", "le", "les", "et", "ou", "dans", "avec", "pour", "sur"}
        
        # Nettoyage et tokenization
        words = re.findall(r'\b[a-zà-ÿ]+\b', context.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Compter les occurrences
        counter = Counter(keywords)
        return [word for word, count in counter.most_common(10)]
    
    @staticmethod
    def detect_context_type(context: str) -> str:
        """Détecte le type de contexte"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ["mémoire", "souvenir", "oubli"]):
            return "mémoriel"
        elif any(word in context_lower for word in ["temps", "temporel", "boucle"]):
            return "temporel"
        elif any(word in context_lower for word in ["réseau", "connexion", "mycélium"]):
            return "réseau"
        elif any(word in context_lower for word in ["virus", "infection", "contamination"]):
            return "viral"
        elif any(word in context_lower for word in ["identité", "double", "masque"]):
            return "identitaire"
        else:
            return "générique"

class PassGenerator:
    """Générateur de passes avec chaînage"""
    
    def __init__(self, resource_manager: ResourceManager, rune_analyzer: RuneAnalyzer):
        self.resource_manager = resource_manager
        self.rune_analyzer = rune_analyzer
        self.chains = []
        self.current_chain_id = 1
    
    def generate_pass(self, context: str, base_rune: str, base_location: str, 
                     base_effect: str, pass_id: int, anchors: dict, 
                     incantations: dict, glitches: dict, locations: dict, 
                     effects: dict, variation_mode: str = "standard",
                     profile: Optional[GenerationProfile] = None,
                     template: Dict = DEFAULT_TEMPLATES["standard"]) -> Dict:
        """Génère une passe complète avec métadonnées"""
        
        # Appliquer les préférences du profil
        if profile:
            # Sélection de couche selon les préférences
            layer = random.choice(profile.layer_preferences) if profile.layer_preferences else "7"
            
            # Biais de danger
            base_danger = random.randint(1, min(6, 3 + pass_id // 2))
            danger = min(6, max(1, int(base_danger * profile.danger_bias)))
            
            # Catégories de glitch préférées
            glitch_categories = list(glitches.keys())
            if profile.preferred_glitch_categories:
                preferred = [c for c in profile.preferred_glitch_categories if c in glitch_categories]
                if preferred:
                    glitch_categories = preferred
        else:
            layer = random.choice(["7", "9", "13", "∞", "Δ"])
            danger = random.randint(1, min(6, 3 + pass_id // 2))
            glitch_categories = list(glitches.keys())
        
        version = random.randint(1, 13)
        
        # Ajustements selon le mode de variation
        if variation_mode == "intense":
            danger = min(6, danger + 1)
            version = random.randint(7, 13)
        elif variation_mode == "subtle":
            danger = max(1, danger - 1)
            version = random.randint(1, 7)
        
        # Sélections avec pondération
        anchor_cat = random.choice(list(anchors.keys()))
        anchor = random.choice(anchors[anchor_cat])
        
        incant_cat = random.choice(list(incantations.keys()))
        incant = random.choice(incantations[incant_cat])
        
        glitch_cat = random.choice(glitch_categories)
        glitch = random.choice(glitches[glitch_cat])
        
        # Préparer les données pour le template
        pass_data = {
            "rune": base_rune,
            "version": version,
            "location": base_location,
            "effect": base_effect,
            "pass_id": pass_id,
            "anchor": anchor,
            "incantation": incant,
            "glitch": glitch,
            "layer": layer,
            "danger": danger
        }
        
        # Générer le texte avec le template
        pass_text = template["pass_template"].format(**pass_data)
        
        # Métadonnées étendues
        metadata = {
            "id": pass_id,
            "data": pass_data,
            "text": pass_text.strip(),
            "hash": hashlib.md5(pass_text.encode()).hexdigest()[:8],
            "profile": profile.name if profile else "default",
            "generated_at": datetime.now().isoformat()
        }
        
        return metadata
    
    def generate_chain(self, base_pass_id: int, chain_type: str = "sequential", 
                      num_linked: int = 3) -> PassChain:
        """Génère une chaîne de passes liées"""
        chain_id = f"chain_{self.current_chain_id}"
        self.current_chain_id += 1
        
        linked_passes = []
        current_id = base_pass_id + 1
        
        for i in range(num_linked):
            linked_passes.append(current_id)
            if chain_type == "sequential":
                current_id += 1
            elif chain_type == "parallel":
                current_id = base_pass_id + i + 1
        
        chain = PassChain(
            id=chain_id,
            base_pass_id=base_pass_id,
            linked_passes=linked_passes,
            chain_type=chain_type,
            narrative_arc=self._generate_narrative_arc(chain_type)
        )
        
        self.chains.append(chain)
        return chain
    
    def _generate_narrative_arc(self, chain_type: str) -> str:
        """Génère un arc narratif pour la chaîne"""
        arcs = {
            "sequential": ["initiation → épreuve → résolution", 
                          "exposition → conflit → dénouement"],
            "parallel": ["réalités divergentes convergent", 
                        "échos multiples, source unique"],
            "convergent": ["flux séparés → nexus unique", 
                          "chemins multiples, destination commune"],
            "divergent": ["source unique → réalités multiples", 
                         "un → plusieurs → infini"]
        }
        return random.choice(arcs.get(chain_type, ["arc narratif non spécifié"]))

# ============================================================================
# 📊 ANALYSES ET STATISTIQUES ÉTENDUES
# ============================================================================

class FracturoAnalyzer:
    """Analyse étendue avec visualisations"""
    
    def __init__(self):
        self.stats = {
            "runes": Counter(),
            "locations": Counter(),
            "effects": Counter(),
            "danger_levels": Counter(),
            "layers": Counter(),
            "glitch_categories": Counter(),
            "anchor_categories": Counter(),
            "incantation_categories": Counter()
        }
        self.temporal_stats = []
    
    def analyze_pass(self, pass_data: Dict):
        """Analyse une passe individuelle avec ses métadonnées"""
        text = pass_data["text"]
        
        # Extraction des patterns
        rune_match = re.search(r"Ω<(\w+)>", text)
        if rune_match:
            self.stats["runes"][rune_match.group(1)] += 1
        
        danger_match = re.search(r"Danger: (\d+)/6", text)
        if danger_match:
            self.stats["danger_levels"][int(danger_match.group(1))] += 1
        
        layer_match = re.search(r"Couche: ([^\s]+)", text)
        if layer_match:
            self.stats["layers"][layer_match.group(1)] += 1
        
        # Analyser les métadonnées si disponibles
        if "data" in pass_data:
            data = pass_data["data"]
            self.stats["locations"][data.get("location", "unknown")] += 1
            self.stats["effects"][data.get("effect", "unknown")] += 1
        
        # Statistiques temporelles
        self.temporal_stats.append({
            "timestamp": datetime.now(),
            "pass_id": pass_data.get("id", 0),
            "danger": int(danger_match.group(1)) if danger_match else 0,
            "rune": rune_match.group(1) if rune_match else "unknown"
        })
    
    def generate_report(self, include_visual: bool = False) -> str:
        """Génère un rapport d'analyse détaillé"""
        report = "\n" + "="*80 + "\n"
        report += "📊 ANALYSE FRACTURO ÉTENDUE\n"
        report += "="*80 + "\n\n"
        
        # Statistiques de base
        if self.stats["runes"]:
            report += "🧬 DISTRIBUTION DES RUNES:\n"
            total_runes = sum(self.stats["runes"].values())
            for rune, count in self.stats["runes"].most_common():
                percentage = (count / total_runes) * 100
                report += f"  • {rune.upper():<12} {count:3d}x ({percentage:5.1f}%) — {RUNE_MEANINGS.get(rune, 'inconnu')}\n"
        
        if self.stats["danger_levels"]:
            report += "\n⚠️ NIVEAUX DE DANGER:\n"
            for level in sorted(self.stats["danger_levels"].keys()):
                count = self.stats["danger_levels"][level]
                bar = "█" * count
                report += f"  • Niveau {level}: {bar} ({count}x)\n"
        
        if self.stats["layers"]:
            report += "\n🌀 COUCHES ACTIVÉES:\n"
            for layer, count in self.stats["layers"].most_common():
                report += f"  • Couche {layer}: {count}x\n"
        
        # Statistiques avancées
        if self.temporal_stats:
            report += "\n⏰ ÉVOLUTION TEMPORELLE:\n"
            dangers = [s["danger"] for s in self.temporal_stats]
            avg_danger = sum(dangers) / len(dangers) if dangers else 0
            report += f"  • Danger moyen: {avg_danger:.2f}/6\n"
            report += f"  • Pic de danger: {max(dangers) if dangers else 0}/6\n"
        
        return report
    
    def generate_json_report(self) -> Dict:
        """Génère un rapport au format JSON"""
        return {
            "summary": {
                "total_passes": len(self.temporal_stats),
                "unique_runes": len(self.stats["runes"]),
                "average_danger": sum(self.stats["danger_levels"].keys()) / len(self.stats["danger_levels"]) 
                    if self.stats["danger_levels"] else 0
            },
            "details": {
                "runes": dict(self.stats["runes"]),
                "danger_levels": dict(self.stats["danger_levels"]),
                "layers": dict(self.stats["layers"])
            },
            "generated_at": datetime.now().isoformat()
        }

# ============================================================================
# 💾 EXPORTS MULTIPLES ÉTENDUS
# ============================================================================

class ExportManager:
    """Gestionnaire d'export étendu"""
    
    @staticmethod
    def export_txt(content: str, filename: str, metadata: Optional[Dict] = None):
        """Export texte brut avec métadonnées"""
        with open(filename, "w", encoding="utf-8") as f:
            if metadata:
                f.write(f"// METADATA: {json.dumps(metadata, ensure_ascii=False)}\n\n")
            f.write(content)
        logging.info(f"Export TXT: {filename}")
    
    @staticmethod
    def export_json(passes: List[dict], filename: str, metadata: dict, 
                   analyzer: Optional[FracturoAnalyzer] = None):
        """Export JSON structuré avec analyse"""
        output = {
            "metadata": metadata,
            "passes": passes,
            "statistics": analyzer.generate_json_report() if analyzer else {}
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2, default=str)
        logging.info(f"Export JSON: {filename}")
    
    @staticmethod
    def export_markdown(content: str, filename: str, metadata: dict,
                       analyzer: Optional[FracturoAnalyzer] = None):
        """Export Markdown avec analyse"""
        md = f"# FracturoScript Amplifié v4\n\n"
        
        # Métadonnées
        md += f"## Métadonnées\n\n"
        md += f"- **Contexte**: {metadata['context']}\n"
        md += f"- **Base**: Ω<{metadata['rune']}> @ {metadata['location']} → {metadata['effect']}\n"
        md += f"- **Profil**: {metadata.get('profile', 'default')}\n"
        md += f"- **Généré**: {metadata['timestamp']}\n\n"
        
        # Analyse si disponible
        if analyzer:
            md += f"## Analyse\n\n"
            report = analyzer.generate_report()
            md += f"```\n{report}\n```\n\n"
        
        # Passes
        md += f"## Passes ({metadata['passes_count']} total)\n\n"
        md += f"```fracturo\n{content}\n```\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)
        logging.info(f"Export Markdown: {filename}")
    
    @staticmethod
    def export_html(passes: List[dict], filename: str, metadata: dict,
                   analyzer: Optional[FracturoAnalyzer] = None):
        """Export HTML avec mise en forme"""
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FracturoScript v4 - {metadata['context'][:50]}</title>
    <style>
        body {{ font-family: 'Courier New', monospace; margin: 20px; background: #0a0a0a; color: #00ff00; }}
        .header {{ border-bottom: 2px solid #00ff00; padding-bottom: 10px; margin-bottom: 20px; }}
        .pass {{ border-left: 3px solid #ff00ff; padding-left: 15px; margin: 15px 0; }}
        .danger-high {{ color: #ff0000; }}
        .danger-medium {{ color: #ffff00; }}
        .danger-low {{ color: #00ffff; }}
        .metadata {{ background: #1a1a1a; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>FracturoScript Amplifié v4</h1>
        <div class="metadata">
            <p><strong>Contexte:</strong> {metadata['context']}</p>
            <p><strong>Rune de base:</strong> {metadata['rune']} ({metadata.get('intensity', 0)}/10)</p>
            <p><strong>Lieu:</strong> {metadata['location']}</p>
            <p><strong>Effet:</strong> {metadata['effect']}</p>
            <p><strong>Généré le:</strong> {metadata['timestamp']}</p>
        </div>
    </div>
    
    <div class="passes">
"""
        
        for pass_data in passes:
            danger_class = "danger-low"
            if pass_data.get('data', {}).get('danger', 0) >= 5:
                danger_class = "danger-high"
            elif pass_data.get('data', {}).get('danger', 0) >= 3:
                danger_class = "danger-medium"
            
            html += f"""
        <div class="pass {danger_class}">
            <h3>Passe {pass_data['id']:02d} • Ω<{pass_data['data'].get('rune', '???')}></h3>
            <pre>{pass_data['text']}</pre>
            <small>Hash: {pass_data.get('hash', '')} • Couche: {pass_data['data'].get('layer', '?')}</small>
        </div>
"""
        
        html += """
    </div>
</body>
</html>"""
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        logging.info(f"Export HTML: {filename}")

# ============================================================================
# 🚀 MAIN ÉTENDU
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="FracturoScript Amplifié v4 — Version étendue avec profils et chaînage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s "mémoire effacée" -p 10 --profile narrative
  %(prog)s "virus temporel" -p 5 --chain sequential --template poetic
  %(prog)s "réseau mycélial" --analyze --export all --log debug
  %(prog)s --validate-all --fix-issues
        """
    )
    
    parser.add_argument("context", type=str, nargs="?", help="Contexte ou description initiale")
    parser.add_argument("-p", "--passes", type=int, default=5, help="Nombre de passes (défaut: 5)")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Graine aléatoire pour reproductibilité")
    parser.add_argument("-o", "--output", type=str, default=None, help="Fichier de sortie (sans extension)")
    parser.add_argument("-f", "--format", choices=["txt", "json", "markdown", "html", "all"], default="txt",
                        help="Format d'export (défaut: txt)")
    parser.add_argument("--profile", type=str, default="standard", 
                       help="Profil de génération (narrative, technical, chaotic, ou nom de fichier)")
    parser.add_argument("--template", type=str, default="standard",
                       help="Template de sortie (standard, poetic, technical)")
    parser.add_argument("-a", "--analyze", action="store_true", help="Générer un rapport d'analyse")
    parser.add_argument("-v", "--variation", choices=["standard", "intense", "subtle"], default="standard",
                        help="Mode de variation (défaut: standard)")
    parser.add_argument("--chain", choices=["sequential", "parallel", "convergent", "divergent", "none"], 
                       default="none", help="Type de chaînage des passes")
    parser.add_argument("--list-profiles", action="store_true", help="Afficher les profils disponibles")
    parser.add_argument("--list-templates", action="store_true", help="Afficher les templates disponibles")
    parser.add_argument("--validate-all", action="store_true", help="Valider tous les fichiers JSON")
    parser.add_argument("--fix-issues", action="store_true", help="Tenter de corriger les problèmes détectés")
    parser.add_argument("--log", choices=["debug", "info", "warning", "error"], default="info",
                       help="Niveau de log (défaut: info)")
    parser.add_argument("--log-file", type=str, help="Fichier de log")
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging(LogLevel(args.log), args.log_file)
    logging.info(f"FracturoScript Amplifié v4 démarré")
    
    # Initialisation des gestionnaires
    resource_manager = ResourceManager()
    rune_analyzer = RuneAnalyzer()
    context_processor = ContextProcessor()
    
    # Commandes utilitaires
    if args.list_profiles:
        profiles = resource_manager.load_profiles("profiles.json")
        print("\n🎭 PROFILS DISPONIBLES\n" + "="*80)
        for name, profile in profiles.items():
            print(f"  • {name}: {profile.description}")
            print(f"    Style: {profile.style} | Intensité: x{profile.intensity_bias} | Danger: x{profile.danger_bias}")
        return
    
    if args.list_templates:
        templates = resource_manager.load_templates("templates.json")
        print("\n🎨 TEMPLATES DISPONIBLES\n" + "="*80)
        for name in templates.keys():
            print(f"  • {name}")
        return
    
    # Validation approfondie
    if args.validate_all:
        print("\n🔍 VALIDATION DES FICHIERS\n" + "="*80)
        files_to_validate = [
            ("anchors.json", DataValidator.validate_anchors),
            ("incompatible_pairs.json", DataValidator.validate_incompatible_pairs),
            ("profiles.json", lambda x: DataValidator.validate_profile(x)[0]),
            ("templates.json", lambda x: isinstance(x, dict))
        ]
        
        all_valid = True
        for filename, validator in files_to_validate:
            if os.path.exists(filename):
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    is_valid, issues = validator(data) if hasattr(validator, '__code__') and 'issues' in validator.__code__.co_varnames else (validator(data), [])
                    if is_valid:
                        print(f"[✓] {filename}: Valide")
                    else:
                        print(f"[✗] {filename}: Invalide - {issues}")
                        all_valid = False
                except Exception as e:
                    print(f"[✗] {filename}: Erreur - {e}")
                    all_valid = False
            else:
                print(f"[ℹ] {filename}: Absent (utilisation des valeurs par défaut)")
        
        if args.fix_issues and not all_valid:
            print("\n🛠️  CORRECTION DES PROBLÈMES")
            # Ici, on pourrait implémenter une logique de correction automatique
            print("Fonctionnalité de correction à implémenter")
        
        return
    
    if not args.context:
        parser.print_help()
        return
    
    # Configuration aléatoire
    if args.seed is not None:
        random.seed(args.seed)
        logging.info(f"Seed: {args.seed}")
    
    # Chargement des ressources
    logging.info("Chargement des ressources")
    anchors = resource_manager.load_json("anchors.json", DEFAULT_ANCHORS, "anchors", DataValidator.validate_anchors)
    incantations = resource_manager.load_json("incantations.json", DEFAULT_INCANTATIONS, "incantations")
    glitches = resource_manager.load_json("glitches.json", DEFAULT_GLITCHES, "glitches")
    locations = resource_manager.load_json("locations.json", DEFAULT_LOCATIONS, "locations")
    effects = resource_manager.load_json("effects.json", DEFAULT_EFFECTS, "effects")
    incompatible_pairs = resource_manager.load_json("incompatible_pairs.json", list(DEFAULT_INCOMPATIBLE_PAIRS), "incompatible pairs")
    incompatible_pairs_set = set((a.upper(), b.upper()) for a, b in incompatible_pairs)
    
    # Chargement des profils
    profiles = resource_manager.load_profiles("profiles.json")
    selected_profile = profiles.get(args.profile)
    if not selected_profile and os.path.exists(args.profile):
        # Essayer de charger un profil personnalisé
        try:
            with open(args.profile, "r", encoding="utf-8") as f:
                profile_data = json.load(f)
                is_valid, issues = DataValidator.validate_profile(profile_data)
                if is_valid:
                    selected_profile = GenerationProfile.from_dict(profile_data)
                    logging.info(f"Profil personnalisé chargé: {args.profile}")
                else:
                    logging.warning(f"Profil personnalisé invalide: {issues}")
                    selected_profile = profiles.get("standard")
        except Exception as e:
            logging.error(f"Erreur chargement profil personnalisé: {e}")
            selected_profile = profiles.get("standard")
    elif not selected_profile:
        selected_profile = profiles.get("standard")
    
    # Chargement des templates
    templates = resource_manager.load_templates("templates.json")
    selected_template = templates.get(args.template, templates["standard"])
    
    # Analyse du contexte
    logging.info(f"Analyse du contexte: {args.context}")
    context = args.context
    context_type = context_processor.detect_context_type(context)
    keywords = context_processor.extract_keywords(context)
    
    # Sélection des éléments de base (compatible avec v3)
    rune_map = {
        ("temps", "temporel", "boucle", "cycle", "aube"): "jera",
        ("mémoire", "souvenir", "oubli", "effacement", "cloche", "mnémonique", "vérité"): "kenaz",
        ("réseau", "racine", "yggdrasil", "connexion", "mycélium"): "eihwaz",
        ("identité", "double", "masque", "personnage", "main rouge"): "mannaz",
        ("protection", "sécurité", "bouclier", "exode"): "algiz",
        ("destruction", "foudre", "colère", "virus"): "thurisaz",
        ("voyage", "prophétie", "vision", "porte"): "raidho",
        ("paleo", "codex", "livre", "stein", "zero", "echo", "fragment"): "ansuz"
    }
    
    candidates = []
    for keyword_list, candidate_rune in rune_map.items():
        if any(kw in context.lower() for kw in keyword_list):
            intensity = rune_analyzer.get_rune_intensity(candidate_rune, context, selected_profile)
            candidates.append((candidate_rune, intensity))
    
    rune = candidates[0][0] if candidates else "kenaz"
    intensity = rune_analyzer.get_rune_intensity(rune, context, selected_profile)
    
    # Sélection du lieu
    loc_map = {
        ("hague", "node", "focal", "centrale"): "hague",
        ("raz", "vortex", "tempête", "mer"): "raz",
        ("rouen", "cathédrale", "archive", "cloche"): "rouen",
        ("caen", "profonde", "nexus", "graffiti"): "caen",
    }
    
    location = next((loc for keywords, loc in loc_map.items() 
                    if any(kw in context.lower() for kw in keywords) and loc in locations), 
                   next(iter(locations)))
    
    # Sélection de l'effet
    effect_mapping = {
        "jera": "temporel",
        "kenaz": "mémoriel", 
        "eihwaz": "réseau",
        "mannaz": "identité",
        "algiz": "protection",
        "thurisaz": "destruction"
    }
    
    cat = effect_mapping.get(rune, "mémoriel")
    if cat in effects and effects[cat]:
        # Filtrer les effets exclus par le profil
        available_effects = effects[cat]
        if selected_profile and selected_profile.excluded_effects:
            available_effects = [e for e in available_effects 
                               if not any(excluded in e.lower() 
                                         for excluded in selected_profile.excluded_effects)]
        
        # Vérifier les incompatibilités
        compatible_effects = []
        for effect in available_effects:
            is_compatible = True
            for eff, blocked_rune in incompatible_pairs_set:
                if eff.lower() in effect.lower() and blocked_rune.lower() == rune.upper():
                    is_compatible = False
                    break
            if is_compatible:
                compatible_effects.append(effect)
        
        effect = random.choice(compatible_effects) if compatible_effects else "mémoire vérité"
    else:
        effect = "mémoire vérité"
    
    # Affichage des informations de contexte
    print(f"\n🧠 ANALYSE DU CONTEXTE\n" + "="*80)
    print(f"Contexte: «{context}»")
    print(f"Type détecté: {context_type}")
    print(f"Mots-clés: {', '.join(keywords[:5])}")
    print(f"Rune: {rune.upper()} ({RUNE_MEANINGS[rune]})")
    print(f"Intensité: {intensity}/10")
    print(f"Lieu: {locations.get(location, location)}")
    print(f"Effet: {effect}")
    print(f"Profil: {selected_profile.name if selected_profile else 'default'}")
    print(f"Template: {args.template}")
    print(f"Chaînage: {args.chain if args.chain != 'none' else 'aucun'}")
    
    # Initialisation du générateur
    pass_generator = PassGenerator(resource_manager, rune_analyzer)
    analyzer = FracturoAnalyzer() if args.analyze else None
    
    # Préparation des métadonnées
    metadata = {
        "context": context,
        "context_type": context_type,
        "keywords": keywords,
        "rune": rune,
        "rune_meaning": RUNE_MEANINGS[rune],
        "intensity": intensity,
        "location": location,
        "location_name": locations.get(location, location),
        "effect": effect,
        "profile": selected_profile.name if selected_profile else "default",
        "template": args.template,
        "passes_count": args.passes,
        "variation": args.variation,
        "chain_type": args.chain if args.chain != 'none' else None,
        "timestamp": datetime.now().isoformat(),
        "seed": args.seed,
        "version": "fracturo_amp_v4"
    }
    
    # Génération du header
    header_template = selected_template.get("header", DEFAULT_TEMPLATES["standard"]["header"])
    full_output = header_template.format(**metadata)
    
    # Génération des passes
    passes_data = []
    chains = []
    
    logging.info(f"Génération de {args.passes} passes")
    for i in range(1, args.passes + 1):
        pass_data = pass_generator.generate_pass(
            context=context,
            base_rune=rune,
            base_location=location,
            base_effect=effect,
            pass_id=i,
            anchors=anchors,
            incantations=incantations,
            glitches=glitches,
            locations=locations,
            effects=effects,
            variation_mode=args.variation,
            profile=selected_profile,
            template=selected_template
        )
        
        full_output += pass_data["text"] + "\n"
        passes_data.append(pass_data)
        
        if analyzer:
            analyzer.analyze_pass(pass_data)
        
        # Création de chaînes si demandé
        if args.chain != "none" and i % 3 == 0:
            chain = pass_generator.generate_chain(
                base_pass_id=i,
                chain_type=args.chain,
                num_linked=random.randint(2, 4)
            )
            chains.append(chain)
            logging.debug(f"Chaîne créée: {chain.id}")
    
    # Ajout des informations de chaînage
    if chains:
        full_output += "\n" + "="*80 + "\n"
        full_output += "🔗 CHAÎNES DÉTECTÉES\n"
        full_output += "="*80 + "\n\n"
        for chain in chains:
            full_output += f"• {chain.id}: {chain.narrative_arc}\n"
            full_output += f"  Base: P{chain.base_pass_id:02d} | Liées: {', '.join(f'P{p:02d}' for p in chain.linked_passes)}\n"
    
    # Rapport d'analyse
    if args.analyze and analyzer:
        analysis_report = analyzer.generate_report()
        full_output += analysis_report
    
    # Footer
    footer_template = selected_template.get("footer", "")
    if footer_template:
        full_output += "\n" + footer_template.format(**metadata)
    
    # Export
    if args.output:
        base_filename = args.output
        export_mgr = ExportManager()
        
        if args.format == "txt" or args.format == "all":
            export_mgr.export_txt(full_output, f"{base_filename}.txt", metadata)
        
        if args.format == "json" or args.format == "all":
            export_mgr.export_json(passes_data, f"{base_filename}.json", metadata, analyzer)
        
        if args.format == "markdown" or args.format == "all":
            export_mgr.export_markdown(full_output, f"{base_filename}.md", metadata, analyzer)
        
        if args.format == "html" or args.format == "all":
            export_mgr.export_html(passes_data, f"{base_filename}.html", metadata, analyzer)
        
        logging.info(f"Export terminé vers {base_filename}.*")
    else:
        print(full_output)
    
    logging.info("FracturoScript terminé avec succès")

if __name__ == "__main__":
    main()
