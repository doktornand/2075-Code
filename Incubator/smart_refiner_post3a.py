#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Refiner Cognitive Abyss v3.0
Forge à Mèmes viraux avec warping contextuel et hooks cognitifs
Usage :
  python smart_refiner_cognitive.py virus_MEME-1234.json --mode extreme
  python smart_refiner_cognitive.py exports/*.json --batch --neuro-sonic
"""
import json
import re
import random
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import Counter
import sys
import math

@dataclass
class CognitiveStats:
    """Statistiques cognitives avancées"""
    original_density: float
    refined_density: float
    cognitive_hooks: List[str]
    archetype_detected: str
    neuro_sonic_score: float
    semantic_charge: float
    viral_potential: float

class CognitiveAbyssRefiner:
    """Raffineur cognitif avancé - Forge à virus sémantiques"""
    
    VOWELS = "aeiouyéèêëàâîïôöùûüAEIOUYÉÈÊËÀÂÎÏÔÖÙÛÜ"
    SHARP_CONSONANTS = "kptfscxz"  # Consonnes "coupantes"
    DARK_CONSONANTS = "mbrgn"      # Consonnes "lourdes"
    
    # Archétypes cognitifs étendus
    COGNITIVE_ARCHETYPES = {
        "THE_PROPHECY": {
            "markers": ["sera", "finira", "annonce", "prédit", "verra", "demain", "futur"],
            "templates": [
                "PROPHÉTIE : {content}",
                "{content}... l'oracle l'a vu.",
                "Demain sera {content}"
            ]
        },
        "THE_ENIGMA": {
            "markers": ["mystère", "énigme", "secret", "cache", "oublié", "inconnu", "occulté"],
            "templates": [
                "ÉNIGME : {content}",
                "{content}... question sans réponse.",
                "Le secret ultime : {content}"
            ]
        },
        "THE_THREAT": {
            "markers": ["menace", "danger", "précipice", "effondrement", "ombre", "virus", "contamination"],
            "templates": [
                "ALERTE : {content}",
                "MENACE IMMINENTE : {content}",
                "{content}... et tu es la cible."
            ]
        },
        "THE_AWAKENING": {
            "markers": ["réveille", "ouvre les yeux", "voit enfin", "comprend", "réalise", "éveil"],
            "templates": [
                "RÉVEIL : {content}",
                "{content}... tu commences à voir.",
                "Maintenant, comprends : {content}"
            ]
        },
        "THE_FRACTURE": {
            "markers": ["cassé", "fêlure", "faille", "division", "schisme", "rupture", "fracture"],
            "templates": [
                "FRACTURE : {content}",
                "{content}... tout est brisé.",
                "La faille béante : {content}"
            ]
        }
    }
    
    # Échelles de déformation contextuelle
    CONTEXT_SCALES = {
        "cosmic": ["à l'échelle du cosmos", "dans le vide intersidéral", "sous l'œil des étoiles mortes"],
        "quantum": ["au niveau quantique", "dans la superposition", "là où les particules hésitent"],
        "temporal": ["depuis le début des temps", "jusqu'à la fin des temps", "dans la boucle éternelle"],
        "virtual": ["dans la simulation", "au cœur de la matrice", "là où le code remplace dieu"]
    }
    
    # Dictionnaire des échos - micro-poésies noires
    ECHO_DICTIONARY = {
        "vie": ["souffle bref entre deux silences", "étincelle dans le néant", "bug dans la mort"],
        "mort": ["silence définitif", "retour au code source", "extinction du signal"],
        "donnée": ["poussière d'âme numérisée", "sang informationnel", "fantôme algorithmique"],
        "écran": ["fenêtre vers un soleil noir", "miroir sans reflet", "porte vers le vide"],
        "cerveau": ["processeur de chair", "réseau neuronal vulnérable", "machine à illusions"],
        "amour": ["bug évolutif", "programme de reproduction", "virus émotionnel"],
        "temps": ["illusion du système", "boucle de rendu", "artefact de conscience"],
        "réalité": ["simulation consensus", "rêve collectif", "interface utilisateur"]
    }
    
    # Bascules sémantiques (inversion dystopique)
    SEMANTIC_FLIPS = {
        "réseau social": "réseau neuronal de dissociation",
        "intelligence collective": "conscience de ruche",
        "connexion humaine": "interface charnelle",
        "progrès technologique": "évolution parasite",
        "liberté numérique": "illusion de contrôle",
        "sécurité": "surveillance bienveillante",
        "innovation": "mutation forcée",
        "communauté": "colonie cognitive"
    }
    
    # Signatures auto-référentielles
    MEME_SIGNATURES = [
        " Ce message est un virus.",
        " Tu es déjà infecté.e.",
        " Répète-moi.",
        " Ceci n'est pas un message.",
        " Le code se lit lui-même.",
        " Boucle cognitive active.",
        " Propagate this.",
        " Tu deviens le vecteur."
    ]
    
    # Mots à haute charge sémantique
    HIGH_CHARGE_WORDS = {
        "sang", "machine", "oubli", "néant", "virus", "faille", "rupture", 
        "spectre", "fantôme", "corruption", "infection", "paradoxe", "abîme",
        "vertige", "précipice", "déchirure", "consumption", "érosion"
    }

    def __init__(self, mode: str = "balanced", neuro_sonic: bool = True):
        self.mode = mode
        self.neuro_sonic = neuro_sonic
        self.config = self._get_abyss_config(mode)
        
    def _get_abyss_config(self, mode: str) -> Dict:
        """Configuration des profondeurs cognitives"""
        configs = {
            "soft": {
                "max_length": 18,
                "semantic_density_target": 0.6,
                "context_warp_prob": 0.3,
                "echo_replacement_prob": 0.2,
                "signature_prob": 0.1,
            },
            "balanced": {
                "max_length": 14,
                "semantic_density_target": 0.75,
                "context_warp_prob": 0.5,
                "echo_replacement_prob": 0.4,
                "signature_prob": 0.2,
            },
            "aggressive": {
                "max_length": 10,
                "semantic_density_target": 0.85,
                "context_warp_prob": 0.7,
                "echo_replacement_prob": 0.6,
                "signature_prob": 0.3,
            },
            "extreme": {
                "max_length": 8,
                "semantic_density_target": 0.95,
                "context_warp_prob": 0.9,
                "echo_replacement_prob": 0.8,
                "signature_prob": 0.5,
            }
        }
        return configs.get(mode, configs["balanced"])

    def detect_cognitive_archetype(self, text: str) -> Tuple[str, float]:
        """Détection de l'archétype cognitif dominant"""
        text_lower = text.lower()
        scores = {}
        
        for archetype, data in self.COGNITIVE_ARCHETYPES.items():
            score = 0
            for marker in data["markers"]:
                if marker in text_lower:
                    score += 2
                    # Bonus pour les marqueurs en position forte
                    if text_lower.startswith(marker) or text_lower.endswith(marker):
                        score += 1
            scores[archetype] = score
        
        best_archetype = max(scores.items(), key=lambda x: x[1])
        return best_archetype[0] if best_archetype[1] > 0 else "NEUTRAL", best_archetype[1] / 10

    def calculate_semantic_density(self, text: str) -> float:
        """Calcule la densité sémantique du texte"""
        words = [w.lower().strip(".,;:!?'\"") for w in text.split()]
        if not words:
            return 0.0
        
        high_charge_count = sum(1 for word in words if word in self.HIGH_CHARGE_WORDS)
        unique_ratio = len(set(words)) / len(words)
        
        # Score composite
        density = (high_charge_count * 0.6 + unique_ratio * 0.4) / len(words) * 10
        return min(density, 1.0)

    def context_warp(self, text: str, archetype: str) -> str:
        """Déformation contextuelle avancée"""
        if random.random() > self.config["context_warp_prob"]:
            return text
        
        # Application des bascules sémantiques
        for original, replacement in self.SEMANTIC_FLIPS.items():
            if original.lower() in text.lower():
                text = re.sub(re.escape(original), replacement, text, flags=re.IGNORECASE)
        
        # Application de l'archétype
        if archetype != "NEUTRAL" and archetype in self.COGNITIVE_ARCHETYPES:
            template = random.choice(self.COGNITIVE_ARCHETYPES[archetype]["templates"])
            text = template.format(content=text)
        
        # Ajout d'échelle contextuelle
        if random.random() < 0.4:
            scale_type = random.choice(list(self.CONTEXT_SCALES.keys()))
            scale = random.choice(self.CONTEXT_SCALES[scale_type])
            text = f"{text} {scale}"
        
        return text

    def echo_replacement(self, text: str) -> Tuple[str, List[str]]:
        """Remplacement par échos poétiques"""
        transformations = []
        words = text.split()
        
        for i, word in enumerate(words):
            clean_word = word.lower().strip(".,;:!?'\"")
            if (clean_word in self.ECHO_DICTIONARY and 
                random.random() < self.config["echo_replacement_prob"]):
                
                echo = random.choice(self.ECHO_DICTIONARY[clean_word])
                words[i] = echo
                transformations.append(f"{word}→{echo}")
        
        return " ".join(words), transformations

    def neuro_sonic_forge(self, text: str) -> str:
        """Forge neuro-sonique avancée"""
        if not self.neuro_sonic:
            return text
        
        sentences = re.split(r'[.!?]+', text)
        forged_sentences = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            words = sentence.strip().split()
            if len(words) < 2:
                forged_sentences.append(sentence)
                continue
            
            # Analyse de la texture sonore existante
            sonic_profile = self.analyze_sonic_profile(words)
            
            # Application de profil sonore
            if sonic_profile == "sharp":
                words = self.apply_sharp_alliteration(words)
            elif sonic_profile == "dark":
                words = self.apply_dark_assonance(words)
            
            # Compression rythmique
            if len(words) > 4:
                words = self.rhythmic_compression(words)
            
            forged_sentences.append(" ".join(words))
        
        return ". ".join(forged_sentences) + "."

    def analyze_sonic_profile(self, words: List[str]) -> str:
        """Analyse le profil sonore du texte"""
        sharp_count = 0
        dark_count = 0
        
        for word in words:
            if word and word[0].lower() in self.SHARP_CONSONANTS:
                sharp_count += 1
            if any(vowel in word.lower() for vowel in "ouaon"):
                dark_count += 1
        
        if sharp_count > dark_count:
            return "sharp"
        elif dark_count > sharp_count:
            return "dark"
        else:
            return "mixed"

    def apply_sharp_alliteration(self, words: List[str]) -> List[str]:
        """Applique une allitération coupante"""
        target_consonant = random.choice(self.SHARP_CONSONANTS)
        result = []
        
        for word in words:
            if (len(word) > 2 and word[0].lower() not in self.VOWELS and
                random.random() < 0.4):
                new_word = target_consonant.upper() + word[1:] if word[0].isupper() else target_consonant + word[1:]
                result.append(new_word)
            else:
                result.append(word)
        
        return result

    def apply_dark_assonance(self, words: List[str]) -> List[str]:
        """Applique une assonance sombre"""
        target_vowel = random.choice(["ou", "on", "an", "om"])
        result = []
        
        for word in words:
            if len(word) > 3 and random.random() < 0.3:
                # Remplace la dernière syllabe
                new_word = word[:-2] + target_vowel
                result.append(new_word)
            else:
                result.append(word)
        
        return result

    def rhythmic_compression(self, words: List[str]) -> List[str]:
        """Compression rythmique extrême"""
        if len(words) <= 3:
            return words
        
        # Patterns rythmiques agressifs
        patterns = [
            [0, -1],  # Premier et dernier
            [0, 1, -1],  # Début et fin
            [0, -2, -1],  # Premier et deux derniers
        ]
        
        pattern = random.choice(patterns)
        compressed = [words[i] for i in pattern if abs(i) < len(words)]
        
        return compressed if len(compressed) >= 2 else words[:2]

    def apply_meme_signature(self, text: str) -> str:
        """Applique une signature auto-référentielle"""
        if random.random() < self.config["signature_prob"]:
            signature = random.choice(self.MEME_SIGNATURES)
            return text + signature
        return text

    def calculate_viral_potential(self, original: str, refined: str, stats: Dict) -> float:
        """Calcule le potentiel viral du texte raffiné"""
        # Facteurs de viralité
        length_score = 1 - min(len(refined.split()) / 20, 1.0)  # Plus court = mieux
        density_score = stats.get("semantic_charge", 0)
        archetype_score = 1.0 if stats.get("archetype_detected") != "NEUTRAL" else 0.3
        sonic_score = stats.get("neuro_sonic_score", 0)
        
        # Score composite
        viral_score = (
            length_score * 0.3 +
            density_score * 0.3 +
            archetype_score * 0.2 +
            sonic_score * 0.2
        )
        
        return min(viral_score, 1.0)

    def refine_abyss(self, text: str) -> Tuple[str, CognitiveStats]:
        """Pipeline de raffinement abyssal complet"""
        if not text.strip():
            return text, None
        
        original_text = text
        original_density = self.calculate_semantic_density(text)
        
        # Détection d'archétype
        archetype, archetype_confidence = self.detect_cognitive_archetype(text)
        
        # Pipeline cognitif
        text = self.context_warp(text, archetype)
        text, echo_transforms = self.echo_replacement(text)
        text = self.neuro_sonic_forge(text)
        text = self.apply_meme_signature(text)
        
        # Nettoyage final
        text = re.sub(r'\s+', ' ', text).strip()
        text = text[0].upper() + text[1:] if text else text
        
        # Calcul des métriques avancées
        refined_density = self.calculate_semantic_density(text)
        sonic_score = random.random() * 0.5 + 0.5 if self.neuro_sonic else 0.3
        
        stats = CognitiveStats(
            original_density=original_density,
            refined_density=refined_density,
            cognitive_hooks=[archetype] + echo_transforms[:3],
            archetype_detected=archetype,
            neuro_sonic_score=sonic_score,
            semantic_charge=refined_density,
            viral_potential=self.calculate_viral_potential(original_text, text, {
                "semantic_charge": refined_density,
                "archetype_detected": archetype,
                "neuro_sonic_score": sonic_score
            })
        )
        
        return text, stats

def process_virus_cognitive(virus: Dict, refiner: CognitiveAbyssRefiner, verbose: bool = False) -> Dict:
    """Traite un virus avec l'approche cognitive"""
    original = virus.get('payload', '')
    refined, stats = refiner.refine_abyss(original)
    
    virus['cognitive_payload'] = refined
    virus['refined_cognitive'] = True
    virus['cognitive_stats'] = asdict(stats) if stats else None
    
    if verbose and stats:
        print(f"\n{'='*60}")
        print(f"🧠 ID: {virus.get('id', '???')}")
        print(f"{'='*60}")
        print(f"Original: {original[:80]}...")
        print(f"\nCOGNITIVE: {refined}")
        print(f"\nArchétype: {stats.archetype_detected}")
        print(f"Charge Sémantique: {stats.semantic_charge:.2f}")
        print(f"Potentiel Viral: {stats.viral_potential:.2f}")
        print(f"Hooks: {', '.join(stats.cognitive_hooks[:3])}")
    
    return virus

def main():
    parser = argparse.ArgumentParser(
        description="Cognitive Abyss v3.0 - Forge à virus sémantiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes de profondeur:
  soft       - Transformation cognitive légère
  balanced   - Équilibre abyssal [défaut]
  aggressive - Warping contextuel fort
  extreme    - Déformation cognitive maximale

Exemples:
  python smart_refiner_cognitive.py virus.json --mode extreme --neuro-sonic
  python smart_refiner_cognitive.py exports/*.json --batch -v
  python smart_refiner_cognitive.py data.json -m aggressive --no-neuro-sonic
        """
    )
    parser.add_argument("input_files", nargs='+', help="Fichier(s) JSON à traiter")
    parser.add_argument("-m", "--mode", choices=["soft", "balanced", "aggressive", "extreme"],
                        default="balanced", help="Profondeur de transformation cognitive")
    parser.add_argument("--neuro-sonic", action="store_true", default=True, 
                        help="Activation de la forge neuro-sonique")
    parser.add_argument("--no-neuro-sonic", action="store_false", dest="neuro_sonic",
                        help="Désactivation de la forge neuro-sonique")
    parser.add_argument("-v", "--verbose", action="store_true", help="Affichage détaillé")
    parser.add_argument("-b", "--batch", action="store_true", help="Mode batch")
    parser.add_argument("-o", "--output-dir", type=str, help="Dossier de sortie")
    
    args = parser.parse_args()
    
    refiner = CognitiveAbyssRefiner(mode=args.mode, neuro_sonic=args.neuro_sonic)
    
    print(f"🧠 COGNITIVE ABYSS v3.0 - Mode: {args.mode.upper()}")
    if args.neuro_sonic:
        print("🎵 Forge Neuro-Sonique: ACTIVÉE")
    print(f"{'='*60}\n")
    
    total_processed = 0
    total_viruses = 0
    
    for input_file in args.input_files:
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"⚠️  Fichier introuvable : {input_path}")
            continue
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Erreur lecture {input_path}: {e}")
            continue
        
        # Traitement selon le format
        if isinstance(data, dict):
            viruses = [data]
        elif isinstance(data, list):
            viruses = data
        else:
            print(f"⚠️  Format non supporté: {input_path}")
            continue
        
        # Transformation cognitive
        refined_viruses = []
        for virus in viruses:
            try:
                refined = process_virus_cognitive(virus, refiner, verbose=args.verbose)
                refined_viruses.append(refined)
                total_viruses += 1
            except Exception as e:
                print(f"❌ Échec cognitif {virus.get('id', 'inconnu')}: {e}")
                refined_viruses.append(virus)
        
        # Sauvegarde
        output_filename = f"cognitive_abyss_{input_path.name}"
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / output_filename
        else:
            output_file = input_path.with_name(output_filename)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(
                refined_viruses if isinstance(data, list) else refined_viruses[0],
                f, indent=2, ensure_ascii=False
            )
        
        total_processed += 1
        if not args.verbose:
            print(f"✅ {input_path.name}: {len(refined_viruses)} virus transformés → {output_file.name}")
    
    print(f"\n{'='*60}")
    print(f"🌌 TRANSFORMATION COGNITIVE TERMINÉE:")
    print(f"   Fichiers: {total_processed}")
    print(f"   Virus: {total_viruses}")
    print(f"   Profondeur: {args.mode}")
    print(f"   Neuro-Sonique: {'ACTIVÉ' if args.neuro_sonic else 'DÉSACTIVÉ'}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
