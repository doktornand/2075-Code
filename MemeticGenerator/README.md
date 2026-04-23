# ⚔️ Memetic Warfare — Laboratoire d'Évolution Mémétique

> *« Le mème qui se sait mème devient dieu de sa propre matrice. »*
> — Édition Soufi-Quantique-Entropique, Lagos 2075 + ∞

Memetic Warfare est un système complet de **simulation, d'évolution et de génération de mèmes weaponisés**. Il combine un automate cellulaire inspiré du Jeu de la Vie, un algorithme génétique darwinien, un moteur de puissance mémétique basé sur la psychologie jungienne, et deux interfaces graphiques Tkinter emboîtées.

---

## 📁 Structure du projet

```
memetic_warfare/
├── memetic_warfare_gui_4c.py     # GUI Ω de configuration et génération de prompts
├── memetic_sim_core.py           # Moteur de simulation et d'évolution génétique
├── memetic_gui.py                # GUI Enhanced : bridge entre GUI et moteur
└── README.md
```

---

## 🧩 Description des modules

### `memetic_warfare_gui_4c.py` — GUI Ω : Générateur de Prompts Mémétiques

Le module fondateur. Définit l'intégralité des **données ontologiques** du système (couches, biais, archétypes, symboles, topologies, émotions), le **moteur de puissance** et l'**interface graphique principale**.

#### Données fondatrices (constantes globales)

| Constante | Contenu |
|---|---|
| `COUCHES` | 27 couches mémétiques de -13 (Abîme Primordial) à +13 (Exode Intérieur) |
| `BIAIS` | 72 biais cognitifs en 6 catégories : classiques, narratifs, spirituels, temporels, quantiques, existentiels |
| `ARCHETYPES_JUNGIENS` | 15 archétypes (Persona, Ombre, Anima, Héros, Tricheur, Dieu, Diable, Fou, Magicien…) avec poids |
| `SYMBOLES_ALCHIMIQUES` | 72 symboles : 20 fixes (ouroboros, phoenix, lapis…) + 52 auto-générés via hash MD5 |
| `TOPOLOGIES_NARRATIVES` | 12 topologies (monomythe, rhizome, fractale, tesseract, bifurcation…) |
| `EMOTIONS_PRIMAIRES` | 12 émotions (vertige ontologique, extase algorithmique, fana, ishq, wajd…) |

#### Classe : `MemeticEngine`

Moteur de calcul de puissance mémétique. Construit des graphes de synergies archétypales, des matrices de co-occurrence symbolique et des maps de résonance émotionnelle.

| Méthode | Description |
|---|---|
| `_build_archetype_graph()` | Graphe pondéré des synergies entre archétypes |
| `_build_symbol_matrix()` | Matrice de co-occurrence entre les 20 premiers symboles |
| `_build_bias_synergy()` | Synergies croisées entre biais de catégories différentes |
| `_build_emotion_map()` | Association émotions → archétypes résonants |
| `calculer_puissance_omega(archetypes, symboles, emotions, biais, public, couches)` | Score de puissance 0–100 combinant résonance, synergies, cohérence et auto-évolution historique |

#### Fonctions de génération

| Fonction | Description |
|---|---|
| `generer_prompt_omega(couches, biais, archetypes, symboles, topologies, emotions, acteur, scenario, public, objectif, mystique, onirique, balise_perso)` | Génère un prompt Ω complet avec score de puissance, directives techniques et mode mystique |
| `generer_symbologie_omega(archetypes, symboles, topologies, emotions)` | Génère les combinaisons symboliques alchimiques à partir des archétypes et symboles sélectionnés |

#### Classe : `MemeticGUI_Omega`

Interface Tkinter principale (1400×900, palette terminal noire). Structure en onglets : **Configuration Ω**, **Prompt Ω**, **Analyse Ω**, **Historique Ω**.

| Méthode | Description |
|---|---|
| `init_vars()` | Initialise toutes les variables Tkinter (BooleanVar, StringVar) |
| `create_widgets()` | Construit l'interface à onglets |
| `build_config_section(parent)` | Section de configuration : couches, biais par catégorie, archétypes, symboles, topologies, émotions, paramètres contextuels |
| `generer_omega()` | Déclenche la génération en thread daemon |
| `_generer_thread()` | Thread de génération : collecte les sélections, appelle `generer_prompt_omega`, affiche le résultat et met à jour l'historique |
| `mettre_a_jour_histo()` | Rafraîchit l'onglet historique trié par puissance |
| `pulse_button(widget, phase)` | Animation cyclique du bouton Générer |

