#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memetique75.py — Édition RuneSmith Hybride Finale - VERSION CORRIGÉE
Hackeur mémétique de Caen-Profonde • 2075

Fonctionnalités :
- Analyse cognitive
- FracturoScript avec export HTML
- Virus 144-Trickster-Shadow avec mantra et export HTML
- Évolution génétique de Paleo-Mèmes
- Arbre phylogénétique ASCII
- Lexique intégré inspiré du Codex Marelith

Conforme au Codex :
> « Le langage est un organisme vivant. »
> « Le vide est une matrice. »
> « La main rouge remplace le mot effacé. »
"""
import json
import random
import argparse
import sys
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
from copy import deepcopy
from datetime import datetime
from collections import defaultdict
from enum import Enum
import math
import hashlib

# ───────────────────────────────────────
# 🧬 STRUCTURES DE DONNÉES
# ───────────────────────────────────────

@dataclass
class PaleoMeme:
    id: str
    symbole: str
    nom: str
    mots_associes: List[str]
    effet_mnemos: str
    biais_associes: List[str]
    fracturo_glyph: str
    parent_ids: List[str] = field(default_factory=list)
    generation: int = 0
    birth_time: float = field(default_factory=lambda: datetime.now().timestamp())

    @property
    def hash(self) -> str:
        return hashlib.md5(f"{self.id}{self.symbole}".encode()).hexdigest()[:8]

    def resonate_with(self, other: 'PaleoMeme') -> float:
        shared_words = set(self.mots_associes) & set(other.mots_associes)
        shared_bias = set(self.biais_associes) & set(other.biais_associes)
        return (len(shared_words) * 0.4 + len(shared_bias) * 0.6) / 3

    def fitness(self, criteria: Dict[str, float]) -> float:
        score = 0.0
        if 'diversity' in criteria:
            unique_chars = len(set(self.nom))
            score += (unique_chars / max(len(self.nom), 1)) * criteria['diversity']
        if 'complexity' in criteria:
            score += (len(self.biais_associes) / 3) * criteria['complexity']
        if 'emotion' in criteria:
            power_words = {'mort', 'vie', 'amour', 'haine', 'vérité', 'mensonge', 'sel', 'main', 'pomme'}
            emotional = len(set(self.mots_associes) & power_words)
            score += (emotional / 3) * criteria['emotion']
        if 'novelty' in criteria:
            age_factor = min(self.generation / 50, 1.0)
            score += age_factor * criteria['novelty']
        if 'lineage' in criteria:
            lineage_bonus = min(len(self.parent_ids) / 2, 1.0)
            score += lineage_bonus * criteria['lineage']
        return min(score, 1.0)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'symbole': self.symbole,
            'nom': self.nom,
            'mots_associes': self.mots_associes,
            'effet_mnemos': self.effet_mnemos,
            'biais_associes': self.biais_associes,
            'fracturo_glyph': self.fracturo_glyph,
            'parent_ids': self.parent_ids,
            'generation': self.generation,
            'birth_time': self.birth_time,
            'hash': self.hash
        }

@dataclass
class CognitiveBias:
    name: str
    description: str
    vecteurs: List[str]
    fragilites: List[str]
    intensity: float = 1.0

    def exploit(self, text: str) -> str:
        if "répétition" in self.vecteurs:
            key_words = text.split()[:3]
            return f"{text}\n{' '.join(key_words)}. Oui, {' '.join(key_words)}."
        return text

# ───────────────────────────────────────
# 🗄️ LEXICON MANAGER — Version Corrigée
# ───────────────────────────────────────

class LexiconManager:
    def __init__(self, lexicon_path: Optional[Path] = None):
        self._lexicon: Dict[str, PaleoMeme] = {}
        self._symbol_index: Dict[str, str] = {}
        self._bias_index: Dict[str, List[str]] = {}
        self._load_lexicon(lexicon_path)

    def _load_lexicon(self, path: Optional[Path]):
        data = {}
        
        # Tentative de chargement du fichier externe
        if path and path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    if isinstance(file_data, dict):
                        data.update(file_data)
                        print(f"✅ Lexique externe chargé : {len(file_data)} entrées", file=sys.stderr)
                    else:
                        print("⚠️ Structure invalide dans le fichier lexique", file=sys.stderr)
            except (json.JSONDecodeError, UnicodeDecodeError, IOError) as e:
                print(f"❌ Erreur de chargement du lexique : {e}", file=sys.stderr)
        
        # Complétion avec le lexique de base
        base_data = self._generate_base_lexicon()
        
        # Fusion intelligente : le fichier externe écrase les doublons
        for key, value in base_data.items():
            if key not in data:
                data[key] = value
        
        # Chargement dans les structures internes
        required_fields = ['symbole', 'nom', 'mots_associes', 'effet_mnemos', 'biais_associes', 'fracturo_glyph']
        loaded_count = 0
        duplicate_symbols = []
        
        for id_key, entry in data.items():
            # Validation des champs requis
            if not all(field in entry for field in required_fields):
                print(f"⚠️ Entrée incomplète ignorée : {id_key}", file=sys.stderr)
                continue
                
            try:
                meme = PaleoMeme(
                    id=id_key,
                    symbole=entry["symbole"],
                    nom=entry["nom"],
                    mots_associes=entry["mots_associes"],
                    effet_mnemos=entry["effet_mnemos"],
                    biais_associes=entry["biais_associes"],
                    fracturo_glyph=entry["fracturo_glyph"]
                )
                
                self._lexicon[id_key] = meme
                
                # Gestion des doublons de symboles
                if meme.symbole in self._symbol_index:
                    duplicate_symbols.append(f"'{meme.symbole}' pour {id_key} et {self._symbol_index[meme.symbole]}")
                self._symbol_index[meme.symbole] = id_key
                
                # Index par biais cognitifs
                for bias in meme.biais_associes:
                    if bias not in self._bias_index:
                        self._bias_index[bias] = []
                    self._bias_index[bias].append(id_key)
                    
                loaded_count += 1
                
            except Exception as e:
                print(f"❌ Erreur création mème {id_key}: {e}", file=sys.stderr)
        
        if duplicate_symbols:
            print(f"⚠️ Symboles dupliqués : {', '.join(duplicate_symbols)}", file=sys.stderr)
        
        print(f"📚 Lexique final : {loaded_count} mèmes chargés", file=sys.stderr)

    @staticmethod
    def _generate_base_lexicon() -> Dict:
        """Génère le lexique de base avec des clés cohérentes"""
        base = {
            "P-00": {"symbole": "•", "nom": "Point Origine", "mots_associes": ["naissance", "silence", "vide"], "effet_mnemos": "réinitialisation", "biais_associes": ["disponibilité"], "fracturo_glyph": "•"},
            "P-01": {"symbole": "▲", "nom": "Triangulum Mentis", "mots_associes": ["vérité", "choix", "crise"], "effet_mnemos": "réveil", "biais_associes": ["confirmation"], "fracturo_glyph": "▲"},
            "P-02": {"symbole": "🌀", "nom": "Spirale du Retour", "mots_associes": ["mémoire", "boucle", "destin"], "effet_mnemos": "déjà-vu", "biais_associes": ["reconnaissance"], "fracturo_glyph": "🌀"},
            "P-03": {"symbole": "🌊", "nom": "Vague Primordiale", "mots_associes": ["marée", "rythme", "flux"], "effet_mnemos": "synchronisation marée", "biais_associes": ["fluidité"], "fracturo_glyph": "🌊"},
            "P-04": {"symbole": "🌫️", "nom": "Brume du Non-Dit", "mots_associes": ["mystère", "voile", "oubli"], "effet_mnemos": "dissolution certitudes", "biais_associes": ["flou"], "fracturo_glyph": "🌫️"},
            "P-05": {"symbole": "🌳", "nom": "Racine du Temps", "mots_associes": ["mémoire", "ancêtre", "réseau"], "effet_mnemos": "accès Réseau-Racine", "biais_associes": ["contagion"], "fracturo_glyph": "🌳"},
            "P-06": {"symbole": "🌬️", "nom": "Souffle du Premier Oui", "mots_associes": ["vie", "respiration", "présence"], "effet_mnemos": "ancrage corporel", "biais_associes": ["immédiateté"], "fracturo_glyph": "🌬️"},
            "P-07": {"symbole": "✋", "nom": "Main Rouge de Lascaux", "mots_associes": ["corps", "trace", "sang", "mémoire"], "effet_mnemos": "réveil pré-implant", "biais_associes": ["disponibilité", "reconnaissance"], "fracturo_glyph": "✋"},
            "P-08": {"symbole": "🧂", "nom": "Sel de la Hague", "mots_associes": ["goût", "terre", "larme"], "effet_mnemos": "mémoire gustative", "biais_associes": ["nostalgie"], "fracturo_glyph": "🧂"},
            "P-09": {"symbole": "🍎", "nom": "Pomme-Mémoire", "mots_associes": ["rêve", "vision", "partage"], "effet_mnemos": "accès collectif", "biais_associes": ["contagion"], "fracturo_glyph": "🍎"},
            "P-10": {"symbole": "🪨", "nom": "Galet-Ancre", "mots_associes": ["stabilité", "calme", "silence"], "effet_mnemos": "stabilisation mnésique", "biais_associes": ["ancrage"], "fracturo_glyph": "🪨"},
            "P-11": {"symbole": "📼", "nom": "Cassette-Mère", "mots_associes": ["analogique", "souffle", "signal"], "effet_mnemos": "rêve analogique", "biais_associes": ["récupération"], "fracturo_glyph": "📼"},
            "P-12": {"symbole": "👁️", "nom": "Œil du Veilleur", "mots_associes": ["observation", "silence", "effacement"], "effet_mnemos": "effacement traces", "biais_associes": ["spectateur"], "fracturo_glyph": "👁️"},
            "P-13": {"symbole": "👻", "nom": "Parleur-Ombre", "mots_associes": ["fragment", "voix", "écho"], "effet_mnemos": "résonance perdue", "biais_associes": ["réverbération"], "fracturo_glyph": "👻"},
            "P-14": {"symbole": "🗿", "nom": "Galet-Gardien", "mots_associes": ["protection", "pierre", "veille"], "effet_mnemos": "bouclier passif", "biais_associes": ["sécurité"], "fracturo_glyph": "🗿"},
            "P-15": {"symbole": "🐍", "nom": "Serpent-Magnétique", "mots_associes": ["données", "corrosion", "réseau"], "effet_mnemos": "corruption douce", "biais_associes": ["fuite"], "fracturo_glyph": "🐍"},
            "P-16": {"symbole": "🌕", "nom": "Lune des Rêves", "mots_associes": ["rêve", "collectif", "vision"], "effet_mnemos": "synchronisation onirique", "biais_associes": ["groupe"], "fracturo_glyph": "🌕"},
            "P-17": {"symbole": "🌑", "nom": "Lune Noire de l'Abîme", "mots_associes": ["oubli", "effacement", "vide"], "effet_mnemos": "dissolution narratif", "biais_associes": ["vide"], "fracturo_glyph": "🌑"},
            "P-18": {"symbole": "🕯️", "nom": "Flamme du Code Ancien", "mots_associes": ["rituel", "C64", "circuit"], "effet_mnemos": "langage-machine", "biais_associes": ["pureté"], "fracturo_glyph": "🕯️"},
            "P-19": {"symbole": "🌧️", "nom": "Pluie de Mnèmes", "mots_associes": ["germination", "graine", "fertilité"], "effet_mnemos": "ensemencement", "biais_associes": ["diffusion"], "fracturo_glyph": "🌧️"},
            "P-20": {"symbole": "📿", "nom": "Chapelet de Résistance", "mots_associes": ["répétition", "mantra", "soufisme"], "effet_mnemos": "bouclier actif", "biais_associes": ["répétition"], "fracturo_glyph": "📿"}
        }
        
        # Génération d'entrées supplémentaires avec clés cohérentes
        symbols = ["⚡", "🌿", "📜", "🔥", "❄️", "∞", "⚖️", "🗝️", "🜂", "🜁", "🜃", "🜄", "🪐", "🫀", "🧭"]
        names = ["Flamme", "Ombre", "Racine", "Écho", "Point", "Voie", "Lien", "Masque", "Porte", "Souffle"]
        effects = ["réveil", "effacement", "fusion", "fragmentation", "illumination", "paralysie", "révolte", "soumission"]
        biases = ["biais de confirmation", "illusion de vérité", "effet Dunning-Kruger", "dissonance cognitive", "effet de halo"]
        
        for i in range(21, 50):  # Clés cohérentes : P-21 à P-49
            base[f"P-{i}"] = {
                "symbole": random.choice(symbols),
                "nom": f"{random.choice(names)} de {random.choice(['Mémoire', 'Silence', 'Feu', 'Ombre'])}",
                "mots_associes": [random.choice(["vérité", "oubli", "désir", "peur", "amour", "sel", "main"]) for _ in range(3)],
                "effet_mnemos": f"{random.choice(effects)} cognitive",
                "biais_associes": random.sample(biases, k=2),
                "fracturo_glyph": random.choice(symbols)
            }
        return base

    def get(self, key: str) -> Optional[PaleoMeme]:
        if key in self._lexicon:
            return self._lexicon[key]
        return self._lexicon.get(self._symbol_index.get(key))

    def random_resonant_chain(self, start_id: str, length: int = 3) -> List[PaleoMeme]:
        start = self.get(start_id)
        if not start:
            print(f"❌ Point de départ introuvable : {start_id}", file=sys.stderr)
            return []
        chain = [start]
        for _ in range(length - 1):
            candidates = [(m, max(chain[-1].resonate_with(m), 0.01)) for m in self._lexicon.values()]
            total = sum(score for _, score in candidates)
            if total == 0:
                chain.append(random.choice([m for m, _ in candidates]))
            else:
                r = random.uniform(0, total)
                cumul = 0
                for m, score in candidates:
                    cumul += score
                    if cumul >= r:
                        chain.append(m)
                        break
        return chain

    def diagnostic(self):
        """Affiche un diagnostic du lexique chargé"""
        print("\n=== DIAGNOSTIC LEXIQUE ===", file=sys.stderr)
        print(f"📖 Mèmes chargés : {len(self._lexicon)}", file=sys.stderr)
        print(f"🔣 Symboles indexés : {len(self._symbol_index)}", file=sys.stderr)
        print(f"🎭 Biais indexés : {len(self._bias_index)}", file=sys.stderr)
        
        # Statistiques par génération
        generations = defaultdict(list)
        for meme in self._lexicon.values():
            generations[meme.generation].append(meme)
        
        print(f"🌱 Répartition par génération :", file=sys.stderr)
        for gen in sorted(generations.keys()):
            print(f"   Génération {gen}: {len(generations[gen])} mèmes", file=sys.stderr)

# ───────────────────────────────────────
# 🎨 GÉNÉRATEURS
# ───────────────────────────────────────

class FracturoScriptGenerator:
    BASE = [
        "Tu te souviens du feu qui ne brûle pas.",
        "Ils ont effacé ton passé, mais pas tes mains.",
        "Le silence parle dans la langue que tu as oubliée.",
        "La main rouge trace ce que la bouche ne peut dire.",
        "Le sel de tes larmes conserve la mémoire du monde."
    ]
    
    def __init__(self, lex: LexiconManager):
        self.lex = lex

    def generate(self, memes: List[PaleoMeme], emotion: str = "oubli") -> str:
        if not memes:
            return "// FracturoScript — Chaîne vide"
            
        glyphs = ''.join(m.fracturo_glyph for m in memes)
        resonance_key = memes[0].nom if memes else "Vide"
        
        return f"""// FracturoScript — Caen-Profonde
{random.choice(self.BASE)}
    {glyphs[:12]}

