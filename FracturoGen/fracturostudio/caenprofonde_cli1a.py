#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caenprofonde_cli.py v1.1
FracturoScript CLI Extended — RuneSmith de Caen-Profonde (2075 → 2025)
Fonctionnalités : mutation avancée, lexique paleo-mnémétique, export Grok.
Usage : terminal, Termux, Android, Ubuntu glitché.
"""

import argparse
import json
import random
import hashlib
import copy
import sys
import os
from datetime import datetime
from collections import defaultdict

# ============================================================================
# DONNÉES (copiées depuis le GUI v2.0)
# ============================================================================

RUNES_EXTENDED = {
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

LIEUX_EXTENDED = {l: d for l, d in {
    'paris': {'pouvoir': 3, 'description': 'Cœur administratif', 'type': 'urbain', 'flux': 'élevé'},
    'marseille': {'pouvoir': 2, 'description': 'Port méditerranéen', 'type': 'portuaire', 'flux': 'moyen'},
    'lyon': {'pouvoir': 2, 'description': 'Carrefour historique', 'type': 'urbain', 'flux': 'élevé'},
    'bordeaux': {'pouvoir': 1, 'description': 'Vigne et pierre', 'type': 'historique', 'flux': 'faible'},
    'lille': {'pouvoir': 1, 'description': 'Frontière nord', 'type': 'frontière', 'flux': 'moyen'},
    'toulouse': {'pouvoir': 2, 'description': 'Rose et espace', 'type': 'technologique', 'flux': 'moyen'},
    'nantes': {'pouvoir': 3, 'description': 'Estuaire de la mémoire', 'type': 'portuaire', 'flux': 'élevé'},
    'strasbourg': {'pouvoir': 2, 'description': 'Frontière linguistique', 'type': 'frontière', 'flux': 'moyen'},
    'montpellier': {'pouvoir': 1, 'description': 'Savoir ancien', 'type': 'académique', 'flux': 'faible'},
    'rennes': {'pouvoir': 2, 'description': 'Forêt et rébellion', 'type': 'mystique', 'flux': 'moyen'},
    'caen': {'pouvoir': 4, 'description': 'Nexus de mémoire fracturée', 'type': 'mémétique', 'flux': 'chaotique'},
    'herouville': {'pouvoir': 2, 'description': 'Zone périphérique', 'type': 'mémoire', 'flux': 'modéré'},
    'ganil': {'pouvoir': 5, 'description': 'Réacteur de conscience', 'type': 'scientifique', 'flux': 'anormal'},
    'internet': {'pouvoir': 5, 'description': 'Réseau global', 'type': 'digital', 'flux': 'extrême'},
    'datacenter': {'pouvoir': 4, 'description': 'Temple des données', 'type': 'digital', 'flux': 'élevé'},
    'darkweb': {'pouvoir': 4, 'description': 'Ombre du réseau', 'type': 'digital', 'flux': 'élevé'},
    'blockchain': {'pouvoir': 3, 'description': 'Registre immuable', 'type': 'digital', 'flux': 'moyen'},
    'cloud': {'pouvoir': 3, 'description': 'Nuage de bits', 'type': 'digital', 'flux': 'élevé'},
    'bibliotheque': {'pouvoir': 3, 'description': 'Archive vivante', 'type': 'savoir', 'flux': 'faible'},
    'cathedrale': {'pouvoir': 4, 'description': 'Pierre sacrée', 'type': 'mystique', 'flux': 'faible'},
    'cimetiere': {'pouvoir': 4, 'description': 'Frontière des morts', 'type': 'mystique', 'flux': 'faible'},
    'foret': {'pouvoir': 2, 'description': 'Réseau racinaire', 'type': 'naturel', 'flux': 'faible'},
    'ocean': {'pouvoir': 5, 'description': 'Abîme liquide', 'type': 'naturel', 'flux': 'extrême'},
    'montagne': {'pouvoir': 3, 'description': 'Épine terrestre', 'type': 'naturel', 'flux': 'faible'},
    'passé': {'pouvoir': 5, 'description': 'Strates révolues', 'type': 'temporel', 'flux': 'nul'},
    'futur': {'pouvoir': 5, 'description': 'Potentiels non-réalisés', 'type': 'temporel', 'flux': 'infini'},
    'présent': {'pouvoir': 3, 'description': 'Instant fugace', 'type': 'temporel', 'flux': 'constant'}
}.items()}

EFFETS_EXTENDED = [
    'révélation mémoire', 'effacement sélectif', 'fusion souvenirs',
    'extraction narrative', 'implantation expérience', 'reconstruction passé',
    'archivage conscience', 'purge traumatique', 'restauration identitaire',
    'glissement temporel', 'boucle causale', 'accélération locale',
    'ralentissement perceptuel', 'synchronisation multiple', 'désalignement chronologique',
    'anticipation événementielle', 'rétro-causalité', 'stase temporelle',
    'téléportation conscience', 'projection astrale', 'déphasage spatial',
    'ancrage géographique', 'fusion lieux', 'cartographie psychique',
    'protection réseau', 'manipulation données', 'encryption quantique',
    'contournement surveillance', 'injection code', 'corruption fichier',
    'génération deepfake', 'anonymisation totale', 'traçage inversé',
    'influence collective', 'mémétique virale', 'persuasion subliminale',
    'effacement identité publique', 'fabrication réputation', 'réseau dormant',
    'synesthésie contrôlée', 'vision augmentée', 'interface rêve',
    'communication silence', 'lecture pensées', 'projection émotionnelle',
    'hallucination dirigée', 'lucidité onirique',
    'invocation entité', 'pacte liminal', 'ouverture portail',
    'scellement dimension', 'ancrage âme', 'libération spectrale',
    'communion Programme', 'éveil dormant'
]

MODIFICATEURS = {
    'amplificateurs': ['×2', '×3', '×5', 'MAX', 'BOOST', '++', '↑↑', '⇈'],
    'atténuateurs': ['÷2', '÷3', 'MIN', 'SOFT', '--', '↓↓', '⇊'],
    'inverseurs': ['¬', '~', 'REV', 'INV', '↔', '⇄'],
    'stabilisateurs': ['LOCK', 'FIX', '◈', '⊞', 'STABLE'],
    'déstabilisateurs': ['CHAOS', 'FLUX', '☢', '⚠', 'WILD'],
    'temporels': ['DELAY', 'INSTANT', 'PERSIST', 'LOOP', 'ONCE'],
    'spatiaux': ['LOCAL', 'GLOBAL', 'RADIUS', 'POINT', 'ZONE']
}

TEMPLATES_ADVANCED = {
    "templates": [
        {"nom": "Classique", "structure": "Ω<{rune}>v{version} {lieu} — {effet} •••", "complexité": 1},
        {"nom": "Multi-Runes", "structure": "{rune1}+{rune2}+{rune3} @ {lieu} :: v{version} :: {effet}", "complexité": 3, "multi_rune": True},
        {"nom": "Chaîne Temporelle", "structure": "{rune}[t={temps}] → {lieu} → {effet} → v{version}", "complexité": 2, "temporal": True},
        {"nom": "Réseau Distribué", "structure": "∇{rune}∇ <{lieu1}⇄{lieu2}⇄{lieu3}> |{effet}| v{version}", "complexité": 3, "multi_lieu": True},
        {"nom": "Modificateur Complexe", "structure": "{mod1}[{rune}]{mod2} :: {lieu} :: {effet} :: v{version}", "complexité": 2, "with_mods": True},
        {"nom": "Encryption Runique", "structure": "#{hash}# {rune}^{version} @ {lieu} ⊕ {effet}", "complexité": 3, "encrypted": True},
        {"nom": "Séquence Fractale", "structure": "{rune}↺{iteration}↻ {lieu}^{dimension} ⟨{effet}⟩ v{version}", "complexité": 4, "fractal": True},
        {"nom": "Interface Quantique", "structure": "|ψ⟩{rune}⟨ψ| ⊗ {lieu} ≡ {effet} ≡ v{version}", "complexité": 4, "quantum": True},
        {"nom": "Glitch Syntaxique", "structure": "{rune}v{version}{lieu}{effet}", "complexité": 2, "glitched": True},
        {"nom": "Palindrome Runique", "structure": "{effet}←{lieu}←v{version}←{rune}→v{version}→{lieu}→{effet}", "complexité": 3, "palindrome": True}
    ]
}

# ============================================================================
# UTILITAIRES D'INTERFACE
# ============================================================================

ANSI = not os.getenv('NO_COLOR') and sys.stdout.isatty()
if not ANSI:
    def C(s, c): return s
else:
    COLORS = {
        'danger': '\033[91m',
        'safe': '\033[92m',
        'glitch': '\033[95m',
        'code': '\033[96m',
        'meta': '\033[93m',
        'reset': '\033[0m'
    }
    def C(s, c): return f"{COLORS.get(c, '')}{s}{COLORS['reset']}"

GLYPHS = {
    'gen': '⚡',
    'mut': '🧬',
    'chain': '⛓',
    'warn': '⚠️',
    'ok': '✅',
    'info': '🌀'
}

def log(msg, glyph='🌀', color='meta'):
    print(C(f"{glyph} {msg}", color))

# ============================================================================
# CLASSE GÉNÉRATEUR CLI
# ============================================================================

class FracturoCLI:
    def __init__(self, args):
        self.args = args
        self.history = []
        self.lexicon = None
        if args.load_lexicon:
            self.load_lexicon(args.load_lexicon)
        random.seed(args.seed if args.seed is not None else None)

    def load_lexicon(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.lexicon = data.get('entries', [])
                log(f"Lexique chargé : {len(self.lexicon)} entrées", 'info', 'safe')
        except Exception as e:
            log(f"Erreur lexique : {e}", 'warn', 'danger')
            sys.exit(1)

    def inject_lexicon(self, params):
        if not self.lexicon:
            return params
        ratio = getattr(self.args, 'lexicon_ratio', 0.3)
        new_params = copy.deepcopy(params)

        if random.random() < ratio and 'effet' in new_params:
            entry = random.choice(self.lexicon)
            if 'effet_mnémétique' in entry:
                new_params['effet'] = entry['effet_mnémétique']

        if random.random() < ratio and 'lieu' in new_params:
            entry = random.choice(self.lexicon)
            if 'paleo_glyphe' in entry:
                lieu_alt = entry['paleo_glyphe'].replace(' ', '_')
                if lieu_alt in LIEUX_EXTENDED:
                    new_params['lieu'] = lieu_alt
                else:
                    new_params['lieu'] = lieu_alt

        if random.random() < ratio and 'rune' in new_params:
            entry = random.choice(self.lexicon)
            if 'glyph' in entry and entry['glyph'] in RUNES_EXTENDED:
                new_params['rune'] = entry['glyph']

        return new_params

    def generate(self, params=None):
        """Génère un code FracturoScript à partir de paramètres ou de manière autonome."""
        # Choix du template (unique et cohérent)
        template_index = self.args.template if self.args.template is not None else 0
        template_index = template_index % len(TEMPLATES_ADVANCED["templates"])
        template = TEMPLATES_ADVANCED["templates"][template_index]

        if params is None:
            # Paramètres de base
            rune = self.args.rune or random.choice(list(RUNES_EXTENDED.keys()))
            lieu = self.args.lieu or random.choice(list(LIEUX_EXTENDED.keys()))
            effet = self.args.effet or random.choice(EFFETS_EXTENDED)
            version = self.args.version or random.randint(1, 13)

            params = {'rune': rune, 'lieu': lieu, 'effet': effet, 'version': version}

            # Paramètres étendus selon les capacités du template
            if template.get('multi_rune'):
                params.update({
                    'rune1': random.choice(list(RUNES_EXTENDED.keys())),
                    'rune2': random.choice(list(RUNES_EXTENDED.keys())),
                    'rune3': random.choice(list(RUNES_EXTENDED.keys())),
                })
            if template.get('multi_lieu'):
                params.update({
                    'lieu1': random.choice(list(LIEUX_EXTENDED.keys())),
                    'lieu2': random.choice(list(LIEUX_EXTENDED.keys())),
                    'lieu3': random.choice(list(LIEUX_EXTENDED.keys())),
                })
            if template.get('with_mods'):
                params['mod1'] = random.choice(MODIFICATEURS['amplificateurs'] + MODIFICATEURS['stabilisateurs'])
                params['mod2'] = random.choice(MODIFICATEURS['temporels'] + MODIFICATEURS['spatiaux'])
            if template.get('temporal'):
                params['temps'] = f"{random.randint(1, 72)}h"
            if template.get('encrypted'):
                params['hash'] = hashlib.sha256(str(random.random()).encode()).hexdigest()[:6]
            if template.get('fractal'):
                params['iteration'] = random.randint(2, 7)
                params['dimension'] = round(random.uniform(1.5, 3.5), 2)

            # Injection du lexique (si chargé)
            params = self.inject_lexicon(params)

        # Génération du code
        try:
            code_str = template["structure"].format(**params)
        except KeyError as e:
            # Gestion gracieuse des clés manquantes
            missing = str(e).strip("'")
            params[missing] = "?"
            code_str = template["structure"].format(**params)

        # Métadonnées
        code_hash = hashlib.sha256(code_str.encode()).hexdigest()[:10]
        danger = self.calculate_danger(params, template)

        result = {
            'code': code_str,
            'hash': code_hash,
            'params': params,
            'template': template['nom'],
            'timestamp': datetime.now().isoformat(),
            'danger': danger,
            'complexité': template.get('complexité', 1)
        }
        self.history.append(result)
        return result



    def calculate_danger(self, params, template):
        d = 0
        if 'rune' in params:
            d += RUNES_EXTENDED.get(params['rune'], {}).get('danger', 1)
        for k in ['rune1', 'rune2', 'rune3']:
            if k in params:
                d += RUNES_EXTENDED.get(params[k], {}).get('danger', 1)
        d *= params.get('version', 1)
        d += template.get('complexité', 1) * 2
        for k in ['lieu', 'lieu1', 'lieu2', 'lieu3']:
            if k in params:
                d += LIEUX_EXTENDED.get(params[k], {}).get('pouvoir', 1)
        return min(d, 100)

    def mutate_code(self, code_obj, mutation_type='random', intensity=1.0):
        mutated = copy.deepcopy(code_obj)
        mutations_applied = []

        if mutation_type == 'random':
            num_mutations = int(1 + intensity * 2)
            possible_mutations = ['rune', 'lieu', 'effet', 'version']
            for _ in range(num_mutations):
                mut_type = random.choice(possible_mutations)
                mutations_applied.append(mut_type)
                if mut_type == 'rune' and 'rune' in mutated['params']:
                    mutated['params']['rune'] = random.choice(list(RUNES_EXTENDED.keys()))
                elif mut_type == 'lieu' and 'lieu' in mutated['params']:
                    mutated['params']['lieu'] = random.choice(list(LIEUX_EXTENDED.keys()))
                elif mut_type == 'effet' and 'effet' in mutated['params']:
                    mutated['params']['effet'] = random.choice(EFFETS_EXTENDED)
                elif mut_type == 'version' and 'version' in mutated['params']:
                    delta = int(random.gauss(0, 2 * intensity))
                    new_version = max(1, min(13, mutated['params']['version'] + delta))
                    mutated['params']['version'] = new_version

        elif mutation_type == 'glitch':
            mutated['code'] = self.add_advanced_glitch(mutated['code'], intensity)
            mutations_applied.append('glitch')

        elif mutation_type == 'hybrid':
            if len(self.history) > 1:
                candidates = [c for c in self.history if c['hash'] != code_obj['hash']]
                if candidates:
                    other = random.choice(candidates)
                    for key in mutated['params']:
                        if key in other['params'] and random.random() < 0.5:
                            mutated['params'][key] = other['params'][key]
                    mutations_applied.append(f"hybrid avec {other['hash'][:6]}")

        elif mutation_type == 'inversion':
            if 'effet' in mutated['params']:
                effet = mutated['params']['effet']
                if 'révélation' in effet:
                    mutated['params']['effet'] = effet.replace('révélation', 'occultation')
                elif 'protection' in effet:
                    mutated['params']['effet'] = effet.replace('protection', 'vulnérabilité')
                else:
                    mutated['params']['effet'] = f"¬({effet})"
            mutations_applied.append('inversion')

        elif mutation_type == 'amplification':
            if 'version' in mutated['params']:
                mutated['params']['version'] = min(13, int(mutated['params']['version'] * (1 + intensity)))
            mutations_applied.append('amplification')

        elif mutation_type == 'fractale':
            mutated['params']['iteration'] = random.randint(3, 8)
            mutated['params']['dimension'] = round(random.uniform(2.0, 4.0), 2)
            mutations_applied.append('fractale')

        # Régénération du code
        template_index = next((i for i, t in enumerate(TEMPLATES_ADVANCED["templates"])
                             if t["nom"] == mutated['template']), 0)
        template = TEMPLATES_ADVANCED["templates"][template_index]
        try:
            mutated['code'] = template["structure"].format(**mutated['params'])
        except KeyError as e:
            pass  # Garde l’ancien code en cas d’erreur

        mutated['hash'] = hashlib.sha256(mutated['code'].encode()).hexdigest()[:10]
        mutated['parent'] = code_obj['hash']
        mutated['mutation_type'] = mutation_type
        mutated['mutations_applied'] = mutations_applied
        mutated['timestamp'] = datetime.now().isoformat()
        mutated['danger'] = self.calculate_danger(mutated['params'], template)
        mutated['generation'] = code_obj.get('generation', 0) + 1
        self.history.append(mutated)
        return mutated

    def add_advanced_glitch(self, code, intensity=1.0):
        num_glitches = int(1 + intensity * 3)
        glitches = [
            lambda s: s.replace('Ω', random.choice(['Ѡ', 'Ѽ', 'Ѿ'])),
            lambda s: s + '' * random.randint(1, 3),
            lambda s: s.replace('•••', '•' * random.randint(1, 5)),
            lambda s: ''.join(c if random.random() > 0.1 else c.upper() for c in s),
            lambda s: s[:len(s)//2] + ' ' * random.randint(1, 3) + s[len(s)//2:],
            lambda s: s.replace('—', random.choice(['~', '≈', '≋', '⁓'])),
            lambda s: re.sub(r'v(\d+)', lambda m: f'v{int(m.group(1)) + random.randint(-2, 2)}', s),
            lambda s: s + f'\\x{random.randint(0, 255):02x}',
        ]
        result = code
        for _ in range(num_glitches):
            result = random.choice(glitches)(result)
        return result

    def to_grok_prompt(self, code_obj):
        params = code_obj['params']
        rune = params.get('rune', '')
        lieu = params.get('lieu', 'inconnu')
        effet = params.get('effet', '')
        rune_info = RUNES_EXTENDED.get(rune, {})
        lieu_info = LIEUX_EXTENDED.get(lieu, {})

        seed = code_obj['code']
        meta = f"[Memetic layer: rune {rune} ({rune_info.get('nom', '?')}), lieu: {lieu} ({lieu_info.get('description', '?')}), effet: {effet}]"

        base_desc = f"FracturoScript seed: {seed}\n{meta}\n→ Generate a hyper-detailed image of "

        if lieu == 'caen':
            base_desc += "a fractured cathedral in Caen, 2075. Cracks in the stone glow with ancient runes."
        else:
            base_desc += f"a symbolic landscape representing '{effet}' in {lieu}. Ancient runes float in the air."

        runes_in_scene = rune
        if 'rune1' in params:
            runes_in_scene = f"{params['rune1']}+{params['rune2']}+{params['rune3']}"

        prompt = f"{base_desc} A translucent figure emerges from a memory vortex, eyes filled with ancestral data. Runic graffiti floats: \"{seed}\". Style: cyberpunk mysticism, glitched realism, monochrome with red accents, ultra-textured, cinematic lighting. Subliminal effect: induce déjà-vu in viewer."

        return prompt

    def display(self, code):
        if self.args.to_grok:
            print(self.to_grok_prompt(code))
            return

        danger_str = f"{code['danger']}/100"
        if code['danger'] > 50:
            danger_str = C(danger_str, 'danger')
        elif code['danger'] < 30:
            danger_str = C(danger_str, 'safe')
        else:
            danger_str = C(danger_str, 'meta')

        print(C(f"\n{GLYPHS['gen']} FRACTUROSCRIPT CLI // RUNESMITH MODE", 'code'))
        print("─" * 60)
        print(C(f"[Caen-Profonde // 2075→2025 // GLITCH ACTIVE]", 'meta'))
        print("─" * 60)
        print(C(f"Generated: {code['code']}", 'code'))
        print(f"Hash: {code['hash']} | Danger: {danger_str} | Stabilité: {max(0, 100 - code['danger'])}%")
        effects = self.predict_side_effects(code)
        if effects:
            print(f"Effets secondaires: {', '.join(effects[:4])}")

    def predict_side_effects(self, code_obj):
        effects = []
        danger = code_obj.get('danger', 0)
        if danger > 70: effects.extend(['Amnésie sévère', 'Désorientation spatio-temporelle'])
        elif danger > 50: effects.extend(['Amnésie temporaire', 'Vertiges'])
        params = code_obj.get('params', {})
        rune = params.get('rune', '')
        if rune in RUNES_EXTENDED:
            elem = RUNES_EXTENDED[rune].get('élément', '')
            if elem == 'feu': effects.append('Sensation de chaleur')
            elif elem == 'glace': effects.append('Frissons persistants')
            elif elem == 'eau': effects.append('Rêves aquatiques')
        effet = params.get('effet', '')
        if 'mémoire' in effet: effects.append('Flashbacks aléatoires')
        return list(set(effects))[:4]

    def find_by_hash(self, short_hash):
        for item in self.history:
            if item['hash'].startswith(short_hash):
                return item
        # Si non trouvé, tente de charger depuis --from-file
        if hasattr(self.args, 'from_file') and self.args.from_file:
            try:
                with open(self.args.from_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    codes = data.get('codes', []) + data.get('history', [])
                    for c in codes:
                        if c['hash'].startswith(short_hash):
                            c.setdefault('generation', 0)
                            self.history.append(c)
                            return c
            except:
                pass
        raise ValueError("Code non trouvé dans l’historique")

    def run(self):
        if self.args.mutate:
            try:
                original = self.find_by_hash(self.args.mutate)
            except ValueError:
                log("Code non trouvé. Générez ou chargez d’abord un code.", 'warn', 'danger')
                return
            mutated = self.mutate_code(
                original,
                mutation_type=self.args.mutation_type,
                intensity=self.args.intensity
            )
            self.display(mutated)
            if self.args.export:
                self.export([mutated], self.args.export)
            return

        if self.args.chain:
            log(f"Chaîne de {self.args.chain} codes", 'chain', 'glitch')
            current = self.generate()
            chain = [current]
            for i in range(self.args.chain - 1):
                current = self.mutate_code(current, mutation_type='random', intensity=0.5)
                chain.append(current)
            for r in chain:
                self.display(r)
            if self.args.export:
                self.export(chain, self.args.export)
            return

        # Génération simple
        code = self.generate()
        self.display(code)
        if self.args.export:
            self.export([code], self.args.export)

    def export(self, codes, filename):
        data = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "source": "caenprofonde_cli.py v1.1",
                "count": len(codes)
            },
            "codes": codes
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log(f"Exporté vers {filename}", 'ok', 'safe')

# ============================================================================
# ARGUMENTS
# ============================================================================

def parse_args():
    p = argparse.ArgumentParser(
        description="FracturoScript CLI v1.1 — RuneSmith de Caen-Profonde (2075 → 2025)",
        epilog="Semence mémétique pour époques naïves. ⚠️ Usage narratif uniquement.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument('-g', '--generate', action='store_true', help="Générer un code (par défaut)")
    p.add_argument('-m', '--mutate', metavar='HASH', help="Mutater un code par hash court")
    p.add_argument('--mutation-type', choices=['random','glitch','hybrid','inversion','amplification','fractale'],
                   default='random', help="Type de mutation")
    p.add_argument('--intensity', type=float, default=1.0, help="Intensité (0.1–3.0)")
    p.add_argument('--chain', type=int, metavar='N', help="Générer une chaîne de N codes")
    p.add_argument('--template', type=int, default=0, help="Index du template")
    p.add_argument('--rune', choices=list(RUNES_EXTENDED.keys()), help="Forcer une rune")
    p.add_argument('--lieu', choices=list(LIEUX_EXTENDED.keys()), help="Forcer un lieu")
    p.add_argument('--effet', help="Forcer un effet (mot-clé)")
    p.add_argument('--version', type=int, choices=range(1,14), help="Version (1-13)")
    p.add_argument('--load-lexicon', metavar='FILE', help="Charger paleo_mnemos_lexicon.json")
    p.add_argument('--lexicon-ratio', type=float, default=0.3, help="Ratio d’injection (0.0–1.0)")
    p.add_argument('--to-grok', action='store_true', help="Générer un prompt optimisé pour Grok")
    p.add_argument('--export', metavar='FILE.json', help="Exporter les résultats")
    p.add_argument('--seed', type=int, help="Seed pour reproductibilité")
    p.add_argument('--no-color', action='store_true', help="Désactiver les couleurs ANSI")
    p.add_argument('--quiet', action='store_true', help="Mode silencieux")
    return p.parse_args()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    args = parse_args()
    if args.no_color:
        ANSI = False
    cli = FracturoCLI(args)
    try:
        cli.run()
    except KeyboardInterrupt:
        log("Interruption. Le FracturoScript persiste.", 'warn')
    except Exception as e:
        log(f"Erreur : {e}", 'warn', 'danger')
        if not args.quiet:
            raise
