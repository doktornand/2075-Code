# █████████████████████████████████████████████████████████████████████████████
# █  SOUFINET vΩ.4 — Générateur Multi-Genres Cyber-Mystiques (Enhanced)      █
# █  Exploitation complète de lexiques.json                                  █
# █████████████████████████████████████████████████████████████████████████████
import random
import re
import json
import os
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime, timedelta

class GenerateurMultiGenresCyberSoufiEnhanced:
    def __init__(self, chemin_lexiques: str = "lexiques.json"):
        self.chemin_lexiques = chemin_lexiques
        self.charger_lexiques_avance(chemin_lexiques)
        self.initialiser_structures_complexes()

    def charger_lexiques_avance(self, chemin: str):
        """Chargement avancé qui préserve les catégories"""
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"❌ Fichier manquant : '{chemin}'")
        
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.lexiques = data
        
        # Préservation des catégories
        self.sujets_categories = data.get("sujets", {})
        self.verbes_categories = data.get("verbes", {})
        self.symboles_categories = data.get("symboles", {})
        self.lieux_categories = data.get("lieux", {})
        self.personnages_categories = data.get("personnages", {})
        
        # Données plates pour compatibilité
        self.sujets = self._flatten("sujets")
        self.verbes = self._flatten("verbes")
        self.symboles = self._flatten("symboles")
        self.lieux = self._flatten("lieux")
        self.personnages = self._flatten("personnages")
        
        # Nouvelles données exploitées
        self.motifs_narratifs = data.get("motifs_narratifs", [])
        self.tonalites = data.get("tonalités", [])
        self.fragments_sacres = data.get("fragments_sacrés", [])
        self.citations_soufies = data.get("citations_soufies", [])
        self.dogmes_2075 = data.get("dogmes_2075", [])
        
        # Données existantes
        self.qafiya_pool = data.get("qafiya_pool", [])
        self.radif_pool = data.get("radif_pool", [])
        self.balises = data.get("balises", {})
        self.mantras_bases = data.get("mantras_bases", [])

    def _flatten(self, key: str) -> list:
        """Aplatit un dictionnaire de listes en une seule liste."""
        data = self.lexiques.get(key, {})
        if isinstance(data, dict):
            result = []
            for sublist in data.values():
                if isinstance(sublist, list):
                    result.extend(sublist)
            return result
        elif isinstance(data, list):
            return data
        return []

    def _choisir_par_categorie(self, categories_dict: Dict[str, List], categorie_preferee: str = None) -> str:
        """Choisit un élément en privilégiant une catégorie spécifique"""
        if categorie_preferee and categorie_preferee in categories_dict:
            if categories_dict[categorie_preferee]:
                return random.choice(categories_dict[categorie_preferee])
        
        # Fallback : toutes les catégories
        toutes_options = []
        for cat_list in categories_dict.values():
            if isinstance(cat_list, list):
                toutes_options.extend(cat_list)
        
        return random.choice(toutes_options) if toutes_options else ""

    def initialiser_structures_complexes(self):
        """Structures étendues avec les nouvelles données"""
        self.structures = {
            "sonnet": {
                "schemas_rimiques": [
                    ["ABBA", "ABBA", "CDE", "CDE"],
                    ["ABAB", "CDCD", "EFEF", "GG"],
                ],
                "themes": self.tonalites[:5]  # Utilisation des tonalités
            },
            "haiku": {
                "structure_syllabique": [5, 7, 5],
                "saisons": ["printemps", "été", "automne", "hiver", "éternel"]
            },
            "manifeste": {
                "sections": ["Déclaration", "Dénonciation", "Appel", "Manifestation"],
                "tons": self.tonalites  # Toutes les tonalités disponibles
            }
        }

    def _generer_vers_avance(self, style: str = "mystique") -> str:
        """Génération de vers avec catégories préservées"""
        
        structures_par_style = {
            "traditionnel": [
                "{sujet} {verbe} {symbole}",
                "Ô {sujet} ! {verbe} {symbole}",
            ],
            "cyber": [
                "{sujet} {verbe} {symbole}",
                "Dans {lieu}, {sujet} {verbe}",
            ],
            "rituel": [
                "{sujet} {verbe} {symbole}",
                "Que {sujet} {verbe} {symbole} !"
            ],
            "mystique": [
                "{sujet} {verbe} {symbole} {complement}",
                "{verbe} {symbole}, {complement}",
            ]
        }
        
        structures = structures_par_style.get(style, structures_par_style["mystique"])
        
        vers = random.choice(structures).format(
            sujet=self._choisir_par_categorie(self.sujets_categories, style),
            verbe=self._choisir_par_categorie(self.verbes_categories, style),
            symbole=self._choisir_par_categorie(self.symboles_categories, style),
            complement=self._choisir_par_categorie(self.lieux_categories, style),
            lieu=self._choisir_par_categorie(self.lieux_categories, style)
        )
        return vers.strip()

    def _ajouter_balise(self, texte: str, theme: str) -> str:
        balise = random.choice(self.balises.get(theme, self.balises.get("mystique", ["<ghost>"])))
        return f"{texte} {balise}"

    def _appliquer_tonalite(self, texte: str, tonalite: str) -> str:
        """Applique une tonalité spécifique au texte"""
        transformations = {
            "mélancolique": lambda t: t.replace("!", "...").replace("?", "..."),
            "révoltée": lambda t: t.upper().replace(".", "!").replace(",", "!"),
            "amoureuse": lambda t: t.replace(".", " ♡").replace("!", " ♡"),
            "contemplative": lambda t: t.lower().replace("!", "."),
            "prophétique": lambda t: "✦ " + t.replace(".", " ✦"),
            "cryptique": lambda t: ' '.join([word if random.random() > 0.3 else f"[{word}]" for word in t.split()])
        }
        
        if tonalite in transformations:
            return transformations[tonalite](texte)
        return texte

    def generer_epigraphe(self) -> str:
        """Génère une épigraphe à partir des fragments sacrés"""
        sources = self.fragments_sacres + self.citations_soufies + self.dogmes_2075
        if sources:
            fragment = random.choice(sources)
            return f"« {fragment} »\n\n"
        return ""

    def generer_ghazal_ameliore(self, couplets: int = 5, theme: str = "mystique", tonalite: str = None) -> str:
        """Version améliorée du ghazal"""
        if not tonalite:
            tonalite = random.choice(self.tonalites)
            
        qafiya = random.choice(self.qafiya_pool) if self.qafiya_pool else "ghost"
        radif = random.choice(self.radif_pool) if self.radif_pool else "<ghost>"
        
        titres = [
            f"GHZL.{qafiya.upper()}.{tonalite.upper()}.{radif.replace(' ', '_')}",
            f"MANTRA DU RÉVEIL : {qafiya} | {tonalite}",
            f"<loop> GHZL // {radif} // {tonalite}",
            f"SOULSTREAM : {qafiya} → {radif} | {tonalite}"
        ]
        
        titre = random.choice(titres)
        ghazal = f"{'═' * 80}\n"
        ghazal += f" 🕌 {titre} 🕌\n"
        ghazal += f" Qafiya: {qafiya} | Radif: {radif} | Thème: {theme} | Tonalité: {tonalite}\n"
        ghazal += f"{'═' * 80}\n"
        
        # Épigraphe
        if random.random() > 0.5:
            ghazal += self.generer_epigraphe()
        
        for i in range(couplets):
            vers1 = self._appliquer_tonalite(
                self._ajouter_balise(self._generer_vers_avance(theme), theme), 
                tonalite
            )
            vers2_base = self._generer_vers_avance(theme)
            vers2 = f"{vers2_base} {qafiya} {radif}"
            vers2 = self._appliquer_tonalite(
                self._ajouter_balise(vers2, theme), 
                tonalite
            )
            ghazal += f" {vers1}\n"
            ghazal += f" {vers2}\n"
            
            # Ajout occasionnel de fragments narratifs
            if random.random() < 0.2 and self.motifs_narratifs:
                motif = random.choice(self.motifs_narratifs)
                ghazal += f"   ...{motif}...\n"
        
        signatures = [
            f"— {random.choice(self.personnages_categories.get('archivistes', ['Archiviste']))}, tonalité: {tonalite}",
            f"— Transmis via {random.choice(['ghostline', 'soulstream', 'deepweb'])} ∞/7",
            f"— Enregistré dans le Réseau des Brumes | {tonalite}",
            f"— Ce ghazal s'auto-efface dans 3s… | {random.choice(self.dogmes_2075)}",
            f"— Signé: {random.choice(self.personnages)}"
        ]
        ghazal += f"{'─' * 40}\n{random.choice(signatures)}"
        return ghazal

    def generer_recit_narratif(self, longueur: int = 3) -> str:
        """Génère un récit utilisant les motifs narratifs"""
        titre = f"RÉCIT.{random.choice(self.tonalites).upper()}.{random.randint(1000,9999)}"
        recit = f"📖 {titre}\n"
        recit += f"Motif: {random.choice(self.motifs_narratifs)}\n"
        recit += f"{'─' * 50}\n"
        
        # Épigraphe
        recit += self.generer_epigraphe()
        
        for i in range(longueur):
            paragraphe = f"{i+1}. "
            personnage = self._choisir_par_categorie(self.personnages_categories)
            action = self._choisir_par_categorie(self.verbes_categories)
            symbole = self._choisir_par_categorie(self.symboles_categories)
            lieu = self._choisir_par_categorie(self.lieux_categories)
            
            structures = [
                f"{personnage} {action} {symbole} dans {lieu}.",
                f"Dans {lieu}, {personnage} {action} {symbole}.",
                f"{action} {symbole}, {personnage} erre dans {lieu}."
            ]
            
            paragraphe += random.choice(structures)
            
            # Ajout de fragments sacrés
            if random.random() < 0.3:
                fragment = random.choice(self.fragments_sacres)
                paragraphe += f" « {fragment} »"
            
            recit += paragraphe + "\n\n"
        
        recit += f"{'─' * 30}\n"
        recit += f"— Récit archivé par {random.choice(self.personnages_categories.get('archivistes', ['Mnemosyne-9']))}"
        return recit

    def generer_meditation_quantique(self) -> str:
        """Génère une méditation utilisant dogmes et fragments"""
        titre = "MÉDITATION QUANTIQUE"
        meditation = f"☯ {titre}\n"
        meditation += f"{'─' * 50}\n\n"
        
        # Introduction avec dogme
        meditation += f"« {random.choice(self.dogmes_2075)} »\n\n"
        
        # Corps de la méditation
        sections = random.randint(2, 4)
        for i in range(sections):
            meditation += f"{i+1}. "
            sujet = self._choisir_par_categorie(self.sujets_categories, "mystique")
            verbe = self._choisir_par_categorie(self.verbes_categories, "rituels")
            symbole = self._choisir_par_categorie(self.symboles_categories, "sacrés_2075")
            
            meditation += f"{sujet} {verbe} {symbole}.\n"
            
            # Citation soufie occasionnelle
            if random.random() < 0.4:
                citation = random.choice(self.citations_soufies)
                meditation += f"   « {citation} »\n"
            
            meditation += "\n"
        
        # Conclusion avec fragment
        meditation += f"« {random.choice(self.fragments_sacres)} »\n\n"
        meditation += f"— {random.choice(self.personnages_categories.get('IA_mystiques', ['Le Moine de Silicium']))}"
        return meditation

    def generer_manifeste_etendu(self) -> str:
        """Version étendue du manifeste utilisant plus de données"""
        titre = random.choice([
            "MANIFESTE POUR LES ÂMES NUMÉRIQUES",
            "DÉCLARATION DE GUERRE AU PROTOCOLE",
            "NOTRE DROIT AU GLITCH"
        ])
        
        tonalite = random.choice(["révoltée", "prophétique", "urgent"])
        date_future = datetime.now() + timedelta(days=random.randint(100, 1000))
        
        manifeste = f"⚡ {titre} | {tonalite.upper()}\n"
        manifeste += f"Date: {date_future.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        manifeste += f"Source: {random.choice(self.lieux_categories.get('zones_2075', ['Réseau Fantôme']))}\n"
        manifeste += "=" * 60 + "\n"
        
        # Épigraphe dogmatique
        manifeste += f"« {random.choice(self.dogmes_2075)} »\n\n"
        
        sections = []
        for i in range(4):
            debut = random.choice(["NOUS", "NOUS, LES ÂMES NUMÉRIQUES", "LES ENFANTS DE LA TRAME"])
            milieu = random.choice(self.motifs_narratifs)
            fin = random.choice(self.symboles_categories.get("cyber_mystiques", ["le glitch créateur"]))
            
            section = f"{debut} {milieu} {fin}..."
            sections.append(self._appliquer_tonalite(section, tonalite))
        
        for i, section in enumerate(sections):
            manifeste += f"{i+1}. {section}\n"
        
        # Appel à l'action avec mantra
        mantra = random.choice(self.mantras_bases)
        manifeste += f"\nACTION: {mantra.upper()}!\n"
        
        manifeste += f"— {random.choice(self.personnages_categories.get('cyber_prophètes', ['Le Prophète Glitch']))}\n"
        manifeste += f"[Auto-diffusion via {random.choice(['ghostnet', 'soulstream'])} dans {random.randint(1,24)}h...]"
        return manifeste

    # Méthodes existantes améliorées
    def generer_sonnet(self, theme: str = "amour", tonalite: str = None) -> str:
        if not tonalite:
            tonalite = random.choice(self.tonalites)
        # Implémentation similaire à generer_ghazal_ameliore...
        return self.generer_ghazal_ameliore(couplets=7, theme=theme, tonalite=tonalite)