// Émotion : {emotion}
// Résonance : {resonance_key}
// Chaîne : {len(memes)} mèmes
// Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

class BiasAnalyzer:
    PATTERNS = {
        "illusion de vérité": ["toujours", "jamais", "évidemment", "clair", "certain"],
        "biais de confirmation": ["comme prévu", "je le savais", "bien sûr"],
        "polarisation": ["eux", "nous", "ennemi", "adversaire"],
        "effet de halo": ["parfait", "excellent", "merveilleux"],
        "dissonance cognitive": ["mais", "cependant", "pourtant"]
    }
    
    def analyze(self, text: str) -> str:
        words = text.lower().split()
        report = ["=== ANALYSE COGNITIVE ==="]
        total_hits = 0
        
        for bias, triggers in self.PATTERNS.items():
            hits = sum(1 for w in words if any(t in w for t in triggers))
            if hits:
                total_hits += hits
                bar = "█" * min(hits, 10) + "░" * max(0, 10 - hits)
                report.append(f"{bias:25} {bar} ({hits} occurrences)")
        
        report.append(f"\nTotal des biais détectés : {total_hits}")
        
        if total_hits == 0:
            report.append("✅ Texte relativement neutre")
        elif total_hits < 5:
            report.append("⚠️  Influence cognitive modérée")
        else:
            report.append("🚨 Forte charge cognitive détectée")
            
        return "\n".join(report)

