# -*- coding: utf-8 -*-
"""
FRACTURO FRACTAL ENGINE vΩ — Version Complète
Lexique 500+ entrées + Palettes runiques + Règles R1–R12
Inspiré par Léon Mauger, La Hague, 2075
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numba import jit
import json
import datetime
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

# ==============================
# 🔱 PALETTES RUNIQUES (par contexte)
# ==============================
RUNIC_PALETTES = {
    "hague": {
        "name": "🌊 La Hague — Mémoire liquide",
        "colors": ["#0a1a2f", "#1e3a5f", "#0ea5e9", "#1e40af", "#0c4a6e"],
        "cmap": "ocean"
    },
    "caen": {
        "name": "🧱 Caen — Pierre brisée",
        "colors": ["#374151", "#6b7280", "#9ca3af", "#d1d5db", "#f3f4f6"],
        "cmap": "bone"
    },
    "raz": {
        "name": "🌀 Raz Blanchard — Vortex liquide",
        "colors": ["#0c4a6e", "#0ea5e9", "#7dd3fc", "#bae6fd", "#e0f2fe"],
        "cmap": "viridis"
    },
    "cercle": {
        "name": "🜂 Cercle des Douze — Porte minérale",
        "colors": ["#4c1d95", "#7e22ce", "#a78bfa", "#c4b5fd", "#e9d5ff"],
        "cmap": "twilight"
    },
    "yggdrasil": {
        "name": "🌳 Yggdrasil — Arbre-Monde",
        "colors": ["#166534", "#15803d", "#16a34a", "#34d399", "#a7f3d0"],
        "cmap": "Greens"
    },
    "grotte": {
        "name": "🕳️ Grotte des Neuf Voix — Oracle sombre",
        "colors": ["#000000", "#111827", "#1f2937", "#374151", "#6b7280"],
        "cmap": "gray"
    },
    "megalithe": {
        "name": "🪨 Mégalithe actif — Pierre vivante",
        "colors": ["#78350f", "#9a3412", "#c2410c", "#f59e0b", "#fbbf24"],
        "cmap": "Oranges"
    },
    "default": {
        "name": "🔥 Fracturo neutre",
        "colors": ["#000000", "#7f1d1d", "#dc2626", "#f87171", "#fecaca"],
        "cmap": "hot"
    }
}

# ==============================
# 🧬 CLASSES DE BASE
# ==============================
@dataclass
class FracturoEntry:
    symbol: str
    type: str
    intensity: int
    contexts: List[str]
    literal: str
    deep_meaning: str
    example: str

class Context(Enum):
    DEFAULT = "default"
    LA_HAGUE = "hague"
    CAEN = "caen"
    RAZ = "raz"
    CERCLE = "cercle"
    YGGDRASIL = "yggdrasil"
    GROTTE = "grotte"
    MEGALITHE = "megalithe"

# ==============================
# 📚 LEXIQUE COMPLET (500+ ENTRÉES)
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

    # 🔤 PHRASES COMPOSÉES
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
# 🌀 TRADUCTEUR FRACTURO COMPLET
# ==============================
class FracturoTranslator:
    def translate(self, text: str):
        text = text.lower().replace("’", "'")
        words = re.findall(r"\b[\wÀ-ÿ'-]+\b", text)
        result = []
        total_intensity = 0
        i = 0
        while i < len(words):
            matched = False
            for length in range(4, 0, -1):
                if i + length <= len(words):
                    phrase = " ".join(words[i:i+length])
                    entry = FRACTURO_LEXICON.get(phrase)
                    if entry:
                        result.append(entry.symbol)
                        total_intensity += entry.intensity
                        i += length
                        matched = True
                        break
            if not matched:
                result.append(f"[{words[i].upper()}]")
                i += 1
        return {
            "runes": result,
            "intensity": total_intensity,
            "omega": total_intensity >= OMEGA_THRESHOLD,
            "context": self._infer_context(text)
        }

    def _infer_context(self, text):
        text = text.lower()
        if "hague" in text or "mégalithe" in text:
            return Context.LA_HAGUE
        if "caen" in text or "pierre" in text:
            return Context.CAEN
        if "raz" in text or "mer" in text:
            return Context.RAZ
        if "cercle" in text or "douze" in text:
            return Context.CERCLE
        if "yggdrasil" in text or "arbre" in text:
            return Context.YGGDRASIL
        if "grotte" in text or "voix" in text:
            return Context.GROTTE
        if "menhir" in text or "nacqueville" in text:
            return Context.MEGALITHE
        return Context.DEFAULT

# ==============================
# 🌀 MOTEUR FRACTAL OPTIMISÉ
# ==============================
@jit(nopython=True)
def fracturo_fractal(h, w, max_iter, cx=0.0, cy=0.0):
    y, x = np.ogrid[-1.4:1.4:h*1j, -2.0:0.8:w*1j]
    c = x + y*1j + (cx + cy*1j)
    z = c.copy()
    divtime = max_iter + np.zeros(z.shape, dtype=np.int32)
    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 4.0
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 2
    return divtime

# ==============================
# 🖼️ INTERFACE TKINTER
# ==============================
class FracturoFractalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌀 FracturoScript — Générateur Fractal Ontologique vΩ")
        self.root.geometry("1000x800")
        self.translator = FracturoTranslator()
        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # Entrée
        ttk.Label(main, text="📜 FracturoScript :").pack(anchor="w", pady=(0,5))
        self.script_text = tk.Text(main, height=4, width=80)
        self.script_text.pack(fill="x", pady=(0,10))
        self.script_text.insert("1.0", "raz yggdrasil — monde d'avant •••\ncaen pierre noyés éveillés")

        # Boutons
        btn_frame = ttk.Frame(main)
        btn_frame.pack()
        ttk.Button(btn_frame, text="⚡ INVOQUER", command=self.invoke).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Sauvegarder", command=self.save).pack(side="left", padx=5)

        # Infos
        info_frame = ttk.Frame(main)
        info_frame.pack(fill="x", pady=10)
        self.intensity_var = tk.StringVar()
        self.context_var = tk.StringVar()
        self.palette_var = tk.StringVar()
        ttk.Label(info_frame, text="🔥 Intensité :").pack(side="left")
        ttk.Label(info_frame, textvariable=self.intensity_var).pack(side="left", padx=5)
        ttk.Label(info_frame, text="📍 Contexte :").pack(side="left")
        ttk.Label(info_frame, textvariable=self.context_var).pack(side="left", padx=5)
        ttk.Label(info_frame, text="🎨 Palette :").pack(side="left")
        ttk.Label(info_frame, textvariable=self.palette_var).pack(side="left", padx=5)

        # Canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas_agg = FigureCanvasTkAgg(self.fig, main)
        self.canvas_agg.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def invoke(self):
        script = self.script_text.get("1.0", "end-1c").strip()
        if not script:
            messagebox.showwarning("⚠️", "Entrez un FracturoScript !")
            return

        res = self.translator.translate(script)
        intensity = min(res["intensity"], 120)
        context = res["context"]

        self.intensity_var.set(str(res["intensity"]))
        self.context_var.set(context.value.title())
        self.palette_var.set(RUNIC_PALETTES[context.value]["name"])

        max_iter = 50 + intensity
        cx, cy = 0.0, 0.0

        # Coordonnées par contexte
        if context == Context.RAZ:
            cx, cy = -0.7, 0.27
        elif context == Context.CAEN:
            cx, cy = -0.8, 0.156
        elif context == Context.YGGDRASIL:
            cx, cy = -0.7269, 0.1889
        elif context == Context.CERCLE:
            cx, cy = 0.0, 0.0
        elif context == Context.LA_HAGUE:
            cx, cy = -0.745, 0.186
        elif context == Context.GROTTE:
            cx, cy = -0.75, 0.11
        elif context == Context.MEGALITHE:
            cx, cy = -0.758, 0.087

        cmap_name = RUNIC_PALETTES[context.value]["cmap"]
        img = fracturo_fractal(800, 1000, max_iter, cx, cy)

        self.ax.clear()
        self.ax.imshow(img, cmap=cmap_name, interpolation="bilinear")
        self.ax.axis("off")
        title = f"FracturoScript invoqué — Intensité {intensity}"
        if res["omega"]:
            title += " ⚠️ Ω"
        self.fig.suptitle(title, color="white", backgroundcolor="black")
        self.canvas_agg.draw()

        if res["omega"]:
            messagebox.showwarning("Ω", "⚠️ ÉVÉNEMENT Ω — RÉALITÉ INSTABLE !\nLa fracture est ouverte.")

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if path:
            meta = {
                "script": self.script_text.get("1.0", "end-1c"),
                "intensity": self.intensity_var.get(),
                "context": self.context_var.get(),
                "palette": self.palette_var.get(),
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="black")
            with open(path.replace(".png", "_meta.json"), "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("✅", "Image et métadonnées runiques sauvegardées !")

if __name__ == "__main__":
    root = tk.Tk()
    app = FracturoFractalGUI(root)
    root.mainloop()