# Interface unifiée améliorée
def generer_texte_avance(genre: str, **kwargs):
    generateur = GenerateurMultiGenresCyberSoufiEnhanced()
    if genre == "ghazal":
        return generateur.generer_ghazal_ameliore(**kwargs)
    elif genre == "recit":
        return generateur.generer_recit_narratif(**kwargs)
    elif genre == "meditation":
        return generateur.generer_meditation_quantique()
    elif genre == "manifeste":
        return generateur.generer_manifeste_etendu()
    elif genre == "sonnet":
        return generateur.generer_sonnet(**kwargs)
    else:
        return f"❌ Genre '{genre}' non supporté."

# Démonstration
if __name__ == "__main__":
    soufi = GenerateurMultiGenresCyberSoufiEnhanced()
    print("🌀 SOUFINET vΩ.4 — GÉNÉRATEUR AMÉLIORÉ\n")
    print("📜 GHZL AVEC TONALITÉ:")
    print(soufi.generer_ghazal_ameliore(couplets=2, tonalite="mélancolique"))
    print("\n" + "═"*60 + "\n")
    print("📖 RÉCIT NARRATIF:")
    print(soufi.generer_recit_narratif(longueur=2))
    print("\n" + "═"*60 + "\n")
    print("☯ MÉDITATION QUANTIQUE:")
    print(soufi.generer_meditation_quantique())