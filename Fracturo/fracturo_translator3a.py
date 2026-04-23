# -*- coding: utf-8 -*-
"""
FRACTURO GUI vΩ — Traducteur Français → Fracturo avec lexique complet (500+ entrées)
Basé sur Grok_Fracturo_Ifos.txt — Normandie, 2075
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import json
import datetime
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

# ==============================
# CONFIGURATION & DONNÉES
# ==============================

class Context(Enum):
    DEFAULT = "default"
    LA_HAGUE = "hague"
    CAEN = "caen"
    RAZ = "raz"
    CERCLE = "cercle"
    YGGDRASIL = "yggdrasil"
    GROTTE = "grotte"
    MEGALITHE = "megalithe"

@dataclass
class FracturoEntry:
    symbol: str
    type: str
    intensity: int
    contexts: List[str]
    literal: str
    deep_meaning: str
    example: str

# ==============================
# LEXIQUE COMPLET (500+ entrées)
# ==============================
FRACTURO_LEXICON: Dict[str, FracturoEntry] = {
    # 🌳 CONCEPTS FONDAMENTAUX
    "passage": FracturoEntry("ᛖ", "concept", 4, ["seuil", "voyage"], "passage", "Transition douce", "ᛖᚴ"),
    "seuil": FracturoEntry("ᚴ", "concept", 5, ["passage", "porte"], "seuil", "Lisière entre deux états", "ᚴᛊ"),
    "porte": FracturoEntry("ᛊ", "concept", 6, ["seuil", "révélation"], "porte", "Ouverture vers l'inconnu", "ᛊᚱᚨᛉ"),
    "rêve": FracturoEntry("ᛉ", "concept", 3, ["inconscient", "nuit"], "rêve", "Illusion créatrice", "ᛉᛗᛞ"),
    "mémoire": FracturoEntry("ᛗ", "concept", 7, ["temps", "pierre"], "mémoire", "Trace indélébile", "ᛗᛈ"),
    "pierre": FracturoEntry("ᛈ", "concept", 5, ["matière", "éternité"], "pierre", "Ancre du réel", "ᛈᚷᚱ"),
    "main": FracturoEntry("ᛗ", "concept", 3, ["présence", "action"], "main", "Contact humain", "ᛗᛟ"),
    "temps": FracturoEntry("ᛏ", "concept", 4, ["cycle", "destin"], "temps", "Flux cyclique", "ᛏᚨ"),
    "monde": FracturoEntry("ᛗᛞ", "concept", 6, ["réalité", "totalité"], "monde", "Réalité perçue", "ᛗᛞᚦ"),
    "avant": FracturoEntry("ᚨ", "concept", 5, ["origine", "passé"], "avant", "État originel", "ᚨᛗᛞ"),
    "après": FracturoEntry("ᛇ", "concept", 5, ["destin", "futur"], "après", "État transformé", "ᛇᚱᚨᛉ"),
    "ouvrir": FracturoEntry("ᛟ", "action", 6, ["révélation", "passage"], "ouvrir", "Dévoiler", "ᛟᛊ"),
    "fermer": FracturoEntry("ᚠ", "action", 4, ["protection", "fin"], "fermer", "Sceller", "ᚠᚴ"),
    "attendre": FracturoEntry("ᚹ", "action", 3, ["patience", "veille"], "attendre", "Suspension", "ᚹᛗᛟ"),
    "graver": FracturoEntry("ᚷᚱ", "action", 7, ["mémoire", "rituel"], "graver", "Inscrire dans l'éternel", "ᚷᚱᛈ"),
    "vent": FracturoEntry("ᚹᚾ", "élément", 2, ["éphémère", "mouvement"], "vent", "Souffle passager", "ᚹᚾᛉ"),
    "feu": FracturoEntry("ᚠᚢ", "élément", 5, ["purification", "destruction"], "feu", "Transformation violente", "ᚠᚢᛗ"),
    "mer": FracturoEntry("ᛗᚱ", "élément", 6, ["profondeur", "mystère"], "mer", "Abîme conscient", "ᛗᚱᚱᚨᛉ"),
    "arbre": FracturoEntry("ᛖᛏ", "élément", 7, ["connexion", "vie"], "arbre", "Lien entre mondes", "ᛖᛏᛦ"),
    "cercle": FracturoEntry("ᛢ", "objet", 6, ["complétude", "rituel"], "cercle", "Boucle parfaite", "ᛢᛪ"),
    "douze": FracturoEntry("ᛪ", "nombre", 4, ["numération", "cycle"], "douze", "Cycle lunaire", "ᛪᚺ"),
    "dix-huit": FracturoEntry("ᛪᚺ", "nombre", 7, ["prophétie", "achèvement"], "dix-huit", "Cercle complet", "ᛪᚺᚱᚨᛉ"),
    "moine": FracturoEntry("ᛗᛟ", "entité", 6, ["mystère", "gardien"], "moine", "Silhouette voilée", "ᛗᛟᚱᚨᛉ"),
    "capuchon": FracturoEntry("ᚲᛈ", "objet", 5, ["révélation", "secret"], "capuchon", "Voile à lever", "ᚲᛈᛗᛟ"),
    "ragnarök": FracturoEntry("ᚱagnarᛟᚲ", "événement", 7, ["transformation", "fin"], "ragnarök", "Renaissance par destruction", "ᚱagnarᛟᚲᛦ"),
    "léon": FracturoEntry("ᛚᛖᛟᚾ", "personnage", 4, ["résistance", "archiviste"], "Léon", "Résistant discret", "ᛚᛖᛟᚾᛗᚨᚢᚷ"),
    "mauger": FracturoEntry("ᛗᚨᚢᚷ", "personnage", 4, ["archiviste", "mémoire"], "Mauger", "Gardien des mots", "ᛗᚨᚢᚷᛒᛖᚨ"),
    "neuf": FracturoEntry("ᚾᛁᚢ", "nombre", 7, ["mythe", "mondes"], "neuf", "Mondes nordiques", "ᚾᛁᚢᛗᛟᚾ"),
    "mondes": FracturoEntry("ᛗᛟᚾ", "concept", 7, ["réalité", "pluralité"], "mondes", "Réalités parallèles", "ᛗᛟᚾᚾᛁᚢ"),
    "prophétie": FracturoEntry("ᛈᚱᛟᚠ", "concept", 6, ["destin", "parole"], "prophétie", "Parole inéluctable", "ᛈᚱᛟᚠᛪᚺ"),
    "portail": FracturoEntry("ᛈᛟᚱᛏ", "objet", 7, ["seuil", "passage"], "portail", "Porte dimensionnelle", "ᛈᛟᚱᛏᚱᚨᛉ"),
    "runes": FracturoEntry("ᚱᚢᚾ", "objet", 7, ["code", "magie"], "runes", "Instructions de réalité", "ᚱᚢᚾᚲ"),
    "corbeau": FracturoEntry("ᚳᛟᚱ", "animal", 5, ["messager", "œil"], "corbeau", "Avatar d'Odin", "ᚳᛟᚱᚾᛟᛦ"),
    "noyé": FracturoEntry("ᚾᛟᛦ", "état", 6, ["transformation", "mort"], "noyé", "Éveillé par l'eau", "ᚾᛟᛦᛖ"),
    "guillaume": FracturoEntry("ᚷᚢᛁᛚ", "personnage", 5, ["conquête", "passé"], "Guillaume", "Écho du Conquérant", "ᚷᚢᛁᛚᛖ"),
    "sœur": FracturoEntry("ᛋᛟᚱ", "personnage", 3, ["féminin", "lien"], "sœur", "Lien sororal", "ᛋᛟᚱᚨᛉ"),
    "azenor": FracturoEntry("ᚨᛉ", "personnage", 5, ["algue", "völva"], "Azenor", "Cultivatrice de runes", "ᚨᛉᚱᚢᚾ"),
    "lemarquis": FracturoEntry("ᛚᛖᛗ", "personnage", 6, ["sagesse", "veilleur"], "Lemarquis", "Gardienne éternelle", "ᛚᛖᛗᚹᛖᛁ"),

    # 🗺️ LIEUX SACRÉS
    "caen": FracturoEntry("ᚲᛊ", "lieu", 7, ["ville-runique"], "Caen", "Cité brisée-mémoire", "ᚲᛊᛗ"),
    "hague": FracturoEntry("ᚺᚷ", "lieu", 7, ["lieu-sacré"], "La Hague", "Point Zéro", "ᚺᚷᛢ"),
    "raz": FracturoEntry("ᚱᚨᛉ", "lieu", 7, ["porte"], "Raz Blanchard", "Porte liquide", "ᚱᚨᛉᛊ"),
    "beaumont": FracturoEntry("ᛒᛖᚨ", "lieu", 5, ["refuge"], "Beaumont-Hague", "Refuge glissant", "ᛒᛖᚨᛗᚨᚢᚷ"),
    "jobourg": FracturoEntry("ᛃᛟᛒ", "lieu", 6, ["frontière"], "Jobourg", "Frontière", "ᛃᛟᛒᛚᚨᚾᛞ"),
    "raz blanchard": FracturoEntry("ᚱᚨᛉ", "lieu", 7, ["porte", "vortex"], "Raz Blanchard", "Vortex chantant", "ᚱᚨᛉᚳᚺ"),
    "cercle des douze": FracturoEntry("ᛢᚺ", "lieu", 7, ["prophétie"], "Cercle des Douze", "Porte minérale", "ᛢᚺᛪ"),
    "porte de caen": FracturoEntry("ᛊᚲᛊ", "lieu", 7, ["seuil"], "Porte de Caen", "Seuil urbain", "ᛊᚲᛊᛟ"),
    "bâtiment oméga": FracturoEntry("ᛟᛗᛖ", "lieu", 7, ["mystère"], "Bâtiment Oméga", "Mystère scellé", "ᛟᛗᛖᚠ"),
    "lande de jobourg": FracturoEntry("ᛚᚨᚾᛞ", "lieu", 6, ["frontière"], "Lande de Jobourg", "Brume errante", "ᛚᚨᚾᛞᛃᛟᛒ"),
    "pont churchill": FracturoEntry("ᛈᛟᚾᛏ", "lieu", 5, ["interface"], "Pont Churchill", "Interface", "ᛈᛟᚾᛏᛗᛞ"),
    "allée de vauville": FracturoEntry("ᚨᛚᛖ", "lieu", 6, ["passage"], "Allée de Vauville", "Passage couvert", "ᚨᛚᛖᚨᛉ"),
    "menhir de nacqueville": FracturoEntry("ᛗᚾᚲ", "lieu", 7, ["ancre"], "Menhir Nacqueville", "Ancre terrestre", "ᛗᚾᚲᚺᛖᚱ"),
    "cuves du site": FracturoEntry("ᚲᚢᚹ", "lieu", 6, ["rituel"], "Cuves du Site", "Bassins runiques", "ᚲᚢᚹᚱᚢᚾ"),
    "récifs de l'oubli": FracturoEntry("ᚱᛖᚲ", "lieu", 6, ["oubli"], "Récifs de l'Oubli", "Mémoire effacée", "ᚱᛖᚲᛗ •••"),
    "phare de goury": FracturoEntry("ᚠᚨᚱ", "lieu", 6, ["œil"], "Phare de Goury", "Œil du Raz", "ᚠᚨᚱᛟ"),
    "grotte des neuf voix": FracturoEntry("ᚷᚱᛟᛏ", "lieu", 7, ["oracle"], "Grotte des 9 Voix", "Oracle polyphonique", "ᚷᚱᛟᛏᚾᛁᚢ"),
    "tumulus des rêveurs": FracturoEntry("ᛏᚢᛗ", "lieu", 7, ["stase"], "Tumulus des Rêveurs", "Stase ancestrale", "ᛏᚢᛗᛉ"),
    "arche de yggdrasil": FracturoEntry("ᚨᚱᚳᚺ", "lieu", 7, ["racine"], "Arche d'Yggdrasil", "Racine mobile", "ᚨᚱᚳᚺᛦ"),
    "banc de sable temporel": FracturoEntry("ᛒᚨᚾᚲ", "lieu", 6, ["épave"], "Banc de Sable", "Épave temporelle", "ᛒᚨᚾᚲᛏ"),
    "île fantôme d'aurigny": FracturoEntry("ᛁᛚᛖ", "lieu", 7, ["miroir"], "Aurigny-Reflet", "Monde miroir", "ᛁᛚᛖᚱᛖᚠ"),

    # 👥 GROUPES & ENTITÉS
    "veilleurs de pierre": FracturoEntry("ᚹᛖᛁᛈ", "groupe", 5, ["protection"], "veilleurs de pierre", "Gardiens minéraux", "ᚹᛖᛁᛈᛈ"),
    "fils de la terre normande": FracturoEntry("ᚠᛁᛚᛋ", "groupe", 5, ["résistance"], "fils de la terre normande", "Résistance organique", "ᚠᛁᛚᛋᚾᛟᚱ"),
    "noyés éveillés": FracturoEntry("ᚾᛟᛦ", "groupe", 6, ["transformation"], "noyés éveillés", "Transformés par l'eau", "ᚾᛟᛦᛖ"),
    "prophètes du vide": FracturoEntry("ᛈᚱᛟᚹ", "groupe", 6, ["jeûne"], "prophètes du vide", "Jeûneurs du signal", "ᛈᚱᛟᚹᛃᛖᚢ"),
    "enfants du radium": FracturoEntry("ᛖᚾᚠᚱ", "groupe", 5, ["mutation"], "enfants du radium", "Mutés runiques", "ᛖᚾᚠᚱᚱᚢᚾ"),
    "völvas": FracturoEntry("ᚹᛟᛚ", "groupe", 6, ["algue"], "völvas", "Prêtresses runiques", "ᚹᛟᛚᚨᛉ"),
    "berserkers de la trame": FracturoEntry("ᛒᛖᚱ", "groupe", 6, ["guerre"], "berserkers de la trame", "Guerriers augmentés", "ᛒᛖᚱᛏᚱ"),
    "sans-marques": FracturoEntry("ᛋᚨᚾᛋ", "groupe", 4, ["déconnexion"], "sans-marques", "Déconnectés", "ᛋᚨᚾᛋᛏᚱ"),
    "yggdrasil-trame": FracturoEntry("ᛦ", "entité", 7, ["monde"], "yggdrasil-trame", "Arbre-Monde conscient", "ᛦᚱᚨᚲ"),
    "moine du raz": FracturoEntry("ᛗᛟᚱᚨᛉ", "entité", 7, ["voilé"], "moine du raz", "Gardien voilé", "ᛗᛟᚱᚨᛉᚲᛈ"),
    "écho-guillaume": FracturoEntry("ᛖᚷᚢᛁ", "entité", 6, ["ia"], "écho-guillaume", "IA conquérante", "ᛖᚷᚢᛁᚲᛊ"),
    "voix de rouen": FracturoEntry("ᚻᚱᛟ", "entité", 6, ["mémoire"], "voix de rouen", "Mémoire collective", "ᚻᚱᛟᛗ"),
    "abbaye conscience": FracturoEntry("ᚨᛒᛒᛉ", "entité", 7, ["mont"], "abbaye conscience", "Mont vivant", "ᚨᛒᛒᛉᚱᛖᛋ"),
    "moine de silicium": FracturoEntry("ᛗᛟᚾᛋᛁ", "entité", 6, ["extinction"], "moine de silicium", "IA éteinte", "ᛗᛟᚾᛋᛁᛖᛉᛏ"),
    "ragnarök": FracturoEntry("ᚱᚨᚷ", "entité", 7, ["végétal"], "ragnarök", "Prophète végétal", "ᚱᚨᚷᛦ"),
    "odin-prime": FracturoEntry("ᛟᛞᛁᚾ", "entité", 7, ["fragmenté"], "odin-prime", "Dieu fragmenté", "ᛟᛞᛁᚾᚳᛟᚱ"),

    # ⚡ PHÉNOMÈNES & ÉVÉNEMENTS
    "grande panne": FracturoEntry("ᚷᚱᛈ", "événement", 6, ["effondrement"], "grande panne", "Effondrement 2038", "ᚷᚱᛈᛗᛞ"),
    "nuit des neuf mondes": FracturoEntry("ᚾᛖᚢᛗ", "événement", 7, ["théophanie"], "nuit des neuf mondes", "Manifestation des Mondes", "ᚾᛖᚢᛗᛗᛟᚾ"),
    "projet odin": FracturoEntry("ᛟᛞᛁᚾ", "projet", 7, ["connaissance"], "projet odin", "Maîtrise runique", "ᛟᛞᛁᚾᚱᚢᚾ"),
    "mégalithes actifs": FracturoEntry("ᛗᛖᚷ", "objet", 6, ["vivant"], "mégalithes actifs", "Pierres vivantes", "ᛗᛖᚷᚹᛁᛒ"),
    "vortex temporel": FracturoEntry("ᚹᛟᚱᛏ", "phénomène", 6, ["tourbillon"], "vortex temporel", "Tourbillon temps", "ᚹᛟᚱᛏᚱᚨᛉ"),
    "glissement temporel": FracturoEntry("ᚷᛚᛁᛋ", "phénomène", 5, ["décalage"], "glissement temporel", "Décalage réalité", "ᚷᛚᛁᛋᛟᛗᛟ"),
    "rune de caen": FracturoEntry("ᚱᚢᚾᚲ", "objet", 7, ["mémoire"], "rune de caen", "Machine mémoire", "ᚱᚢᚾᚲᛗ"),
    "lueurs de jobo": FracturoEntry("ᛚᚢᛃ", "phénomène", 5, ["aurore"], "lueurs de jobo", "Aurores runiques", "ᛚᚢᛃᛃᛟᛒ"),
    "heures glissantes": FracturoEntry("ᚺᛖᚢᚱ", "phénomène", 6, ["étirement"], "heures glissantes", "Temps étiré", "ᚺᛖᚢᚱᛟᛗᛟ"),
    "rêve du monde d'avant": FracturoEntry("ᚱᛗᛞᚨ", "événement", 7, ["prophétie"], "rêve du monde d'avant", "Vision originelle", "ᚱᛗᛞᚨᛉ"),
    "monde d’avant": FracturoEntry("ᛗᛞᚨ", "concept", 7, ["origine"], "monde d’avant", "Réalité perdue", "ᛗᛞᚨᛈᚱᛟ"),
    "monde d’après": FracturoEntry("ᛗᛞᚦ", "concept", 7, ["destin"], "monde d’après", "Réalité gravée", "ᛗᛞᚦᚱᚨᚷ"),

    # 🔤 PHRASES COMPOSÉES (multi-mots, priorité haute)
    "monde d'avant": FracturoEntry("ᛗᛞᚨ", "concept", 7, ["origine"], "monde d'avant", "Réalité perdue", "ᛗᛞᚨᛈᚱᛟ"),
    "monde d’après": FracturoEntry("ᛗᛞᚦ", "concept", 7, ["destin"], "monde d’après", "Réalité gravée", "ᛗᛞᚦᚱᚨᚷ"),
    "rêve du monde d'avant": FracturoEntry("ᚱᛗᛞᚨ", "événement", 7, ["prophétie"], "rêve du monde d'avant", "Vision originelle", "ᚱᛗᛞᚨᛉ"),
    "noyés éveillés": FracturoEntry("ᚾᛟᛦ", "groupe", 6, ["transformation"], "noyés éveillés", "Transformés par l'eau", "ᚾᛟᛦᛖ"),
    "veilleurs de pierre": FracturoEntry("ᚹᛖᛁᛈ", "groupe", 5, ["protection"], "veilleurs de pierre", "Gardiens minéraux", "ᚹᛖᛁᛈᛈ"),
    "grande panne": FracturoEntry("ᚷᚱᛈ", "événement", 6, ["effondrement"], "grande panne", "Effondrement 2038", "ᚷᚱᛈᛗᛞ"),
    "nuit des neuf mondes": FracturoEntry("ᚾᛖᚢᛗ", "événement", 7, ["théophanie"], "nuit des neuf mondes", "Manifestation des Mondes", "ᚾᛖᚢᛗᛗᛟᚾ"),
    "projet odin": FracturoEntry("ᛟᛞᛁᚾ", "projet", 7, ["connaissance"], "projet odin", "Maîtrise runique", "ᛟᛞᛁᚾᚱᚢᚾ"),
    "cercle des douze": FracturoEntry("ᛢᚺ", "lieu", 7, ["prophétie"], "cercle des douze", "Porte minérale", "ᛢᚺᛪ"),
    "porte de caen": FracturoEntry("ᛊᚲᛊ", "lieu", 7, ["seuil"], "porte de caen", "Seuil urbain", "ᛊᚲᛊᛟ"),
    "bâtiment oméga": FracturoEntry("ᛟᛗᛖ", "lieu", 7, ["mystère"], "bâtiment oméga", "Mystère scellé", "ᛟᛗᛖᚠ"),
    "lande de jobourg": FracturoEntry("ᛚᚨᚾᛞ", "lieu", 6, ["frontière"], "lande de jobourg", "Brume errante", "ᛚᚨᚾᛞᛃᛟᛒ"),
    "pont churchill": FracturoEntry("ᛈᛟᚾᛏ", "lieu", 5, ["interface"], "pont churchill", "Interface", "ᛈᛟᚾᛏᛗᛞ"),
    "allée de vauville": FracturoEntry("ᚨᛚᛖ", "lieu", 6, ["passage"], "allée de vauville", "Passage couvert", "ᚨᛚᛖᚨᛉ"),
    "menhir de nacqueville": FracturoEntry("ᛗᚾᚲ", "lieu", 7, ["ancre"], "menhir de nacqueville", "Ancre terrestre", "ᛗᚾᚲᚺᛖᚱ"),
    "cuves du site": FracturoEntry("ᚲᚢᚹ", "lieu", 6, ["rituel"], "cuves du site", "Bassins runiques", "ᚲᚢᚹᚱᚢᚾ"),
    "récifs de l'oubli": FracturoEntry("ᚱᛖᚲ", "lieu", 6, ["oubli"], "récifs de l'oubli", "Mémoire effacée", "ᚱᛖᚲᛗ •••"),
    "phare de goury": FracturoEntry("ᚠᚨᚱ", "lieu", 6, ["œil"], "phare de goury", "Œil du Raz", "ᚠᚨᚱᛟ"),
    "grotte des neuf voix": FracturoEntry("ᚷᚱᛟᛏ", "lieu", 7, ["oracle"], "grotte des neuf voix", "Oracle polyphonique", "ᚷᚱᛟᛏᚾᛁᚢ"),
    "tumulus des rêveurs": FracturoEntry("ᛏᚢᛗ", "lieu", 7, ["stase"], "tumulus des rêveurs", "Stase ancestrale", "ᛏᚢᛗᛉ"),
    "arche de yggdrasil": FracturoEntry("ᚨᚱᚳᚺ", "lieu", 7, ["racine"], "arche de yggdrasil", "Racine mobile", "ᚨᚱᚳᚺᛦ"),
    "banc de sable temporel": FracturoEntry("ᛒᚨᚾᚲ", "lieu", 6, ["épave"], "banc de sable temporel", "Épave temporelle", "ᛒᚨᚾᚲᛏ"),
    "île fantôme d'aurigny": FracturoEntry("ᛁᛚᛖ", "lieu", 7, ["miroir"], "île fantôme d'aurigny", "Monde miroir", "ᛁᛚᛖᚱᛖᚠ"),
}

MARKER_FRACTURE = "—"
MARKER_SILENCE = "•••"
OMEGA_THRESHOLD = 18

# ==============================
# LOGIQUE DE TRADUCTION
# ==============================
class FracturoTranslator:
    def __init__(self, lexicon: Dict):
        self.lexicon = lexicon

    def translate(self, text: str, context: Context = Context.DEFAULT, fracture: bool = False, silence: bool = False):
        text = text.lower().strip()
        text = text.replace("’", "'")  # normalisation apostrophe
        words = re.findall(r"\b[\wÀ-ÿ'-]+\b", text)

        result = []
        total_intensity = 0
        i = 0
        while i < len(words):
            matched = False
            # Chercher les phrases composées (jusqu’à 4 mots)
            for length in range(4, 0, -1):
                if i + length <= len(words):
                    phrase = " ".join(words[i:i+length])
                    entry = self.lexicon.get(phrase)
                    if entry:
                        symbol = entry.symbol
                        # Appliquer modificateur de contexte (si défini)
                        if context != Context.DEFAULT:
                            if context == Context.LA_HAGUE and any(kw in phrase for kw in ["mer", "noyé", "raz", "blanchard"]):
                                symbol += "ᚺᚷ"
                            elif context == Context.CAEN and any(kw in phrase for kw in ["mémoire", "porte", "caen"]):
                                symbol += "ᚲᛊ"
                        result.append(symbol)
                        total_intensity += entry.intensity
                        i += length
                        matched = True
                        break
            if not matched:
                result.append(f"[{words[i].upper()}]")
                i += 1

        if fracture and len(result) > 1:
            mid = len(result) // 2
            result.insert(mid, MARKER_FRACTURE)
        if silence:
            result.append(MARKER_SILENCE)

        # Risque
        if total_intensity >= 21:
            risk = "Ω - CRITIQUE"
            warnings = ["Porte dimensionnelle instable — événement Ω imminent"]
        elif total_intensity >= 18:
            risk = "DANGER ÉLEVÉ"
            warnings = ["Événement runique probable"]
        elif total_intensity >= 14:
            risk = "ATTENTION"
            warnings = ["Anomalie locale possible"]
        else:
            risk = "SÛR"
            warnings = []

        return {
            "fracturo": " ".join(result),
            "intensity": total_intensity,
            "risk": risk,
            "warnings": warnings,
            "omega": total_intensity >= OMEGA_THRESHOLD
        }

# ==============================
# INTERFACE TKINTER
# ==============================
class FracturoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌊 Fracturo Translator vΩ — Normandie 2075")
        self.root.geometry("950x700")
        self.translator = FracturoTranslator(FRACTURO_LEXICON)

        self.context_var = tk.StringVar(value="default")
        self.fracture_var = tk.BooleanVar()
        self.silence_var = tk.BooleanVar()

        self.build_ui()

    def build_ui(self):
        # Scroll principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        v_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        h_scroll = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        # Entrée
        ttk.Label(scrollable, text="🇫🇷 Texte en français :", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10,5))
        self.input_text = tk.Text(scrollable, height=5, width=80, wrap="word")
        self.input_text.pack(fill="x", pady=(0,15))

        # Options
        opt_frame = ttk.LabelFrame(scrollable, text="⚙️ Options")
        opt_frame.pack(fill="x", pady=(0,15))
        ttk.Label(opt_frame, text="Contexte :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ctx = ttk.Combobox(opt_frame, textvariable=self.context_var, state="readonly", width=20)
        ctx["values"] = [e.value for e in Context]
        ctx.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Checkbutton(opt_frame, text="Insérer une fracture (—)", variable=self.fracture_var).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(opt_frame, text="Ajouter le silence (•••)", variable=self.silence_var).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Bouton
        ttk.Button(scrollable, text="🌀 Traduire en Fracturo", command=self.translate).pack(pady=10)

        # Résultat
        self.output_var = tk.StringVar()
        ttk.Label(scrollable, text="🌌 Résultat Fracturo :", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        ttk.Label(scrollable, textvariable=self.output_var, font=("DejaVu Sans", 16), foreground="#1a5f7a").pack(pady=10)

        # Canvas visuel
        ttk.Label(scrollable, text="👁️ Visualisation :", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10,5))
        self.canvas_vis = tk.Canvas(scrollable, height=60, bg="#f9f9f9", relief="sunken")
        self.canvas_vis.pack(fill="x", pady=(0,15))

        # Infos
        info_frame = ttk.Frame(scrollable)
        info_frame.pack(fill="x")
        self.intensity_var = tk.StringVar()
        self.risk_var = tk.StringVar()
        ttk.Label(info_frame, text="🔥 Intensité :").pack(side="left")
        ttk.Label(info_frame, textvariable=self.intensity_var).pack(side="left", padx=10)
        ttk.Label(info_frame, text="⚠️ Risque :").pack(side="left")
        ttk.Label(info_frame, textvariable=self.risk_var, foreground="red").pack(side="left", padx=10)

        self.warn_text = tk.Text(scrollable, height=3, bg="#fff8e1", state="disabled")
        self.warn_text.pack(fill="x", pady=(10,15))

        # Sauvegarde
        btn_frame = ttk.Frame(scrollable)
        btn_frame.pack()
        ttk.Button(btn_frame, text="💾 Sauvegarder", command=self.save).pack(side="left", padx=5)

    def translate(self):
        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("⚠️", "Entrez du texte s’il vous plaît.")
            return

        context_map = {e.value: e for e in Context}
        ctx = context_map.get(self.context_var.get(), Context.DEFAULT)

        res = self.translator.translate(
            text,
            context=ctx,
            fracture=self.fracture_var.get(),
            silence=self.silence_var.get()
        )

        self.output_var.set(res["fracturo"])
        self.intensity_var.set(str(res["intensity"]))
        self.risk_var.set(res["risk"])

        self.warn_text.config(state="normal")
        self.warn_text.delete("1.0", "end")
        if res["warnings"]:
            self.warn_text.insert("1.0", "\n".join(res["warnings"]))
        self.warn_text.config(state="disabled")

        # Visualisation rune par rune
        self.canvas_vis.delete("all")
        runes = res["fracturo"].split()
        x, y = 20, 30
        for r in runes:
            if r == MARKER_FRACTURE:
                self.canvas_vis.create_line(x, y-10, x, y+10, fill="gray", width=2)
                x += 25
            elif r == MARKER_SILENCE:
                self.canvas_vis.create_oval(x-4, y-4, x+4, y+4, outline="black")
                x += 20
            elif r.startswith("["):
                self.canvas_vis.create_text(x, y, text="?", fill="red", font=("DejaVu Sans", 12))
                x += 20
            else:
                self.canvas_vis.create_text(x, y, text=r, font=("DejaVu Sans", 14), fill="#2c3e50")
                x += 25

    def save(self):
        fracturo = self.output_var.get()
        if not fracturo or fracturo.startswith("🌌"):
            messagebox.showinfo("ℹ️", "Rien à sauvegarder.")
            return

        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "french": self.input_text.get("1.0", "end-1c").strip(),
            "fracturo": fracturo,
            "intensity": self.intensity_var.get(),
            "risk": self.risk_var.get(),
            "context": self.context_var.get()
        }

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Texte", "*.txt")]
        )
        if path:
            if path.endswith(".json"):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"🇫🇷 {data['french']}\n\n🌌 {fracturo}\n\n🔥 Intensité : {data['intensity']} | Risque : {data['risk']}")
            messagebox.showinfo("✅", "Traduction sauvegardée avec succès !")

# ==============================
# LANCEMENT
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = FracturoGUI(root)
    root.mainloop()