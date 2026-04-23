"""
INTEGRATION: GUI original + Moteur de simulation
Bridge entre l'interface de ton collègue et le moteur d'évolution
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
from datetime import datetime

# Import du GUI original
from memetic_warfare_gui_4c import (
    MemeticGUI_Omega, COUCHES, BIAIS, ARCHETYPES_JUNGIENS,
    SYMBOLES_ALCHIMIQUES, TOPOLOGIES_NARRATIVES, EMOTIONS_PRIMAIRES
)

# Import du moteur de simulation
from memetic_sim_core import (
    MemeConfig, MemeticCellularAutomaton, MemeticGeneticAlgorithm,
    GliderVisualizer, generate_training_dataset
)

class MemeticGUI_Enhanced(MemeticGUI_Omega):
    """
    Version améliorée du GUI avec intégration du moteur de simulation.
    Ajoute 2 nouveaux onglets: Simulation et Évolution
    """
    
    def __init__(self, root):
        # Appel au constructeur parent
        super().__init__(root)
        
        # Variables pour la simulation
        self.current_automaton = None
        self.current_ga = None
        self.simulation_running = False
        
        # Ajouter les nouveaux onglets
        self.add_simulation_tab()
        self.add_evolution_tab()
        
        # Modifier le titre
        self.root.title("MEMETIC WARFARE Ω • Édition Complète avec Simulation")
    
    def add_simulation_tab(self):
        """Onglet pour tester la propagation d'un mème unique"""
        tab_sim = ttk.Frame(self.root.nametowidget('.!notebook'))
        self.root.nametowidget('.!notebook').add(tab_sim, text="🔬 Simulation")
        
        # Frame de contrôle
        control_frame = ttk.LabelFrame(tab_sim, text="CONTRÔLES DE SIMULATION", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Paramètres de réseau
        ttk.Label(control_frame, text="Type de réseau:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.network_type_var = tk.StringVar(value='small_world')
        network_combo = ttk.Combobox(control_frame, textvariable=self.network_type_var, 
                                     values=['small_world', 'scale_free', 'random', 'grid', 'community'],
                                     state='readonly', width=20)
        network_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Taille du réseau:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.network_size_var = tk.StringVar(value='500')
        ttk.Entry(control_frame, textvariable=self.network_size_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Steps max:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.max_steps_var = tk.StringVar(value='1000')
        ttk.Entry(control_frame, textvariable=self.max_steps_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        
        # Boutons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="▶ SIMULER PROPAGATION", 
                  command=self.run_simulation).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📊 VISUALISER TRAJECTOIRE", 
                  command=self.visualize_trajectory).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🎬 ANIMATION", 
                  command=self.animate_propagation).pack(side='left', padx=5)
        
        # Zone de résultats
        results_frame = ttk.LabelFrame(tab_sim, text="RÉSULTATS DE SIMULATION", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.sim_output = tk.Text(results_frame, bg="#050505", fg="#00ff41", 
                                  font=("Consolas", 10), wrap=tk.WORD)
        self.sim_output.pack(fill='both', expand=True)
    
    def add_evolution_tab(self):
        """Onglet pour l'évolution génétique"""
        tab_evo = ttk.Frame(self.root.nametowidget('.!notebook'))
        self.root.nametowidget('.!notebook').add(tab_evo, text="🧬 Évolution")
        
        # Frame de contrôle
        control_frame = ttk.LabelFrame(tab_evo, text="PARAMÈTRES D'ÉVOLUTION", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Paramètres GA
        ttk.Label(control_frame, text="Taille population:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.pop_size_var = tk.StringVar(value='50')
        ttk.Entry(control_frame, textvariable=self.pop_size_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Nombre de générations:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.num_gen_var = tk.StringVar(value='20')
        ttk.Entry(control_frame, textvariable=self.num_gen_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Taux de mutation:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.mutation_var = tk.StringVar(value='0.3')
        ttk.Entry(control_frame, textvariable=self.mutation_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Taux de crossover:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.crossover_var = tk.StringVar(value='0.7')
        ttk.Entry(control_frame, textvariable=self.crossover_var, width=10).grid(row=1, column=3, padx=5, pady=5)
        
        # Boutons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="🚀 LANCER ÉVOLUTION", 
                  command=self.run_evolution).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="⏸ ARRÊTER", 
                  command=self.stop_evolution).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="💾 EXPORTER GLIDERS (CSV)", 
                  command=self.export_gliders).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📈 COURBE ÉVOLUTION", 
                  command=self.plot_evolution).pack(side='left', padx=5)
        
        # Zone de log
        log_frame = ttk.LabelFrame(tab_evo, text="LOG D'ÉVOLUTION", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.evo_output = tk.Text(log_frame, bg="#050505", fg="#ff00ff", 
                                  font=("Consolas", 9), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, command=self.evo_output.yview)
        self.evo_output.configure(yscrollcommand=scrollbar.set)
        
        self.evo_output.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def get_current_meme_config(self) -> MemeConfig:
        """Extrait la configuration actuelle du GUI et la convertit en MemeConfig"""
        selected_couches = [k for k, v in self.couches_var.items() if v.get()]
        selected_biais = {cat: [b for b in liste if self.biais_var[b].get()] 
                         for cat, liste in BIAIS.items()}
        selected_biais = {k: v for k, v in selected_biais.items() if v}  # Retirer vides
        selected_archetypes = [k for k, v in self.archetypes_var.items() if v.get()]
        selected_symboles = [k for k, v in self.symboles_var.items() if v.get()]
        selected_topologies = [k for k, v in self.topologies_var.items() if v.get()]
        selected_emotions = [k for k, v in self.emotions_var.items() if v.get()]
        
        if not selected_couches or not selected_archetypes:
            raise ValueError("Sélectionnez au moins 1 couche et 1 archétype")
        
        return MemeConfig(
            id="",
            couches=selected_couches,
            archetypes=selected_archetypes,
            biais=selected_biais,
            symboles=selected_symboles,
            topologies=selected_topologies,
            emotions=selected_emotions
        )
    
    def run_simulation(self):
        """Lance la simulation d'un mème unique"""
        try:
            meme = self.get_current_meme_config()
            network_type = self.network_type_var.get()
            network_size = int(self.network_size_var.get())
            max_steps = int(self.max_steps_var.get())
            
            self.sim_output.insert(tk.END, f"\n{'='*60}\n")
            self.sim_output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] DÉMARRAGE SIMULATION\n")
            self.sim_output.insert(tk.END, f"{'='*60}\n")
            self.sim_output.insert(tk.END, f"Réseau: {network_type} ({network_size} nœuds)\n")
            self.sim_output.insert(tk.END, f"Mème: {meme.signature()}\n\n")
            self.sim_output.see(tk.END)
            
            # Lancer en thread pour ne pas bloquer l'UI
            def simulate():
                # Créer l'automate
                automaton = MemeticCellularAutomaton(
                    network_type=network_type,
                    size=network_size
                )
                
                # Calculer fitness statique pour la transmission
                static_fitness = sum(ARCHETYPES_JUNGIENS[a]['poids'] * 10 for a in meme.archetypes)
                meme.fitness = static_fitness
                
                # Simuler
                automaton.infect_initial_node(meme)
                trajectory = automaton.simulate(max_steps=max_steps)
                
                # Analyser
                analysis = automaton.analyze_trajectory()
                is_glider = automaton.is_glider()
                
                # Stocker pour visualisation
                self.current_automaton = automaton
                
                # Afficher résultats
                self.root.after(0, lambda: self._display_simulation_results(analysis, is_glider))
            
            threading.Thread(target=simulate, daemon=True).start()
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la simulation: {e}")
    
    def _display_simulation_results(self, analysis, is_glider):
        """Affiche les résultats de simulation dans le GUI"""
        self.sim_output.insert(tk.END, "RÉSULTATS:\n")
        self.sim_output.insert(tk.END, f"  Longévité: {analysis['longevity']} steps\n")
        self.sim_output.insert(tk.END, f"  Portée maximale: {analysis['max_reach']} nœuds\n")
        self.sim_output.insert(tk.END, f"  Pic atteint à: step {analysis['peak_time']}\n")
        self.sim_output.insert(tk.END, f"  Stabilité: {analysis['stability']:.3f}\n")
        self.sim_output.insert(tk.END, f"  Taux de croissance: {analysis['growth_rate']:.2f} nœuds/step\n")
        self.sim_output.insert(tk.END, f"\n  {'🚀 C\'EST UN GLIDER!' if is_glider else '❌ Pas un glider'}\n")
        self.sim_output.insert(tk.END, f"{'='*60}\n\n")
        self.sim_output.see(tk.END)
    
    def visualize_trajectory(self):
        """Affiche la trajectoire du dernier mème simulé"""
        if self.current_automaton is None:
            messagebox.showwarning("Attention", "Lancez d'abord une simulation!")
            return
        
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.plot(self.current_automaton.history, color='#00ff41', linewidth=2)
        plt.fill_between(range(len(self.current_automaton.history)), 
                        self.current_automaton.history, alpha=0.3, color='#00ff41')
        plt.xlabel('Time Step', fontsize=12)
        plt.ylabel('Nœuds Infectés', fontsize=12)
        plt.title('Trajectoire de Propagation du Mème', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def animate_propagation(self):
        """Lance l'animation de propagation"""
        if self.current_automaton is None:
            messagebox.showwarning("Attention", "Lancez d'abord une simulation!")
            return
        
        # Recréer une nouvelle simulation pour l'animation
        try:
            meme = self.get_current_meme_config()
            network_type = self.network_type_var.get()
            network_size = int(self.network_size_var.get())
            
            automaton = MemeticCellularAutomaton(
                network_type=network_type,
                size=min(network_size, 200)  # Limiter pour performance
            )
            
            static_fitness = sum(ARCHETYPES_JUNGIENS[a]['poids'] * 10 for a in meme.archetypes)
            meme.fitness = static_fitness
            automaton.infect_initial_node(meme)
            
            # Lancer l'animation
            GliderVisualizer.animate_propagation(automaton)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'animation: {e}")
    
    def run_evolution(self):
        """Lance l'évolution génétique"""
        try:
            pop_size = int(self.pop_size_var.get())
            num_gen = int(self.num_gen_var.get())
            mutation_rate = float(self.mutation_var.get())
            crossover_rate = float(self.crossover_var.get())
            network_type = self.network_type_var.get()
            
            self.evo_output.insert(tk.END, f"\n{'='*60}\n")
            self.evo_output.insert(tk.END, f"DÉMARRAGE ÉVOLUTION GÉNÉTIQUE\n")
            self.evo_output.insert(tk.END, f"{'='*60}\n")
            self.evo_output.insert(tk.END, f"Population: {pop_size}\n")
            self.evo_output.insert(tk.END, f"Générations: {num_gen}\n")
            self.evo_output.insert(tk.END, f"⚠️  Ceci peut prendre plusieurs minutes...\n\n")
            self.evo_output.see(tk.END)
            
            self.simulation_running = True
            
            def evolve():
                # Créer l'algorithme génétique
                ga = MemeticGeneticAlgorithm(
                    population_size=pop_size,
                    network_type=network_type,
                    network_size=300,  # Fixe pour vitesse
                    mutation_rate=mutation_rate,
                    crossover_rate=crossover_rate
                )
                
                # Évolution avec callback pour log
                for gen in range(num_gen):
                    if not self.simulation_running:
                        self.root.after(0, lambda: self.evo_output.insert(tk.END, "\n❌ ÉVOLUTION ARRÊTÉE\n"))
                        break
                    
                    best_fitness = ga.evolve_generation(verbose=False)
                    
                    # Log dans le GUI
                    log_msg = f"[Gen {ga.generation}] Best fitness: {best_fitness:.2f}"
                    if ga.gliders_discovered and ga.gliders_discovered[-1]['generation'] == ga.generation - 1:
                        log_msg += f" 🚀 GLIDER DÉCOUVERT!"
                    log_msg += "\n"
                    
                    self.root.after(0, lambda msg=log_msg: self.evo_output.insert(tk.END, msg))
                    self.root.after(0, lambda: self.evo_output.see(tk.END))
                
                # Stocker pour export
                self.current_ga = ga
                
                # Résumé final
                summary = f"\n{'='*60}\n"
                summary += f"ÉVOLUTION TERMINÉE\n"
                summary += f"{'='*60}\n"
                summary += f"Gliders découverts: {len(ga.gliders_discovered)}\n"
                summary += f"Meilleure fitness finale: {ga.best_fitness_history[-1]:.2f}\n"
                summary += f"{'='*60}\n\n"
                
                self.root.after(0, lambda: self.evo_output.insert(tk.END, summary))
                self.root.after(0, lambda: self.evo_output.see(tk.END))
                self.root.after(0, lambda: messagebox.showinfo("Terminé", 
                    f"Évolution terminée!\n{len(ga.gliders_discovered)} gliders découverts."))
            
            threading.Thread(target=evolve, daemon=True).start()
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Paramètres invalides: {e}")
    
    def stop_evolution(self):
        """Arrête l'évolution en cours"""
        self.simulation_running = False
    
    def export_gliders(self):
        """Exporte les gliders vers CSV pour KNIME"""
        if self.current_ga is None:
            messagebox.showwarning("Attention", "Lancez d'abord une évolution!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="gliders_export.csv"
        )
        
        if filepath:
            try:
                self.current_ga.export_gliders_for_knime(filepath)
                messagebox.showinfo("Succès", f"Gliders exportés vers:\n{filepath}\n\nPrêt pour KNIME!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur d'export: {e}")
    
    def plot_evolution(self):
        """Affiche la courbe d'évolution"""
        if self.current_ga is None:
            messagebox.showwarning("Attention", "Lancez d'abord une évolution!")
            return
        
        GliderVisualizer.plot_evolution_curve(self.current_ga)

# =============================================================================
# [LANCEMENT]
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeticGUI_Enhanced(root)
    root.mainloop()