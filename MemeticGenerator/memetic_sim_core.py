"""
MEMETIC WARFARE - SIMULATION CORE
Moteur de simulation et d'évolution mémétique inspiré du Prof
Version complète : Automate cellulaire + Algorithme génétique + Détection de gliders
"""

import numpy as np
import networkx as nx
import random
import json
import hashlib
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass, asdict
import pandas as pd

# Import des données du GUI original
from memetic_warfare_gui_4c import (
    COUCHES, BIAIS, ARCHETYPES_JUNGIENS, 
    SYMBOLES_ALCHIMIQUES, TOPOLOGIES_NARRATIVES, EMOTIONS_PRIMAIRES
)

# =============================================================================
# [STRUCTURES DE DONNÉES]
# =============================================================================

@dataclass
class MemeConfig:
    """Configuration complète d'un mème"""
    id: str
    couches: List[str]
    archetypes: List[str]
    biais: Dict[str, List[str]]
    symboles: List[str]
    topologies: List[str]
    emotions: List[str]
    fitness: float = 0.0
    is_glider: bool = False
    trajectory: List[int] = None
    generation: int = 0
    
    def __post_init__(self):
        if self.trajectory is None:
            self.trajectory = []
        if not self.id:
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Génère un ID unique basé sur la configuration"""
        config_str = f"{self.couches}{self.archetypes}{self.biais}"
        return hashlib.md5(config_str.encode()).hexdigest()[:12]
    
    def signature(self) -> str:
        """Signature lisible du mème (pour les gliders)"""
        bias_cats = '-'.join(sorted([k for k, v in self.biais.items() if v]))
        archs = '-'.join(sorted(self.archetypes)[:2])
        return f"{bias_cats}_{archs}"
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire pour export"""
        return {
            'id': self.id,
            'couches': self.couches,
            'archetypes': self.archetypes,
            'biais': self.biais,
            'symboles': self.symboles,
            'topologies': self.topologies,
            'emotions': self.emotions,
            'fitness': self.fitness,
            'is_glider': self.is_glider,
            'max_reach': max(self.trajectory) if self.trajectory else 0,
            'longevity': len(self.trajectory),
            'signature': self.signature(),
            'generation': self.generation
        }

# =============================================================================
# [AUTOMATE CELLULAIRE - Le "Jeu de la Vie" mémétique]
# =============================================================================

