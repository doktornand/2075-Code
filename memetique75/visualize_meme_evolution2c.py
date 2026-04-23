#!/usr/bin/env python3
# visualize_meme_evolution_v2_fixed.py
# Compatible NumPy ≥1.20 • Labels lisibles • Export PNG/SVG • Stats

# --- COMPATIBILITÉ NUMPY (à supprimer si networkx ≥ 2.6) ---
import numpy as np
if not hasattr(np, 'int'):
    np.int = int
if not hasattr(np, 'float'):
    np.float = float
if not hasattr(np, 'bool'):
    np.bool = bool
# ---------------------------------------------------------

import re
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys
import argparse
from matplotlib.cm import ScalarMappable

def parse_log_file(filepath: str):
    memes = []
    current_gen = None
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            gen_match = re.match(r'^Génération\s+(\d+)', line)
            if gen_match:
                current_gen = int(gen_match.group(1))
                continue

            if current_gen is None:
                continue

            # Pattern robuste pour les mèmes
            match = re.match(r'^([^\s]+)\s+([^()]+)\s+\(f:([\d.]+)\)\s*(?:←\s*([^)]+))?$', line)
            if not match:
                continue

            symbole = match.group(1)
            nom_full = match.group(2).strip()
            fitness = float(match.group(3))
            parents_str = match.group(4) or ""

            parts = nom_full.split(' ', 1)
            meme_id = parts[0]
            display_name = parts[1] if len(parts) > 1 else meme_id

            parents = [p.strip() for p in parents_str.split(',')] if parents_str else []

            memes.append({
                "generation": current_gen,
                "id": meme_id,
                "name": display_name,
                "fitness": fitness,
                "parents": parents,
                "symbole": symbole
            })
    return memes

def filter_by_generation(memes, min_gen=None, max_gen=None):
    if min_gen is None and max_gen is None:
        return memes
    return [m for m in memes if
            (min_gen is None or m["generation"] >= min_gen) and
            (max_gen is None or m["generation"] <= max_gen)]

def build_graph(memes):
    G = nx.DiGraph()
    meme_ids = {m["id"] for m in memes}
    for m in memes:
        G.add_node(m["id"], **m)
        for p in m["parents"]:
            if p in meme_ids:
                G.add_edge(p, m["id"])
    return G

def plot_stats(memes):
    if not memes:
        print("⚠️ Aucun mème à analyser.")
        return
    gens = [m["generation"] for m in memes]
    fitnesses = [m["fitness"] for m in memes]
    print("📊 STATISTIQUES")
    print(f"Total mèmes : {len(memes)}")
    print(f"Fitness moyenne : {sum(fitnesses)/len(fitnesses):.3f}")
    print(f"Fitness max : {max(fitnesses):.2f}")
    top = sorted(memes, key=lambda x: x["fitness"], reverse=True)[:5]
    print("\n🏆 Top 5 mèmes :")
    for m in top:
        print(f"  {m['symbole']} {m['name']} (f:{m['fitness']:.2f}) — G{m['generation']}")
    print(f"\nGénérations analysées : {min(gens)} → {max(gens)}")

def visualize_and_export(G, title="Évolution Mémétique", output_file=None):
    if G.number_of_nodes() == 0:
        print("⚠️ Aucun nœud à visualiser.")
        return

    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(G, k=1.0, iterations=50, seed=42)

    fitness_vals = [G.nodes[n]['fitness'] for n in G.nodes()]
    sizes = [80 + G.nodes[n]['generation'] * 1.5 for n in G.nodes()]
    cmap = plt.get_cmap('Reds')
    norm = mcolors.Normalize(vmin=min(fitness_vals), vmax=max(fitness_vals))

    nx.draw_networkx_nodes(
        G, pos,
        node_color=[cmap(norm(f)) for f in fitness_vals],
        node_size=sizes,
        edgecolors='black',
        linewidths=0.5
    )
    nx.draw_networkx_edges(G, pos, arrows=True, alpha=0.3, arrowstyle='->', width=0.5)

    # === LABELS DÉCALÉS + BOÎTE DE FOND ===
    labels = {}
    label_pos = {}
    for node in G.nodes():
        sym = G.nodes[node].get('symbole', '')
        name = G.nodes[node].get('name', '')
        display_text = (sym + " " + name[:15] + ("..." if len(name) > 15 else "")).strip()
        labels[node] = display_text
        x, y = pos[node]
        label_pos[node] = (x + 0.03, y)

    nx.draw_networkx_labels(
        G, label_pos,
        labels=labels,
        font_size=7,
        font_color='white',
        font_weight='bold',
        bbox=dict(facecolor='black', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.1')
    )

    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, label="Fitness", shrink=0.8)
    plt.title(title, fontsize=14, color='white')
    plt.axis('off')
    plt.tight_layout()

    if output_file:
        plt.savefig(
            output_file,
            dpi=300 if not output_file.endswith('.svg') else None,
            format='svg' if output_file.endswith('.svg') else 'png',
            bbox_inches='tight',
            facecolor='black'
        )
        print(f"✅ Exporté : {output_file}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="Fichier de log (ex: Gen1000Pop40.txt)")
    parser.add_argument("--min-gen", type=int, help="Génération minimale")
    parser.add_argument("--max-gen", type=int, help="Génération maximale")
    parser.add_argument("--output", help="Fichier de sortie (PNG ou SVG)")
    args = parser.parse_args()

    memes = parse_log_file(args.logfile)
    memes = filter_by_generation(memes, args.min_gen, args.max_gen)
    plot_stats(memes)
    G = build_graph(memes)
    title = f"Évolution Mémétique — G{args.min_gen or 'début'} à G{args.max_gen or 'fin'}"
    visualize_and_export(G, title=title, output_file=args.output)

if __name__ == "__main__":
    main()
