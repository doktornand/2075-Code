#!/usr/bin/env python3
# omega_prompt_to_json.py
# Convertit un Ω-PROMPT (.txt) en JSON compatible avec smart_refiner_post3a.py
# Usage : python3 omega_prompt_to_json.py PromptTwo.txt --output virus_MEME-2511.json

import re
import json
import argparse
from datetime import datetime

def parse_omega_prompt(text: str) -> dict:
    """Parse un Ω-PROMPT et retourne un dict JSON structuré."""
    data = {
        "metadata": {},
        "config": {
            "couches": [],
            "archetypes": {},
            "symboles": [],
            "topologies": [],
            "emotions": [],
            "biais": {},
        },
        "directives": {
            "frequences": [],
            "formats": [],
            "balise_onirique": None,
            "mode_mystique": False
        }
    }

    # === METADATA ===
    date_match = re.search(r"// Ω-PROMPT \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", text)
    if date_match:
        data["metadata"]["timestamp"] = date_match.group(1)
    else:
        data["metadata"]["timestamp"] = datetime.utcnow().isoformat()

    puissance_match = re.search(r"PUISSANCE\s+([\d.]+)/100", text)
    data["metadata"]["puissance"] = float(puissance_match.group(1)) if puissance_match else 0.0

    operateur_match = re.search(r"Ω-OPÉRATEUR\s*:\s*(.+?)\s*\|", text)
    scenario_match = re.search(r"OPÉRATION\s*:\s*«\s*(.+?)\s*»", text)
    if operateur_match:
        data["metadata"]["operateur"] = operateur_match.group(1).strip()
    if scenario_match:
        data["metadata"]["operation"] = scenario_match.group(1).strip()

    public_match = re.search(r"PUBLIC\s*:\s*(.+)", text)
    if public_match:
        data["metadata"]["public"] = public_match.group(1).strip()

    objectif_match = re.search(r"OBJECTIF\s*:\s*(.+)", text)
    if objectif_match:
        data["metadata"]["objectif"] = objectif_match.group(1).strip()

    # === COUCHES ===
    couches_line = re.search(r"COUCHES ACTIVÉES.*?:\s*(.+)", text)
    if couches_line:
        couches_raw = couches_line.group(1)
        data["config"]["couches"] = [c.strip() for c in couches_raw.split(",")]

    # === BIAIS ===
    biais_section = re.findall(r"\[([A-ZÀ-Ÿ]+)\]\s*(.+?)(?=\n\[|\nARCHÉTYPES|\nSYMBOLOGIE|\nSORTIE|\Z)", text, re.DOTALL)
    for cat, biais_str in biais_section:
        cat_clean = cat.lower()
        biais_list = [b.strip() for b in biais_str.split(",")]
        data["config"]["biais"][cat_clean] = biais_list

    # === ARCHÉTYPES ===
    arch_section = re.findall(r"•\s*([^(]+)\s*\(\s*×([\d.]+)\s*\)\s*—\s*(.+)", text)
    for nom, poids, desc in arch_section:
        key = nom.lower().replace("le ", "").replace("la ", "").replace(" ", "_")
        data["config"]["archetypes"][key] = {
            "nom": nom.strip(),
            "poids": float(poids),
            "desc": desc.strip()
        }

    # === SYMBOLOGIE ===
    symb_section = re.findall(r"•\s*(.+)", text.split("SYMBOLOGIE ALCHIMIQUE")[1].split("PUISSANCE")[0])
    for line in symb_section:
        if "Émotion Ω" in line:
            emo = line.replace("Émotion Ω :", "").strip()
            data["config"]["emotions"].append(emo)
        elif "Topologie" in line:
            topo = line.replace("Topologie :", "").strip()
            data["config"]["topologies"].append(topo)
        else:
            data["config"]["symboles"].append(line.strip())

    # === DIRECTIVES TECHNIQUES ===
    if "7.83Hz" in text:
        data["directives"]["frequences"].extend(["7.83Hz", "432Hz", "19kHz"])
    if "Poème cyber-soufi" in text:
        data["directives"]["formats"].append("cyber_soufi_poem")
    if "deepfake 8K" in text:
        data["directives"]["formats"].append("deepfake_8k_audiovisual")
    if "BALISE ONIRIQUE" in text:
        balise_match = re.search(r"BALISE ONIRIQUE\s*:\s*(<[^>]+>)", text)
        if balise_match:
            data["directives"]["balise_onirique"] = balise_match.group(1)
    if "MODE MYSTIQUE Ω" in text:
        data["directives"]["mode_mystique"] = True

    return data

def main():
    parser = argparse.ArgumentParser(description="Convertit un Ω-PROMPT en JSON compatible avec smart_refiner_post3a.py")
    parser.add_argument("input", help="Fichier Ω-PROMPT (.txt)")
    parser.add_argument("--output", "-o", default="omega_virus.json", help="Fichier JSON de sortie")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    json_data = parse_omega_prompt(prompt_text)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"[Ω] Conversion réussie : {args.input} → {args.output}")
    print(f"[★] Puissance : {json_data['metadata'].get('puissance', 0):.1f}/100")

if __name__ == "__main__":
    main()