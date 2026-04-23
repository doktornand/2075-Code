# 🕌 SoufiNet — Générateur Multi-Genres Cyber-Mystique

> *« Ces textes s'auto-effacent dans l'âme du réseau… »*

SoufiNet est un système de génération poétique procédurale mêlant esthétique soufie, imaginaire cyberpunk et mystique numérique. Il produit des textes dans plusieurs genres littéraires (ghazals, sonnets, haïkus, manifestes, journaux, dialogues, récits, méditations) à partir d'un lexique JSON configurable, et s'utilise aussi bien en ligne de commande qu'à travers une interface graphique Tkinter.

---

## 📁 Structure du projet

```
SoufiNet/
├── SoufiGen4a.py              # Générateur ghazal v1 (simple, JSON-driven)
├── SoufiGen4b.py              # Générateur multi-genres v2 (JSON-driven)
├── SoufiGen4b_enhanced.py     # Générateur multi-genres v3 (Enhanced, tonalités avancées)
├── SoufiNetGui.py             # Interface graphique v1 (ghazals uniquement)
├── SoufiNetGUI_v3.py          # Interface graphique v3 (multi-genres, enhanced)
├── lexiques.json              # Lexique principal (requis)
└── README.md
```

---

## 🧩 Description des modules

### `SoufiGen4a.py` — Générateur Ghazal v1

Le générateur d'origine, centré sur la forme du **ghazal**. Charge un fichier `lexiques.json` structuré par thèmes (`amour_divin`, `rêve_partagé`, etc.) et génère des vers en combinant préfixes sacrés, mots traditionnels, termes cyber et balises oniriques (`<burn>`, `<still>`, etc.).

**Classe principale :** `GenerateurGhazalCyberSoufi`

| Méthode | Description |
|---|---|
| `generer_vers(theme, inclure_balise, style)` | Génère un vers unique |
| `generer_ghazal(nb_vers, theme)` | Génère un ghazal complet |

---

### `SoufiGen4b.py` — Générateur Multi-Genres v2

Extension majeure supportant **7 genres** distincts, tous pilotés par `lexiques.json`. Introduit les pools de qafiya/radif pour les ghazals, les schémas rimiques pour les sonnets, et des structures narratives propres à chaque genre.

**Classe principale :** `GenerateurMultiGenresCyberSoufi`

| Méthode | Genre | Description |
|---|---|---|
| `generer_ghazal(couplets, theme)` | Ghazal | Avec qafiya, radif et balises |
| `generer_sonnet(theme)` | Sonnet | 14 vers, schéma rimique variable |
| `generer_haiku_quantique()` | Haïku | Structure 5-7-5, saison aléatoire |
| `generer_manifeste_hacktiviste()` | Manifeste | Déclaration datée, 5 sections |
| `generer_journal_bord(jours)` | Journal | Journal de N jours d'un netrunner |
| `generer_dialogue_philosophique()` | Dialogue | Entre deux personnages du lexique |
| `generer_ode_technomantique()` | Ode | 4 strophes de 4 vers |
| `generer_mantra_court(theme)` | Mantra | Fragment loop court |

**Fonction utilitaire :** `generer_texte(genre, **kwargs)` — point d'entrée unifié pour la GUI.

---

### `SoufiGen4b_enhanced.py` — Générateur Multi-Genres v3 (Enhanced)

Version améliorée qui exploite l'intégralité de `lexiques.json` : préservation des **catégories de lexique**, gestion des **tonalités** (mélancolique, révoltée, amoureuse, contemplative, prophétique, cryptique…), intégration de **motifs narratifs**, **fragments sacrés**, **citations soufies** et **dogmes 2075**.

**Classe principale :** `GenerateurMultiGenresCyberSoufiEnhanced`

| Méthode | Description |
|---|---|
| `generer_ghazal_ameliore(couplets, theme, tonalite)` | Ghazal avec tonalité et épigraphe |
| `generer_recit_narratif(longueur)` | Récit en N paragraphes avec motifs narratifs |
| `generer_meditation_quantique()` | Méditation basée sur dogmes et citations |
| `generer_manifeste_etendu()` | Manifeste utilisant motifs et mantras |
| `generer_sonnet(theme, tonalite)` | Sonnet avec tonalité appliquée |
| `generer_epigraphe()` | Épigraphe tirée des fragments sacrés |
| `_appliquer_tonalite(texte, tonalite)` | Transforme le texte selon la tonalité |
| `_generer_vers_avance(style)` | Vers avec sélection par catégorie |

**Fonction utilitaire :** `generer_texte_avance(genre, **kwargs)` — point d'entrée pour `SoufiNetGUI_v3`.

---

### `SoufiNetGui.py` — Interface Graphique v1

Interface Tkinter simple dédiée à la génération de **ghazals** via `SoufiGen4a`. Palette mystique sombre (violet, fond nuit), thème sélectionnable depuis `lexiques.json`, choix du nombre de vers et option d'inclusion des balises oniriques.

**Classe :** `SoufiNetGui`

---

### `SoufiNetGUI_v3.py` — Interface Graphique v3 (Enhanced)

