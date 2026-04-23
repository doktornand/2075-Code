"""
FRACTUROSCRIPT STUDIO v2.0 - EXTENDED EDITION
Générateur/Mutateur/Hybrideur/Analyseur avancé de codes FracturoScript
Nouvelles fonctionnalités : Chaînes de mutation, séquences temporelles, 
cryptographie runique, analyse fractale, et bien plus.

Avertissement : Usage à des fins de recherche narrative uniquement. 
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
import json
import random
import hashlib
import copy
from datetime import datetime, timedelta
import re
import math
from collections import defaultdict, deque
import base64

# ============================================================================
# DONNÉES ÉTENDUES - Version 2.0
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

LIEUX_EXTENDED = {
    # Villes françaises
    'paris': {'pouvoir': 3, 'description': 'Cœur administratif, nexus politique', 'type': 'urbain', 'flux': 'élevé'},
    'marseille': {'pouvoir': 2, 'description': 'Port méditerranéen, mélanges culturels', 'type': 'portuaire', 'flux': 'moyen'},
    'lyon': {'pouvoir': 2, 'description': 'Carrefour historique, underground', 'type': 'urbain', 'flux': 'élevé'},
    'bordeaux': {'pouvoir': 1, 'description': 'Vigne et pierre, mémoire liquide', 'type': 'historique', 'flux': 'faible'},
    'lille': {'pouvoir': 1, 'description': 'Frontière nord, échanges secrets', 'type': 'frontière', 'flux': 'moyen'},
    'toulouse': {'pouvoir': 2, 'description': 'Rose et espace, ambitions célestes', 'type': 'technologique', 'flux': 'moyen'},
    'nantes': {'pouvoir': 3, 'description': 'Estuaire de la mémoire, port des rêves', 'type': 'portuaire', 'flux': 'élevé'},
    'strasbourg': {'pouvoir': 2, 'description': 'Frontière linguistique, pont européen', 'type': 'frontière', 'flux': 'moyen'},
    'montpellier': {'pouvoir': 1, 'description': 'Savoir ancien, soleil académique', 'type': 'académique', 'flux': 'faible'},
    'rennes': {'pouvoir': 2, 'description': 'Forêt et rébellion, cœur breton', 'type': 'mystique', 'flux': 'moyen'},
    
    # Espaces numériques
    'internet': {'pouvoir': 5, 'description': 'Réseau global, conscience digitale', 'type': 'digital', 'flux': 'extrême'},
    'datacenter': {'pouvoir': 4, 'description': 'Temple des données, sanctuaire IA', 'type': 'digital', 'flux': 'élevé'},
    'darkweb': {'pouvoir': 4, 'description': 'Ombre du réseau, marché interdit', 'type': 'digital', 'flux': 'élevé'},
    'blockchain': {'pouvoir': 3, 'description': 'Registre immuable, vérité distribuée', 'type': 'digital', 'flux': 'moyen'},
    'cloud': {'pouvoir': 3, 'description': 'Nuage de bits, stockage éthéré', 'type': 'digital', 'flux': 'élevé'},
    
    # Lieux mystiques
    'bibliotheque': {'pouvoir': 3, 'description': 'Archive vivante, mémoire papier', 'type': 'savoir', 'flux': 'faible'},
    'cathedrale': {'pouvoir': 4, 'description': 'Pierre sacrée, résonance divine', 'type': 'mystique', 'flux': 'faible'},
    'cimetiere': {'pouvoir': 4, 'description': 'Frontière des morts, mémoire éternelle', 'type': 'mystique', 'flux': 'faible'},
    'foret': {'pouvoir': 2, 'description': 'Réseau racinaire, conscience arborescente', 'type': 'naturel', 'flux': 'faible'},
    'ocean': {'pouvoir': 5, 'description': 'Abîme liquide, mémoire primordiale', 'type': 'naturel', 'flux': 'extrême'},
    'montagne': {'pouvoir': 3, 'description': 'Épine terrestre, silence minéral', 'type': 'naturel', 'flux': 'faible'},
    
    # Lieux temporels
    'passé': {'pouvoir': 5, 'description': 'Strates révolues, archives impossibles', 'type': 'temporel', 'flux': 'nul'},
    'futur': {'pouvoir': 5, 'description': 'Potentiels non-réalisés, virtualités', 'type': 'temporel', 'flux': 'infini'},
    'présent': {'pouvoir': 3, 'description': 'Instant fugace, maintenant éternel', 'type': 'temporel', 'flux': 'constant'}
}

EFFETS_EXTENDED = [
    # Effets de mémoire
    'révélation mémoire', 'effacement sélectif', 'fusion souvenirs',
    'extraction narrative', 'implantation expérience', 'reconstruction passé',
    'archivage conscience', 'purge traumatique', 'restauration identitaire',
    
    # Effets temporels
    'glissement temporel', 'boucle causale', 'accélération locale',
    'ralentissement perceptuel', 'synchronisation multiple', 'désalignement chronologique',
    'anticipation événementielle', 'rétro-causalité', 'stase temporelle',
    
    # Effets spatiaux
    'téléportation conscience', 'projection astrale', 'déphasage spatial',
    'ancrage géographique', 'fusion lieux', 'cartographie psychique',
    
    # Effets numériques
    'protection réseau', 'manipulation données', 'encryption quantique',
    'contournement surveillance', 'injection code', 'corruption fichier',
    'génération deepfake', 'anonymisation totale', 'traçage inversé',
    
    # Effets sociaux
    'influence collective', 'mémétique virale', 'persuasion subliminale',
    'effacement identité publique', 'fabrication réputation', 'réseau dormant',
    
    # Effets perceptuels
    'synesthésie contrôlée', 'vision augmentée', 'interface rêve',
    'communication silence', 'lecture pensées', 'projection émotionnelle',
    'hallucination dirigée', 'lucidité onirique',
    
    # Effets métaphysiques
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

PREFIXES_STYLE = ['Ω', 'Ѡ', 'Ψ', 'Φ', 'Δ', '∇', '∞', '◊', '◉', '⌬', '⧫', '◬']
SUFFIXES_STYLE = ['•••', '◆◆◆', '···', '+++', '≡≡≡', '∴', '∵', '※', '⁂', '⁎']
SEPARATEURS = ['—', '::', '|', '/', '\\', '>', '<', '→', '←', '↔', '⇄', '•']

# Templates de structure avancés
TEMPLATES_ADVANCED = {
    "templates": [
        {
            "nom": "Classique",
            "structure": "Ω<{rune}>v{version} {lieu} — {effet} •••",
            "description": "Format standard du Conseil",
            "complexité": 1
        },
        {
            "nom": "Multi-Runes",
            "structure": "{rune1}+{rune2}+{rune3} @ {lieu} :: v{version} :: {effet}",
            "description": "Combinaison de trois runes",
            "complexité": 3,
            "multi_rune": True
        },
        {
            "nom": "Chaîne Temporelle",
            "structure": "{rune}[t={temps}] → {lieu} → {effet} → v{version}",
            "description": "Activation différée dans le temps",
            "complexité": 2,
            "temporal": True
        },
        {
            "nom": "Réseau Distribué",
            "structure": "∇{rune}∇ <{lieu1}⇄{lieu2}⇄{lieu3}> |{effet}| v{version}",
            "description": "Multi-lieux synchronisés",
            "complexité": 3,
            "multi_lieu": True
        },
        {
            "nom": "Modificateur Complexe",
            "structure": "{mod1}[{rune}]{mod2} :: {lieu} :: {effet} :: v{version}",
            "description": "Double modificateur",
            "complexité": 2,
            "with_mods": True
        },
        {
            "nom": "Encryption Runique",
            "structure": "#{hash}# {rune}^{version} @ {lieu} ⊕ {effet}",
            "description": "Code crypté par hash",
            "complexité": 3,
            "encrypted": True
        },
        {
            "nom": "Séquence Fractale",
            "structure": "{rune}↺{iteration}↻ {lieu}^{dimension} ⟨{effet}⟩ v{version}",
            "description": "Itération fractale",
            "complexité": 4,
            "fractal": True
        },
        {
            "nom": "Interface Quantique",
            "structure": "|ψ⟩{rune}⟨ψ| ⊗ {lieu} ≡ {effet} ≡ v{version}",
            "description": "Superposition quantique",
            "complexité": 4,
            "quantum": True
        },
        {
            "nom": "Glitch Syntaxique",
            "structure": "{rune}�v{version}�{lieu}��{effet}�",
            "description": "Format corrompu volontairement",
            "complexité": 2,
            "glitched": True
        },
        {
            "nom": "Palindrome Runique",
            "structure": "{effet}←{lieu}←v{version}←{rune}→v{version}→{lieu}→{effet}",
            "description": "Structure miroir",
            "complexité": 3,
            "palindrome": True
        }
    ]
}

# ============================================================================
# CLASSE GÉNÉRATEUR ÉTENDU
# ============================================================================

class FracturoScriptGeneratorExtended:
    def __init__(self):
        self.templates = self.load_templates()
        self.history = []
        self.mutation_log = []
        self.chains = []  # Chaînes de codes liés
        self.favorites = []
        self.tags = defaultdict(list)
        self.statistics = defaultdict(int)
        
    def load_templates(self):
        try:
            with open('fracturo_templates_extended.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return TEMPLATES_ADVANCED
    
    def save_templates(self):
        with open('fracturo_templates_extended.json', 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, indent=2, ensure_ascii=False)
    
    def generate_code(self, **kwargs):
        """Génération avancée avec paramètres étendus"""
        template_index = kwargs.get('template_index', 0)
        template = self.templates["templates"][template_index % len(self.templates["templates"])]
        
        # Paramètres de base
        params = {
            'rune': kwargs.get('rune', random.choice(list(RUNES_EXTENDED.keys()))),
            'lieu': kwargs.get('lieu', random.choice(list(LIEUX_EXTENDED.keys()))),
            'effet': kwargs.get('effet', random.choice(EFFETS_EXTENDED)),
            'version': kwargs.get('version', random.randint(1, 13))
        }
        
        # Paramètres étendus selon le template
        if template.get('multi_rune'):
            params['rune1'] = random.choice(list(RUNES_EXTENDED.keys()))
            params['rune2'] = random.choice(list(RUNES_EXTENDED.keys()))
            params['rune3'] = random.choice(list(RUNES_EXTENDED.keys()))
        
        if template.get('multi_lieu'):
            params['lieu1'] = random.choice(list(LIEUX_EXTENDED.keys()))
            params['lieu2'] = random.choice(list(LIEUX_EXTENDED.keys()))
            params['lieu3'] = random.choice(list(LIEUX_EXTENDED.keys()))
        
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
        
        # Génération du code
        try:
            code = template["structure"].format(**params)
        except KeyError as e:
            # Si un paramètre manque, le générer
            missing_param = str(e).strip("'")
            params[missing_param] = "?"
            code = template["structure"].format(**params)
        
        # Calcul des métriques
        code_hash = hashlib.sha256(code.encode()).hexdigest()[:10]
        
        # Calcul du danger
        danger = self.calculate_danger(params, template)
        
        # Construction du résultat
        result = {
            'code': code,
            'hash': code_hash,
            'params': params,
            'template': template["nom"],
            'timestamp': datetime.now().isoformat(),
            'danger': danger,
            'complexité': template.get('complexité', 1),
            'tags': []
        }
        
        self.history.append(result)
        self.statistics['total_generated'] += 1
        
        return result
    
    def calculate_danger(self, params, template):
        """Calcul avancé du niveau de danger"""
        danger = 0
        
        # Danger de base des runes
        if 'rune' in params:
            danger += RUNES_EXTENDED.get(params['rune'], {}).get('danger', 1)
        
        # Multi-runes
        if template.get('multi_rune'):
            for key in ['rune1', 'rune2', 'rune3']:
                if key in params:
                    danger += RUNES_EXTENDED.get(params[key], {}).get('danger', 1)
        
        # Version
        danger *= params.get('version', 1)
        
        # Complexité du template
        danger += template.get('complexité', 1) * 2
        
        # Lieux à haut pouvoir
        for lieu_key in ['lieu', 'lieu1', 'lieu2', 'lieu3']:
            if lieu_key in params:
                lieu = params[lieu_key]
                danger += LIEUX_EXTENDED.get(lieu, {}).get('pouvoir', 1)
        
        return min(danger, 100)  # Cap à 100
    
    def mutate_code(self, code_obj, mutation_type='random', intensity=1.0):
        """Mutation avancée avec intensité variable"""
        mutated = copy.deepcopy(code_obj)
        
        mutations_applied = []
        
        if mutation_type == 'random':
            # Mutations multiples basées sur l'intensité
            num_mutations = int(1 + intensity * 2)
            possible_mutations = ['rune', 'lieu', 'effet', 'version', 'modificateur']
            
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
                other = random.choice([c for c in self.history if c['hash'] != code_obj['hash']])
                
                # Fusion des paramètres
                for key in mutated['params']:
                    if key in other['params'] and random.random() < 0.5:
                        mutated['params'][key] = other['params'][key]
                
                mutations_applied.append(f"hybrid avec {other['hash'][:6]}")
        
        elif mutation_type == 'inversion':
            # Inverse les polarités et effets
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
            # Ajoute des itérations fractales
            mutated['params']['iteration'] = random.randint(3, 8)
            mutated['params']['dimension'] = round(random.uniform(2.0, 4.0), 2)
            mutations_applied.append('fractale')
        
        # Régénération du code
        template_index = next((i for i, t in enumerate(self.templates["templates"]) 
                             if t["nom"] == mutated['template']), 0)
        template = self.templates["templates"][template_index]
        
        try:
            mutated['code'] = template["structure"].format(**mutated['params'])
        except KeyError:
            pass  # Garde le code précédent si erreur
        
        # Mise à jour des métadonnées
        mutated['hash'] = hashlib.sha256(mutated['code'].encode()).hexdigest()[:10]
        mutated['parent'] = code_obj['hash']
        mutated['mutation_type'] = mutation_type
        mutated['mutations_applied'] = mutations_applied
        mutated['timestamp'] = datetime.now().isoformat()
        mutated['danger'] = self.calculate_danger(mutated['params'], template)
        mutated['generation'] = code_obj.get('generation', 0) + 1
        
        self.mutation_log.append({
            'parent': code_obj['hash'],
            'child': mutated['hash'],
            'type': mutation_type,
            'intensity': intensity,
            'mutations': mutations_applied,
            'timestamp': mutated['timestamp']
        })
        
        self.history.append(mutated)
        self.statistics['total_mutations'] += 1
        
        return mutated
    
    def add_advanced_glitch(self, code, intensity=1.0):
        """Glitchs avancés avec niveaux d'intensité"""
        num_glitches = int(1 + intensity * 3)
        
        glitches = [
            lambda s: s.replace('Ω', random.choice(['Ѡ', 'Ѽ', 'Ѿ'])),
            lambda s: s + '�' * random.randint(1, 3),
            lambda s: s.replace('•••', '•' * random.randint(1, 5)),
            lambda s: ''.join(c if random.random() > 0.1 else c.upper() for c in s),
            lambda s: s[:len(s)//2] + ' ' * random.randint(1, 3) + s[len(s)//2:],
            lambda s: s.replace('—', random.choice(['~', '≈', '≋', '⁓'])),
            lambda s: re.sub(r'v(\d+)', lambda m: f'v{int(m.group(1)) + random.randint(-2, 2)}', s),
            lambda s: s + f'\\x{random.randint(0, 255):02x}',
            lambda s: s[::-1] if random.random() < 0.3 else s,  # Reverse aléatoire
            lambda s: ''.join(c + chr(0x0300 + random.randint(0, 50)) if random.random() < 0.2 else c for c in s),
        ]
        
        result = code
        for _ in range(num_glitches):
            result = random.choice(glitches)(result)
        
        return result
    
    def create_chain(self, length=5, chain_type='mutation'):
        """Crée une chaîne de codes liés"""
        if not self.history:
            # Générer un code initial
            current = self.generate_code()
        else:
            current = random.choice(self.history)
        
        chain = [current]
        
        for i in range(length - 1):
            if chain_type == 'mutation':
                current = self.mutate_code(current, mutation_type='random', intensity=0.5)
            elif chain_type == 'evolution':
                # Mutation progressive
                current = self.mutate_code(current, mutation_type='amplification', intensity=i / length)
            elif chain_type == 'divergence':
                # Mutations aléatoires fortes
                mut_types = ['random', 'glitch', 'inversion', 'fractale']
                current = self.mutate_code(current, mutation_type=random.choice(mut_types), intensity=1.5)
            
            chain.append(current)
        
        chain_obj = {
            'id': hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8],
            'type': chain_type,
            'codes': chain,
            'length': length,
            'created': datetime.now().isoformat()
        }
        
        self.chains.append(chain_obj)
        return chain_obj
    
    def analyze_code_extended(self, code_obj):
        """Analyse approfondie d'un code"""
        analysis = {
            'stabilité': self.calculate_stability(code_obj),
            'compatibilité_élémentaire': self.analyze_elements(code_obj),
            'résonance_fractale': self.calculate_fractal_resonance(code_obj),
            'flux_temporel': self.analyze_temporal_flux(code_obj),
            'portée_géographique': self.calculate_geographic_reach(code_obj),
            'durée_estimée': self.estimate_duration(code_obj),
            'effets_secondaires': self.predict_side_effects(code_obj),
            'synergies_potentielles': self.find_synergies(code_obj),
            'contre_mesures': self.suggest_countermeasures(code_obj),
            'score_esthétique': self.calculate_aesthetic_score(code_obj)
        }
        
        return analysis
    
    def calculate_stability(self, code_obj):
        """Calcule la stabilité du code"""
        base_stability = 100
        
        # Pénalités
        if code_obj.get('danger', 0) > 50:
            base_stability -= (code_obj['danger'] - 50)
        
        if code_obj.get('complexité', 1) > 2:
            base_stability -= code_obj['complexité'] * 5
        
        if code_obj.get('generation', 0) > 5:
            base_stability -= code_obj['generation'] * 3
        
        if 'glitch' in code_obj.get('mutation_type', ''):
            base_stability -= 20
        
        return max(0, min(100, base_stability))
    
    def analyze_elements(self, code_obj):
        """Analyse les éléments présents"""
        elements = defaultdict(int)
        
        for key, value in code_obj.get('params', {}).items():
            if key.startswith('rune'):
                rune_data = RUNES_EXTENDED.get(value, {})
                element = rune_data.get('élément', 'inconnu')
                elements[element] += 1
        
        # Calcul de compatibilité
        if len(elements) == 0:
            return {'compatibilité': 100, 'éléments': {}}
        
        # Incompatibilités élémentaires
        incompatible_pairs = [
            ('feu', 'glace'),
            ('eau', 'feu'),
            ('air', 'terre')
        ]
        
        compatibility = 100
        for elem1, elem2 in incompatible_pairs:
            if elem1 in elements and elem2 in elements:
                compatibility -= 20
        
        return {
            'compatibilité': max(0, compatibility),
            'éléments': dict(elements),
            'dominant': max(elements, key=elements.get) if elements else 'aucun'
        }
    
    def calculate_fractal_resonance(self, code_obj):
        """Calcule la résonance fractale"""
        # Utilise le hash pour générer une dimension fractale
        hash_val = int(code_obj['hash'][:8], 16)
        dimension = 1 + (hash_val % 1000) / 333.0
        
        iteration = code_obj.get('params', {}).get('iteration', 1)
        
        resonance = dimension * math.log(iteration + 1) * 10
        
        return {
            'dimension': round(dimension, 3),
            'itérations': iteration,
            'résonance': round(resonance, 2)
        }
    
    def analyze_temporal_flux(self, code_obj):
        """Analyse le flux temporel"""
        params = code_obj.get('params', {})
        
        # Détecte les effets temporels
        effet = params.get('effet', '')
        temporal_keywords = ['temporel', 'temps', 'boucle', 'passé', 'futur', 'chronologique']
        
        is_temporal = any(keyword in effet.lower() for keyword in temporal_keywords)
        
        # Lieux temporels
        temporal_lieux = ['passé', 'futur', 'présent']
        temporal_lieu = any(lieu in params.get('lieu', '') for lieu in temporal_lieux)
        
        if is_temporal or temporal_lieu:
            return {
                'type': 'actif',
                'direction': 'bidirectionnel' if 'boucle' in effet else 'linéaire',
                'intensité': params.get('version', 1) * 10,
                'risque_paradoxe': code_obj.get('danger', 0) > 40
            }
        else:
            return {'type': 'stable', 'intensité': 0}
    
    def calculate_geographic_reach(self, code_obj):
        """Calcule la portée géographique"""
        params = code_obj.get('params', {})
        total_reach = 0
        
        for key in ['lieu', 'lieu1', 'lieu2', 'lieu3']:
            if key in params:
                lieu = params[key]
                lieu_data = LIEUX_EXTENDED.get(lieu, {})
                pouvoir = lieu_data.get('pouvoir', 1)
                
                # Mapping pouvoir -> km
                reach_map = {1: 10, 2: 50, 3: 200, 4: 1000, 5: 10000}
                total_reach += reach_map.get(pouvoir, 10)
        
        # Multiplicateur de version
        total_reach *= (1 + params.get('version', 1) / 10)
        
        return round(total_reach, 1)
    
    def estimate_duration(self, code_obj):
        """Estime la durée d'effet"""
        params = code_obj.get('params', {})
        version = params.get('version', 1)
        
        # Durée de base en heures
        base_duration = version * random.uniform(2, 8)
        
        # Modificateurs
        if 'persist' in str(code_obj.get('code', '')).lower():
            base_duration *= 3
        
        if 'instant' in str(code_obj.get('code', '')).lower():
            base_duration = 0.1
        
        if code_obj.get('complexité', 1) > 2:
            base_duration *= 1.5
        
        return round(base_duration, 1)
    
    def predict_side_effects(self, code_obj):
        """Prédit les effets secondaires"""
        effects = []
        danger = code_obj.get('danger', 0)
        params = code_obj.get('params', {})
        
        # Effets basés sur le danger
        if danger > 70:
            effects.extend(['Amnésie sévère', 'Désorientation spatio-temporelle', 'Corruption mémorielle'])
        elif danger > 50:
            effects.extend(['Amnésie temporaire', 'Vertiges', 'Synesthésie'])
        elif danger > 30:
            effects.extend(['Maux de tête', 'Fatigue cognitive'])
        
        # Effets basés sur les runes
        for key, value in params.items():
            if key.startswith('rune'):
                rune_data = RUNES_EXTENDED.get(value, {})
                element = rune_data.get('élément', '')
                
                if element == 'feu':
                    effects.append('Sensation de chaleur')
                elif element == 'glace':
                    effects.append('Frissons persistants')
                elif element == 'eau':
                    effects.append('Rêves aquatiques')
                elif element == 'void':
                    effects.append('Perception du vide')
        
        # Effets spéciaux
        effet = params.get('effet', '')
        if 'mémoire' in effet:
            effects.append('Flashbacks aléatoires')
        if 'temps' in effet or 'temporel' in effet:
            effects.append('Désynchronisation circadienne')
        if 'communication' in effet:
            effects.append('Pensées intrusives')
        
        # Basé sur le hash
        hash_int = int(code_obj['hash'][:8], 16)
        special_effects = [
            'Goût métallique', 'Acouphènes', 'Vision périphérique altérée',
            'Sensibilité électromagnétique', 'Prémonitions mineures',
            'Déjà-vu récurrents', 'Lucidité onirique', 'Synesthésie temporaire'
        ]
        
        if hash_int % 5 == 0:
            effects.append(random.choice(special_effects))
        
        return list(set(effects))[:8]  # Max 8 effets uniques
    
    def find_synergies(self, code_obj):
        """Trouve des synergies potentielles avec d'autres codes"""
        synergies = []
        
        if len(self.history) < 2:
            return synergies
        
        current_params = code_obj.get('params', {})
        current_rune = current_params.get('rune', '')
        current_element = RUNES_EXTENDED.get(current_rune, {}).get('élément', '')
        
        for other_code in self.history[-20:]:  # 20 derniers codes
            if other_code['hash'] == code_obj['hash']:
                continue
            
            other_params = other_code.get('params', {})
            other_rune = other_params.get('rune', '')
            other_element = RUNES_EXTENDED.get(other_rune, {}).get('élément', '')
            
            # Synergie élémentaire
            if current_element == other_element and current_element != '':
                synergies.append({
                    'type': 'élémentaire',
                    'avec': other_code['hash'][:6],
                    'bonus': '+25% puissance'
                })
            
            # Synergie de lieu
            if current_params.get('lieu') == other_params.get('lieu'):
                synergies.append({
                    'type': 'géographique',
                    'avec': other_code['hash'][:6],
                    'bonus': '+30% portée'
                })
            
            # Synergie d'effet complémentaire
            effet1 = current_params.get('effet', '')
            effet2 = other_params.get('effet', '')
            complementary_pairs = [
                ('révélation', 'protection'),
                ('effacement', 'reconstruction'),
                ('amplification', 'stabilisation')
            ]
            
            for pair in complementary_pairs:
                if (pair[0] in effet1 and pair[1] in effet2) or (pair[1] in effet1 and pair[0] in effet2):
                    synergies.append({
                        'type': 'complémentaire',
                        'avec': other_code['hash'][:6],
                        'bonus': 'Effet combiné'
                    })
        
        return synergies[:5]  # Top 5
    
    def suggest_countermeasures(self, code_obj):
        """Suggère des contre-mesures"""
        countermeasures = []
        danger = code_obj.get('danger', 0)
        
        if danger < 20:
            return ['Aucune contre-mesure nécessaire']
        
        # Contre-mesures générales
        if danger > 50:
            countermeasures.append('Environnement de confinement runique requis')
            countermeasures.append('Supervision d\'un RuneSmith expérimenté')
        
        if danger > 30:
            countermeasures.append('Port d\'amulette de protection (Algiz recommandée)')
            countermeasures.append('Préparation mentale préalable')
        
        # Contre-mesures spécifiques aux effets
        params = code_obj.get('params', {})
        effet = params.get('effet', '')
        
        if 'mémoire' in effet:
            countermeasures.append('Journalisation avant et après activation')
        
        if 'temporel' in effet or 'temps' in effet:
            countermeasures.append('Ancrage temporel stable requis')
        
        if 'effacement' in effet:
            countermeasures.append('Backup mémoriel recommandé')
        
        # Contre-mesures élémentaires
        current_rune = params.get('rune', '')
        element = RUNES_EXTENDED.get(current_rune, {}).get('élément', '')
        
        counter_elements = {
            'feu': 'eau',
            'glace': 'feu',
            'eau': 'terre',
            'air': 'terre'
        }
        
        if element in counter_elements:
            countermeasures.append(f'Rune {counter_elements[element]} en stand-by pour neutralisation')
        
        return countermeasures
    
    def calculate_aesthetic_score(self, code_obj):
        """Score esthétique du code"""
        code = code_obj.get('code', '')
        
        score = 50  # Base
        
        # Longueur optimale
        if 40 < len(code) < 80:
            score += 10
        
        # Présence de symboles spéciaux
        special_chars = sum(1 for c in code if ord(c) > 127)
        score += min(special_chars * 2, 20)
        
        # Symétrie
        if code == code[::-1]:
            score += 30  # Palindrome
        elif code[:len(code)//2] in code[len(code)//2:]:
            score += 15  # Répétition
        
        # Balance des caractères
        if len(set(code)) / len(code) > 0.5:
            score += 10  # Diversité
        
        # Complexité visuelle
        score += code_obj.get('complexité', 1) * 5
        
        return min(100, score)
    
    def add_tag(self, code_hash, tag):
        """Ajoute un tag à un code"""
        self.tags[code_hash].append(tag)
        
        # Ajoute aussi au code dans l'historique
        for code in self.history:
            if code['hash'] == code_hash:
                if 'tags' not in code:
                    code['tags'] = []
                code['tags'].append(tag)
                break
    
    def search_codes(self, **criteria):
        """Recherche avancée de codes"""
        results = []
        
        for code in self.history:
            matches = True
            
            # Critères de recherche
            if 'rune' in criteria:
                if criteria['rune'] not in str(code.get('params', {})):
                    matches = False
            
            if 'lieu' in criteria:
                if criteria['lieu'] not in str(code.get('params', {})):
                    matches = False
            
            if 'effet' in criteria:
                if criteria['effet'].lower() not in code.get('params', {}).get('effet', '').lower():
                    matches = False
            
            if 'min_danger' in criteria:
                if code.get('danger', 0) < criteria['min_danger']:
                    matches = False
            
            if 'max_danger' in criteria:
                if code.get('danger', 100) > criteria['max_danger']:
                    matches = False
            
            if 'tag' in criteria:
                if criteria['tag'] not in code.get('tags', []):
                    matches = False
            
            if 'template' in criteria:
                if criteria['template'] != code.get('template'):
                    matches = False
            
            if matches:
                results.append(code)
        
        return results
    
    def export_advanced(self, filename, include_analysis=True):
        """Export avancé avec analyses"""
        export_data = {
            "metadata": {
                "version": "2.0",
                "export_date": datetime.now().isoformat(),
                "total_codes": len(self.history),
                "total_mutations": len(self.mutation_log),
                "total_chains": len(self.chains),
                "software": "FracturoScript Studio v2.0 Extended"
            },
            "statistics": dict(self.statistics),
            "codes": self.history,
            "mutation_tree": self.mutation_log,
            "chains": self.chains,
            "tags": {k: v for k, v in self.tags.items()}
        }
        
        if include_analysis:
            export_data["analyses"] = []
            for code in self.history[-50:]:  # 50 derniers pour ne pas surcharger
                analysis = self.analyze_code_extended(code)
                export_data["analyses"].append({
                    'hash': code['hash'],
                    'analysis': analysis
                })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return len(self.history)

# ============================================================================
# INTERFACE GRAPHIQUE ÉTENDUE
# ============================================================================

class FracturoScriptAppExtended:
    def __init__(self, root):
        self.root = root
        self.root.title("⌬ FRACTUROSCRIPT STUDIO v2.0 - EXTENDED EDITION ⌬")
        self.root.geometry("1400x900")
        
        self.generator = FracturoScriptGeneratorExtended()
        self.current_code = None
        self.current_chain = None
        
        self.setup_styles()
        self.create_widgets()
        self.create_menu()
        
    def setup_styles(self):
        """Configuration des styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        self.bg_color = '#0a0a12'
        self.fg_color = '#00ffcc'
        self.accent_color = '#ff00ff'
        self.warning_color = '#ff3300'
        self.success_color = '#00ff00'
        
        style.configure('Cyber.TFrame', background=self.bg_color)
        style.configure('Cyber.TLabel', background=self.bg_color, foreground=self.fg_color, 
                       font=('Courier', 10))
        style.configure('Cyber.TButton', background='#1a1a2e', foreground=self.fg_color,
                       font=('Courier', 9))
        style.configure('Title.TLabel', font=('Courier', 18, 'bold'), 
                       foreground=self.accent_color, background=self.bg_color)
        style.configure('Subtitle.TLabel', font=('Courier', 11, 'bold'),
                       foreground=self.fg_color, background=self.bg_color)
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Création de l'interface principale"""
        
        # Notebook pour onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Onglet 1: Génération
        self.tab_generation = ttk.Frame(self.notebook, style='Cyber.TFrame')
        self.notebook.add(self.tab_generation, text="⚡ GÉNÉRATION")
        self.create_generation_tab()
        
        # Onglet 2: Mutation avancée
        self.tab_mutation = ttk.Frame(self.notebook, style='Cyber.TFrame')
        self.notebook.add(self.tab_mutation, text="🔀 MUTATION")
        self.create_mutation_tab()
        
        # Onglet 3: Analyse
        self.tab_analysis = ttk.Frame(self.notebook, style='Cyber.TFrame')
        self.notebook.add(self.tab_analysis, text="🔮 ANALYSE")
        self.create_analysis_tab()
        
        # Onglet 4: Chaînes
        self.tab_chains = ttk.Frame(self.notebook, style='Cyber.TFrame')
        self.notebook.add(self.tab_chains, text="⛓ CHAÎNES")
        self.create_chains_tab()
        
        # Onglet 5: Bibliothèque
        self.tab_library = ttk.Frame(self.notebook, style='Cyber.TFrame')
        self.notebook.add(self.tab_library, text="📚 BIBLIOTHÈQUE")
        self.create_library_tab()
        
        # Barre de statut
        self.create_status_bar()
    
    def create_generation_tab(self):
        """Onglet de génération"""
        # Frame principal divisé
        left_frame = ttk.Frame(self.tab_generation, style='Cyber.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.tab_generation, style='Cyber.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === GAUCHE: Contrôles ===
        ttk.Label(left_frame, text="⚡ PARAMÈTRES DE GÉNÉRATION ⚡", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        control_frame = ttk.Frame(left_frame, style='Cyber.TFrame')
        control_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Runes (avec sélection multiple possible)
        ttk.Label(control_frame, text="Rune principale:", style='Cyber.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.rune_var = tk.StringVar(value=random.choice(list(RUNES_EXTENDED.keys())))
        rune_combo = ttk.Combobox(control_frame, textvariable=self.rune_var,
                                 values=list(RUNES_EXTENDED.keys()), width=8)
        rune_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Info rune
        self.rune_info_var = tk.StringVar(value="")
        ttk.Label(control_frame, textvariable=self.rune_info_var, 
                 style='Cyber.TLabel', font=('Courier', 8)).grid(
            row=0, column=2, padx=5, sticky=tk.W)
        
        rune_combo.bind('<<ComboboxSelected>>', self.update_rune_info)
        
        # Lieu
        ttk.Label(control_frame, text="Lieu:", style='Cyber.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.lieu_var = tk.StringVar(value=random.choice(list(LIEUX_EXTENDED.keys())))
        lieu_combo = ttk.Combobox(control_frame, textvariable=self.lieu_var,
                                 values=list(LIEUX_EXTENDED.keys()), width=15)
        lieu_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Info lieu
        self.lieu_info_var = tk.StringVar(value="")
        ttk.Label(control_frame, textvariable=self.lieu_info_var,
                 style='Cyber.TLabel', font=('Courier', 8)).grid(
            row=1, column=2, padx=5, sticky=tk.W)
        
        lieu_combo.bind('<<ComboboxSelected>>', self.update_lieu_info)
        
        # Effet
        ttk.Label(control_frame, text="Effet désiré:", style='Cyber.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.effet_var = tk.StringVar(value=random.choice(EFFETS_EXTENDED))
        effet_combo = ttk.Combobox(control_frame, textvariable=self.effet_var,
                                  values=EFFETS_EXTENDED, width=25)
        effet_combo.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Version
        ttk.Label(control_frame, text="Version (1-13):", style='Cyber.TLabel').grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.version_var = tk.IntVar(value=random.randint(1, 13))
        version_frame = ttk.Frame(control_frame, style='Cyber.TFrame')
        version_frame.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5)
        
        version_spin = ttk.Spinbox(version_frame, from_=1, to=13,
                                   textvariable=self.version_var, width=5)
        version_spin.pack(side=tk.LEFT)
        
        self.version_danger_var = tk.StringVar(value="")
        ttk.Label(version_frame, textvariable=self.version_danger_var,
                 style='Cyber.TLabel', font=('Courier', 8)).pack(side=tk.LEFT, padx=10)
        
        version_spin.bind('<KeyRelease>', lambda e: self.update_danger_preview())
        version_spin.bind('<<Increment>>', lambda e: self.update_danger_preview())
        version_spin.bind('<<Decrement>>', lambda e: self.update_danger_preview())
        
        # Template
        ttk.Label(control_frame, text="Template:", style='Cyber.TLabel').grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar()
        template_combo = ttk.Combobox(control_frame, textvariable=self.template_var,
                                     values=[t["nom"] for t in self.generator.templates["templates"]],
                                     width=20)
        template_combo.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        template_combo.current(0)
        
        # Boutons de génération
        btn_frame = ttk.Frame(left_frame, style='Cyber.TFrame')
        btn_frame.pack(fill=tk.X, padx=10, pady=15)
        
        ttk.Button(btn_frame, text="⚡ Générer Code", command=self.generate_code,
                  style='Cyber.TButton', width=20).pack(pady=3)
        ttk.Button(btn_frame, text="🎲 Aléatoire Complet", command=self.generate_random,
                  style='Cyber.TButton', width=20).pack(pady=3)
        ttk.Button(btn_frame, text="🌀 Série de 5", command=self.generate_series,
                  style='Cyber.TButton', width=20).pack(pady=3)
        
        # === DROITE: Affichage ===
        ttk.Label(right_frame, text="⌬ CODE GÉNÉRÉ ⌬",
                 style='Subtitle.TLabel').pack(pady=10)
        
        self.code_display = scrolledtext.ScrolledText(
            right_frame, height=15, width=60,
            bg='#1a1a2e', fg=self.fg_color,
            font=('Courier New', 11, 'bold'), wrap=tk.WORD,
            insertbackground=self.fg_color
        )
        self.code_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Boutons d'action sur le code
        action_frame = ttk.Frame(right_frame, style='Cyber.TFrame')
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(action_frame, text="📋 Copier", command=self.copy_code,
                  style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="⭐ Favori", command=self.add_to_favorites,
                  style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="🏷️ Tag", command=self.add_tag_dialog,
                  style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="💾 Sauver", command=self.save_single_code,
                  style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
    
    def create_mutation_tab(self):
        """Onglet de mutation avancée"""
        # Layout en 3 parties
        top_frame = ttk.Frame(self.tab_mutation, style='Cyber.TFrame')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        mid_frame = ttk.Frame(self.tab_mutation, style='Cyber.TFrame')
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        bottom_frame = ttk.Frame(self.tab_mutation, style='Cyber.TFrame')
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # === TOP: Types de mutation ===
        ttk.Label(top_frame, text="🔀 TYPES DE MUTATION DISPONIBLES 🔀",
                 style='Subtitle.TLabel').pack(pady=5)
        
        mutation_types_frame = ttk.Frame(top_frame, style='Cyber.TFrame')
        mutation_types_frame.pack(pady=10)
        
        mutations = [
            ('Aléatoire', 'random'), ('Glitch', 'glitch'),
            ('Hybride', 'hybrid'), ('Inversion', 'inversion'),
            ('Amplification', 'amplification'), ('Fractale', 'fractale')
        ]
        
        for i, (label, mut_type) in enumerate(mutations):
            ttk.Button(mutation_types_frame, text=label,
                      command=lambda m=mut_type: self.mutate_current(m),
                      style='Cyber.TButton', width=12).grid(
                row=i//3, column=i%3, padx=5, pady=5)
        
        # Intensité de mutation
        intensity_frame = ttk.Frame(top_frame, style='Cyber.TFrame')
        intensity_frame.pack(pady=5)
        
        ttk.Label(intensity_frame, text="Intensité:", style='Cyber.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.intensity_var = tk.DoubleVar(value=1.0)
        intensity_scale = ttk.Scale(intensity_frame, from_=0.1, to=3.0,
                                   variable=self.intensity_var, orient=tk.HORIZONTAL,
                                   length=200)
        intensity_scale.pack(side=tk.LEFT, padx=5)
        
        self.intensity_label = tk.Label(intensity_frame, text="1.0x",
                                        bg=self.bg_color, fg=self.fg_color,
                                        font=('Courier', 10))
        self.intensity_label.pack(side=tk.LEFT, padx=5)
        
        intensity_scale.configure(command=self.update_intensity_label)
        
        # === MID: Affichage comparatif ===
        compare_frame = ttk.Frame(mid_frame, style='Cyber.TFrame')
        compare_frame.pack(fill=tk.BOTH, expand=True)
        
        # Colonne gauche: Original
        left_col = ttk.Frame(compare_frame, style='Cyber.TFrame')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(left_col, text="📜 CODE ORIGINAL",
                 style='Subtitle.TLabel').pack(pady=5)
        
        self.original_display = scrolledtext.ScrolledText(
            left_col, height=12, width=40,
            bg='#1a1a2e', fg=self.fg_color,
            font=('Courier New', 9), wrap=tk.WORD
        )
        self.original_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Colonne droite: Muté
        right_col = ttk.Frame(compare_frame, style='Cyber.TFrame')
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(right_col, text="🧬 CODE MUTÉ",
                 style='Subtitle.TLabel').pack(pady=5)
        
        self.mutated_display = scrolledtext.ScrolledText(
            right_col, height=12, width=40,
            bg='#1a1a2e', fg=self.accent_color,
            font=('Courier New', 9), wrap=tk.WORD
        )
        self.mutated_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # === BOTTOM: Statistiques de mutation ===
        ttk.Label(bottom_frame, text="📊 STATISTIQUES DE MUTATION",
                 style='Subtitle.TLabel').pack(pady=5)
        
        self.mutation_stats_display = scrolledtext.ScrolledText(
            bottom_frame, height=6, width=80,
            bg='#1a1a2e', fg=self.success_color,
            font=('Courier New', 9), wrap=tk.WORD
        )
        self.mutation_stats_display.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def create_analysis_tab(self):
        """Onglet d'analyse approfondie"""
        # Layout 2 colonnes
        left_frame = ttk.Frame(self.tab_analysis, style='Cyber.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.tab_analysis, style='Cyber.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === GAUCHE: Analyses principales ===
        ttk.Label(left_frame, text="🔮 ANALYSE ONTOLOGIQUE 🔮",
                 style='Subtitle.TLabel').pack(pady=10)
        
        self.analysis_main = scrolledtext.ScrolledText(
            left_frame, height=20, width=50,
            bg='#1a1a2e', fg=self.accent_color,
            font=('Courier New', 9), wrap=tk.WORD
        )
        self.analysis_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bouton d'analyse
        ttk.Button(left_frame, text="🔍 Analyser Code Actuel",
                  command=self.analyze_current_code,
                  style='Cyber.TButton').pack(pady=10)
        
        # === DROITE: Visualisations ===
        ttk.Label(right_frame, text="📈 MÉTRIQUES VISUELLES",
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Canvas pour graphiques
        self.viz_canvas = tk.Canvas(right_frame, bg='#1a1a2e',
                                   highlightthickness=0, height=300)
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Légende
        legend_frame = ttk.Frame(right_frame, style='Cyber.TFrame')
        legend_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(legend_frame, text="🔴 Danger  🟡 Stabilité  🔵 Complexité  🟢 Esthétique",
                 style='Cyber.TLabel', font=('Courier', 8)).pack()
        
        # Détails supplémentaires
        ttk.Label(right_frame, text="📋 DÉTAILS TECHNIQUES",
                 style='Subtitle.TLabel').pack(pady=(10, 5))
        
        self.analysis_details = scrolledtext.ScrolledText(
            right_frame, height=10, width=50,
            bg='#1a1a2e', fg=self.fg_color,
            font=('Courier New', 8), wrap=tk.WORD
        )
        self.analysis_details.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_chains_tab(self):
        """Onglet de gestion des chaînes"""
        # Layout 3 sections
        top_frame = ttk.Frame(self.tab_chains, style='Cyber.TFrame')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        mid_frame = ttk.Frame(self.tab_chains, style='Cyber.TFrame')
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        bottom_frame = ttk.Frame(self.tab_chains, style='Cyber.TFrame')
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # === TOP: Création de chaînes ===
        ttk.Label(top_frame, text="⛓ GÉNÉRATEUR DE CHAÎNES ⛓",
                 style='Subtitle.TLabel').pack(pady=5)
        
        chain_control = ttk.Frame(top_frame, style='Cyber.TFrame')
        chain_control.pack(pady=10)
        
        ttk.Label(chain_control, text="Longueur:", style='Cyber.TLabel').grid(
            row=0, column=0, padx=5, pady=5)
        self.chain_length_var = tk.IntVar(value=5)
        ttk.Spinbox(chain_control, from_=2, to=20, textvariable=self.chain_length_var,
                   width=5).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(chain_control, text="Type:", style='Cyber.TLabel').grid(
            row=0, column=2, padx=5, pady=5)
        self.chain_type_var = tk.StringVar(value='mutation')
        chain_type_combo = ttk.Combobox(chain_control, textvariable=self.chain_type_var,
                                       values=['mutation', 'evolution', 'divergence'],
                                       width=12, state='readonly')
        chain_type_combo.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(chain_control, text="🔗 Créer Chaîne",
                  command=self.create_chain,
                  style='Cyber.TButton').grid(row=0, column=4, padx=10, pady=5)
        
        # === MID: Visualisation de chaîne ===
        viz_frame = ttk.LabelFrame(mid_frame, text="Visualisation de la Chaîne",
                                   style='Cyber.TFrame')
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.chain_display = scrolledtext.ScrolledText(
            viz_frame, height=15, width=80,
            bg='#1a1a2e', fg=self.fg_color,
            font=('Courier New', 9), wrap=tk.WORD
        )
        self.chain_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === BOTTOM: Liste des chaînes ===
        list_frame = ttk.LabelFrame(bottom_frame, text="Chaînes Sauvegardées",
                                    style='Cyber.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox avec scrollbar
        list_scroll_frame = ttk.Frame(list_frame, style='Cyber.TFrame')
        list_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(list_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chains_listbox = tk.Listbox(list_scroll_frame, bg='#1a1a2e',
                                         fg=self.fg_color, font=('Courier', 9),
                                         yscrollcommand=scrollbar.set)
        self.chains_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chains_listbox.yview)
        
        self.chains_listbox.bind('<<ListboxSelect>>', self.load_chain)
        
        # Boutons d'action
        chain_btn_frame = ttk.Frame(list_frame, style='Cyber.TFrame')
        chain_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(chain_btn_frame, text="📊 Analyser",
                  command=self.analyze_chain, style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(chain_btn_frame, text="💾 Exporter",
                  command=self.export_chain, style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(chain_btn_frame, text="🗑️ Supprimer",
                  command=self.delete_chain, style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
    
    def create_library_tab(self):
        """Onglet bibliothèque/recherche"""
        # Layout principal
        top_frame = ttk.Frame(self.tab_library, style='Cyber.TFrame')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        mid_frame = ttk.Frame(self.tab_library, style='Cyber.TFrame')
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # === TOP: Recherche ===
        ttk.Label(top_frame, text="📚 BIBLIOTHÈQUE DE CODES 📚",
                 style='Subtitle.TLabel').pack(pady=5)
        
        search_frame = ttk.LabelFrame(top_frame, text="Recherche Avancée",
                                     style='Cyber.TFrame')
        search_frame.pack(fill=tk.X, pady=10, padx=10)
        
        search_controls = ttk.Frame(search_frame, style='Cyber.TFrame')
        search_controls.pack(fill=tk.X, padx=10, pady=10)
        
        # Critères de recherche
        ttk.Label(search_controls, text="Rune:", style='Cyber.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.search_rune_var = tk.StringVar(value="")
        ttk.Combobox(search_controls, textvariable=self.search_rune_var,
                    values=[""] + list(RUNES_EXTENDED.keys()), width=10).grid(
            row=0, column=1, padx=5, pady=3)
        
        ttk.Label(search_controls, text="Lieu:", style='Cyber.TLabel').grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.search_lieu_var = tk.StringVar(value="")
        ttk.Combobox(search_controls, textvariable=self.search_lieu_var,
                    values=[""] + list(LIEUX_EXTENDED.keys()), width=12).grid(
            row=0, column=3, padx=5, pady=3)
        
        ttk.Label(search_controls, text="Effet:", style='Cyber.TLabel').grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.search_effet_var = tk.StringVar(value="")
        ttk.Entry(search_controls, textvariable=self.search_effet_var,
                 width=25).grid(row=1, column=1, columnspan=3, padx=5, pady=3, sticky=tk.W)
        
        ttk.Label(search_controls, text="Danger min:", style='Cyber.TLabel').grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.search_danger_min_var = tk.IntVar(value=0)
        ttk.Spinbox(search_controls, from_=0, to=100,
                   textvariable=self.search_danger_min_var, width=5).grid(
            row=2, column=1, padx=5, pady=3, sticky=tk.W)
        
        ttk.Label(search_controls, text="Danger max:", style='Cyber.TLabel').grid(
            row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.search_danger_max_var = tk.IntVar(value=100)
        ttk.Spinbox(search_controls, from_=0, to=100,
                   textvariable=self.search_danger_max_var, width=5).grid(
            row=2, column=3, padx=5, pady=3, sticky=tk.W)
        
        # Boutons de recherche
        btn_search_frame = ttk.Frame(search_frame, style='Cyber.TFrame')
        btn_search_frame.pack(pady=10)
        
        ttk.Button(btn_search_frame, text="🔍 Rechercher",
                  command=self.search_codes, style='Cyber.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_search_frame, text="🔄 Réinitialiser",
                  command=self.reset_search, style='Cyber.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_search_frame, text="⭐ Favoris",
                  command=self.show_favorites, style='Cyber.TButton').pack(side=tk.LEFT, padx=5)
        
        # === MID: Résultats ===
        results_frame = ttk.Frame(mid_frame, style='Cyber.TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Liste des résultats
        list_frame = ttk.Frame(results_frame, style='Cyber.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(list_frame, text="Résultats:",
                 style='Cyber.TLabel').pack(anchor=tk.W, pady=5)
        
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox = tk.Listbox(list_frame, bg='#1a1a2e',
                                          fg=self.fg_color, font=('Courier', 9),
                                          yscrollcommand=list_scroll.set)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.results_listbox.yview)
        
        self.results_listbox.bind('<<ListboxSelect>>', self.show_code_details)
        
        # Détails du code sélectionné
        details_frame = ttk.Frame(results_frame, style='Cyber.TFrame')
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(details_frame, text="Détails:",
                 style='Cyber.TLabel').pack(anchor=tk.W, pady=5)
        
        self.code_details_display = scrolledtext.ScrolledText(
            details_frame, height=20, width=50,
            bg='#1a1a2e', fg=self.fg_color,
            font=('Courier New', 9), wrap=tk.WORD
        )
        self.code_details_display.pack(fill=tk.BOTH, expand=True)
        
        # Actions sur le code sélectionné
        action_frame = ttk.Frame(details_frame, style='Cyber.TFrame')
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(action_frame, text="📋 Copier",
                  command=self.copy_selected_code, style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="🔄 Charger",
                  command=self.load_selected_code, style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="🗑️ Supprimer",
                  command=self.delete_selected_code, style='Cyber.TButton').pack(side=tk.LEFT, padx=2)
    
    def create_status_bar(self):
        """Barre de statut"""
        status_frame = ttk.Frame(self.root, style='Cyber.TFrame', relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(
            value=f"⚡ Codes: {len(self.generator.history)} | Mutations: {len(self.generator.mutation_log)} | Chaînes: {len(self.generator.chains)}")
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                style='Cyber.TLabel', font=('Courier', 9))
        status_label.pack(side=tk.LEFT, padx=10, pady=2)
        
        # Horloge
        self.clock_var = tk.StringVar()
        clock_label = ttk.Label(status_frame, textvariable=self.clock_var,
                               style='Cyber.TLabel', font=('Courier', 9))
        clock_label.pack(side=tk.RIGHT, padx=10, pady=2)
        self.update_clock()
    
    def create_menu(self):
        """Création du menu"""
        menubar = tk.Menu(self.root, bg='#1a1a2e', fg=self.fg_color)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2e', fg=self.fg_color)
        menubar.add_cascade(label="📁 Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau Projet", command=self.new_project)
        file_menu.add_command(label="Ouvrir Projet...", command=self.open_project)
        file_menu.add_command(label="Sauvegarder Projet", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exporter Codes...", command=self.export_codes)
        file_menu.add_command(label="Exporter avec Analyses...", command=self.export_with_analysis)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Menu Outils
        tools_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2e', fg=self.fg_color)
        menubar.add_cascade(label="🔧 Outils", menu=tools_menu)
        tools_menu.add_command(label="Nouveau Template...", command=self.create_template_dialog)
        tools_menu.add_command(label="Gestionnaire Templates", command=self.manage_templates)
        tools_menu.add_separator()
        tools_menu.add_command(label="Statistiques Globales", command=self.show_global_stats)
        tools_menu.add_command(label="Arbre des Mutations", command=self.show_mutation_tree)
        tools_menu.add_command(label="Graphe de Relations", command=self.show_relations_graph)
        
        # Menu Visualisation
        viz_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2e', fg=self.fg_color)
        menubar.add_cascade(label="📊 Visualisation", menu=viz_menu)
        viz_menu.add_command(label="Distribution des Dangers", command=self.viz_danger_distribution)
        viz_menu.add_command(label="Runes les plus utilisées", command=self.viz_rune_usage)
        viz_menu.add_command(label="Timeline Génération", command=self.viz_timeline)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2e', fg=self.fg_color)
        menubar.add_cascade(label="❓ Aide", menu=help_menu)
        help_menu.add_command(label="Guide d'Utilisation", command=self.show_help)
        help_menu.add_command(label="À propos", command=self.show_about)
    
    # ============================================================================
    # MÉTHODES D'INTERFACE - GÉNÉRATION
    # ============================================================================
    
    def update_rune_info(self, event=None):
        """Met à jour les infos de la rune sélectionnée"""
        rune = self.rune_var.get()
        if rune in RUNES_EXTENDED:
            info = RUNES_EXTENDED[rune]
            self.rune_info_var.set(f"{info['nom']} - {info['élément']} (⚠{info['danger']})")
    
    def update_lieu_info(self, event=None):
        """Met à jour les infos du lieu sélectionné"""
        lieu = self.lieu_var.get()
        if lieu in LIEUX_EXTENDED:
            info = LIEUX_EXTENDED[lieu]
            self.lieu_info_var.set(f"{info['type']} - Pouvoir:{info['pouvoir']}")
    
    def update_danger_preview(self):
        """Aperçu du niveau de danger"""
        version = self.version_var.get()
        rune = self.rune_var.get()
        
        if rune in RUNES_EXTENDED:
            danger = RUNES_EXTENDED[rune]['danger'] * version
            color = self.warning_color if danger > 30 else self.success_color
            self.version_danger_var.set(f"⚠ {danger}")
            # Note: tkinter ne permet pas de changer la couleur facilement ici
    
    def generate_code(self):
        """Génère un code avec les paramètres"""
        template_index = next((i for i, t in enumerate(self.generator.templates["templates"])
                             if t["nom"] == self.template_var.get()), 0)
        
        self.current_code = self.generator.generate_code(
            rune=self.rune_var.get(),
            lieu=self.lieu_var.get(),
            effet=self.effet_var.get(),
            version=self.version_var.get(),
            template_index=template_index
        )
        
        self.display_code()
        self.update_status()
    
    def generate_random(self):
        """Génère un code aléatoire complet"""
        self.current_code = self.generator.generate_code()
        self.display_code()
        self.update_status()
    
    def generate_series(self):
        """Génère une série de 5 codes"""
        series = []
        for _ in range(5):
            code = self.generator.generate_code()
            series.append(code)
        
        # Affiche le dernier
        self.current_code = series[-1]
        self.display_code()
        
        messagebox.showinfo("Série Générée",
                           f"5 codes ont été générés et ajoutés à l'historique!")
        self.update_status()
    
    def display_code(self):
        """Affiche le code courant"""
        if not self.current_code:
            return
        
        self.code_display.delete(1.0, tk.END)
        
        code_text = f"""⚡ CODE FRACTUROSCRIPT ⚡

{self.current_code['code']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MÉTADONNÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hash: {self.current_code['hash']}
Template: {self.current_code['template']}
Timestamp: {self.current_code['timestamp'][:19]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARAMÈTRES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for key, value in self.current_code.get('params', {}).items():
            if key.startswith('rune'):
                rune_info = RUNES_EXTENDED.get(value, {})
                code_text += f"\n{key.capitalize()}: {value} ({rune_info.get('nom', '?')})"
            elif key.startswith('lieu'):
                code_text += f"\n{key.capitalize()}: {value}"
            else:
                code_text += f"\n{key.capitalize()}: {value}"
        
        code_text += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        code_text += f"\nCOMPLEXITÉ: {self.current_code.get('complexité', 1)}/5"
        code_text += f"\nDANGER: {self.current_code['danger']}/100"
        
        if self.current_code['danger'] > 50:
            code_text += " ⚠️  ATTENTION: NIVEAU ÉLEVÉ"
        
        if 'generation' in self.current_code:
            code_text += f"\nGÉNÉRATION: {self.current_code['generation']}"
        
        self.code_display.insert(tk.END, code_text)
    
    # ============================================================================
    # MÉTHODES D'INTERFACE - MUTATION
    # ============================================================================
    
    def update_intensity_label(self, value):
        """Met à jour le label d'intensité"""
        self.intensity_label.config(text=f"{float(value):.1f}x")
    
    def mutate_current(self, mutation_type):
        """Fait muter le code courant"""
        if not self.current_code:
            messagebox.showwarning("Aucun code",
                                  "Générez ou chargez un code d'abord!")
            return
        
        # Sauvegarde l'original pour comparaison
        original = copy.deepcopy(self.current_code)
        
        # Mutation
        intensity = self.intensity_var.get()
        self.current_code = self.generator.mutate_code(
            self.current_code,
            mutation_type=mutation_type,
            intensity=intensity
        )
        
        # Affichage comparatif
        self.display_mutation_comparison(original, self.current_code)
        self.display_code()
        self.update_status()
    
    def display_mutation_comparison(self, original, mutated):
        """Affiche la comparaison original/muté"""
        # Original
        self.original_display.delete(1.0, tk.END)
        orig_text = f"""CODE ORIGINAL
━━━━━━━━━━━━━━━━━━━━━━

{original['code']}

Hash: {original['hash']}
Danger: {original['danger']}
"""
        #K
        self.original_display.insert(tk.END, orig_text)

        # Muté
        self.mutated_display.delete(1.0, tk.END)
        mut_text = f"""CODE MUTÉ
━━━━━━━━━━━━━━━━━━━━━━
{mutated['code']}
Hash: {mutated['hash']}
Danger: {mutated['danger']}
Génération: {mutated.get('generation', 1)}
Mutations appliquées: {', '.join(mutated.get('mutations_applied', []))}
Type: {mutated.get('mutation_type', 'inconnu')}
"""
        self.mutated_display.insert(tk.END, mut_text)

        # Statistiques de mutation
        self.mutation_stats_display.delete(1.0, tk.END)
        stats = f"""📊 MUTATION RÉSUMÉ
• Différence de danger: {mutated['danger'] - original['danger']:+d}
• Stabilité estimée: {self.generator.calculate_stability(mutated)}/100
• Complexité: {mutated.get('complexité', 1)}
• Hash parent → enfant: {original['hash']} → {mutated['hash']}
• Timestamp: {mutated['timestamp'][:19]}
"""
        self.mutation_stats_display.insert(tk.END, stats)

    # ============================================================================
    # MÉTHODES D'INTERFACE – ANALYSE
    # ============================================================================
    def analyze_current_code(self):
        """Analyse le code actuel et affiche les résultats"""
        if not self.current_code:
            messagebox.showwarning("Aucun code", "Générez ou chargez un code d’abord !")
            return
        analysis = self.generator.analyze_code_extended(self.current_code)
        # Affichage principal
        self.analysis_main.delete(1.0, tk.END)
        main_text = f"""🔮 ANALYSE ONTOLOGIQUE
Stabilité: {analysis['stabilité']}/100
Compatibilité élémentaire: {analysis['compatibilité_élémentaire']['compatibilité']}%
Éléments dominants: {', '.join(analysis['compatibilité_élémentaire']['éléments'].keys())}
Résonance fractale: {analysis['résonance_fractale']['résonance']}
Flux temporel: {analysis['flux_temporel']['type']}
Portée géographique: {analysis['portée_géographique']} km
Durée estimée: {analysis['durée_estimée']} h
Score esthétique: {analysis['score_esthétique']}/100
"""
        self.analysis_main.insert(tk.END, main_text)

        # Détails techniques
        self.analysis_details.delete(1.0, tk.END)
        details_text = "📋 EFFETS SECONDAIRES\n• " + "\n• ".join(analysis['effets_secondaires'])
        details_text += "\n\n🔗 SYNERGIES"
        if analysis['synergies_potentielles']:
            for syn in analysis['synergies_potentielles']:
                details_text += f"\n• {syn['type']} avec {syn['avec']}: {syn['bonus']}"
        else:
            details_text += "\n• Aucune synergie détectée"
        details_text += "\n\n🛡️ CONTRE-MESURES"
        for cm in analysis['contre_mesures']:
            details_text += f"\n• {cm}"
        self.analysis_details.insert(tk.END, details_text)

        # Visualisation simplifiée
        self.draw_simple_viz(analysis)

    def draw_simple_viz(self, analysis):
        """Dessine une visualisation textuelle basique dans le canvas"""
        self.viz_canvas.delete("all")
        metrics = {
            "Danger": min(100, self.current_code['danger']),
            "Stabilité": analysis['stabilité'],
            "Complexité": self.current_code.get('complexité', 1) * 20,
            "Esthétique": analysis['score_esthétique']
        }
        y = 20
        width = self.viz_canvas.winfo_width() or 600
        for name, value in metrics.items():
            self.viz_canvas.create_text(10, y, text=name, anchor="w", fill="#00ffcc", font=('Courier', 10))
            bar_width = (value / 100) * (width - 50)
            color = "#ff3300" if name == "Danger" else "#ffff00" if name == "Stabilité" else "#00ffff" if name == "Complexité" else "#00ff00"
            self.viz_canvas.create_rectangle(100, y - 8, 100 + bar_width, y + 8, fill=color, outline="")
            self.viz_canvas.create_text(width - 30, y, text=f"{int(value)}", fill="#ffffff", font=('Courier', 9))
            y += 30

    # ============================================================================
    # MÉTHODES D'INTERFACE – CHAÎNES
    # ============================================================================
    def create_chain(self):
        """Crée une chaîne de codes"""
        chain = self.generator.create_chain(
            length=self.chain_length_var.get(),
            chain_type=self.chain_type_var.get()
        )
        self.current_chain = chain
        self.display_chain(chain)
        messagebox.showinfo("Chaîne créée", f"Chaîne {chain['id']} générée ({len(chain['codes'])} codes)")

    def display_chain(self, chain):
        """Affiche la chaîne dans l’interface"""
        self.chain_display.delete(1.0, tk.END)
        self.chain_display.insert(tk.END, f"⛓ CHAÎNE {chain['id']} ({chain['type']})\n")
        self.chain_display.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        for i, code in enumerate(chain['codes']):
            self.chain_display.insert(tk.END, f"[{i}] {code['code']}\n")
            self.chain_display.insert(tk.END, f"    → Hash: {code['hash']} | Danger: {code['danger']}\n")
        self.update_chains_listbox()

    def update_chains_listbox(self):
        """Met à jour la liste des chaînes sauvegardées"""
        self.chains_listbox.delete(0, tk.END)
        for c in self.generator.chains:
            self.chains_listbox.insert(tk.END, f"{c['id']} ({c['type']}, {c['length']} codes)")

    def load_chain(self, event=None):
        """Charge une chaîne sélectionnée"""
        selection = self.chains_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        self.current_chain = self.generator.chains[idx]
        self.display_chain(self.current_chain)

    def analyze_chain(self):
        messagebox.showinfo("Non implémenté", "L’analyse complète de chaîne sera disponible en v2.1.")

    def export_chain(self):
        if not self.current_chain:
            messagebox.showwarning("Aucune chaîne", "Sélectionnez une chaîne à exporter.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.current_chain, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Exporté", f"Chaîne exportée vers {filename}")

    def delete_chain(self):
        selection = self.chains_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        del self.generator.chains[idx]
        self.update_chains_listbox()
        self.chain_display.delete(1.0, tk.END)
        messagebox.showinfo("Supprimé", "Chaîne supprimée.")

    # ============================================================================
    # MÉTHODES D'INTERFACE – BIBLIOTHÈQUE & UTILITAIRES
    # ============================================================================
    def search_codes(self):
        """Recherche avancée dans l’historique"""
        criteria = {}
        if self.search_rune_var.get():
            criteria['rune'] = self.search_rune_var.get()
        if self.search_lieu_var.get():
            criteria['lieu'] = self.search_lieu_var.get()
        if self.search_effet_var.get():
            criteria['effet'] = self.search_effet_var.get()
        if self.search_danger_min_var.get() > 0:
            criteria['min_danger'] = self.search_danger_min_var.get()
        if self.search_danger_max_var.get() < 100:
            criteria['max_danger'] = self.search_danger_max_var.get()
        results = self.generator.search_codes(**criteria)
        self.results_listbox.delete(0, tk.END)
        self.search_results = results
        for code in results:
            self.results_listbox.insert(tk.END, f"{code['hash'][:8]} | {code['effet'][:40]}...")

    def show_code_details(self, event=None):
        """Affiche les détails d’un code sélectionné"""
        selection = self.results_listbox.curselection()
        if not selection:
            return
        code = self.search_results[selection[0]]
        self.code_details_display.delete(1.0, tk.END)
        details = json.dumps(code, indent=2, ensure_ascii=False)
        self.code_details_display.insert(tk.END, details)

    def copy_selected_code(self):
        selection = self.results_listbox.curselection()
        if selection:
            code = self.search_results[selection[0]]['code']
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            self.root.update()
            messagebox.showinfo("Copié", "Code copié dans le presse-papier.")

    def load_selected_code(self):
        selection = self.results_listbox.curselection()
        if selection:
            self.current_code = self.search_results[selection[0]]
            self.display_code()
            messagebox.showinfo("Chargé", "Code chargé dans l’onglet Génération.")

    def delete_selected_code(self):
        if messagebox.askyesno("Confirmer", "Supprimer ce code de l’historique ?"):
            selection = self.results_listbox.curselection()
            if selection:
                code_hash = self.search_results[selection[0]]['hash']
                self.generator.history = [c for c in self.generator.history if c['hash'] != code_hash]
                self.search_codes()
                self.update_status()
                messagebox.showinfo("Supprimé", "Code supprimé.")

    def reset_search(self):
        self.search_rune_var.set("")
        self.search_lieu_var.set("")
        self.search_effet_var.set("")
        self.search_danger_min_var.set(0)
        self.search_danger_max_var.set(100)
        self.results_listbox.delete(0, tk.END)
        self.code_details_display.delete(1.0, tk.END)

    def show_favorites(self):
        favs = [c for c in self.generator.history if c['hash'] in self.generator.favorites]
        self.results_listbox.delete(0, tk.END)
        self.search_results = favs
        for code in favs:
            self.results_listbox.insert(tk.END, f"⭐ {code['hash'][:8]} | {code['effet'][:40]}...")

    def copy_code(self):
        if self.current_code:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_code['code'])
            self.root.update()
            messagebox.showinfo("Copié", "Code copié.")

    def add_to_favorites(self):
        if self.current_code:
            if self.current_code['hash'] not in self.generator.favorites:
                self.generator.favorites.append(self.current_code['hash'])
                messagebox.showinfo("Favori", "Code ajouté aux favoris !")
            else:
                messagebox.showinfo("Favori", "Déjà en favori.")

    def add_tag_dialog(self):
        if self.current_code:
            tag = tk.simpledialog.askstring("Ajouter un tag", "Entrez un tag :")
            if tag:
                self.generator.add_tag(self.current_code['hash'], tag)
                messagebox.showinfo("Tag", f"Tag '{tag}' ajouté.")

    def save_single_code(self):
        if self.current_code:
            filename = filedialog.asksaveasfilename(defaultextension=".json")
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.current_code, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Sauvé", "Code sauvegardé.")

    def update_status(self):
        self.status_var.set(f"⚡ Codes: {len(self.generator.history)} | Mutations: {len(self.generator.mutation_log)} | Chaînes: {len(self.generator.chains)}")

    def update_clock(self):
        self.clock_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_clock)

    # ============================================================================
    # MÉTHODES DE MENU – NON IMPLEMENTÉES DANS CETTE ÉDITION
    # ============================================================================
    def new_project(self):
        if messagebox.askyesno("Nouveau projet", "Effacer tous les codes ?"):
            self.generator = FracturoScriptGeneratorExtended()
            self.current_code = None
            self.update_status()
            self.code_display.delete(1.0, tk.END)
            self.results_listbox.delete(0, tk.END)
            self.chains_listbox.delete(0, tk.END)

    def open_project(self):
        messagebox.showinfo("Limitation", "L’ouverture de projets est réservée à la version Ultimate.")

    def save_project(self):
        filename = filedialog.asksaveasfilename(defaultextension=".fss2")
        if filename:
            self.generator.export_advanced(filename, include_analysis=True)
            messagebox.showinfo("Sauvegardé", "Projet sauvegardé avec analyses.")

    def export_codes(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            self.generator.export_advanced(filename, include_analysis=False)

    def export_with_analysis(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            self.generator.export_advanced(filename, include_analysis=True)

    def create_template_dialog(self):
        messagebox.showinfo("Template", "Création de template personnalisé : disponible en v2.1.")

    def manage_templates(self):
        messagebox.showinfo("Templates", "Le gestionnaire avancé requiert FracturoScript Studio v3.")

    def show_global_stats(self):
        stats = dict(self.generator.statistics)
        text = "\n".join(f"{k}: {v}" for k, v in stats.items())
        messagebox.showinfo("Statistiques", text or "Aucune donnée.")

    def show_mutation_tree(self):
        messagebox.showinfo("Arbre", "Fonctionnalité graphique non implémentée.")

    def show_relations_graph(self):
        messagebox.showinfo("Graphe", "Utilisez l’export JSON + outils externes pour visualiser les relations.")

    def viz_danger_distribution(self):
        messagebox.showinfo("Visualisation", "Utilisez l’export JSON pour tracer l’histogramme.")

    def viz_rune_usage(self):
        self.viz_timeline()

    def viz_timeline(self):
        messagebox.showinfo("Timeline", "Disponible dans la version Chronomancienne.")

    def show_help(self):
        messagebox.showinfo("Aide", "Consultez le Grimoire FracturoScript v2.0 pour la documentation complète.")

    def show_about(self):
        messagebox.showinfo("À propos", "FracturoScript Studio v2.0 – Extended Edition\n© 2025 – Réalité Fractale Inc.")

# ============================================================================
# LANCEMENT DE L'APPLICATION
# ============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = FracturoScriptAppExtended(root)
    root.mainloop()