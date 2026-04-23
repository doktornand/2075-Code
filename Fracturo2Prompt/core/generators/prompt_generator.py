#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur de prompts avancés
"""

import random
from datetime import datetime

class PromptGenerator:
    """Générateur de prompts mnémétiques étendus"""
    
    def generate(self, analysis, config, options):
        """Génère un prompt complet"""
        elements = []
        lang = options.get('lang', 'fr')
        
        # Éléments de base des runes
        rune_effects = analysis['runes'].get('effects', [])
        elements.extend(rune_effects)
        
        # Contextes et lieux
        for location in analysis['contexts'].get('locations', []):
            elements.append(location['description'])
        
        # Éléments temporels
        for era in analysis['temporal'].get('eras', []):
            elements.extend(era.get('aesthetic', []))
        
        # Archétypes narratifs
        archetype_name = options.get('archetype')
        if archetype_name:
            archetype_data = config['archetypes'].get(archetype_name, {})
            if archetype_data:
                archetype_elements = archetype_data.get('elements', [])
                if isinstance(archetype_elements, list):
                    elements.extend(archetype_elements)
                else:
                    elements.append(archetype_elements)
        
        # Matériaux et textures
        material_name = options.get('material')
        if material_name:
            material_data = config['materials'].get(material_name, {})
            if material_data:
                elements.append(material_data.get('texture', ''))
                elements.append(material_data.get('quality', ''))
        
        # Émotions et atmosphères
        emotion_name = options.get('emotion')
        if emotion_name:
            emotion_data = config['emotions'].get(emotion_name, {})
            if emotion_data:
                visual_cues = emotion_data.get('visual_cues', [])
                if isinstance(visual_cues, list):
                    elements.extend(visual_cues)
                else:
                    elements.append(visual_cues)
                elements.append(emotion_data.get('lighting', ''))
        
        # Glitch selon niveau
        glitch_level = options.get('glitch', 1)
        glitch_effects = config['glitches'].get(str(glitch_level), [])
        elements.extend(glitch_effects)
        
        # Mantras de base
        base_mantras = config['mantras']['base'].get(lang, [])
        if isinstance(base_mantras, list):
            elements.extend(base_mantras)
        else:
            elements.append(base_mantras)
        
        # Éléments quantiques avancés
        if analysis['quantum']['superposition_level'] > 2:
            elements.append("quantum superposition reality layers")
            elements.append("multiple timelines visible simultaneously")
        
        if analysis['quantum']['quantum_instability'] > 15:
            elements.append("reality glitching at the edges")
            elements.append("temporal fragments floating in void")
        
        # Silence sacré détecté
        if analysis['contexts']['silence_detected']:
            silence_mantra = config['mantras']['silence'].get(lang, '')
            elements.append(silence_mantra)
        
        # Nettoyage et optimisation
        elements = self._clean_elements(elements)
        elements = self._apply_style(elements, options.get('style', 'standard'))
        
        return self._finalize_prompt(elements, analysis, options)
    
    def _clean_elements(self, elements):
        """Nettoie et déduplique les éléments"""
        # Retirer éléments vides
        elements = [e for e in elements if e and str(e).strip()]
        # Déduplication en préservant l'ordre
        seen = set()
        unique_elements = []
        for e in elements:
            if e not in seen:
                seen.add(e)
                unique_elements.append(e)
        return unique_elements
    
    def _apply_style(self, elements, style):
        """Applique un style spécifique à la structure"""
        if style == 'poetic':
            # Regroupe par paires poétiques
            poetic_elements = []
            for i in range(0, len(elements), 2):
                pair = elements[i:i+2]
                poetic_elements.append(", ".join(pair))
            return poetic_elements
        elif style == 'technical':
            # Ajoute des spécifications techniques
            tech_elements = []
            for element in elements:
                tech_elements.append(f"[{element}]")
            return tech_elements
        elif style == 'ritual':
            # Structure rituelle
            ritual_elements = []
            for i, element in enumerate(elements):
                prefix = "• " if i % 2 == 0 else "∘ "
                ritual_elements.append(f"{prefix}{element.upper()}")
            return ritual_elements
        else:
            return elements
    
    def _finalize_prompt(self, elements, analysis, options):
        """Finalise le format du prompt"""
        style = options.get('style', 'standard')
        
        if style == 'poetic':
            return ".\n".join(elements) + "."
        elif style == 'ritual':
            header = "** INVOCATION MNÉMOTIQUE **\n"
            header += "Par les runes et les marées,\n"
            body = "\n".join(elements)
            footer = f"\n** OMEGA {datetime.now().strftime('%H:%M:%S')} **"
            return header + body + footer
        elif style == 'technical':
            return " ".join(elements)
        else:
            return ", ".join(elements)