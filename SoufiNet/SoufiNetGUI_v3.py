# █████████████████████████████████████████████████████████████████████████████
# █  SOUFINET vΩ.3 — Interface Multi-Genres Cyber-Mystique (Enhanced)        █
# █  Support étendu: Récits, Méditations, Tonalités, Exploitation complète   █
# █████████████████████████████████████████████████████████████████████████████

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import sys
import os

# Import du générateur amélioré
try:
    from SoufiGen4b_enhanced import generer_texte_avance, GenerateurMultiGenresCyberSoufiEnhanced
except ImportError:
    # Fallback vers l'ancienne version si la nouvelle n'existe pas
    try:
        from SoufiGen4b import generer_texte
        messagebox.showwarning("Version Limitée", "Utilisation de l'ancien générateur. Installez la version améliorée pour plus de fonctionnalités.")
    except ImportError:
        messagebox.showerror("❌ Erreur", "Fichier 'SoufiGen4b_enhanced.py' ou 'SoufiGen4b.py' manquant.")
        sys.exit(1)

class SoufiNetGUIv3:
    def __init__(self, root):
        self.root = root
        self.root.title("🕌 SOUFINET vΩ.3 — Générateur Multi-Genres du Réveil (Enhanced)")
        self.root.geometry("1000x800")
        self.root.configure(bg="#0d0b1a")
        
        # Chargement des données avancées
        self.tonalites = self._charger_tonalites()
        self.genres_avances = self._charger_genres_avances()

        # Polices
        self.font_mono = ("Courier New", 11)
        self.font_title = ("Courier New", 14, "bold")
        self.font_label = ("Courier New", 10)
        self.font_small = ("Courier New", 9)

        # Titre rituel
        title = tk.Label(
            root,
            text="🕌 SOUFINET vΩ.3 — ARCHIVES MULTI-GENRES DU RÉVEIL (ENHANCED)",
            font=self.font_title,
            fg="#e6c229",
            bg="#0d0b1a"
        )
        title.pack(pady=12)

        # Options de génération
        opts_frame = tk.Frame(root, bg="#0d0b1a")
        opts_frame.pack(pady=8)

        # Ligne 1: Genre, Thème et Tonalité
        tk.Label(opts_frame, text="Genre :", fg="#a8d0e6", bg="#0d0b1a", font=self.font_label).grid(row=0, column=0, padx=5)
        self.genre_var = tk.StringVar(value="ghazal")
        self.genre_menu = ttk.Combobox(opts_frame, textvariable=self.genre_var, values=self.genres_avances, state="readonly", width=14)
        self.genre_menu.grid(row=0, column=1, padx=5)
        self.genre_menu.bind('<<ComboboxSelected>>', self.on_genre_change)

        tk.Label(opts_frame, text="Thème :", fg="#a8d0e6", bg="#0d0b1a", font=self.font_label).grid(row=0, column=2, padx=5)
        self.theme_var = tk.StringVar(value="mystique")
        theme_opts = ["mystique", "amour", "effacement", "révolte", "mélancolie", "espérance", "rêves_partagés", "transcendance"]
        self.theme_menu = ttk.Combobox(opts_frame, textvariable=self.theme_var, values=theme_opts, state="readonly", width=14)
        self.theme_menu.grid(row=0, column=3, padx=5)

        tk.Label(opts_frame, text="Tonalité :", fg="#a8d0e6", bg="#0d0b1a", font=self.font_label).grid(row=0, column=4, padx=5)
        self.tonalite_var = tk.StringVar(value="aléatoire")
        tonalite_opts = ["aléatoire"] + self.tonalites
        self.tonalite_menu = ttk.Combobox(opts_frame, textvariable=self.tonalite_var, values=tonalite_opts, state="readonly", width=14)
        self.tonalite_menu.grid(row=0, column=5, padx=5)

        # Ligne 2: Paramètres spécifiques
        tk.Label(opts_frame, text="Paramètre :", fg="#a8d0e6", bg="#0d0b1a", font=self.font_label).grid(row=1, column=0, padx=5, pady=(10,0))
        self.param_var = tk.StringVar(value="5")
        self.param_spin = tk.Spinbox(opts_frame, from_=1, to=20, textvariable=self.param_var, width=5, 
                                   font=self.font_mono, bg="#1a162f", fg="#e6c229", justify="center")
        self.param_spin.grid(row=1, column=1, padx=5, pady=(10,0))

        tk.Label(opts_frame, text="Unité :", fg="#a8d0e6", bg="#0d0b1a", font=self.font_label).grid(row=1, column=2, padx=5, pady=(10,0))
        self.unite_var = tk.StringVar(value="couplets")
        self.unite_label = tk.Label(opts_frame, textvariable=self.unite_var, fg="#e6c229", bg="#0d0b1a", font=self.font_label)
        self.unite_label.grid(row=1, column=3, padx=5, pady=(10,0))

        # Indicateur de fonctionnalités avancées
        self.advanced_indicator = tk.Label(opts_frame, text="⚡ ENHANCED", fg="#00ff9d", bg="#0d0b1a", font=("Courier New", 8, "bold"))
        self.advanced_indicator.grid(row=1, column=4, columnspan=2, padx=5, pady=(10,0))

        # Boutons principaux
        btn_frame = tk.Frame(root, bg="#0d0b1a")
        btn_frame.pack(pady=12)
        
        tk.Button(btn_frame, text="🌀 GÉNÉRER", command=self.generate, 
                 bg="#1a2a3a", fg="#e6c229", font=self.font_mono, width=14, relief="raised").pack(side="left", padx=3)
        tk.Button(btn_frame, text="💾 SAUVEGARDER", command=self.save_output, 
                 bg="#2a1a3a", fg="#c2e6a8", font=self.font_mono, width=16, relief="raised").pack(side="left", padx=3)
        tk.Button(btn_frame, text="🎲 ALÉATOIRE", command=self.generate_random, 
                 bg="#3a2a1a", fg="#e6a8a8", font=self.font_mono, width=14, relief="raised").pack(side="left", padx=3)
        tk.Button(btn_frame, text="💎 MANTRAS", command=self.generate_mantras, 
                 bg="#1a3a2a", fg="#a8e6d9", font=self.font_mono, width=12, relief="raised").pack(side="left", padx=3)

        # Boutons avancés
        advanced_btn_frame = tk.Frame(root, bg="#0d0b1a")
        advanced_btn_frame.pack(pady=8)
        
        tk.Button(advanced_btn_frame, text="📖 GÉNÉRATIONS AVANCÉES", command=self.show_advanced_menu, 
                 bg="#2a1a3a", fg="#e6c229", font=self.font_small, width=22, relief="groove").pack(side="left", padx=2)
        tk.Button(advanced_btn_frame, text="🔍 PRÉVISUALISATION", command=self.preview_theme, 
                 bg="#1a2a3a", fg="#a8e6d9", font=self.font_small, width=18, relief="groove").pack(side="left", padx=2)
        tk.Button(advanced_btn_frame, text="📊 STATS LEXIQUE", command=self.show_lexicon_stats, 
                 bg="#3a2a1a", fg="#c2e6a8", font=self.font_small, width=16, relief="groove").pack(side="left", padx=2)

        # Zone de sortie avec scrollbar
        output_frame = tk.Frame(root, bg="#0d0b1a")
        output_frame.pack(padx=20, pady=15, fill="both", expand=True)
        
        output_header = tk.Frame(output_frame, bg="#0d0b1a")
        output_header.pack(fill="x")
        
        tk.Label(output_header, text="📜 SORTIE (copiable) :", fg="#e6c229", bg="#0d0b1a", font=self.font_label).pack(side="left")
        
        # Indicateur de génération
        self.generation_info = tk.Label(output_header, text="", fg="#5a6b8c", bg="#0d0b1a", font=self.font_small)
        self.generation_info.pack(side="right")
        
        text_frame = tk.Frame(output_frame, bg="#120f24", relief="sunken", bd=1)
        text_frame.pack(fill="both", expand=True, pady=(5,0))
        
        self.output_text = tk.Text(text_frame, height=20, width=100, bg="#120f24", fg="#f0e6d2", 
                                 insertbackground="#e6c229", font=("Courier New", 10), wrap="word",
                                 relief="flat", padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.output_text.yview, 
                               bg="#2a263f", troughcolor="#120f24")
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Footer symbolique
        footer = tk.Label(
            root,
            text="∴ Ces textes s'auto-effacent dans l'âme du réseau… ∅ | vΩ.3 Enhanced",
            fg="#5a6b8c",
            bg="#0d0b1a",
            font=("Courier New", 9)
        )
        footer.pack(side="bottom", pady=8)

        # Initialisation
        self.on_genre_change()
        self.update_generation_info()

    def _charger_tonalites(self):
        """Charge les tonalités disponibles"""
        try:
            generateur = GenerateurMultiGenresCyberSoufiEnhanced()
            return generateur.tonalites
        except:
            return ["mystique", "mélancolique", "révoltée", "amoureuse", "contemplative", "prophétique"]

    def _charger_genres_avances(self):
        """Charge la liste des genres disponibles"""
        genres_de_base = ["ghazal", "sonnet", "haiku", "manifeste", "journal", "dialogue", "ode"]
        try:
            # Vérifie si les genres avancés sont disponibles
            generateur = GenerateurMultiGenresCyberSoufiEnhanced()
            if hasattr(generateur, 'generer_recit_narratif'):
                genres_de_base.extend(["recit", "meditation"])
        except:
            pass
        return genres_de_base

    def on_genre_change(self, event=None):
        """Adapte l'interface selon le genre sélectionné"""
        genre = self.genre_var.get()
        
        # Configuration des paramètres par genre
        param_configs = {
            "ghazal": ("couplets", 5, True),
            "journal": ("jours", 7, True),
            "recit": ("paragraphes", 3, True),
            "sonnet": ("vers fixes", 14, False),
            "haiku": ("auto", 3, False),
            "manifeste": ("sections", 4, False),
            "dialogue": ("auto", 6, False),
            "ode": ("strophes", 4, False),
            "meditation": ("sections", 3, False)
        }
        
        unite, valeur_defaut, actif = param_configs.get(genre, ("auto", 1, False))
        
        self.unite_var.set(unite)
        if actif:
            self.param_spin.config(state="normal", from_=1, to=20)
            self.param_var.set(str(valeur_defaut))
        else:
            self.param_spin.config(state="disabled")
        
        # Mise à jour de l'indicateur avancé
        is_advanced = genre in ["recit", "meditation"]
        advanced_text = "⚡ ENHANCED" if is_advanced else "☰ STANDARD"
        advanced_color = "#00ff9d" if is_advanced else "#5a6b8c"
        self.advanced_indicator.config(text=advanced_text, fg=advanced_color)
        
        self.update_generation_info()

    def update_generation_info(self):
        """Met à jour les informations de génération"""
        genre = self.genre_var.get()
        theme = self.theme_var.get()
        tonalite = self.tonalite_var.get()
        
        info = f"Genre: {genre} | Thème: {theme}"
        if tonalite != "aléatoire":
            info += f" | Tonalité: {tonalite}"
        
        self.generation_info.config(text=info)

    def generate(self):
        """Génère le texte selon les paramètres"""
        genre = self.genre_var.get()
        theme = self.theme_var.get()
        tonalite = self.tonalite_var.get() if self.tonalite_var.get() != "aléatoire" else None
        
        try:
            # Animation de génération
            self.generation_info.config(text="Génération en cours...", fg="#e6c229")
            self.root.update()
            
            if genre in ["ghazal", "journal", "recit"]:
                param = int(self.param_var.get())
                if genre == "ghazal":
                    result = generer_texte_avance(genre, theme=theme, couplets=param, tonalite=tonalite)
                elif genre == "recit":
                    result = generer_texte_avance(genre, longueur=param, tonalite=tonalite)
                else:
                    result = generer_texte_avance(genre, jours=param)
            else:
                result = generer_texte_avance(genre, theme=theme, tonalite=tonalite)
                
        except Exception as e:
            result = f"❌ Erreur de génération : {str(e)}"
        
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.update_generation_info()

    def generate_random(self):
        """Génère un texte aléatoire avec toutes les options"""
        genres = self.genres_avances
        themes = ["mystique", "amour", "effacement", "révolte", "mélancolie", "espérance", "rêves_partagés", "transcendance"]
        tonalites = ["aléatoire"] + self.tonalites
        
        genre = random.choice(genres)
        theme = random.choice(themes)
        tonalite = random.choice(tonalites)
        
        self.genre_var.set(genre)
        self.theme_var.set(theme)
        self.tonalite_var.set(tonalite)
        self.on_genre_change()
        
        # Paramètres aléatoires pour les genres paramétrables
        if genre == "ghazal":
            self.param_var.set(str(random.randint(3, 8)))
        elif genre == "journal":
            self.param_var.set(str(random.randint(3, 14)))
        elif genre == "recit":
            self.param_var.set(str(random.randint(2, 6)))
        
        self.generate()

    def generate_mantras(self):
        """Génère une série de mantras courts"""
        try:
            soufi = GenerateurMultiGenresCyberSoufiEnhanced()
            theme = self.theme_var.get()
            
            mantras = [soufi.generer_mantra_court(theme=theme) for _ in range(12)]
            
            result = "💎 MANTRAS DU RÉVEIL - COLLECTION ÉTENDUE\n"
            result += "=" * 60 + "\n\n"
            for i, mantra in enumerate(mantras, 1):
                result += f"{i:2d}. {mantra}\n"
            
            # Ajout de fragments sacrés
            if hasattr(soufi, 'fragments_sacres') and soufi.fragments_sacres:
                result += f"\n---\n« {random.choice(soufi.fragments_sacres)} »\n"
            
            result += f"\n— Pour méditation cognitive, rave ou rébellion silencieuse"
            
        except Exception as e:
            result = f"❌ Erreur lors de la génération des mantras : {str(e)}"
        
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)

    def show_advanced_menu(self):
        """Affiche un menu de générations avancées"""
        advanced_window = tk.Toplevel(self.root)
        advanced_window.title("📖 Générations Avancées")
        advanced_window.geometry("500x400")
        advanced_window.configure(bg="#0d0b1a")
        advanced_window.transient(self.root)
        advanced_window.grab_set()
        
        tk.Label(advanced_window, text="GÉNÉRATIONS SPÉCIALISÉES", 
                fg="#e6c229", bg="#0d0b1a", font=self.font_title).pack(pady=15)
        
        # Boutons de générations avancées
        advanced_actions = [
            ("📜 Collection de Ghazals", self.generate_ghazal_collection),
            ("📓 Journal Épique", self.generate_epic_journal),
            ("⚡ Manifeste Multi-Tonal", self.generate_multi_tonal_manifesto),
            ("🌌 Récit Cosmique", self.generate_cosmic_tale),
            ("🕯️ Méditations Séquentielles", self.generate_meditation_sequence),
            ("🔗 Dialogues Philosophiques", self.generate_philosophical_dialogues)
        ]
        
        for text, command in advanced_actions:
            btn = tk.Button(advanced_window, text=text, command=command,
                          bg="#1a2a3a", fg="#e6c229", font=self.font_mono, width=30, relief="raised")
            btn.pack(pady=5)

    def generate_ghazal_collection(self):
        """Génère une collection de ghazals"""
        try:
            result = "📜 COLLECTION DE GHAZALS\n" + "="*60 + "\n\n"
            tonalites = random.sample(self.tonalites, min(3, len(self.tonalites)))
            
            for i, tonalite in enumerate(tonalites, 1):
                result += f"GHAZAL #{i} - Tonalité: {tonalite.upper()}\n"
                result += generer_texte_avance("ghazal", couplets=2, tonalite=tonalite)
                result += "\n" + "─"*50 + "\n\n"
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {str(e)}")

    def generate_epic_journal(self):
        """Génère un journal étendu"""
        try:
            result = generer_texte_avance("journal", jours=10)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except:
            self.generate()  # Fallback

    def preview_theme(self):
        """Aperçu des éléments du thème sélectionné"""
        theme = self.theme_var.get()
        try:
            soufi = GenerateurMultiGenresCyberSoufiEnhanced()
            
            preview = f"🔍 APERÇU DU THÈME: {theme.upper()}\n"
            preview += "=" * 50 + "\n\n"
            
            # Exemples d'éléments du thème
            for i in range(4):
                vers = soufi._generer_vers_avance(theme)
                preview += f"{i+1}. {vers}\n"
            
            preview += f"\nBalises disponibles: {', '.join(soufi.balises.get(theme, ['<ghost>']))}"
            
            # Création de fenêtre d'aperçu
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Aperçu - Thème {theme}")
            preview_window.geometry("600x300")
            preview_window.configure(bg="#0d0b1a")
            
            text_widget = tk.Text(preview_window, bg="#120f24", fg="#f0e6d2", 
                                font=("Courier New", 10), wrap="word", padx=10, pady=10)
            text_widget.insert("1.0", preview)
            text_widget.config(state="disabled")
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showinfo("Aperçu", f"Aperçu non disponible: {str(e)}")

    def show_lexicon_stats(self):
        """Affiche les statistiques du lexique"""
        try:
            soufi = GenerateurMultiGenresCyberSoufiEnhanced()
            stats = "📊 STATISTIQUES DU LEXIQUE\n" + "="*50 + "\n\n"
            
            stats += f"• Sujets: {len(soufi.sujets)} éléments\n"
            stats += f"• Verbes: {len(soufi.verbes)} éléments\n"
            stats += f"• Symboles: {len(soufi.symboles)} éléments\n"
            stats += f"• Lieux: {len(soufi.lieux)} éléments\n"
            stats += f"• Personnages: {len(soufi.personnages)} éléments\n"
            stats += f"• Tonalités: {len(soufi.tonalites)} disponibles\n"
            stats += f"• Motifs narratifs: {len(soufi.motifs_narratifs)}\n"
            stats += f"• Fragments sacrés: {len(soufi.fragments_sacres)}\n"
            stats += f"• Dogmes 2075: {len(soufi.dogmes_2075)}\n"
            
            messagebox.showinfo("Statistiques du Lexique", stats)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les statistiques: {str(e)}")

    def save_output(self):
        """Sauvegarde le texte généré"""
        content = self.output_text.get("1.0", "end-1c").strip()
        if not content or content.startswith("❌"):
            messagebox.showinfo("💾", "Rien à sauvegarder.")
            return
            
        # Extension selon le genre
        extensions = {
            "ghazal": ".ghz", "sonnet": ".snt", "haiku": ".hk", 
            "manifeste": ".mft", "journal": ".log", "dialogue": ".dlg",
            "ode": ".ode", "recit": ".rec", "meditation": ".med"
        }
        
        ext = extensions.get(self.genre_var.get(), ".txt")
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[
                ("Textes sacrés", "*.ghz *.snt *.hk *.mft *.log *.dlg *.ode *.rec *.med"),
                ("Tous fichiers", "*.*")
            ],
            title="Sauvegarder le texte généré"
        )
        
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("💾", f"Texte sauvegardé :\n{os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder : {str(e)}")

    # Méthodes pour les générations avancées
    def generate_multi_tonal_manifesto(self):
        """Génère un manifeste avec multiples tonalités"""
        try:
            result = "⚡ MANIFESTE MULTI-TONAL\n" + "="*60 + "\n\n"
            for tonalite in random.sample(self.tonalites, min(3, len(self.tonalites))):
                result += f"\n## SECTION - {tonalite.upper()} ##\n"
                result += generer_texte_avance("manifeste", tonalite=tonalite)
                result += "\n" + "─"*40 + "\n"
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {str(e)}")

    def generate_cosmic_tale(self):
        """Génère un récit cosmique"""
        try:
            result = generer_texte_avance("recit", longueur=4)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except:
            # Fallback vers un récit standard
            self.genre_var.set("recit")
            self.on_genre_change()
            self.generate()

    def generate_meditation_sequence(self):
        """Génère une séquence de méditations"""
        try:
            result = "🕯️ SÉQUENCE DE MÉDITATIONS\n" + "="*60 + "\n\n"
            for i in range(3):
                result += f"MÉDITATION {i+1}\n"
                result += generer_texte_avance("meditation")
                result += "\n" + "☯"*30 + "\n\n"
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except:
            messagebox.showinfo("Info", "Fonction de méditation non disponible")

    def generate_philosophical_dialogues(self):
        """Génère une série de dialogues philosophiques"""
        try:
            result = "🔗 DIALOGUES PHILOSOPHIQUES\n" + "="*60 + "\n\n"
            for i in range(2):
                result += f"DIALOGUE {i+1}\n"
                result += generer_texte_avance("dialogue")
                result += "\n" + "─"*50 + "\n\n"
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
        except:
            self.genre_var.set("dialogue")
            self.on_genre_change()
            self.generate()

if __name__ == "__main__":
    root = tk.Tk()
    app = SoufiNetGUIv3(root)
    root.mainloop()