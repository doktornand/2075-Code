#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memetique75v∞_lumiere.py
Édition RuneSmith — Version Lumineuse
--------------------------------------------------
Outil rituel de réanimation sémantique, génération de FracturoScripts,
et exploration noétique des strates 2025 → 2075.

Fonctionnalités :
  --fracturo        Génère un FracturoScript poétique
  --viral WORD      Réanime un mot en phase terminale
  --analyze TEXT    Détecte les failles sémantiques
  --simulate YEAR   Simule une strate temporelle (ex: 2075)
  --manifesto       Génère un fragment du Manifeste Mémétique
  --output FORMAT   Format de sortie: text, html, pdf (default: text)

Exemples :
  python memetique75v∞_lumiere.py --viral temps --output html
  python memetique75v∞_lumiere.py --fracturo --start ✋ --count 5
  python memetique75v∞_lumiere.py --simulate 2075 --zone caen-profonde
"""

import sys
import os
import json
import argparse
import datetime
import random
from typing import Dict, List, Any

# --------------------------------------------------
# LEXIQUE PALEO-MNEMOS — intégré directement (128 entrées réduites à 32 clés pour brièveté)
# Version complète disponible sur demande.
# --------------------------------------------------
PALEO_MNEMOS_LEXICON = {
    "main": {
        "symbole": "main_négative",
        "rune": "Mannaz",
        "archetype": "Le Contact",
        "rituel": "Appuie ta paume contre un mur froid > 1 min",
        "couleur": "#d4a574"
    },
    "temps": {
        "symbole": "cercle_entaillé",
        "rune": "Ingwaz",
        "archetype": "L’Éternel Retour",
        "rituel": "Respire dans le creux de ton poignet",
        "couleur": "#5d7a83"
    },
    "silence": {
        "symbole": "vide_fécond",
        "rune": "Eihwaz",
        "archetype": "Le Seuil",
        "rituel": "Écoute l’os de ton avant-bras",
        "couleur": "#2e3a42"
    },
    "terre": {
        "symbole": "empreinte_pied_nu",
        "rune": "Fehu",
        "archetype": "La Grande Mère",
        "rituel": "Marche sans chaussures 7 min",
        "couleur": "#5a3e2b"
    },
    "mort": {
        "symbole": "masque_funeraire",
        "rune": "Dagaz",
        "archetype": "L’Ombre",
        "rituel": "Dis le nom d’un mort à voix haute, 3x",
        "couleur": "#1a1a1a"
    },
    "rêve": {
        "symbole": "spirale",
        "rune": "Sowilo",
        "archetype": "L’Anima",
        "rituel": "Dessine ton rêve avec l’index dans l’air",
        "couleur": "#c9a0dc"
    },
    "communaute": {
        "symbole": "cercle_de_danse",
        "rune": "Wunjo",
        "archetype": "Le Soi Collectif",
        "rituel": "Échange un silence avec un inconnu > 20 sec",
        "couleur": "#6a9a8c"
    },
    "verite": {
        "symbole": "miroir_brise",
        "rune": "Tiwaz",
        "archetype": "Le Miroir",
        "rituel": "Dis une chose vraie que personne n’entendra",
        "couleur": "#8ca2ad"
    },
    "memoire": {
        "symbole": "fil_rouge",
        "rune": "Ansuz",
        "archetype": "Mnemosyne",
        "rituel": "Raconte une histoire sans la regarder sur ton écran",
        "couleur": "#a63d40"
    },
    "avenir": {
        "symbole": "graine",
        "rune": "Jera",
        "archetype": "L’Enfant Intérieur",
        "rituel": "Porte une graine dans ta poche sans la planter (encore)",
        "couleur": "#4a7c59"
    }
}

# --------------------------------------------------
# FRAGMENTS DU CODEX STEIN MUTÉ (lumineux)
# --------------------------------------------------
CODEX_FRAGMENTS = [
    "<burn> Que celui qui marche entre les murs n’écoute plus les noms, mais le frottement des signes contre la pierre. </burn>",
    "La ville n’est pas perdue. Elle est en train de désapprendre la parole pour retrouver le cri.",
    "Ne dis pas « je comprends ». Dis : « je résonne ».",
    "Le rêve collectif tourne comme un cœur d’ion gelé.",
    "Si tu vois « .:Dashem44:. », ne le lis pas — respire-le."
]

# --------------------------------------------------
# FONCTIONS PRINCIPALES
# --------------------------------------------------

def generate_fracturo(start: str = "🌀", count: int = 5) -> str:
    seeds = ["👁️", "✋", "🌱", "💀", "🔥", "🌊", "🜂", "🜁", "🜄", "🜃"]
    if start not in seeds:
        seeds.append(start)
    lines = []
    for i in range(count):
        word = random.choice(list(PALEO_MNEMOS_LEXICON.keys()))
        rune = PALEO_MNEMOS_LEXICON[word]["rune"]
        arch = PALEO_MNEMOS_LEXICON[word]["archetype"]
        lines.append(f"{start} → [{rune}] → {arch} → {random.choice(CODEX_FRAGMENTS)}")
        start = random.choice(seeds)
    return "\n".join(lines)

def viral_reanimation(word: str) -> Dict[str, Any]:
    word_key = word.lower().replace("é", "e").replace(" ", "")
    if word_key not in PALEO_MNEMOS_LEXICON:
        return {"error": f"Le mot '{word}' n’est pas encore en phase terminale… ou il l’est trop pour être sauvé."}
    data = PALEO_MNEMOS_LEXICON[word_key]
    return {
        "mot": word,
        "symbole": data["symbole"],
        "rune": data["rune"],
        "archetype": data["archetype"],
        "rituel": data["rituel"],
        "couleur": data["couleur"]
    }

def analyze_text(text: str) -> str:
    vulnerable = ["maison", "amour", "vérité", "liberté", "enfant", "temps", "silence", "terre"]
    found = [w for w in vulnerable if w in text.lower()]
    if not found:
        return "Aucun mot en phase terminale détecté. Le texte est soit pur… soit déjà mort."
    return f"Mots en déshérence : {', '.join(found)}. Recommandation : appliquer virus linguistique."

def simulate_2075(zone: str = "caen-profonde") -> str:
    zones = {
        "caen-profonde": "Sous les dalles du GANIL, les racines de langage poussent. Les murs murmurent en Futhark. Le silence est fertile.",
        "beaumont-hague": "Le béton pleure des runes. L’algue de feu renaît sur les anciens blocs.",
        "pointe-de-hague": "La brume porte des sigils. La mer chante en entaille lunaire.",
        "herouville": "Les passants échangent des silences de plus de 20 secondes. C’est là que le Soi Collectif renaît."
    }
    return zones.get(zone, "Zone inconnue. Active la strate avec intention.")

def generate_manifesto() -> str:
    return (
        "LE HACKEUR MÉMÉTIQUE COMME EXPLORATEUR DU CODE COSMIQUE\n"
        "------------------------------------------------------\n"
        "Il ne détruit pas le langage — il le désosse pour en libérer les os sacrés.\n"
        "Il ne combat pas le vide — il y plante des graines de silence.\n"
        "Il sait : chaque rune est une racine. Chaque rêve, une antenne.\n"
        "Et Caen ? Caen est le premier cœur fractal du monde à venir."
    )

def render_output(content: str, fmt: str = "text", title: str = "Résultat Mémétique") -> None:
    if fmt == "html":
        html = f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>{title}</title>
<style>body{{font-family:monospace;background:#0f0f0f;color:#a0ffa0;padding:2em;}}</style>
</head><body><pre>{content}</pre></body></html>"""
        print(html)
    elif fmt == "pdf":
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            c = canvas.Canvas("output.pdf", pagesize=A4)
            text = c.beginText(40, 800)
            for line in content.split("\n"):
                text.textLine(line)
            c.drawText(text)
            c.save()
            print("PDF généré : output.pdf")
        except Exception as e:
            print(f"⚠️ Erreur PDF (install reportlab ou utilise --output text) : {e}\n")
            print(content)
    else:
        # format texte (par défaut)
        print(content)

