#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parseur des états quantiques et réalités superposées
"""

import re
import random

class QuantumParser:
    """Parseur des phénomènes quantiques et effondrements de réalité"""
    
    def parse(self, text, config):
        """Analyse les états quantiques du texte"""
        states = []
        collapses = []
        superpositions = []
        
        # États quantiques depuis la config
        quantum_config = config.get('quantum', {})
        for state, data in quantum_config.get('states', {}).items():
            indicators = data.get('indicators', [])
            state_indicators_found = []
            
            for indicator in indicators:
                if indicator.lower() in text.lower():
                    state_indicators_found.append(indicator)
            
            if state_indicators_found:
                states.append({
                    'state': state,
                    'description': data.get('description', ''),
                    'indicators_found': state_indicators_found,
                    'intensity': len(state_indicators_found)
                })
        
        # Effondrements de réalité
        collapse_triggers = [
            ('omega', r'[OΩω]-*mega', 3, "effondrement oméga"),
            ('recursion', r'recurs\w+', 2, "boucle récursive"),
            ('cascade', r'cascade\w*', 2, "cascade de réalité"),
            ('superposition', r'superpos\w+', 4, "superposition quantique"),
            ('entanglement', r'entangl\w+', 3, "intrication mnémonique"),
            ('observer', r'observ\w+', 2, "effet observateur"),
            ('collapse', r'collaps\w+', 5, "effondrement de fonction d'onde")
        ]
        
        for collapse_type, pattern, intensity, description in collapse_triggers:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                collapses.append({
                    'type': collapse_type,
                    'intensity': intensity * len(matches),
                    'triggers': matches,
                    'description': description,
                    'count': len(matches)
                })
        
        # Détection de superpositions
        superposition_indicators = [
            "à la fois", "simultanément", "multiple", "parallele",
            "double", "dual", "twinned", "mirror"
        ]
        
        for indicator in superposition_indicators:
            if indicator in text.lower():
                count = text.lower().count(indicator)
                superpositions.append({
                    'indicator': indicator,
                    'count': count,
                    'layers': count + 1
                })
        
        # Calcul du niveau de superposition
        superposition_level = len(states) + len(superpositions)
        quantum_instability = sum(collapse['intensity'] for collapse in collapses)
        
        return {
            'states': states,
            'collapses': collapses,
            'superpositions': superpositions,
            'superposition_level': superposition_level,
            'quantum_instability': quantum_instability,
            'reality_integrity': max(0, 100 - quantum_instability),
            'is_coherent': quantum_instability < 20
        }