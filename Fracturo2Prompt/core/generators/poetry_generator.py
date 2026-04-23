#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur de poésie procédurale
"""

import random

class PoetryGenerator:
    """Générateur de poésie mnémétique"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Charge les templates poétiques"""
        return {
            'minimal': [
                ["{line1}", "{line2}", "{line3}"],
                ["{element1}", "{element2} et {element3}"],
                ["dans le {context}", "{emotion}", "{archetype} se souvient"]
            ],
            'lyrical': [
                ["Ô {archetype} des {context}", "tes {element1} sont {quality}"],
                ["{emotion} comme les {element2}", "dans le creux du {material}"],
                ["{rune_effect}", "{temporal_era} se déchire"],
                ["raz••• {silence}"]
            ],
            'epic': [
                ["QUAND {archetype_upper} RENCONTRE {context_upper}"],
                ["{element1_upper} MÉLANGE À {element2_upper}"],
                ["{temporal_era_upper} TREMBLE SOUS {emotion_upper}"],
                ["{rune_effect_upper}"],
                ["OMEGA {quantum_state}"]
            ]
        }
    
    def generate(self, analysis, config, options):
        """Génère un poème procédural"""
        lang = options.get('lang', 'fr')
        
        # Sélection du template basé sur l'analyse
        power_level = analysis['runes'].get('power_level', 0)
        if power_level > 10:
            template_type = 'epic'
        elif power_level > 5:
            template_type = 'lyrical'
        else:
            template_type = 'minimal'
        
        templates = self.templates[template_type]
        poem_lines = []
        
        # Données pour remplissage
        fill_data = self._prepare_fill_data(analysis, config, lang)
        
        for template_stanza in templates[:3]:  # Maximum 3 strophes
            stanza = []
            for template_line in template_stanza:
                line = self._fill_template(template_line, fill_data)
                stanza.append(line)
            poem_lines.extend(stanza)
            poem_lines.append("")  # Ligne vide entre strophes
        
        return "\n".join(poem_lines).strip()
    
    def _prepare_fill_data(self, analysis, config, lang):
        """Prépare les données pour le remplissage des templates"""
        data = {}
        
        # Archétype
        archetype = analysis['archetypal'].get('dominant_archetype', 'wanderer')
        data['archetype'] = archetype
        data['archetype_upper'] = archetype.upper()
        
        # Contexte
        contexts = analysis['contexts'].get('locations', [])
        data['context'] = contexts[0]['location'] if contexts else 'vide'
        data['context_upper'] = data['context'].upper()
        
        # Éléments
        elements = analysis['runes'].get('effects', [])[:3]
        for i, element in enumerate(elements, 1):
            data[f'element{i}'] = element
            data[f'element{i}_upper'] = element.upper()
        
        # Émotion
        emotion = analysis['emotional'].get('primary_emotion', 'neutral')
        data['emotion'] = emotion
        data['emotion_upper'] = emotion.upper()
        
        # Matériau
        data['material'] = 'pierre'  # Par défaut
        
        # Ère temporelle
        temporal_era = analysis['temporal'].get('dominant_era', 'present')
        data['temporal_era'] = temporal_era
        data['temporal_era_upper'] = temporal_era.upper()
        
        # Effet de rune
        rune_effects = analysis['runes'].get('effects', [])
        data['rune_effect'] = rune_effects[0] if rune_effects else "silence runique"
        data['rune_effect_upper'] = data['rune_effect'].upper()
        
        # Silence
        data['silence'] = config['mantras']['silence'].get(lang, 'silence primordial')
        
        # État quantique
        quantum_states = analysis['quantum'].get('states', [])
        data['quantum_state'] = quantum_states[0]['state'] if quantum_states else "stabilité"
        
        # Qualité
        data['quality'] = random.choice(['ancien', 'fractal', 'mnémonique', 'temporel'])
        
        return data
    
    def _fill_template(self, template, data):
        """Remplit un template avec les données"""
        try:
            return template.format(**data)
        except KeyError:
            return template