class MemeticCellularAutomaton:
    """
    Automate cellulaire pour simuler la propagation des mèmes.
    Inspiré du Jeu de la Vie de Conway mais avec règles mémétiques.
    """
    
    def __init__(self, network_type: str = 'small_world', size: int = 500, seed: int = None):
        self.network_type = network_type
        self.size = size
        self.network = self._generate_network(network_type, size)
        self.state = np.empty(size, dtype=object)  # None ou MemeConfig
        self.state.fill(None)
        self.history = []  # Historique des comptes d'infectés
        self.step_count = 0
        
        if seed:
            random.seed(seed)
            np.random.seed(seed)
    
    def _generate_network(self, net_type: str, size: int) -> nx.Graph:
        """Génère différents types de réseaux sociaux"""
        if net_type == 'small_world':
            # Watts-Strogatz: haute clusterisation + courte distance
            return nx.watts_strogatz_graph(size, k=6, p=0.1)
        
        elif net_type == 'scale_free':
            # Barabási-Albert: hubs dominants (Twitter-like)
            return nx.barabasi_albert_graph(size, m=3)
        
        elif net_type == 'grid':
            # Grille 2D (comme le vrai Jeu de la Vie)
            side = int(np.sqrt(size))
            return nx.grid_2d_graph(side, side)
        
        elif net_type == 'random':
            # Erdős-Rényi: connexions aléatoires
            return nx.erdos_renyi_graph(size, p=0.05)
        
        elif net_type == 'community':
            # Réseau avec communautés distinctes
            return nx.community.LFR_benchmark_graph(
                size, tau1=3, tau2=1.5, mu=0.1, 
                average_degree=5, min_community=20
            )
        
        else:
            return nx.watts_strogatz_graph(size, k=6, p=0.1)
    
    def infect_initial_node(self, meme: MemeConfig, node_id: int = None):
        """Infecte un nœud initial avec le mème"""
        if node_id is None:
            node_id = random.randint(0, self.size - 1)
        self.state[node_id] = meme
        self.history.append(1)
    
    def step(self):
        """Un time-step de propagation (comme une génération du Jeu de la Vie)"""
        new_state = self.state.copy()
        
        for node in range(self.size):
            if self.state[node] is not None:  # Si le nœud est infecté
                meme = self.state[node]
                neighbors = list(self.network.neighbors(node))
                
                for neighbor in neighbors:
                    if self.state[neighbor] is None:  # Si le voisin est susceptible
                        # Calcul de la probabilité de transmission
                        p_transmit = self._transmission_probability(meme, node, neighbor)
                        
                        if random.random() < p_transmit:
                            new_state[neighbor] = meme
        
        self.state = new_state
        infected_count = np.count_nonzero(self.state)
        self.history.append(infected_count)
        self.step_count += 1
        
        return infected_count
    
    def _transmission_probability(self, meme: MemeConfig, source: int, target: int) -> float:
        """
        Calcule la probabilité de transmission basée sur:
        - Fitness du mème
        - Structure du réseau (hubs transmettent mieux)
        - Saturation locale
        """
        # Base: fitness normalisée
        base_fitness = meme.fitness / 100.0
        
        # Facteur hub: les nœuds bien connectés transmettent mieux
        degree_source = self.network.degree(source)
        hub_factor = 1.0 + (degree_source / 20.0)
        
        # Facteur de saturation: si beaucoup de voisins infectés, résistance
        neighbors_target = list(self.network.neighbors(target))
        infected_neighbors = sum(1 for n in neighbors_target if self.state[n] is not None)
        saturation = infected_neighbors / len(neighbors_target) if neighbors_target else 0
        resistance_factor = 1.0 - (saturation * 0.5)
        
        # Probabilité finale
        p = base_fitness * hub_factor * resistance_factor * 0.3
        return min(p, 0.95)  # Cap à 95%
    
    def simulate(self, max_steps: int = 1000, extinction_threshold: int = 3) -> List[int]:
        """
        Simule la propagation jusqu'à extinction ou max_steps
        extinction_threshold: nombre de steps consécutifs sans changement
        """
        stagnation_count = 0
        last_infected = 0
        
        for step in range(max_steps):
            infected = self.step()
            
            # Critère d'extinction
            if infected == 0:
                break
            
            # Critère de stagnation
            if infected == last_infected:
                stagnation_count += 1
                if stagnation_count >= extinction_threshold:
                    break
            else:
                stagnation_count = 0
            
            last_infected = infected
        
        return self.history
    
    def analyze_trajectory(self) -> Dict:
        """Analyse détaillée de la trajectoire"""
        if not self.history:
            return {}
        
        trajectory = np.array(self.history)
        
        return {
            'longevity': len(trajectory),
            'max_reach': int(np.max(trajectory)),
            'avg_infected': float(np.mean(trajectory)),
            'peak_time': int(np.argmax(trajectory)),
            'stability': float(1.0 / (1.0 + np.std(trajectory[100:]) if len(trajectory) > 100 else np.std(trajectory))),
            'final_reach': int(trajectory[-1]),
            'growth_rate': float((trajectory[min(50, len(trajectory)-1)] - trajectory[0]) / 50) if len(trajectory) > 50 else 0.0
        }
    
    def is_glider(self) -> bool:
        """
        Détecte si le mème est un "glider" (structure stable et mobile)
        Critères du Prof:
        - Longévité élevée (>500 steps)
        - Stabilité après phase initiale (variance faible)
        - Portée significative (>20% du réseau)
        """
        analysis = self.analyze_trajectory()
        
        if not analysis:
            return False
        
        longevity_check = analysis['longevity'] > 500
        stability_check = analysis['stability'] > 0.6
        reach_check = analysis['max_reach'] / self.size > 0.2
        
        return longevity_check and stability_check and reach_check

# =============================================================================
# [ALGORITHME GÉNÉTIQUE - Évolution darwinienne]
# =============================================================================

