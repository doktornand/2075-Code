# ⚡ CreoNet — Traducteur CréoNeural Multi-Villes

> *« SYSTÈME MULTI-VILLES — GWADAR | NAPLES | LAGOS | DJIBOUTI | ABIDJAN | PORT-AU-PRINCE »*

CreoNet est un système de traduction poétique et créolisante qui transforme un texte source (français/anglais) en une langue hybride — le **CréoNeural** — mêlant créole, français, anglais, argot et code selon un profil géographique configurable. Chaque ville possède ses propres poids linguistiques, sa syntaxe régionale et ses effets de sortie spécifiques.

---

## 📁 Structure du projet

```
CreoNet/
├── CreoNet4c.py                  # Moteur de traduction CréoNeural
├── creonet_gui_v2.py             # Interface graphique multi-villes
├── creo_lexicon_core.json        # Lexique de base (requis)
├── creo_lexicon_creole.json      # Lexique créole (requis)
├── creo_lexicon_french.json      # Lexique français (requis)
├── creo_lexicon_english.json     # Lexique anglais (requis)
├── creo_lexicon_slang.json       # Lexique argot (optionnel)
├── creo_lexicon_dreams.json      # Lexique onirique (optionnel)
├── creo_config.json              # Configuration globale (requis)
├── language_profiles.json        # Profils linguistiques par ville (requis)
└── README.md
```

---

## 🧩 Description des modules

### `CreoNet4c.py` — Moteur de traduction CréoNeural

Le cœur du système. Charge les lexiques JSON, applique les poids linguistiques selon le profil de ville, tokenise le texte source et produit une sortie CréoNeural via une pipeline de transformation en plusieurs étapes.

#### Classe principale : `CreoNetTranslator`

| Méthode | Description |
|---|---|
| `load_all_resources()` | Charge tous les lexiques JSON et les profils de ville |
| `flatten_lexicon(data)` | Aplatit un lexique catégorisé en dictionnaire plat |
| `build_master_lookup()` | Fusionne tous les lexiques en un index de recherche global |
| `get_language_weights(profile)` | Retourne les poids linguistiques d'une ville |
| `find_best_translation(word, weights, style)` | Trouve la meilleure traduction selon les poids et le style |
| `apply_regional_syntax(tokens, weights)` | Applique les règles de syntaxe régionale (créole, français, anglais) |

#### Fonctions utilitaires

| Fonction | Description |
|---|---|
| `creofy_word(word, style)` | Transforme un mot selon les règles CréoNeurales et le style |
| `simple_tokenize(text)` | Tokenise le texte (mots + ponctuation) |
| `remove_accents(s)` | Normalise les caractères accentués |
| `is_punctuation(tok)` | Détecte si un token est un signe de ponctuation |

#### Fonction principale : `creonet_translate`

```python
creonet_translate(
    text: str,
    mood: str = "neutre",
    style: str = "street",
    city_profile: str = "gwadar",
    seed: Optional[int] = None,
    conserve_punct: bool = False
) -> str
```

Pipeline de traduction complète : tokenisation → traduction pondérée → syntaxe régionale → particules spécifiques à la ville → densité de particules → tag d'émotion → séparateurs → post-processing.

#### Fonctions API pour la GUI

| Fonction | Description |
|---|---|
| `get_city_profiles()` | Liste des villes disponibles |
| `get_emotion_tags()` | Dictionnaire des tags d'émotion par mood |
| `get_styles()` | Liste des styles disponibles |

---

### `creonet_gui_v2.py` — Interface Graphique v2

Interface Tkinter en mode **multi-villes**. Palette terminal sombre (vert néon, noir profond), saisie libre du texte source, contrôles de mood, style, seed et profil de ville, avec indicateurs de poids linguistique en temps réel.

**Classe :** `CreoNetGUIv2`

| Méthode | Description |
|---|---|
| `update_city_info()` | Met à jour les indicateurs de poids linguistique selon la ville sélectionnée |
| `translate()` | Lance la traduction et affiche le résultat |
| `save_output()` | Sauvegarde la sortie en `.creo` ou `.txt` |
| `test_multi_city()` | Traduit le même texte sur toutes les villes et compare les résultats |

---

## 📦 Installation

### Prérequis

- Python 3.8+
- Tkinter (inclus avec Python standard)

### Installation de Tkinter si nécessaire

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Lancement

```bash
# Interface graphique
python creonet_gui_v2.py

# En ligne de commande (démo)
python CreoNet4c.py
```