---

### `memetic_sim_core.py` — Moteur de Simulation et d'Évolution

Le cœur computationnel. Implémente un **automate cellulaire mémétique**, un **algorithme génétique** et un module de **visualisation**. Importe les données ontologiques de `memetic_warfare_gui_4c`.

#### Dataclass : `MemeConfig`

Structure de données d'un mème. Champs : `id`, `couches`, `archetypes`, `biais`, `symboles`, `topologies`, `emotions`, `fitness`, `is_glider`, `trajectory`, `generation`.

| Méthode | Description |
|---|---|
| `_generate_id()` | ID unique MD5 basé sur la configuration |
| `signature()` | Signature lisible (catégories de biais + archétypes) pour identifier les gliders |
| `to_dict()` | Sérialisation pour export CSV/JSON |

#### Classe : `MemeticCellularAutomaton`

Automate cellulaire simulant la propagation d'un mème sur un réseau social. Inspiré du Jeu de la Vie de Conway.

| Méthode | Description |
|---|---|
| `_generate_network(net_type, size)` | Génère le réseau : `small_world` (Watts-Strogatz), `scale_free` (Barabási-Albert), `grid` (2D), `random` (Erdős-Rényi), `community` (LFR) |
| `infect_initial_node(meme, node_id)` | Infecte le nœud de départ |
| `step()` | Un pas de propagation : calcule les transmissions nœud par nœud |
| `_transmission_probability(meme, source, target)` | Probabilité de transmission = fitness × facteur hub × résistance à la saturation, plafonnée à 95% |
| `simulate(max_steps, extinction_threshold)` | Simule jusqu'à extinction ou `max_steps` |
| `analyze_trajectory()` | Retourne longévité, portée max, moyenne, pic, stabilité, taux de croissance |
| `is_glider()` | Détecte les gliders : longévité > 500 steps, stabilité > 0.6, portée > 20% du réseau |

#### Classe : `MemeticGeneticAlgorithm`

Algorithme génétique faisant évoluer des populations de mèmes par sélection darwinienne.

**Paramètres de construction :** `population_size`, `network_type`, `network_size`, `mutation_rate` (défaut 0.3), `crossover_rate` (défaut 0.7), `elite_size` (défaut 5).

| Méthode | Description |
|---|---|
| `_initialize_population()` | Génère la population initiale aléatoire |
| `_random_meme()` | Crée un mème aléatoire avec configuration cohérente |
| `evaluate_fitness(meme)` | Fitness réelle via simulation complète : combine longévité (×0.3), portée max (×0.25), stabilité (×0.25), score statique (×0.2) + bonus ×1.5 si glider |
| `_calculate_static_fitness(meme)` | Score statique : poids archétypes + biais + équilibre couches + diversité émotionnelle |
| `evolve_generation(verbose)` | Un cycle complet : évaluation → tri → sélection (top 20%) → crossover → mutation |
| `_tournament_selection(pool, tournament_size)` | Sélection par tournoi de taille 3 |
| `_crossover(parent1, parent2)` | Croisement génétique : mix aléatoire des couches, archétypes, biais, symboles, émotions |
| `_mutate(meme)` | Mutation : archétypes (30%), couches (20%), biais (25%), émotions (15%) |
| `run_evolution(num_generations, verbose, save_interval)` | Boucle d'évolution complète avec sauvegarde périodique |
| `export_gliders_for_knime(filepath)` | Export CSV des gliders avec features ML pour KNIME |
| `save_checkpoint(filepath)` | Sauvegarde JSON de l'état courant de l'évolution |

#### Classe : `GliderVisualizer`

Visualisations Matplotlib de la propagation et de l'évolution.

| Méthode | Description |
|---|---|
| `animate_propagation(automaton, filepath)` | Animation en temps réel : graphe réseau (nœuds infectés en vert) + courbe de propagation |
| `plot_network_heatmap(automaton, step)` | Heatmap de la matrice d'adjacence colorée par infection |
| `plot_evolution_curve(ga, filepath)` | Courbe de fitness au fil des générations |
| `plot_glider_trajectories(ga, max_gliders)` | Trajectoires superposées des N meilleurs gliders |

#### Fonctions batch

| Fonction | Description |
|---|---|
| `main_evolution_experiment()` | 3 expériences guidées : test du glider légendaire 1-4-4, évolution complète, comparaison de topologies réseau |
| `generate_training_dataset(num_memes, network_type, output_file)` | Génère un dataset CSV massif de mèmes (gliders + non-gliders) pour KNIME |