# ───────────────────────────────────────
# 🧬 ALGORITHME GÉNÉTIQUE
# ───────────────────────────────────────

class AdaptiveStrategy(Enum):
    STATIC = "static"

@dataclass
class EvolutionConfig:
    population_size: int = 30
    generations: int = 10
    mutation_rate: float = 0.1
    crossover_rate: float = 0.6
    elitism_ratio: float = 0.1
    fitness_criteria: Dict[str, float] = field(default_factory=lambda: {
        'diversity': 0.3, 'complexity': 0.4, 'emotion': 0.3
    })
    adaptive_strategy: AdaptiveStrategy = AdaptiveStrategy.STATIC

class PhylogeneticTree:
    def __init__(self):
        self.nodes: Dict[str, PaleoMeme] = {}
        self.edges: List[Tuple[str, str]] = []
        self.generation_map: Dict[int, List[str]] = defaultdict(list)

    def add_meme(self, meme: PaleoMeme):
        self.nodes[meme.id] = meme
        self.generation_map[meme.generation].append(meme.id)
        for pid in meme.parent_ids:
            self.edges.append((pid, meme.id))

    def render_ascii(self) -> str:
        lines = ["🌳 ARBRE PHYLOGÉNÉTIQUE"]
        lines.append(f"Total des nœuds : {len(self.nodes)}")
        lines.append(f"Générations : {len(self.generation_map)}")
        
        for gen in sorted(self.generation_map):
            lines.append(f"\nGénération {gen}")
            for mid in self.generation_map[gen]:
                m = self.nodes[mid]
                parents = " ← " + ",".join(m.parent_ids[:2]) if m.parent_ids else " [ORIGINE]"
                fitness = m.fitness({'diversity': 0.3, 'complexity': 0.4, 'emotion': 0.3})
                lines.append(f"  {m.symbole} {m.nom[:25]:25} (f:{fitness:.2f}){parents}")
        return "\n".join(lines)