---

## ⚙️ Configuration

### `creo_config.json`

Contient la configuration globale du moteur.

| Clé | Type | Description |
|---|---|---|
| `particles` | `list[str]` | Particules insérées aléatoirement (`yo`, `mi`, `dat`…) |
| `emotion_tags` | `dict[str, list]` | Tags d'émotion par mood (`<burn>`, `<null>`, `<rise>`…) |
| `separators` | `dict[str, str]` | Séparateur de tokens par style (`" / "`, `" // "`…) |

### `language_profiles.json`

Définit les poids linguistiques de chaque ville.

```json
{
  "language_profiles": {
    "gwadar":         { "creole": 0.3, "french": 0.2, "english": 0.4, "code": 0.1 },
    "port_au_prince": { "creole": 0.6, "french": 0.3, "english": 0.1, "code": 0.0 },
    "djibouti":       { "creole": 0.1, "french": 0.5, "english": 0.2, "code": 0.2 }
  }
}
```

### Lexiques (`creo_lexicon_*.json`)

Chaque fichier lexique est structuré par catégories, chaque catégorie étant un dictionnaire `mot_source → traduction`.

```json
{
  "salutations": {
    "bonjour": "bon",
    "merci": "mèsi"
  },
  "verbes": {
    "aller": "ale",
    "voir": "wè"
  }
}
```

| Fichier | Rôle |
|---|---|
| `creo_lexicon_core.json` | Vocabulaire de base CréoNeural |
| `creo_lexicon_creole.json` | Traductions créoles |
| `creo_lexicon_french.json` | Variantes françaises |
| `creo_lexicon_english.json` | Variantes anglaises |
| `creo_lexicon_slang.json` | Argot et registres populaires |
| `creo_lexicon_dreams.json` | Vocabulaire onirique |

---

## 🌍 Profils de villes

Chaque ville applique des règles syntaxiques et des effets de sortie spécifiques.

| Ville | Dominante linguistique | Effets spéciaux |
|---|---|---|
| `gwadar` | Anglais + code | Insertion de `data`, `net`, `node`, `stream` |
| `port_au_prince` | Créole | Particules `wi`, `non`, `vre` + suffixe `// sak pase` |
| `naples` | — | Préfixe emoji 🇮🇹 |
| `djibouti` | Français | Préfixe `alors` + suffixe `// wallahi` |
| `lagos` | Créole | Poids créole élevé |
| `abidjan` | Français | Structure française préservée |

---

## 🎨 Styles disponibles

Le style influe sur la transformation des mots (`creofy_word`) et la densité des particules insérées.

| Style | Comportement | Densité particules |
|---|---|---|
| `street` | Contractions, `th→d`, `ph→f`, suffixes aléatoires | Haute (0.25) |
| `hacker` | Transformations agressives | Haute (0.25) |
| `ritual` | Préfixes `ghost.`, coupures internes | Basse (0.1) |
| `liturgical` | Sortie convertie en MAJUSCULES | Basse (0.1) |

---

## 🗺️ Architecture et pipeline de traduction

```
Texte source
     │
     ▼
simple_tokenize()
     │
     ▼
find_best_translation()  ←── lexiques pondérés par profil de ville
     │
     ▼
apply_regional_syntax()  ←── règles créole / français / anglais
     │
     ▼
Particules spécifiques à la ville
     │
     ▼
Densité de particules (selon style)
     │
     ▼
Tag d'émotion (selon mood)
     │
     ▼
Séparateur (selon style)
     │
     ▼
Post-processing (nettoyage, MAJUSCULES si ritual/liturgical)
     │
     ▼
Sortie CréoNeural
```

---

## 💡 Exemples d'utilisation

**En Python :**

```python
from CreoNet4c import creonet_translate, get_city_profiles

# Traduction simple
result = creonet_translate("Je vais au marché", city_profile="port_au_prince", mood="joyeux")
print(result)
# → mwen / ale / mache / wi / <burn> // sak pase

# Traduction reproductible (seed fixée)
result = creonet_translate("La nuit tombe", city_profile="gwadar", style="hacker", seed=42)

# Test multi-villes
for city in get_city_profiles():
    print(f"{city:15} → {creonet_translate('Le réseau parle', city_profile=city, seed=0)}")
```

**Format de sortie `.creo` :**

```
// CRÉONEURAL - PORT_AU_PRINCE
mwen / ale / mache / wi / <burn> // sak pase
```

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
