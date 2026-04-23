#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plugin DreamLogic - Logique onirique et associations surréalistes
"""

import random

class DreamLogicPlugin:
    """Injecte une logique onirique dans la génération"""
    
    def __init__(self):
        self.name = "DreamLogic"
        self.version = "1.0"
        self.dream_associations = self._load_dream_associations()
    
    def _load_dream_associations(self):
        """Charge les associations oniriques"""
        return {
            "stone": ["whispers", "memories", "lightness"],
            "water": ["solidity", "mathematics", "silence"],
            "light": ["weight", "taste", "echoes"],
            "data": ["breathing", "growth", "erosion"],
            "memory": ["texture", "color", "temperature"]
        }
    
    def process_analysis(self, analysis, config):
        """Traite l'analyse pour injecter de la logique onirique"""
        if 'dream' not in analysis:
            analysis['dream'] = {}
        
        # Associations oniriques basées sur les éléments trouvés
        dream_elements = []
        for location in analysis['contexts'].get('locations', []):
            loc_name = location['location'].lower()
            for key, associations in self.dream_associations.items():
                if key in loc_name:
                    dream_elements.extend(associations)
        
        # Limiter et ajouter
        analysis['dream']['associations'] = list(set(dream_elements))[:5]
        analysis['dream']['logic_level'] = random.randint(1, 10)
        analysis['dream']['surreal_factor'] = analysis['metrics']['overall_weirdness'] / 10
        
        return analysis
    
    def enhance_prompt(self, elements, analysis):
        """Améliore le prompt avec des éléments oniriques"""
        if analysis['dream']['logic_level'] > 5:
            elements.extend(analysis['dream']['associations'])
            elements.append("dream logic composition")
            elements.append("surreal association field")
        
        return elements