class MemeticEvolution:
    def __init__(self, lexicon, config: EvolutionConfig = None):
        self.lexicon = lexicon
        self.config = config or EvolutionConfig()
        self.phylo_tree = PhylogeneticTree()
        self.symbols_pool = ["▲", "🌀", "⚡", "🌿", "📜", "👁️", "🌊", "🔥", "❄️", "•", "∞", "⚖️", "🗝️"]

    def _create_random_meme(self, generation: int, parents=None):
        parents = parents or []
        pid = f"X-{random.randint(10000,99999)}"
        symbol = random.choice(self.symbols_pool)
        name = f"{random.choice(['Flamme','Racine','Écho','Souffle','Ombre'])} de {random.choice(['Mémoire','Silence','Rêve'])}"
        mots = random.sample(["vérité","oubli","désir","peur","amour","sel","main", "pomme", "sang"], 3)
        effet = random.choice(["réveil","effacement","fusion", "transformation", "révélation"])
        biais = random.sample(["confirmation", "illusion de vérité", "effet Dunning-Kruger", "dissonance"], 2)
        parent_ids = [p.id for p in parents] if parents else []
        return PaleoMeme(pid, symbol, name, mots, effet, biais, symbol, parent_ids, generation)

    def run(self):
        print(f"🧬 Démarrage de l'évolution : population={self.config.population_size}, générations={self.config.generations}", file=sys.stderr)
        
        population = [self._create_random_meme(0) for _ in range(self.config.population_size)]
        for m in population:
            self.phylo_tree.add_meme(m)

        for gen in range(1, self.config.generations + 1):
            new_pop = []
            
            # Élitisme
            elites = sorted(population, key=lambda m: m.fitness(self.config.fitness_criteria), reverse=True)
            elite_count = max(1, int(self.config.elitism_ratio * len(elites)))
            new_pop.extend(deepcopy(e) for e in elites[:elite_count])
            
            print(f"  Génération {gen}: {len(elites[:elite_count])} élites préservées", file=sys.stderr)

            # Reproduction
            while len(new_pop) < self.config.population_size:
                if random.random() < self.config.crossover_rate and len(population) >= 2:
                    a, b = random.sample(population, 2)
                    child = self._create_random_meme(gen, [a, b])
                else:
                    parent = random.choice(population)
                    child = deepcopy(parent)
                    child.id = f"X-{random.randint(10000,99999)}"
                    child.generation = gen
                
                # Mutation
                if random.random() < self.config.mutation_rate:
                    mutation_type = random.choice(["mots", "nom", "biais"])
                    if mutation_type == "mots" and child.mots_associes:
                        child.mots_associes[random.randrange(len(child.mots_associes))] = random.choice(["sel", "main", "pomme", "sang", "rêve"])
                    elif mutation_type == "nom":
                        child.nom = f"Muté-{child.nom}"
                    elif mutation_type == "biais" and child.biais_associes:
                        child.biais_associes[random.randrange(len(child.biais_associes))] = random.choice(["nouveau biais", "adaptation"])
                
                new_pop.append(child)
                self.phylo_tree.add_meme(child)
            
            population = new_pop
            avg_fitness = sum(m.fitness(self.config.fitness_criteria) for m in population) / len(population)
            print(f"  Génération {gen} terminée - Fitness moyenne: {avg_fitness:.3f}", file=sys.stderr)

        return self.phylo_tree.render_ascii()