class MemeticGeneticAlgorithm:
    """
    Algorithme génétique pour faire évoluer des mèmes optimaux.
    Reproduit l'approche du Prof avec sélection, mutation, crossover.
    """
    
    def __init__(
        self, 
        population_size: int = 100,
        network_type: str = 'small_world',
        network_size: int = 500,
        mutation_rate: float = 0.3,
        crossover_rate: float = 0.7,
        elite_size: int = 5
    ):
        self.population_size = population_size
        self.network_type = network_type
        self.network_size = network_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        
        self.population: List[MemeConfig] = []
        self.generation = 0
        self.best_fitness_history = []
        self.gliders_discovered = []
        
        # Initialisation
        self.population = self._initialize_population()
    
    def _initialize_population(self) -> List[MemeConfig]:
        """Génère une population initiale aléatoire"""
        population = []
        for _ in range(self.population_size):
            meme = self._random_meme()
            population.append(meme)
        return population
    
    def _random_meme(self) -> MemeConfig:
        """Génère un mème aléatoire avec configuration cohérente"""
        # Sélection aléatoire des composants
        num_couches = random.randint(2, 6)
        couches = random.sample(list(COUCHES.keys()), k=num_couches)
        
        num_archetypes = random.randint(1, 3)
        archetypes = random.sample(list(ARCHETYPES_JUNGIENS.keys()), k=num_archetypes)
        
        # Biais: 2-4 catégories, 1-3 biais par catégorie
        num_categories = random.randint(2, 4)
        biais = {}
        for cat in random.sample(list(BIAIS.keys()), k=num_categories):
            num_biais = random.randint(1, 3)
            biais[cat] = random.sample(BIAIS[cat], k=num_biais)
        
        # Symboles et autres
        symboles = random.sample(list(SYMBOLES_ALCHIMIQUES.keys()), k=random.randint(1, 5))
        topologies = random.sample(list(TOPOLOGIES_NARRATIVES.keys()), k=random.randint(0, 2))
        emotions = random.sample(list(EMOTIONS_PRIMAIRES.keys()), k=random.randint(1, 3))
        
        return MemeConfig(
            id="",
            couches=couches,
            archetypes=archetypes,
            biais=biais,
            symboles=symboles,
            topologies=topologies,
            emotions=emotions,
            generation=self.generation
        )
    
    def evaluate_fitness(self, meme: MemeConfig) -> float:
        """
        Évalue la fitness via SIMULATION réelle (pas juste un score statique)
        C'est ici que la magie opère: on simule vraiment la propagation!
        """
        # Créer un automate cellulaire
        automaton = MemeticCellularAutomaton(
            network_type=self.network_type,
            size=self.network_size
        )
        
        # Calculer une fitness statique de base (du GUI original)
        static_fitness = self._calculate_static_fitness(meme)
        meme.fitness = static_fitness  # Nécessaire pour la transmission
        
        # Injecter le mème et simuler
        automaton.infect_initial_node(meme)
        trajectory = automaton.simulate(max_steps=1000)
        
        # Analyser les résultats
        analysis = automaton.analyze_trajectory()
        meme.trajectory = trajectory
        meme.is_glider = automaton.is_glider()
        
        # Fitness finale = combinaison de critères
        if not analysis:
            return 0.0
        
        # Pondération des métriques
        fitness = (
            analysis['longevity'] * 0.3 +
            analysis['max_reach'] * 0.25 +
            analysis['stability'] * 100 * 0.25 +
            static_fitness * 0.2
        )
        
        # Bonus massif pour les gliders
        if meme.is_glider:
            fitness *= 1.5
        
        meme.fitness = fitness
        return fitness
    
    def _calculate_static_fitness(self, meme: MemeConfig) -> float:
        """Calcul de fitness statique (inspiré du GUI original)"""
        score = 0.0
        
        # Poids des archétypes
        for arch in meme.archetypes:
            score += ARCHETYPES_JUNGIENS[arch]['poids'] * 10
        
        # Nombre de biais (plus = mieux, jusqu'à un point)
        total_biais = sum(len(b) for b in meme.biais.values())
        score += min(total_biais * 5, 50)
        
        # Balance couches positives/négatives
        neg = sum(1 for c in meme.couches if c.startswith('-'))
        pos = len(meme.couches) - neg
        balance = abs(neg - pos)
        score += (10 - balance) * 2
        
        # Diversité émotionnelle
        score += len(meme.emotions) * 3
        
        return min(score, 100.0)
    
    def evolve_generation(self, verbose: bool = True) -> float:
        """
        Fait évoluer la population d'une génération.
        Retourne la meilleure fitness de cette génération.
        """
        # 1. ÉVALUATION (partie la plus coûteuse)
        if verbose:
            print(f"\n=== GÉNÉRATION {self.generation} ===")
            print("Évaluation de la population...")
        
        for i, meme in enumerate(self.population):
            if verbose and i % 20 == 0:
                print(f"  Évaluation {i}/{len(self.population)}...")
            self.evaluate_fitness(meme)
        
        # 2. TRI par fitness
        self.population.sort(key=lambda m: m.fitness, reverse=True)
        best_fitness = self.population[0].fitness
        self.best_fitness_history.append(best_fitness)
        
        if verbose:
            print(f"Meilleure fitness: {best_fitness:.2f}")
            print(f"Champion: {self.population[0].signature()}")
        
        # 3. SAUVEGARDE des gliders découverts
        for meme in self.population[:self.elite_size]:
            if meme.is_glider:
                glider_entry = {
                    'generation': self.generation,
                    'meme': meme,
                    'signature': meme.signature(),
                    'fitness': meme.fitness
                }
                self.gliders_discovered.append(glider_entry)
                if verbose:
                    print(f"  🚀 GLIDER DÉCOUVERT: {meme.signature()} (fitness: {meme.fitness:.2f})")
        
        # 4. SÉLECTION (top 20% survivent)
        survivors = self.population[:int(0.2 * self.population_size)]
        
        # 5. REPRODUCTION + MUTATION
        new_population = survivors.copy()  # Elite directe
        
        while len(new_population) < self.population_size:
            # Sélection des parents (avec biais vers les meilleurs)
            parent1 = self._tournament_selection(survivors)
            parent2 = self._tournament_selection(survivors)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child = self._crossover(parent1, parent2)
            else:
                child = parent1  # Clone
            
            # Mutation
            if random.random() < self.mutation_rate:
                child = self._mutate(child)
            
            child.generation = self.generation + 1
            child.fitness = 0.0  # Sera réévalué
            child.trajectory = []
            child.is_glider = False
            child.id = ""  # Sera régénéré
            
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
        
        return best_fitness
    
    def _tournament_selection(self, pool: List[MemeConfig], tournament_size: int = 3) -> MemeConfig:
        """Sélection par tournoi (favorise les bons sans éliminer la diversité)"""
        tournament = random.sample(pool, min(tournament_size, len(pool)))
        return max(tournament, key=lambda m: m.fitness)
    
    def _crossover(self, parent1: MemeConfig, parent2: MemeConfig) -> MemeConfig:
        """Croisement génétique entre deux parents"""
        child = MemeConfig(
            id="",
            # Mix aléatoire des couches
            couches=list(set(
                random.sample(parent1.couches, k=len(parent1.couches)//2) +
                random.sample(parent2.couches, k=len(parent2.couches)//2)
            ))[:6],  # Limite à 6
            
            # Mix des archétypes (garder max 3)
            archetypes=list(set(parent1.archetypes[:2] + parent2.archetypes[:2]))[:3],
            
            # Mix des biais
            biais={},
            
            # Mix des symboles
            symboles=list(set(
                random.sample(parent1.symboles, k=len(parent1.symboles)//2) +
                random.sample(parent2.symboles, k=len(parent2.symboles)//2)
            ))[:5],
            
            # Choisir une topologie au hasard
            topologies=random.choice([parent1.topologies, parent2.topologies]),
            
            # Mix des émotions
            emotions=list(set(parent1.emotions + parent2.emotions))[:3],
            
            generation=self.generation
        )
        
        # Biais: combiner les catégories des deux parents
        all_cats = set(list(parent1.biais.keys()) + list(parent2.biais.keys()))
        for cat in all_cats:
            if cat in parent1.biais and cat in parent2.biais:
                child.biais[cat] = list(set(parent1.biais[cat] + parent2.biais[cat]))[:3]
            elif cat in parent1.biais:
                child.biais[cat] = parent1.biais[cat]
            else:
                child.biais[cat] = parent2.biais[cat]
        
        return child
    
    def _mutate(self, meme: MemeConfig) -> MemeConfig:
        """Mutation aléatoire du mème"""
        # Mutation des archétypes (30% chance)
        if random.random() < 0.3 and meme.archetypes:
            idx = random.randint(0, len(meme.archetypes) - 1)
            meme.archetypes[idx] = random.choice(list(ARCHETYPES_JUNGIENS.keys()))
        
        # Mutation des couches (20% chance)
        if random.random() < 0.2:
            if random.random() < 0.5 and len(meme.couches) < 8:
                # Ajouter une couche
                new_couche = random.choice(list(COUCHES.keys()))
                if new_couche not in meme.couches:
                    meme.couches.append(new_couche)
            elif len(meme.couches) > 2:
                # Retirer une couche
                meme.couches.pop(random.randint(0, len(meme.couches) - 1))
        
        # Mutation des biais (25% chance)
        if random.random() < 0.25:
            if meme.biais:
                cat = random.choice(list(meme.biais.keys()))
                if random.random() < 0.5 and len(meme.biais[cat]) < 5:
                    # Ajouter un biais
                    new_bias = random.choice(BIAIS[cat])
                    if new_bias not in meme.biais[cat]:
                        meme.biais[cat].append(new_bias)
                elif len(meme.biais[cat]) > 1:
                    # Retirer un biais
                    meme.biais[cat].pop(random.randint(0, len(meme.biais[cat]) - 1))
        
        # Mutation des émotions (15% chance)
        if random.random() < 0.15:
            meme.emotions = random.sample(list(EMOTIONS_PRIMAIRES.keys()), k=random.randint(1, 3))
        
        return meme
    
    def run_evolution(self, num_generations: int, verbose: bool = True, save_interval: int = 10):
        """
        Lance l'évolution pour N générations.
        C'est ici que la magie du Prof se reproduit!
        """
        print(f"\n{'='*60}")
        print(f"LANCEMENT DE L'ÉVOLUTION MÉMÉTIQUE")
        print(f"{'='*60}")
        print(f"Population: {self.population_size}")
        print(f"Générations: {num_generations}")
        print(f"Réseau: {self.network_type} ({self.network_size} nœuds)")
        print(f"{'='*60}\n")
        
        for gen in range(num_generations):
            best_fitness = self.evolve_generation(verbose=verbose)
            
            # Sauvegarde périodique
            if (gen + 1) % save_interval == 0:
                self.save_checkpoint(f"evolution_gen_{gen+1}.json")
        
        print(f"\n{'='*60}")
        print(f"ÉVOLUTION TERMINÉE")
        print(f"{'='*60}")
        print(f"Gliders découverts: {len(self.gliders_discovered)}")
        print(f"Meilleure fitness finale: {self.best_fitness_history[-1]:.2f}")
        print(f"{'='*60}\n")
    
    def export_gliders_for_knime(self, filepath: str = "gliders_export.csv"):
        """
        Exporte les gliders découverts au format CSV pour KNIME.
        C'est le pont vers la Phase 3 de ton projet!
        """
        if not self.gliders_discovered:
            print("Aucun glider à exporter.")
            return
        
        records = []
        for entry in self.gliders_discovered:
            meme = entry['meme']
            
            # Extraire les features pour le ML
            bias_list = [b for liste in meme.biais.values() for b in liste]
            
            record = {
                'meme_id': meme.id,
                'signature': entry['signature'],
                'generation': entry['generation'],
                'fitness': entry['fitness'],
                
                # Biais (pad avec 0 si moins de 3)
                'bias_cat_1': list(meme.biais.keys())[0] if meme.biais else '',
                'bias_cat_2': list(meme.biais.keys())[1] if len(meme.biais) > 1 else '',
                'bias_cat_3': list(meme.biais.keys())[2] if len(meme.biais) > 2 else '',
                'num_biais': len(bias_list),
                
                # Archétypes
                'archetype_1': meme.archetypes[0] if meme.archetypes else '',
                'archetype_2': meme.archetypes[1] if len(meme.archetypes) > 1 else '',
                'num_archetypes': len(meme.archetypes),
                
                # Métriques de performance
                'max_reach': max(meme.trajectory) if meme.trajectory else 0,
                'longevity': len(meme.trajectory),
                'peak_time': meme.trajectory.index(max(meme.trajectory)) if meme.trajectory else 0,
                'stability': 1.0 / (1.0 + np.std(meme.trajectory[100:])) if len(meme.trajectory) > 100 else 0,
                
                # Couches
                'num_couches': len(meme.couches),
                'has_negative_couches': sum(1 for c in meme.couches if c.startswith('-')),
                'has_positive_couches': sum(1 for c in meme.couches if not c.startswith('-')),
                
                # Label
                'is_glider': 1
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        df.to_csv(filepath, index=False)
        print(f"✅ {len(records)} gliders exportés vers {filepath}")
        print(f"Prêt pour l'importation dans KNIME!")
    
    def save_checkpoint(self, filepath: str):
        """Sauvegarde l'état actuel de l'évolution"""
        checkpoint = {
            'generation': self.generation,
            'population_size': self.population_size,
            'best_fitness_history': self.best_fitness_history,
            'gliders_count': len(self.gliders_discovered),
            'gliders': [
                {
                    'generation': g['generation'],
                    'signature': g['signature'],
                    'fitness': g['fitness'],
                    'meme': g['meme'].to_dict()
                }
                for g in self.gliders_discovered
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        print(f"💾 Checkpoint sauvegardé: {filepath}")

# =============================================================================
# [VISUALISATION - Comme le Prof]
# =============================================================================

class GliderVisualizer:
    """Visualise la propagation type "Jeu de la Vie" """
    
    @staticmethod
    def animate_propagation(automaton: MemeticCellularAutomaton, filepath: str = None):
        """Animation de la propagation (comme le Jeu de la Vie du Prof)"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.patch.set_facecolor('black')
        
        # Position des nœuds (calculé une seule fois)
        pos = nx.spring_layout(automaton.network, seed=42)
        
        # Pour stocker les frames
        frames_data = []
        
        def update(frame):
            ax1.clear()
            ax2.clear()
            
            # Step de simulation
            infected_count = automaton.step()
            
            # Graph visualization
            colors = ['#00ff00' if automaton.state[n] is not None else '#1a1a1a' 
                      for n in automaton.network.nodes()]
            
            nx.draw(automaton.network, pos, 
                    node_color=colors, 
                    node_size=30,
                    edge_color='#333333',
                    width=0.5,
                    ax=ax1)
            
            ax1.set_facecolor('black')
            ax1.set_title(f'Propagation - Step {frame}', color='#00ff41', fontsize=16)
            
            # Trajectory plot
            if len(automaton.history) > 1:
                ax2.plot(automaton.history, color='#00ff41', linewidth=2)
                ax2.fill_between(range(len(automaton.history)), automaton.history, alpha=0.3, color='#00ff41')
            
            ax2.set_facecolor('black')
            ax2.set_xlabel('Time Step', color='#00ff41')
            ax2.set_ylabel('Nœuds Infectés', color='#00ff41')
            ax2.set_title(f'Infectés: {infected_count}/{automaton.size}', color='#ff00ff', fontsize=14)
            ax2.grid(True, alpha=0.2, color='#333333')
            ax2.tick_params(colors='#00ff41')
            
            # Arrêt si extinction
            if infected_count == 0:
                ani.event_source.stop()
        
        ani = animation.FuncAnimation(fig, update, frames=500, 
                                      interval=100, repeat=False)
        
        if filepath:
            ani.save(filepath, writer='pillow', fps=10)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_network_heatmap(automaton: MemeticCellularAutomaton, step: int = None):
        """Heatmap du réseau à un instant donné"""
        if step is not None and step < len(automaton.history):
            # Reconstruire l'état à ce step (simplifié)
            pass
        
        plt.figure(figsize=(12, 10))
        
        # Convertir le graphe en matrice d'adjacence
        adj_matrix = nx.to_numpy_array(automaton.network)
        
        # Identifier les nœuds infectés
        infected_nodes = [i for i, state in enumerate(automaton.state) if state is not None]
        
        # Créer une matrice d'infection
        infection_matrix = np.zeros_like(adj_matrix)
        for i in infected_nodes:
            infection_matrix[i, :] = adj_matrix[i, :]
            infection_matrix[:, i] = adj_matrix[:, i]
        
        plt.imshow(infection_matrix, cmap='hot', interpolation='nearest')
        plt.colorbar(label='Connexion avec nœud infecté')
        plt.title('Heatmap du Réseau d\'Infection', fontsize=14)
        plt.xlabel('Nœud ID')
        plt.ylabel('Nœud ID')
        plt.tight_layout()
        plt.show()

# =============================================================================
# [EXEMPLE D'UTILISATION - Script principal]
# =============================================================================

def main_evolution_experiment():
    """
    Exemple complet d'utilisation du système.
    Reproduit l'expérience du Prof!
    """
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  MEMETIC WARFARE - LABORATOIRE D'ÉVOLUTION                   ║
    ║  Reproduction de l'expérience du Prof (2018)                 ║
    ║  Lisp/Maxima → Python/NetworkX                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # === EXPÉRIENCE 1: Test d'un glider connu ===
    print("\n[EXPÉRIENCE 1] Test du glider '1-4-4-Trickster-Shadow'\n")
    
    # Recréer la configuration du glider légendaire du Prof
    glider_1_4_4 = MemeConfig(
        id="glider_1_4_4",
        couches=['1', '4', '4'],  # Les catégories de biais
        archetypes=['tricheur', 'ombre'],  # Trickster + Shadow
        biais={
            'classiques': ['confirmation', 'ancrage'],
            'narratifs': ['dissonance', 'vérité illusoire'],
            'spirituels': ['transcendance']
        },
        symboles=['ouroboros', 'dragon'],
        topologies=['monomythe'],
        emotions=['vertige_ontologique', 'fana']
    )
    
    # Simuler sa propagation
    print("Simulation de la propagation...")
    automaton = MemeticCellularAutomaton(network_type='small_world', size=500)
    automaton.infect_initial_node(glider_1_4_4)
    trajectory = automaton.simulate(max_steps=1000)
    
    analysis = automaton.analyze_trajectory()
    is_glider = automaton.is_glider()
    
    print(f"\nRÉSULTATS:")
    print(f"  Longévité: {analysis['longevity']} steps")
    print(f"  Portée max: {analysis['max_reach']}/{automaton.size} nœuds ({analysis['max_reach']/automaton.size*100:.1f}%)")
    print(f"  Stabilité: {analysis['stability']:.3f}")
    print(f"  Est un glider? {'✅ OUI' if is_glider else '❌ NON'}")
    
    # Visualiser
    GliderVisualizer.plot_glider_trajectories(
        type('obj', (object,), {
            'gliders_discovered': [{'meme': glider_1_4_4, 'signature': '1-4-4-Trickster-Shadow', 'generation': 0, 'fitness': 0}]
        })()
    )
    
    # === EXPÉRIENCE 2: Évolution génétique complète ===
    print("\n\n[EXPÉRIENCE 2] Évolution génétique sur 50 générations\n")
    print("⚠️  ATTENTION: Cette simulation peut prendre 15-30 minutes!")
    print("    Chaque génération évalue 100 mèmes via simulation complète.")
    
    response = input("\nLancer l'évolution complète? (o/n): ")
    
    if response.lower() == 'o':
        # Créer l'algorithme génétique
        ga = MemeticGeneticAlgorithm(
            population_size=50,  # Réduit pour demo (le Prof utilisait 100-200)
            network_type='small_world',
            network_size=300,  # Réduit pour vitesse
            mutation_rate=0.3,
            crossover_rate=0.7,
            elite_size=5
        )
        
        # Lancer l'évolution
        ga.run_evolution(
            num_generations=20,  # Réduit pour demo (le Prof faisait 1000+)
            verbose=True,
            save_interval=5
        )
        
        # Visualiser les résultats
        print("\n[VISUALISATIONS]")
        GliderVisualizer.plot_evolution_curve(ga, filepath='evolution_curve.png')
        GliderVisualizer.plot_glider_trajectories(ga)
        
        # Exporter pour KNIME
        ga.export_gliders_for_knime('gliders_for_knime.csv')
        
        # Afficher les champions
        print("\n[TOP 5 GLIDERS DÉCOUVERTS]")
        gliders = sorted(ga.gliders_discovered, key=lambda g: g['fitness'], reverse=True)[:5]
        for i, g in enumerate(gliders, 1):
            print(f"{i}. {g['signature']}")
            print(f"   Génération: {g['generation']}")
            print(f"   Fitness: {g['fitness']:.2f}")
            print(f"   Portée max: {max(g['meme'].trajectory)}")
            print()
    
    else:
        print("\nÉvolution annulée. Utilisez le mode test pour des expériences rapides.")
    
    # === EXPÉRIENCE 3: Comparaison de topologies de réseaux ===
    print("\n\n[EXPÉRIENCE 3] Comparaison des topologies de réseaux\n")
    
    test_meme = glider_1_4_4
    networks = ['small_world', 'scale_free', 'random', 'grid']
    results = {}
    
    for net_type in networks:
        print(f"Test sur réseau {net_type}...")
        automaton = MemeticCellularAutomaton(network_type=net_type, size=400)
        automaton.infect_initial_node(test_meme)
        trajectory = automaton.simulate(max_steps=500)
        analysis = automaton.analyze_trajectory()
        results[net_type] = analysis
    
    # Comparaison
    print("\n[COMPARAISON DES RÉSEAUX]")
    print(f"{'Réseau':<15} {'Longévité':<12} {'Portée Max':<12} {'Stabilité':<12}")
    print("-" * 60)
    for net_type, analysis in results.items():
        print(f"{net_type:<15} {analysis['longevity']:<12} {analysis['max_reach']:<12} {analysis['stability']:<12.3f}")
    
    print("\n" + "="*60)
    print("EXPÉRIENCES TERMINÉES")
    print("="*60)

# =============================================================================
# [MODE BATCH - Pour générer des datasets massifs]
# =============================================================================

def generate_training_dataset(
    num_memes: int = 1000,
    network_type: str = 'small_world',
    output_file: str = 'meme_training_data.csv'
):
    """
    Génère un large dataset de mèmes pour entraîner le modèle KNIME.
    Mélange de gliders et non-gliders.
    """
    print(f"\n[GÉNÉRATION DE DATASET]")
    print(f"Nombre de mèmes: {num_memes}")
    print(f"Réseau: {network_type}")
    print(f"Fichier de sortie: {output_file}\n")
    
    records = []
    
    for i in range(num_memes):
        if i % 100 == 0:
            print(f"Progression: {i}/{num_memes}...")
        
        # Générer un mème aléatoire
        meme = MemeConfig(
            id="",
            couches=random.sample(list(COUCHES.keys()), k=random.randint(2, 6)),
            archetypes=random.sample(list(ARCHETYPES_JUNGIENS.keys()), k=random.randint(1, 3)),
            biais={
                cat: random.sample(BIAIS[cat], k=random.randint(1, 3))
                for cat in random.sample(list(BIAIS.keys()), k=random.randint(2, 4))
            },
            symboles=random.sample(list(SYMBOLES_ALCHIMIQUES.keys()), k=random.randint(1, 5)),
            topologies=random.sample(list(TOPOLOGIES_NARRATIVES.keys()), k=random.randint(0, 2)),
            emotions=random.sample(list(EMOTIONS_PRIMAIRES.keys()), k=random.randint(1, 3))
        )
        
        # Simuler
        automaton = MemeticCellularAutomaton(network_type=network_type, size=300)
        
        # Fitness statique pour la simulation
        static_fitness = sum(ARCHETYPES_JUNGIENS[a]['poids'] * 10 for a in meme.archetypes)
        meme.fitness = static_fitness
        
        automaton.infect_initial_node(meme)
        trajectory = automaton.simulate(max_steps=500)
        analysis = automaton.analyze_trajectory()
        
        # Extraire features
        bias_cats = list(meme.biais.keys())
        bias_list = [b for liste in meme.biais.values() for b in liste]
        
        record = {
            'meme_id': meme.id or f"meme_{i}",
            'num_couches': len(meme.couches),
            'has_negative': sum(1 for c in meme.couches if c.startswith('-')),
            'has_positive': sum(1 for c in meme.couches if not c.startswith('-')),
            
            'num_archetypes': len(meme.archetypes),
            'archetype_1': meme.archetypes[0] if meme.archetypes else '',
            'archetype_2': meme.archetypes[1] if len(meme.archetypes) > 1 else '',
            'archetype_weight_sum': sum(ARCHETYPES_JUNGIENS[a]['poids'] for a in meme.archetypes),
            
            'num_bias_categories': len(meme.biais),
            'total_biases': len(bias_list),
            'bias_cat_1': bias_cats[0] if bias_cats else '',
            'bias_cat_2': bias_cats[1] if len(bias_cats) > 1 else '',
            
            'num_symbols': len(meme.symboles),
            'num_emotions': len(meme.emotions),
            
            'longevity': analysis.get('longevity', 0),
            'max_reach': analysis.get('max_reach', 0),
            'stability': analysis.get('stability', 0),
            'peak_time': analysis.get('peak_time', 0),
            'growth_rate': analysis.get('growth_rate', 0),
            
            'is_glider': 1 if automaton.is_glider() else 0
        }
        
        records.append(record)
    
    # Sauvegarder
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Dataset généré: {output_file}")
    print(f"Total: {len(records)} mèmes")
    print(f"Gliders: {df['is_glider'].sum()} ({df['is_glider'].sum()/len(records)*100:.1f}%)")
    print(f"Non-gliders: {len(records) - df['is_glider'].sum()}")
    
    return df

# =============================================================================
# [MAIN - Point d'entrée]
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║  MEMETIC WARFARE - SIMULATION CORE v1.0                      ║
    ║  Évolution darwinienne de mèmes weaponisés                   ║
    ║                                                               ║
    ║  Inspiré par le Prof de Maths (2018)                         ║
    ║  Lisp/Maxima → Python/NetworkX                               ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("\nMODES DISPONIBLES:")
    print("  1. Expériences guidées (test + évolution + comparaison)")
    print("  2. Génération de dataset massif pour KNIME")
    print("  3. Test rapide d'un glider spécifique")
    print("  4. Évolution personnalisée")
    
    try:
        choice = input("\nChoisir un mode (1-4): ").strip()
        
        if choice == '1':
            main_evolution_experiment()
        
        elif choice == '2':
            num = int(input("Nombre de mèmes à générer (500-5000): "))
            net = input("Type de réseau (small_world/scale_free/random/grid): ").strip()
            generate_training_dataset(num_memes=num, network_type=net)
        
        elif choice == '3':
            print("\n[TEST RAPIDE]")
            print("Simulation du glider légendaire 1-4-4-Trickster-Shadow...\n")
            
            glider = MemeConfig(
                id="test_glider",
                couches=['1', '4', '4'],
                archetypes=['tricheur', 'ombre'],
                biais={
                    'classiques': ['confirmation', 'ancrage'],
                    'narratifs': ['dissonance'],
                    'spirituels': ['fana']
                },
                symboles=['ouroboros'],
                topologies=['monomythe'],
                emotions=['vertige_ontologique']
            )
            
            automaton = MemeticCellularAutomaton(network_type='small_world', size=500)
            automaton.infect_initial_node(glider)
            trajectory = automaton.simulate(max_steps=1000)
            
            print(f"Longévité: {len(trajectory)} steps")
            print(f"Portée max: {max(trajectory)}/{automaton.size}")
            print(f"Est un glider? {'✅ OUI' if automaton.is_glider() else '❌ NON'}")
            
            # Plot simple
            plt.figure(figsize=(10, 6))
            plt.plot(trajectory, color='#00ff41', linewidth=2)
            plt.title('Trajectoire du Glider 1-4-4-Trickster-Shadow')
            plt.xlabel('Time Step')
            plt.ylabel('Nœuds Infectés')
            plt.grid(True, alpha=0.3)
            plt.show()
        
        elif choice == '4':
            pop_size = int(input("Taille de population (50-200): "))
            num_gen = int(input("Nombre de générations (10-100): "))
            
            ga = MemeticGeneticAlgorithm(
                population_size=pop_size,
                network_type='small_world',
                network_size=300
            )
            
            ga.run_evolution(num_generations=num_gen, verbose=True)
            ga.export_gliders_for_knime()
            
            GliderVisualizer.plot_evolution_curve(ga)
        
        else:
            print("Choix invalide.")
    
    except KeyboardInterrupt:
        print("\n\nInterruption utilisateur. Au revoir!")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    def plot_evolution_curve(ga: MemeticGeneticAlgorithm, filepath: str = None):
        """Courbe d'évolution de la fitness"""
        plt.figure(figsize=(12, 6))
        plt.plot(ga.best_fitness_history, linewidth=2, color='#00ff41')
        plt.xlabel('Génération', fontsize=12)
        plt.ylabel('Meilleure Fitness', fontsize=12)
        plt.title('Évolution de la Fitness au fil des Générations', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if filepath:
            plt.savefig(filepath, dpi=150, facecolor='#000000')
        plt.show()
    
    @staticmethod
    def plot_glider_trajectories(ga: MemeticGeneticAlgorithm, max_gliders: int = 5):
        """Plot des trajectoires des meilleurs gliders"""
        plt.figure(figsize=(14, 8))
        
        gliders = sorted(ga.gliders_discovered, key=lambda g: g['fitness'], reverse=True)[:max_gliders]
        
        for i, glider in enumerate(gliders):
            trajectory = glider['meme'].trajectory
            plt.plot(trajectory, label=f"{glider['signature']} (gen {glider['generation']})", linewidth=2)
        
        plt.xlabel('Time Step', fontsize=12)
        plt.ylabel('Nœuds Infectés', fontsize=12)
        plt.title(f'Trajectoires des {len(gliders)} Meilleurs Gliders', fontsize=14)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    @staticmethod