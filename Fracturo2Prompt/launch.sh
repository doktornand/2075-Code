#!/bin/bash
cd "$(dirname "$0")"
echo "📁 Répertoire: $(pwd)"
echo "🚀 Lancement de Fracturo Mk.II..."
python3 fracturo2prompt_mk2c.py "$@"