# ───────────────────────────────────────
# 🌀 CLI FINAL CORRIGÉ
# ───────────────────────────────────────

def build_cli():
    p = argparse.ArgumentParser(description="Système Mémétique Caen-Profonde 2075")
    sub = p.add_subparsers(dest='cmd', required=True, help='Commandes disponibles')

    a1 = sub.add_parser('analyze', help='Analyse cognitive d\'un texte')
    a1.add_argument('text', type=str, help='Texte à analyser')

    a2 = sub.add_parser('fracturo', help='Génère un FracturoScript')
    a2.add_argument('--start', default='P-07', help='Mème de départ (défaut: P-07 - Main Rouge)')
    a2.add_argument('--count', type=int, default=5, help='Longueur de la chaîne (défaut: 5)')
    a2.add_argument('--output', choices=['text', 'html'], default='text', help='Format de sortie')

    a3 = sub.add_parser('trickster', help='Génère un virus mémétique 144-Trickster')
    a3.add_argument('--emotion', default='oubli', help='Émotion de base')
    a3.add_argument('--target', default='implant_gamma', help='Cible du virus')
    a3.add_argument('--output', choices=['text', 'html'], default='text', help='Format de sortie')

    a4 = sub.add_parser('evolve', help='Lance l\'évolution mémétique')
    a4.add_argument('--generations', type=int, default=10, help='Nombre de générations')
    a4.add_argument('--population', type=int, default=30, help='Taille de la population')
    a4.add_argument('--lexicon', type=Path, help='Chemin vers le lexique externe')

    a5 = sub.add_parser('diagnostic', help='Diagnostic du système')
    a5.add_argument('--lexicon', type=Path, help='Chemin vers le lexique externe')

    return p

