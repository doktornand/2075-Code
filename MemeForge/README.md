# 🧠 MemeForge — Meme-Forgery Engine v2.0

Système avancé de génération de mèmes artistiques basé sur des archétypes mémétiques, des effets glitch, des runes et une CLI complète.

---

## ✨ Fonctionnalités

- **Effets glitch avancés** — décalage de canaux RGB, data bending, scanlines, avec 3 niveaux d'intensité et 3 styles (`subtle`, `medium`, `extreme`)
- **Archétypes mémétiques** — génération de narratives thématiques selon des archétypes configurables (ex. `glitch`, `resistance`)
- **Runes** — incorporation de symboles runiques (Ansuz, Berkano, Fehu, Algiz…) avec leurs fréquences et effets associés
- **QR code AR** — ajout d'un QR code de réalité augmentée positionné aléatoirement sur l'image
- **Flux d'actualités** — génération de narratives basée sur des titres RSS en temps réel (BBC, NYT…)
- **Art glitch algorithmique** — génération procédurale d'images si aucune source n'est fournie
- **Mode batch** — génération de plusieurs mèmes en une seule commande
- **Export de métadonnées** — fichier JSON associé à chaque mème généré
- **Configuration JSON externe** — tous les archétypes, runes, narratives et effets sont configurables via des fichiers JSON

---

## 📦 Installation

### Prérequis

- Python 3.8+
- pip

### Dépendances

```bash
pip install pillow numpy requests qrcode feedparser
```

### Clonage

```bash
git clone https://github.com/votre-utilisateur/memeforge.git
cd memeforge
```

---

## ⚙️ Configuration

MemeForge charge ses paramètres depuis un dossier `./config/` contenant les fichiers JSON suivants :

| Fichier | Contenu |
|---|---|
| `runes.json` | Définitions des runes (nom, effet, fréquence) |
| `archetypes.json` | Archétypes mémétiques (palette de couleurs, mots-clés, intensité) |
| `narratives.json` | Templates de narratives et concepts |
| `glitch_effects.json` | Paramètres des effets glitch avancés |
| `sources.json` | URLs des flux RSS et sources d'images |

Si les fichiers sont absents, une configuration de fallback intégrée est utilisée automatiquement.

### Exemple — `runes.json`

```json
{
  "runes": {
    "ᚨ": { "name": "Ansuz", "effect": "communication_divine", "frequency": "14.225" },
    "ᛒ": { "name": "Berkano", "effect": "naissance_transformation", "frequency": "14.100" }
  }
}
```

### Exemple — `archetypes.json`

```json
{
  "archetypes": {
    "glitch": {
      "keywords": ["corruption", "fracture", "erreur_systeme"],
      "color_palette": ["#ff0000", "#00ffff", "#ffff00"],
      "intensity": 2.5
    }
  }
}
```

---

## 🚀 Utilisation

```bash
python memeforge.py [OPTIONS]
```

### Options principales

| Option | Description |
|---|---|
| `-i`, `--input` | Image source (URL ou chemin local) |
| `-t`, `--text` | Texte personnalisé pour le mème |
| `-a`, `--archetype` | Archétype mémétique à appliquer |
| `-r`, `--rune` | Rune spécifique à incorporer |
| `-g`, `--glitch` | Niveau de glitch : `1` (subtle), `2` (medium), `3` (extreme) |
| `--glitch-style` | Style de glitch : `subtle`, `medium`, `extreme` |
| `--ar` | Ajouter un QR code de réalité augmentée |
| `--ar-url` | URL personnalisée pour le QR code AR |
| `--news` | Générer un narrative basé sur l'actualité du jour |
| `--batch N` | Générer un lot de N mèmes |
| `--theme` | Thème narratif spécifique |
| `-o`, `--output` | Préfixe du fichier de sortie |
| `--format` | Format de sortie : `png` (défaut), `jpg`, `webp` |
| `--quality` | Qualité pour JPEG/WEBP (1–100, défaut : 85) |
| `--metadata` | Exporter un fichier JSON de métadonnées |
| `--verbose` | Afficher les logs détaillés |

---

## 💡 Exemples

**Mème simple avec image locale et effet glitch extrême :**
```bash
python memeforge.py -i photo.jpg -a glitch -g 3 -o mon_meme
```

**Mème avec rune, QR code AR et texte personnalisé :**
```bash
python memeforge.py -i input.jpg -a resistance -r ᚨ --ar -t "La vérité est dans le glitch" -o resultat
```

**Génération basée sur l'actualité du jour :**
```bash
python memeforge.py --news -a glitch --verbose
```

**Génération d'un lot de 5 mèmes avec métadonnées :**
```bash
python memeforge.py --batch 5 --metadata -o batch_output
```

**Art glitch algorithmique pur (sans image source) :**
```bash
python memeforge.py -a glitch -g 3 --format webp -o glitch_art
```

---

## 📁 Structure des fichiers de sortie

Pour chaque mème généré, MemeForge produit :

- `<nom>.png` (ou `.jpg` / `.webp`) — l'image du mème
- `<nom>_metadata.json` — métadonnées associées (si `--metadata` activé)

### Exemple de métadonnées

```json
{
  "narrative": "What if reality was never what we thought?",
  "archetype": "glitch",
  "rune": "ᚨ",
  "rune_data": { "name": "Ansuz", "effect": "communication_divine", "frequency": "14.225" },
  "glitch_level": 3,
  "glitch_style": "extreme",
  "ar_content": "https://example.com/ar/a1b2c3d4",
  "timestamp": "2026-04-23T14:32:00",
  "version": "2.0",
  "generator": "MemeForge-Advanced"
}
```

---

## 🏗️ Architecture

```
memeforge.py
└── AdvancedMemeForge
    ├── load_configurations()       # Chargement JSON depuis ./config/
    ├── load_fallback_config()      # Config intégrée de secours
    ├── setup_glitch_luts()         # Tables de lookup pour effets glitch
    ├── parse_arguments()           # CLI via argparse
    ├── load_image_source()         # Chargement URL ou fichier local
    ├── apply_advanced_glitch()     # Effets glitch (data bending, RGB shift, scanlines)
    ├── generate_archetypal_narrative()  # Génération de texte par archétype
    ├── get_current_news_headline() # Récupération RSS
    ├── add_ar_qr_code()            # Génération et incrustation de QR code
    ├── generate_glitch_art()       # Art algorithmique procédural
    ├── overlay_advanced_text()     # Superposition de texte stylisé
    ├── create_advanced_meme()      # Pipeline principal de génération
    ├── save_results()              # Export image + JSON
    └── batch_generate()            # Génération en lot
```

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