---

### `memetic_gui.py` — GUI Enhanced : Bridge Intégré

Pont entre les deux modules précédents. Étend `MemeticGUI_Omega` par héritage et ajoute deux onglets de simulation/évolution directement dans l'interface principale.

**Classe :** `MemeticGUI_Enhanced` ← hérite de `MemeticGUI_Omega`

| Méthode | Description |
|---|---|
| `add_simulation_tab()` | Onglet 🔬 Simulation : choix réseau, taille, steps max |
| `add_evolution_tab()` | Onglet 🧬 Évolution : taille population, générations, taux mutation/crossover |
| `get_current_meme_config()` | Extrait les sélections du GUI Ω et les convertit en `MemeConfig` |
| `run_simulation()` | Lance la simulation du mème courant en thread daemon |
| `_display_simulation_results(analysis, is_glider)` | Affiche longévité, portée, pic, stabilité, taux de croissance |
| `visualize_trajectory()` | Trace la courbe de propagation du dernier mème simulé |
| `animate_propagation()` | Lance l'animation (réseau limité à 200 nœuds pour la performance) |
| `run_evolution()` | Lance l'algorithme génétique en thread daemon avec log en temps réel |
| `stop_evolution()` | Interrompt l'évolution en cours |
| `export_gliders()` | Ouvre un dialogue de sauvegarde et exporte le CSV pour KNIME |
| `plot_evolution()` | Affiche la courbe de fitness via `GliderVisualizer` |

---

## 📦 Installation

### Prérequis

- Python 3.8+
- Tkinter (inclus avec Python standard)

### Dépendances

```bash
pip install numpy networkx matplotlib pandas
```

### Installation de Tkinter si nécessaire

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Lancement

```bash
# Interface complète (recommandée) — GUI Ω + Simulation + Évolution
python memetic_gui.py

# Interface Ω seule (génération de prompts uniquement)
python memetic_warfare_gui_4c.py

# Moteur en ligne de commande (4 modes interactifs)
python memetic_sim_core.py
```

---

## 🖥️ Modes CLI (`memetic_sim_core.py`)

| Mode | Description |
|---|---|
| `1` | Expériences guidées : test glider légendaire + évolution + comparaison réseaux |
| `2` | Génération de dataset massif (500–5000 mèmes) pour KNIME |
| `3` | Test rapide du glider `1-4-4-Trickster-Shadow` avec plot |
| `4` | Évolution personnalisée (taille population + nombre de générations) |

---

## 🌐 Types de réseaux sociaux simulés

| Type | Modèle | Caractéristiques |
|---|---|---|
| `small_world` | Watts-Strogatz | Haute clusterisation + courtes distances (Facebook-like) |
| `scale_free` | Barabási-Albert | Hubs dominants (Twitter-like) |
| `grid` | Grille 2D | Comme le vrai Jeu de la Vie |
| `random` | Erdős-Rényi | Connexions aléatoires uniformes |
| `community` | LFR Benchmark | Communautés distinctes avec liens inter-groupes |

---

## 📊 Exports

| Fichier | Format | Contenu |
|---|---|---|
| `gliders_export.csv` | CSV | Features ML des gliders : biais, archétypes, métriques de propagation, label `is_glider` |
| `meme_training_data.csv` | CSV | Dataset d'entraînement mixte (gliders + non-gliders) pour KNIME |
| `evolution_gen_N.json` | JSON | Checkpoint d'évolution : génération, fitness history, gliders découverts |
| `*.prompt` | Texte | Prompt Ω généré (export depuis le GUI) |

---

## 🗺️ Architecture et dépendances entre modules

```
memetic_warfare_gui_4c.py
│   ├── Données : COUCHES, BIAIS, ARCHETYPES_JUNGIENS,
│   │             SYMBOLES_ALCHIMIQUES, TOPOLOGIES_NARRATIVES, EMOTIONS_PRIMAIRES
│   ├── MemeticEngine          (moteur de puissance)
│   ├── generer_prompt_omega() (générateur de prompts)
│   └── MemeticGUI_Omega       (GUI principale)
│             ↑
│         hérite
│             │
memetic_sim_core.py            memetic_gui.py
│   ├── MemeConfig             └── MemeticGUI_Enhanced
│   ├── MemeticCellularAutomaton    (hérite de MemeticGUI_Omega)
│   ├── MemeticGeneticAlgorithm     (importe les deux modules)
│   └── GliderVisualizer
│             ↑
│         importe
│             │
memetic_gui.py
```

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