Interface complète et étendue utilisant `SoufiGen4b_enhanced` (avec fallback automatique sur `SoufiGen4b`). Fenêtre 1000×800, palette cyber-mystique dorée, support de tous les genres et tonalités.

**Classe :** `SoufiNetGUIv3`

Fonctionnalités :

- Sélection du **genre**, du **thème** et de la **tonalité**
- Paramètre dynamique (nombre de couplets, jours, longueur…) avec unité adaptée au genre
- **Génération aléatoire** complète (genre + tonalité tirés au sort)
- **Collection de mantras** (tirés du lexique)
- Menu de **générations avancées** : manifeste multi-tonal, récit cosmique, séquence de méditations, dialogues philosophiques, collection de ghazals
- **Prévisualisation** du thème sélectionné dans une fenêtre dédiée
- **Statistiques du lexique** (nombre d'éléments par catégorie)
- **Sauvegarde** avec extension spécifique par genre (`.ghz`, `.snt`, `.hk`, `.mft`, `.log`, `.dlg`, `.ode`, `.rec`, `.med`)

---

## 📦 Installation

### Prérequis

- Python 3.8+
- Tkinter (inclus dans la plupart des distributions Python standard)

### Dépendances

Aucune dépendance externe. Tkinter est fourni avec Python. Sur certaines distributions Linux, il peut être nécessaire d'installer le paquet système :

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Lancement

```bash
# Interface graphique v3 (recommandée, multi-genres)
python SoufiNetGUI_v3.py

# Interface graphique v1 (ghazals uniquement)
python SoufiNetGui.py

# En ligne de commande — démo v2
python SoufiGen4b.py

# En ligne de commande — démo v3 Enhanced
python SoufiGen4b_enhanced.py
```

---

## ⚙️ Configuration — `lexiques.json`

Tous les modules chargent leur vocabulaire depuis `lexiques.json`, à placer à la racine du projet. Ce fichier structure l'intégralité du lexique cyber-mystique.

### Clés attendues

| Clé | Type | Description |
|---|---|---|
| `sujets` | `dict[str, list]` | Sujets par catégorie (mystiques, cyber, etc.) |
| `verbes` | `dict[str, list]` | Verbes par catégorie (rituels, cyber, etc.) |
| `symboles` | `dict[str, list]` | Symboles par catégorie |
| `lieux` | `dict[str, list]` | Lieux (zones 2075, espaces mystiques…) |
| `personnages` | `dict[str, list]` | Personnages (archivistes, IA mystiques, cyber-prophètes…) |
| `qafiya_pool` | `list[str]` | Rimes finales pour les ghazals |
| `radif_pool` | `list[str]` | Refrains pour les ghazals |
| `balises` | `dict[str, list]` | Balises oniriques par thème (`<burn>`, `<still>`, `<ghost>`…) |
| `mantras_bases` | `list[str]` | Fragments de mantras courts |
| `fragments_sacrés` | `list[str]` | Citations et épigraphes |
| `citations_soufies` | `list[str]` | Citations mystiques |
| `dogmes_2075` | `list[str]` | Dogmes futuristes du corpus |
| `motifs_narratifs` | `list[str]` | Motifs pour récits et manifestes |
| `tonalités` | `list[str]` | Tonalités disponibles |
| `thèmes` | `dict[str, dict]` | Thèmes pour SoufiGen4a (traditionnel / cyber) |
| `préfixes_sacrés` | `list[str]` | Préfixes pour SoufiGen4a |
| `suffixes_cyber` | `list[str]` | Suffixes pour SoufiGen4a |

---

## 🗺️ Architecture et relations entre modules

```
lexiques.json
      │
      ├──► SoufiGen4a.py                (GenerateurGhazalCyberSoufi)
      │         └──► SoufiNetGui.py     (GUI v1 — ghazals)
      │
      ├──► SoufiGen4b.py                (GenerateurMultiGenresCyberSoufi)
      │         └──► SoufiNetGUI_v3.py  (fallback si enhanced absent)
      │
      └──► SoufiGen4b_enhanced.py       (GenerateurMultiGenresCyberSoufiEnhanced)
                └──► SoufiNetGUI_v3.py  (GUI v3 — prioritaire)
```

`SoufiNetGUI_v3` charge d'abord `SoufiGen4b_enhanced` et se rabat automatiquement sur `SoufiGen4b` si la version améliorée est absente.

---

## 🎭 Genres supportés par version

| Genre | v4a | v4b | v4b Enhanced | GUI v1 | GUI v3 |
|---|:---:|:---:|:---:|:---:|:---:|
| Ghazal | ✅ | ✅ | ✅ + tonalité | ✅ | ✅ |
| Sonnet | — | ✅ | ✅ + tonalité | — | ✅ |
| Haïku | — | ✅ | — | — | ✅ |
| Manifeste | — | ✅ | ✅ étendu | — | ✅ |
| Journal de bord | — | ✅ | — | — | ✅ |
| Dialogue philosophique | — | ✅ | — | — | ✅ |
| Ode technomantique | — | ✅ | — | — | ✅ |
| Récit narratif | — | — | ✅ | — | ✅ |
| Méditation quantique | — | — | ✅ | — | ✅ |

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
