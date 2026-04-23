#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FracturoScript Mk.II → Machine Mnémétique Fractale
Version 2.Ω — Caen-Profonde, 2077
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Configuration des chemins avant tout import
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR / "core"))
sys.path.insert(0, str(ROOT_DIR / "plugins"))
sys.path.insert(0, str(ROOT_DIR))

# Import du moteur principal
try:
    from core.engine import FracturoEngine
    print("✅ Moteur Fracturo chargé avec succès")
except ImportError as e:
    print(f"❌ Erreur import du moteur: {e}")
    print("💡 Structure des fichiers:")
    for root, dirs, files in os.walk(ROOT_DIR):
        level = root.replace(str(ROOT_DIR), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f'{subindent}{file}')
    sys.exit(1)

def parse_inject_args(kv_list):
    """Convertit ['lieu=raz', 'intensite=21'] en dict"""
    d = {}
    for kv in kv_list:
        if '=' not in kv:
            continue
        k, v = kv.split('=', 1)
        d[k] = v
    return d

def main():
    parser = argparse.ArgumentParser(
        description="FracturoScript Mk.II — Machine Mnémétique Fractale",
        epilog="Ya Hu… raz••• Alou… Ω"
    )
    
    # Arguments de base étendus
    parser.add_argument("-i", "--input", help="Fichier FracturoScript source")
    parser.add_argument("-c", "--config", default="config", help="Dossier de config JSON")
    parser.add_argument("-o", "--output", 
                       choices=["prompt", "json", "manifest", "poetry", "ritual"],
                       default="prompt", help="Format de sortie étendu")
    parser.add_argument("-l", "--lang", choices=["fr", "en"], default="fr", 
                       help="Langue du prompt")
    
    # Nouveaux paramètres artistiques
    parser.add_argument("--archetype", help="Archétype narratif (ex: wanderer, oracle, machine)")
    parser.add_argument("--material", help="Matériau dominant (ex: granite, data, flesh, light)")
    parser.add_argument("--emotion", help="Émotion cible (ex: melancholy, awe, dread, euphoria)")
    parser.add_argument("--temporal-era", help="Ère temporelle (ex: paleolithic, cyber, post-omega)")
    
    # Paramètres techniques avancés
    parser.add_argument("--glitch", type=int, choices=[0, 1, 2, 3, 4], default=1, help="Niveau de corruption")
    parser.add_argument("--recursion-depth", type=int, default=3, help="Profondeur de récursion")
    parser.add_argument("--style", choices=["standard", "poetic", "technical", "ritual"], 
                       default="standard", help="Style de sortie")
    
    # Extensions et plugins
    parser.add_argument("--plugin", action="append", default=[], help="Plugins à charger")
    parser.add_argument("--inject", action="append", default=[], help="Surcharge clé=valeur (ex: lieu=raz)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()

    # Initialisation du moteur
    try:
        config_path = ROOT_DIR / args.config
        engine = FracturoEngine(config_path)
        
        if args.verbose:
            print("🚀 Moteur Fracturo Mk.II initialisé")
            caps = engine.get_capabilities()
            print(f"   Parseurs: {', '.join(caps['parsers'])}")
            print(f"   Générateurs: {', '.join(caps['generators'])}")
            print(f"   Répertoire config: {config_path}")
    except Exception as e:
        print(f"❌ Erreur initialisation: {e}")
        sys.exit(1)
    
    # Chargement des plugins
    for plugin_name in args.plugin:
        if args.verbose:
            print(f"🔌 Chargement du plugin: {plugin_name}")
        engine.load_plugin(plugin_name)
    
    # Lecture de l'entrée
    if args.input:
        try:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"❌ Fichier introuvable: {args.input}")
                sys.exit(1)
                
            with open(input_path, 'r', encoding='utf-8') as f:
                source = f.read()
                
            if args.verbose:
                print(f"📖 Fichier lu: {args.input} ({len(source)} caractères)")
        except Exception as e:
            print(f"❌ Erreur lecture {args.input}: {e}")
            sys.exit(1)
    else:
        print("📋 Collapse your reality here (Ctrl+D to end):", file=sys.stderr)
        source = sys.stdin.read()
    
    # Options étendues
    options = {
        'lang': args.lang,
        'glitch': args.glitch,
        'archetype': args.archetype,
        'material': args.material, 
        'emotion': args.emotion,
        'temporal_era': args.temporal_era,
        'recursion_depth': args.recursion_depth,
        'style': args.style,
        'verbose': args.verbose
    }
    
    # Traitement des injections
    overrides = parse_inject_args(args.inject)
    options.update(overrides)
    
    try:
        # Analyse
        if args.verbose:
            print("🔍 Analyse du FracturoScript en cours...")
            
        analysis = engine.analyze(source, options)
        
        if args.verbose:
            print(f"   Runes détectées: {len(analysis['runes'].get('runes', []))}")
            print(f"   Lieux trouvés: {len(analysis['contexts'].get('locations', []))}")
            print(f"   Niveau quantique: {analysis['quantum'].get('superposition_level', 0)}")
            print(f"   Stabilité réalité: {analysis['metrics'].get('reality_stability', 100)}%")
        
        # Génération
        output = engine.generate_output(analysis, args.output, options)
        
        # Sortie
        if args.output == "json":
            result = {
                "analysis": analysis,
                "output": output,
                "metadata": {
                    "engine": "Fracturo Mk.II",
                    "timestamp": datetime.now().isoformat(),
                    "reality_stability": analysis['metrics'].get('reality_stability', 100),
                    "plugins_loaded": analysis.get('plugins', [])
                }
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(output)
            
    except Exception as e:
        print(f"❌ Erreur traitement: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
