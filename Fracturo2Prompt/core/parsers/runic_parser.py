#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parseur avancé des runes et symboles
"""

import re

class RunicParser:
    """Parseur des runes étendu avec combinaisons"""
    
    def __init__(self, config):
        self.config = config
        self.combinations = self._load_combinations()
    
    def _load_combinations(self):
        """Charge les combinaisons runiques avancées"""
        return {
            "Ansuz+Algiz": {
                "fr": "invocation protectrice, voix des ancêtres",
                "en": "protective invocation, ancestral voices",
                "power": 5
            },
            "Dagaz+Algiz": {
                "fr": "aube protectrice, renaissance gardée", 
                "en": "protective dawn, guarded rebirth",
                "power": 6
            },
            "Ansuz+Dagaz": {
                "fr": "révélation de l'aube, parole fractale",
                "en": "dawn revelation, fractal speech", 
                "power": 7
            },
            "Ansuz+Algiz+Dagaz": {
                "fr": "trinité runique, complétude mnémonique",
                "en": "runic trinity, mnemonic completeness",
                "power": 10
            }
        }
    
    def parse(self, text):
        """Analyse approfondie des runes dans le texte"""
        findings = {
            'runes': [],
            'combinations': [],
            'effects': [],
            'power_level': 0,
            'resonances': []
        }
        
        # Détection runes simples
        all_runes = self._flatten_runes()
        
        for rune, data in all_runes.items():
            matches = list(re.finditer(r'\b' + re.escape(rune) + r'\b', text, re.IGNORECASE))
            if matches:
                effect = data.get('effect', {}).get('fr', 'effet inconnu')
                findings['runes'].append({
                    'rune': rune,
                    'effect': effect,
                    'positions': [m.start() for m in matches],
                    'count': len(matches),
                    'power': data.get('power', 1)
                })
                findings['effects'].append(effect)
                findings['power_level'] += data.get('power', 1) * len(matches)
        
        # Détection combinaisons runiques
        for combo, effect_data in self.combinations.items():
            runes_in_combo = combo.split('+')
            if all(any(rune == found_rune['rune'] for found_rune in findings['runes']) for rune in runes_in_combo):
                findings['combinations'].append({
                    'combo': combo,
                    'effect': effect_data.get('fr', 'effet de combinaison'),
                    'synergy': len(runes_in_combo) * 2,
                    'power': effect_data.get('power', 0)
                })
                findings['power_level'] += effect_data.get('power', 0)
                findings['effects'].append(effect_data.get('fr', ''))
        
        # Résonances spéciales
        if findings['power_level'] > 15:
            findings['resonances'].append("résonance mnémonique majeure")
        if len(findings['combinations']) > 0:
            findings['resonances'].append("harmonie runique")
        
        return findings
    
    def _flatten_runes(self):
        """Aplatit la structure des runes pour analyse"""
        flat_runes = {}
        for category, runes in self.config.get('runes', {}).items():
            for rune, data in runes.items():
                flat_runes[rune] = data
        return flat_runes