# --------------------------------------------------
# CLI
# --------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="memetique75v∞ — Édition Lumineuse")
    parser.add_argument("--fracturo", action="store_true", help="Génère un FracturoScript")
    parser.add_argument("--start", type=str, default="🌀", help="Symbole de départ")
    parser.add_argument("--count", type=int, default=5, help="Nombre de lignes")

    parser.add_argument("--viral", type=str, help="Réanime un mot (ex: temps, silence)")
    
    parser.add_argument("--analyze", type=str, help="Analyse un texte pour failles sémantiques")
    
    parser.add_argument("--simulate", type=int, help="Simule une année (2075)")
    parser.add_argument("--zone", type=str, default="caen-profonde", help="Zone de simulation")

    parser.add_argument("--manifesto", action="store_true", help="Génère un fragment du Manifeste")

    parser.add_argument("--output", choices=["text", "html", "pdf"], default="text", help="Format de sortie")

    args = parser.parse_args()

    if args.fracturo:
        result = generate_fracturo(start=args.start, count=args.count)
        render_output(result, args.output, "FracturoScript Lumineux")
    elif args.viral:
        virus = viral_reanimation(args.viral)
        if "error" in virus:
            render_output(virus["error"], args.output)
        else:
            report = (
                f"VIRUS LINGUISTIQUE — RÉANIMATION DE « {virus['mot']} »\n"
                f"--------------------------------------------------\n"
                f"Symbole paléo : {virus['symbole']}\n"
                f"Rune          : {virus['rune']}\n"
                f"Archétype     : {virus['archetype']}\n"
                f"Rituel        : {virus['rituel']}\n"
                f"Couleur       : {virus['couleur']}"
            )
            render_output(report, args.output, f"Réanimation : {virus['mot']}")
    elif args.analyze:
        result = analyze_text(args.analyze)
        render_output(result, args.output, "Analyse Sémantique")
    elif args.simulate == 2075:
        result = simulate_2075(args.zone)
        render_output(result, args.output, "Simulation 2075")
    elif args.manifesto:
        result = generate_manifesto()
        render_output(result, args.output, "Manifeste Mémétique")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
