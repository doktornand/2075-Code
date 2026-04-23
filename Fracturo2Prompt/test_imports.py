#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
print(f"📁 Repertoire racine: {ROOT_DIR}")

# Tester tous les imports
try:
    sys.path.insert(0, str(ROOT_DIR / "core"))
    sys.path.insert(0, str(ROOT_DIR / "plugins"))
    
    from core.engine import FracturoEngine
    print("✅ core.engine importé")
    
    from core.parsers.runic_parser import RunicParser
    print("✅ core.parsers.runic_parser importé")
    
    from core.generators.prompt_generator import PromptGenerator
    print("✅ core.generators.prompt_generator importé")
    
    print("🎉 Tous les imports fonctionnent !")
    
except ImportError as e:
    print(f"❌ Erreur: {e}")
    
    # Lister les fichiers disponibles
    print("\n📂 Fichiers disponibles:")
    for py_file in ROOT_DIR.rglob("*.py"):
        rel_path = py_file.relative_to(ROOT_DIR)
        print(f"  {rel_path}")
