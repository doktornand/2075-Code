#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gestion des chemins pour Fracturo Mk.II
"""

import os
import sys
from pathlib import Path

# Déterminer le répertoire racine du projet
ROOT_DIR = Path(__file__).parent

# Ajouter les chemins nécessaires à sys.path
CORE_DIR = ROOT_DIR / "core"
PLUGINS_DIR = ROOT_DIR / "plugins"
CONFIG_DIR = ROOT_DIR / "config"

# Ajouter aux chemins de recherche Python
sys.path.insert(0, str(CORE_DIR))
sys.path.insert(0, str(PLUGINS_DIR))
sys.path.insert(0, str(ROOT_DIR))

def get_config_path(filename):
    """Retourne le chemin complet d'un fichier de configuration"""
    return CONFIG_DIR / filename

def ensure_paths():
    """Vérifie que tous les chemins nécessaires existent"""
    required_dirs = [CORE_DIR, PLUGINS_DIR, CONFIG_DIR]
    required_subdirs = [CORE_DIR / "parsers", CORE_DIR / "generators"]
    
    all_dirs = required_dirs + required_subdirs
    
    for directory in all_dirs:
        if not directory.exists():
            print(f"⚠️  Création du répertoire: {directory}")
            directory.mkdir(parents=True, exist_ok=True)
    
    return True
