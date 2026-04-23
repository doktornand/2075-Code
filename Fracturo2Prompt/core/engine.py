#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moteur principal Fracturo Mk.II
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Import du gestionnaire de chemins
sys.path.append(str(Path(__file__).parent.parent))
from paths import get_config_path, ensure_paths

# Assurer que les chemins existent
ensure_paths()

# Import absolu des parseurs
from parsers.runic_parser import RunicParser
from parsers.temporal_parser import TemporalParser
from parsers.quantum_parser import QuantumParser

# Import absolu des générateurs
from generators.prompt_generator import PromptGenerator
from generators.poetry_generator import PoetryGenerator
from generators.manifest_generator import ManifestGenerator

class FracturoEngine:
    """Moteur mnémétique principal étendu"""
    
    def __init__(self, config_dir="./config"):
        self.config_dir = Path(config_dir)
        self.config = self._load_extended_config()
        self.parsers = self._initialize_parsers()
        self.generators = self._initialize_generators()
        self.plugins = []
    
    def _load_extended_config(self):
        """Charge toute la configuration étendue"""
        config_files = {
            'runes': 'runes.json',
            'contexts': 'contents.json',
            'glitches': 'glitches.json', 
            'mantras': 'mantras.json',
            'defaults': 'defaults.json',
            'archetypes': 'archetypes.json',
            'materials': 'materials.json',
            'emotions': 'emotions.json',
            'temporal': 'temporal.json',
            'quantum': 'quantum.json',
            'biomes': 'biomes.json'
        }
        
        config = {}
        for key, filename in config_files.items():
            path = self.config_dir / filename
            if not path.exists():
                # Essayer avec le chemin absolu
                path = get_config_path(filename)
            
            if path.exists():
                config[key] = self._load_json_file(path)
            else:
                print(f"⚠️  Fichier config manquant: {path}")
                config[key] = {}
        
        return config
    
    def _load_json_file(self, path):
        """Charge un fichier JSON avec gestion d'erreur"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur chargement {path}: {e}")
            return {}
    
    def _initialize_parsers(self):
        """Initialise tous les parseurs spécialisés"""
        return {
            'runic': RunicParser(self.config),
            'temporal': TemporalParser(),
            'quantum': QuantumParser()
        }
    
    def _initialize_generators(self):
        """Initialise tous les générateurs"""
        return {
            'prompt': PromptGenerator(),
            'poetry': PoetryGenerator(), 
            'manifest': ManifestGenerator()
        }
    
    def load_plugin(self, plugin_name):
        """Charge un plugin dynamiquement"""
        try:
            # Mécanisme simplifié de chargement
            if plugin_name == "dreamlogic":
                from dreamlogic import DreamLogicPlugin
                plugin = DreamLogicPlugin()
            elif plugin_name == "tidal_recursion":
                from tidal_recursion import TidalRecursionPlugin
                plugin = TidalRecursionPlugin()
            elif plugin_name == "reality_cascade":
                from reality_cascade import RealityCascadePlugin
                plugin = RealityCascadePlugin()
            else:
                print(f"❌ Plugin inconnu: {plugin_name}")
                return False
            
            self.plugins.append(plugin)
            print(f"🔌 Plugin chargé: {plugin.name} v{plugin.version}")
            return True
            
        except ImportError as e:
            print(f"❌ Erreur chargement plugin {plugin_name}: {e}")
            return False
    
    def analyze(self, text, options=None):
        """Analyse approfondie du texte FracturoScript"""
        if options is None:
            options = {}
        
        analysis = {}
        
        # Analyses parallèles par tous les parseurs
        analysis['runes'] = self.parsers['runic'].parse(text)
        analysis['temporal'] = self.parsers['temporal'].parse(text, self.config)
        analysis['quantum'] = self.parsers['quantum'].parse(text, self.config)
        analysis['contexts'] = self._analyze_contexts(text)
        analysis['emotional'] = self._analyze_emotional(text)
        analysis['archetypal'] = self._analyze_archetypal(text)
        
        # Métriques avancées
        analysis['metrics'] = self._calculate_metrics(analysis)
        analysis['plugins'] = [p.name for p in self.plugins]
        
        return analysis
    
    def _analyze_contexts(self, text):
        """Analyse des contextes et lieux"""
        contexts_found = []
        themes = []
        
        for lieu, data in self.config['contexts'].items():
            if lieu.lower() in text.lower():
                lang = 'fr'  # Par défaut
                desc = data.get('description', {}).get(lang, '')
                contexts_found.append({
                    'location': lieu,
                    'description': desc,
                    'intensity': text.lower().count(lieu.lower())
                })
                # Extraction des thèmes
                if 'theme' in data:
                    themes.extend(data['theme'])
        
        # Détection raz•••
        raz_pattern = r'raz\s*•{3,}'
        raz_matches = re.findall(raz_pattern, text, re.IGNORECASE)
        
        return {
            'locations': contexts_found,
            'themes': list(set(themes)),
            'raz_occurrences': len(raz_matches),
            'silence_detected': len(raz_matches) > 0
        }
    
    def _analyze_emotional(self, text):
        """Analyse de la charge émotionnelle"""
        emotions_found = []
        intensity = 0
        
        for emotion, data in self.config['emotions'].items():
            indicators = data.get('indicators', [])
            for indicator in indicators:
                if indicator in text.lower():
                    emotions_found.append({
                        'emotion': emotion,
                        'cue': indicator,
                        'data': data
                    })
                    intensity += 1
                    break
        
        return {
            'emotions': emotions_found,
            'intensity': intensity,
            'primary_emotion': emotions_found[0]['emotion'] if emotions_found else 'neutral'
        }
    
    def _analyze_archetypal(self, text):
        """Analyse des archétypes présents"""
        archetypes_found = []
        
        for archetype, data in self.config['archetypes'].items():
            indicators = data.get('indicators', [])
            for indicator in indicators:
                if indicator in text.lower():
                    archetypes_found.append({
                        'archetype': archetype,
                        'data': data
                    })
                    break
        
        return {
            'archetypes': archetypes_found,
            'dominant_archetype': archetypes_found[0]['archetype'] if archetypes_found else 'wanderer'
        }
    
    def _calculate_metrics(self, analysis):
        """Calcule des métriques avancées"""
        power_level = analysis['runes'].get('power_level', 0)
        quantum_level = analysis['quantum'].get('superposition_level', 0)
        emotional_intensity = analysis['emotional'].get('intensity', 0)
        
        stability = max(0, 100 - (power_level * 3 + quantum_level * 10 + emotional_intensity * 5))
        
        return {
            'reality_stability': stability,
            'mnemonic_power': power_level,
            'temporal_coherence': 80 if not analysis['temporal']['is_anachronic'] else 30,
            'quantum_entanglement': quantum_level * 15,
            'overall_weirdness': (power_level + quantum_level + emotional_intensity) * 8
        }
    
    def generate_output(self, analysis, output_format, options=None):
        """Génère la sortie dans le format demandé"""
        if options is None:
            options = {}
        
        if output_format in self.generators:
            return self.generators[output_format].generate(analysis, self.config, options)
        else:
            # Fallback vers le prompt standard
            return self.generators['prompt'].generate(analysis, self.config, options)
    
    def get_capabilities(self):
        """Retourne les capacités du moteur"""
        return {
            'parsers': list(self.parsers.keys()),
            'generators': list(self.generators.keys()),
            'plugins': [p.name for p in self.plugins],
            'config_files': [f for f in self.config_dir.glob('*.json')]
        }
