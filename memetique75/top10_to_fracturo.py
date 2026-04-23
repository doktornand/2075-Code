#!/usr/bin/env python3
# top10_to_fracturo_fixed.py
# Version corrigée : ne plante pas si la ligne ne contient pas "Génération"

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
import random

class MiniMeme:
    def __init__(self, id_: str, symbole: str, nom: str, fitness: float):
        self.id = id_
        self.symbole = symbole
        self.nom = nom
        self.fitness = fitness
        self.fracturo_glyph = symbole

def parse_log_for_top10(filepath: Path) -> list:
    memes = []
    current_gen = None  # commence à None, pas 0

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Vérifie si c'est une ligne de génération
            gen_match = re.match(r'^Génération\s+(\d+)', line)
            if gen_match:
                current_gen = int(gen_match.group(1))
                continue

            # Si ce n’est pas une génération, c’est potentiellement un mème
            if current_gen is None:
                # On n’a pas encore vu de "Génération", donc on ignore
                continue

            # On essaie de parser le mème
            match = re.match(r'^([^\s])\s+([^(]+)\s+\(f:([\d.]+)\)', line)
            if not match:
                continue  # ignore les lignes non conformes

            symbole = match.group(1)
            nom_full = match.group(2).strip()
            fitness = float(match.group(3))

            # Extraction de l'ID (premier mot du nom)
            meme_id = nom_full.split(' ', 1)[0] if ' ' in nom_full else nom_full

            memes.append(MiniMeme(meme_id, symbole, nom_full, fitness))

    # Trier par fitness décroissante et prendre top 10
    top10 = sorted(memes, key=lambda m: m.fitness, reverse=True)[:10]
    return top10

def generate_fracturo_script(meme: MiniMeme, emotion: str = "oubli") -> str:
    BASE_LINES = [
        "Tu te souviens du feu qui ne brûle pas.",
        "Ils ont effacé ton passé, mais pas tes mains.",
        "Le silence parle dans la langue que tu as oubliée.",
        "La main rouge trace ce que la bouche ne peut dire.",
        "Le sel de tes larmes conserve la mémoire du monde."
    ]
    glyph = meme.fracturo_glyph
    base = random.choice(BASE_LINES)
    return f"""// FracturoScript — Caen-Profonde
{base}
{glyph * 12}
// Émotion : {emotion}
// Résonance : {meme.nom}
// Fitness : {meme.fitness:.2f}
// Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

def generate_html_output(scripts: list, meme_list: list, output_path: Path):
    html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>🏆 Top 10 FracturoScripts</title>
  <style>
    body { background: #000; color: #0f8; font-family: 'Courier New', monospace; padding: 2em; }
    .script { border-left: 3px solid #ff6b6b; padding-left: 1.5em; margin: 2em 0; }
    h1 { color: #ff6b6b; text-align: center; }
  </style>
</head>
<body>
  <h1>🏆 TOP 10 FRACTUROSCRIPTS<br>Extrait de Gen1000Pop40</h1>
"""
    for i, (script, meme) in enumerate(zip(scripts, meme_list), 1):
        html += f'  <div class="script"><h3>🔸 #{i} — {meme.symbole} {meme.nom} (f:{meme.fitness:.2f})</h3><pre>{script}</pre></div>\n'
    html += "</body>\n</html>"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Export HTML : {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", type=Path, help="Fichier Gen1000Pop40.txt")
    parser.add_argument("--emotion", default="oubli", help="Émotion de base (défaut: oubli)")
    parser.add_argument("--output", choices=["text", "html"], default="text")
    parser.add_argument("--html-file", type=Path, default="top10_fracturo.html")
    args = parser.parse_args()

    top10 = parse_log_for_top10(args.logfile)
    if not top10:
        print("⚠️ Aucun mème trouvé dans le fichier.", file=sys.stderr)
        sys.exit(1)

    scripts = [generate_fracturo_script(m, args.emotion) for m in top10]

    if args.output == "html":
        generate_html_output(scripts, top10, args.html_file)
    else:
        for i, (script, meme) in enumerate(zip(scripts, top10), 1):
            print(f"\n{'='*60}")
            print(f"🔸 #{i} — {meme.symbole} {meme.nom} (f:{meme.fitness:.2f})")
            print(f"{'='*60}")
            print(script)

if __name__ == "__main__":
    main()