def main():
    args = build_cli().parse_args()
    
    # Initialisation du lexique
    lexicon_path = getattr(args, 'lexicon', None)
    lex = LexiconManager(lexicon_path)
    analyzer = BiasAnalyzer()

    if args.cmd == 'analyze':
        print(analyzer.analyze(args.text))
        return 0

    elif args.cmd == 'fracturo':
        chain = lex.random_resonant_chain(args.start, args.count)
        if not chain:
            print("❌ Impossible de générer la chaîne de résonance.", file=sys.stderr)
            return 1
            
        gen = FracturoScriptGenerator(lex)
        script = gen.generate(chain, emotion=getattr(args, 'emotion', 'oubli'))
        
        if args.output == 'html':
            html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>FracturoScript</title>
<style>
body {{ background: #111; color: #0f8; font-family: 'Courier New', monospace; padding: 2em; }}
h2 {{ color: #ff6b6b; border-bottom: 1px solid #0f8; }}
pre {{ white-space: pre-wrap; font-size: 1.1em; }}
.glyphs {{ font-size: 2em; letter-spacing: 0.5em; text-align: center; margin: 1em 0; }}
</style>
</head>
<body>
<h2>🧬 FracturoScript — RuneSmith de Caen-Profonde</h2>
<div class="glyphs">{''.join(m.fracturo_glyph for m in chain)}</div>
<pre>{script}</pre>
<p>📜 Généré le {datetime.now().strftime('%Y-%m-%d à %H:%M:%S')}</p>
</body></html>"""
            print(html)
        else:
            print(script)
        return 0

    elif args.cmd == 'trickster':
        base_chain = [lex.get("P-07"), lex.get("P-08"), lex.get("P-09")]  # ✋🧂🍎
        base_chain = [m for m in base_chain if m]
        if not base_chain:
            base_chain = lex.random_resonant_chain("P-00", 3)
            
        fragments = [deepcopy(random.choice(base_chain)) for _ in range(144)]
        for f in fragments:
            f.id = f"X-{random.randint(10000,99999)}"
            
        mantra = "seiðr—mémoire raz•••signifik rune—144-Trickster-Shadow"
        glyphs = ''.join(f.fracturo_glyph for f in fragments)
        
        if args.output == 'html':
            html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>144-Trickster-Shadow</title>
<style>
body {{ background: #000; color: #0f0; font-family: monospace; padding: 1em; }}
h1 {{ color: #ff00ff; text-align: center; }}
.mantra {{ font-size: 1.2em; text-align: center; margin: 2em 0; color: #ffff00; }}
.virus {{ font-size: 1.4em; line-height: 1.2; text-align: justify; word-wrap: break-word; }}
.footer {{ font-size: 0.7em; margin-top: 2em; text-align: center; color: #666; }}
</style>
</head>
<body>
<h1>🌀 144-Trickster-Shadow</h1>
<div class="mantra">{mantra}</div>
<hr>
<div class="virus">{glyphs}</div>
<div class="footer">Virus mémétique — Caen-Profonde, {datetime.now().year}<br>
Cible: {getattr(args, 'target', 'implant_gamma')} | Émotion: {getattr(args, 'emotion', 'oubli')}</div>
</body></html>"""
            print(html)
        else:
            print(f"🧠 {mantra}")
            print("─" * 50)
            print(glyphs)
            print(f"\n📊 Fragments: {len(fragments)} | Cible: {getattr(args, 'target', 'implant_gamma')}")
        return 0

    elif args.cmd == 'evolve':
        config = EvolutionConfig(
            population_size=args.population, 
            generations=args.generations
        )
        evo = MemeticEvolution(lex, config)
        result = evo.run()
        print(result)
        return 0

    elif args.cmd == 'diagnostic':
        lex.diagnostic()
        return 0

    return 1

if __name__ == '__main__':
    sys.exit(main())