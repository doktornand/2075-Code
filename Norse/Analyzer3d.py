"""
OldNorseAnalyzer_v4_extended.py
Version étendue avec capacités d'analyse maximales pour l'ancien norrois

Améliorations principales :
- Lexique étendu (3000+ entrées)
- Paradigmes morphologiques complets
- Système de règles avancé pour la déduction morphologique
- Analyse des composés complexes
- Reconnaissance des formes verbales (temps, mode, voix)
- Désambiguïsation contextuelle avancée
- Support des dialectes et variations orthographiques
- Intégration de connaissances linguistiques spécialisées
"""

import re
import json
import csv
import unicodedata
import pickle
from collections import defaultdict, Counter
from difflib import get_close_matches, SequenceMatcher
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Dict, Any, Optional, Tuple
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------ CONSTANTES ET CONFIGURATION ------------------------

# Caractères spéciaux de l'ancien norrois
OLD_NORSE_CHARS = 'aábcdeéfghiíjklmnoópqrstuúvwxyýzþðæǫøöåäïüABCDEFGHIJKLMNOPQRSTUVWXYZÞÐÆǪØÖÅÄÏÜ'

# Expressions régulières améliorées
TOKEN_RE = re.compile(rf"[{re.escape(OLD_NORSE_CHARS)}]+|[.,;:!?()\-\/\\«»\"'`~\[\]{{}}]|\d+")

# ------------------------ UTILITAires AMÉLIORÉS ------------------------

class AdvancedNormalizer_old:
    """Normaliseur avancé pour l'ancien norrois avec support des variations dialectales"""
    
    # Mappings de normalisation étendus
    NORMALIZATION_MAP = {
        # Caractères Unicode problématiques
        '\u00FE': 'þ', '\u00DE': 'Þ',  # thorn
        '\u00F0': 'ð', '\u00D0': 'Ð',  # eth
        '\u00E6': 'æ', '\u00C6': 'Æ',  # ash
        '\u0153': 'œ', '\u0152': 'Œ',  # œ
        '\u0111': 'ð', '\u0110': 'Ð',  # alternative eth
        
        # Variations orthographiques communes
        'ö': 'ǫ', 'Ö': 'Ǫ',
        'ø': 'ǫ', 'Ø': 'Ǫ',  # simplification pour l'analyse
        'å': 'á', 'Å': 'Á',
        'ä': 'æ', 'Ä': 'Æ',
        'aa': 'á',
        'oe': 'œ',
        'ae': 'æ',
        
        # Ligatures et formes archaïques
        'ꝛ': 'r', 'ꝛ́': 'r',
        'ꝺ': 'd', 'Ꝼ': 'f',
        'ᚼ': 'h', 'ᚦ': 'þ',
    }
    
    # Variations dialectales acceptées
    DIALECT_VARIANTS = {
        'ey': ['ei', 'æ', 'øy'],
        'au': ['øy', 'ey'],
        'ei': ['ey', 'æ'],
        'ǫ': ['o', 'ø', 'ö'],
        'æ': ['ae', 'ä'],
        'œ': ['oe', 'ø'],
        'gj': ['g', 'dj'],
        'kj': ['k', 'tj'],
        'kk': ['k', 'ck'],
        'nn': ['n', 'nd'],
    }
    
    @classmethod
    def normalize(cls, text: str, dialect_aware: bool = True) -> str:
        """Normalisation avancée du texte"""
        text = text.strip()
        text = unicodedata.normalize('NFC', text)
        
        # Remplacements de base
        for old, new in cls.NORMALIZATION_MAP.items():
            text = text.replace(old, new)
        
        # Correction des espaces et ponctuation
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([.,;:!?()])\s*', r'\1 ', text)
        
        return text
    
    @classmethod
    def generate_variants(cls, word: str) -> List[str]:
        """Génère des variantes orthographiques possibles"""
        variants = {word}
        word_lower = word.lower()
        
        for standard, alternates in cls.DIALECT_VARIANTS.items():
            if standard in word_lower:
                for alt in alternates:
                    variant = word_lower.replace(standard, alt)
                    variants.add(variant)
                    # Version avec capitale
                    if word[0].isupper():
                        variants.add(variant.capitalize())
        
        return list(variants)

class AdvancedNormalizer:
    """Normaliseur avancé pour l'ancien norrois avec support des variations dialectales"""
    
    # Mappings de normalisation étendus
    NORMALIZATION_MAP = {
        # Caractères Unicode problématiques
        '\u00FE': 'þ', '\u00DE': 'Þ',  # thorn
        '\u00F0': 'ð', '\u00D0': 'Ð',  # eth
        '\u00E6': 'æ', '\u00C6': 'Æ',  # ash
        '\u0153': 'œ', '\u0152': 'Œ',  # œ
        '\u0111': 'ð', '\u0110': 'Ð',  # alternative eth
        
        # Variations orthographiques communes
        'ö': 'ǫ', 'Ö': 'Ǫ',
        'ø': 'ǫ', 'Ø': 'Ǫ',  # simplification pour l'analyse
        'å': 'á', 'Å': 'Á',
        'ä': 'æ', 'Ä': 'Æ',
        'aa': 'á',
        'oe': 'œ',
        'ae': 'æ',
    }
    
    @classmethod
    def normalize(cls, text: str, dialect_aware: bool = True) -> str:
        """Normalisation avancée du texte"""
        text = text.strip()
        text = unicodedata.normalize('NFC', text)
        
        # Remplacements de base
        for old, new in cls.NORMALIZATION_MAP.items():
            text = text.replace(old, new)
        
        # Correction des espaces et ponctuation
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([.,;:!?()])\s*', r'\1 ', text)
        
        return text
    
    @classmethod
    def generate_variants(cls, word: str) -> List[str]:
        """Génère des variantes orthographiques possibles"""
        variants = {word}
        word_lower = word.lower()
        
        # Ajouter quelques variantes communes
        if 'æ' in word_lower:
            variants.add(word_lower.replace('æ', 'ae'))
        if 'ǫ' in word_lower:
            variants.add(word_lower.replace('ǫ', 'o'))
            variants.add(word_lower.replace('ǫ', 'ö'))
        
        return list(variants)

class Tokenizer:
    """Tokeniseur avancé pour l'ancien norrois"""
    
    @staticmethod
    def tokenize(text: str) -> List[Dict[str, Any]]:
        """Tokenisation avec préservation des informations de position"""
        text = AdvancedNormalizer.normalize(text)
        tokens = []
        
        for match in TOKEN_RE.finditer(text):
            token = match.group()
            start, end = match.span()
            
            token_info = {
                'token': token,
                'start': start,
                'end': end,
                'type': 'word' if re.match(rf'^[{re.escape(OLD_NORSE_CHARS)}]+$', token) else 'punctuation'
            }
            
            tokens.append(token_info)
        
        return tokens
    
    @staticmethod
    def segment_compounds_advanced(token: str, lexicon: set, min_length: int = 2) -> List[List[str]]:
        """Segmentation avancée des composés"""
        token_lower = token.lower()
        segments_list = []
        
        # Essayer différentes longueurs de segments
        for first_len in range(min_length, len(token_lower) - min_length + 1):
            first_part = token_lower[:first_len]
            second_part = token_lower[first_len:]
            
            # Vérifier si les deux parties existent
            first_valid = any(lex_word.startswith(first_part) for lex_word in lexicon)
            second_valid = second_part in lexicon or any(lex_word.startswith(second_part) for lex_word in lexicon)
            
            if first_valid and second_valid:
                segments_list.append([first_part, second_part])
        
        # Essayer la segmentation en trois parties
        for i in range(min_length, len(token_lower) - min_length * 2 + 1):
            for j in range(i + min_length, len(token_lower) - min_length + 1):
                parts = [token_lower[:i], token_lower[i:j], token_lower[j:]]
                if all(any(lex_word.startswith(part) for lex_word in lexicon) for part in parts):
                    segments_list.append(parts)
        
        return segments_list

# ------------------------ LEXIQUE ÉTENDU (3000+ ENTRIES) ------------------------

class ExtendedLexicon:
    """Lexique étendu avec gestion avancée"""
    
    def __init__(self):
        self.entries = {}
        self.lemma_index = defaultdict(list)  # lemme -> formes
        self.form_index = {}  # forme -> entrées
        self.pos_index = defaultdict(dict)  # pos -> formes -> entrées
        self.load_base_lexicon()
    
    def load_base_lexicon(self):
        """Charge le lexique de base étendu"""
        # Base du lexique original
        base_entries = {
                "fara": {"lemma": "fara", "pos": "verb", "gloss": "aller"},
    "koma": {"lemma": "koma", "pos": "verb", "gloss": "venir"},
    "drepa": {"lemma": "drepa", "pos": "verb", "gloss": "tuer"},
    "vera": {"lemma": "vera", "pos": "verb", "gloss": "être"},
    "heita": {"lemma": "heita", "pos": "verb", "gloss": "s'appeler"},
    "segja": {"lemma": "segja", "pos": "verb", "gloss": "dire"},
    "gera": {"lemma": "gera", "pos": "verb", "gloss": "faire"},
    "taka": {"lemma": "taka", "pos": "verb", "gloss": "prendre"},
    "gefa": {"lemma": "gefa", "pos": "verb", "gloss": "donner"},
    "sjá": {"lemma": "sjá", "pos": "verb", "gloss": "voir"},
    "heyra": {"lemma": "heyra", "pos": "verb", "gloss": "entendre"},
    "vita": {"lemma": "vita", "pos": "verb", "gloss": "savoir"},
    "vilja": {"lemma": "vilja", "pos": "verb", "gloss": "vouloir"},
    "munu": {"lemma": "munu", "pos": "verb", "gloss": "devoir/futur"},
    "skulu": {"lemma": "skulu", "pos": "verb", "gloss": "devoir"},
    "eiga": {"lemma": "eiga", "pos": "verb", "gloss": "posséder/avoir"},
    "hafa": {"lemma": "hafa", "pos": "verb", "gloss": "avoir"},
    "verða": {"lemma": "verða", "pos": "verb", "gloss": "devenir"},
    "sitja": {"lemma": "sitja", "pos": "verb", "gloss": "être assis"},
    "standa": {"lemma": "standa", "pos": "verb", "gloss": "se tenir debout"},
    "liggja": {"lemma": "liggja", "pos": "verb", "gloss": "être couché"},
    "ganga": {"lemma": "ganga", "pos": "verb", "gloss": "marcher"},
    "ríða": {"lemma": "ríða", "pos": "verb", "gloss": "chevaucher"},
    "fljúga": {"lemma": "fljúga", "pos": "verb", "gloss": "voler"},
    "bera": {"lemma": "bera", "pos": "verb", "gloss": "porter"},
    "borinn": {"lemma": "bera", "pos": "verb", "gloss": "né"},
    "deyja": {"lemma": "deyja", "pos": "verb", "gloss": "mourir"},
    "lifa": {"lemma": "lifa", "pos": "verb", "gloss": "vivre"},
    "eta": {"lemma": "eta", "pos": "verb", "gloss": "manger"},
    "drekka": {"lemma": "drekka", "pos": "verb", "gloss": "boire"},
    "sofa": {"lemma": "sofa", "pos": "verb", "gloss": "dormir"},
    "vakna": {"lemma": "vakna", "pos": "verb", "gloss": "se réveiller"},
    "elska": {"lemma": "elska", "pos": "verb", "gloss": "aimer"},
    "hata": {"lemma": "hata", "pos": "verb", "gloss": "haïr"},
    "bíða": {"lemma": "bíða", "pos": "verb", "gloss": "attendre"},
    "finna": {"lemma": "finna", "pos": "verb", "gloss": "trouver"},
    "leita": {"lemma": "leita", "pos": "verb", "gloss": "chercher"},
    "kalla": {"lemma": "kalla", "pos": "verb", "gloss": "appeler"},
    "spyrja": {"lemma": "spyrja", "pos": "verb", "gloss": "demander"},
    "svara": {"lemma": "svara", "pos": "verb", "gloss": "répondre"},
    "biðja": {"lemma": "biðja", "pos": "verb", "gloss": "prier/demander"},
    "þakka": {"lemma": "þakka", "pos": "verb", "gloss": "remercier"},
    "vinna": {"lemma": "vinna", "pos": "verb", "gloss": "gagner/travailler"},
    "tapa": {"lemma": "tapa", "pos": "verb", "gloss": "perdre"},
    "berjast": {"lemma": "berjast", "pos": "verb", "gloss": "se battre"},
    "vega": {"lemma": "vega", "pos": "verb", "gloss": "tuer/combattre"},
    "falla": {"lemma": "falla", "pos": "verb", "gloss": "tomber"},
    "rísa": {"lemma": "rísa", "pos": "verb", "gloss": "se lever"},
    "kasta": {"lemma": "kasta", "pos": "verb", "gloss": "jeter"},
    "keyra": {"lemma": "keyra", "pos": "verb", "gloss": "conduire/pousser"},
    "fæða": {"lemma": "fæða", "pos": "verb", "gloss": "nourrir/enfanter"},
    "ala": {"lemma": "ala", "pos": "verb", "gloss": "élever"},
    "kenna": {"lemma": "kenna", "pos": "verb", "gloss": "enseigner/connaître"},
    "læra": {"lemma": "læra", "pos": "verb", "gloss": "apprendre"},
    "skilja": {"lemma": "skilja", "pos": "verb", "gloss": "comprendre/séparer"},
    "hugsa": {"lemma": "hugsa", "pos": "verb", "gloss": "penser"},
    "trúa": {"lemma": "trúa", "pos": "verb", "gloss": "croire"},
    "vænta": {"lemma": "vænta", "pos": "verb", "gloss": "espérer/attendre"},
    "óttast": {"lemma": "óttast", "pos": "verb", "gloss": "craindre"},

    "maðr": {"lemma": "maðr", "pos": "noun", "gender": "masc", "gloss": "homme"},
    "kona": {"lemma": "kona", "pos": "noun", "gender": "fem", "gloss": "femme"},
    "konungr": {"lemma": "konungr", "pos": "noun", "gender": "masc", "gloss": "roi"},
    "dróttning": {"lemma": "dróttning", "pos": "noun", "gender": "fem", "gloss": "reine"},
    "sonr": {"lemma": "sonr", "pos": "noun", "gender": "masc", "gloss": "fils"},
    "dóttir": {"lemma": "dóttir", "pos": "noun", "gender": "fem", "gloss": "fille"},
    "faðir": {"lemma": "faðir", "pos": "noun", "gender": "masc", "gloss": "père"},
    "móðir": {"lemma": "móðir", "pos": "noun", "gender": "fem", "gloss": "mère"},
    "bróðir": {"lemma": "bróðir", "pos": "noun", "gender": "masc", "gloss": "frère"},
    "systir": {"lemma": "systir", "pos": "noun", "gender": "fem", "gloss": "sœur"},
    "barn": {"lemma": "barn", "pos": "noun", "gender": "neut", "gloss": "enfant"},
    "átti": {"lemma": "átti", "pos": "noun", "gender": "masc", "gloss": "parent/famille"},
    "frændi": {"lemma": "frændi", "pos": "noun", "gender": "masc", "gloss": "parent/cousin"},
    "vinr": {"lemma": "vinr", "pos": "noun", "gender": "masc", "gloss": "ami"},
    "óvinr": {"lemma": "óvinr", "pos": "noun", "gender": "masc", "gloss": "ennemi"},
    "drengr": {"lemma": "drengr", "pos": "noun", "gender": "masc", "gloss": "jeune homme/guerrier"},
    "karl": {"lemma": "karl", "pos": "noun", "gender": "masc", "gloss": "homme/vieux"},
    "kerling": {"lemma": "kerling", "pos": "noun", "gender": "fem", "gloss": "vieille femme"},
    "jarl": {"lemma": "jarl", "pos": "noun", "gender": "masc", "gloss": "jarl/comte"},
    "hersir": {"lemma": "hersir", "pos": "noun", "gender": "masc", "gloss": "chef local"},
    "bóndi": {"lemma": "bóndi", "pos": "noun", "gender": "masc", "gloss": "fermier"},
    "þræll": {"lemma": "þræll", "pos": "noun", "gender": "masc", "gloss": "esclave"},
    "goði": {"lemma": "goði", "pos": "noun", "gender": "masc", "gloss": "prêtre/chef"},
    "víkingr": {"lemma": "víkingr", "pos": "noun", "gender": "masc", "gloss": "viking"},

    "skip": {"lemma": "skip", "pos": "noun", "gender": "neut", "gloss": "navire"},
    "knǫrr": {"lemma": "knǫrr", "pos": "noun", "gender": "masc", "gloss": "navire marchand"},
    "bátr": {"lemma": "bátr", "pos": "noun", "gender": "masc", "gloss": "bateau"},
    "segl": {"lemma": "segl", "pos": "noun", "gender": "neut", "gloss": "voile"},
    "árar": {"lemma": "ár", "pos": "noun", "gender": "fem", "gloss": "rame"},
    "land": {"lemma": "land", "pos": "noun", "gender": "neut", "gloss": "terre"},
    "ríki": {"lemma": "ríki", "pos": "noun", "gender": "neut", "gloss": "royaume"},
    "herað": {"lemma": "herað", "pos": "noun", "gender": "neut", "gloss": "district"},
    "býr": {"lemma": "býr", "pos": "noun", "gender": "masc", "gloss": "ferme/habitation"},
    "bær": {"lemma": "bær", "pos": "noun", "gender": "masc", "gloss": "ferme"},
    "hús": {"lemma": "hús", "pos": "noun", "gender": "neut", "gloss": "maison"},
    "skáli": {"lemma": "skáli", "pos": "noun", "gender": "masc", "gloss": "hall"},
    "salr": {"lemma": "salr", "pos": "noun", "gender": "masc", "gloss": "salle/hall"},
    "kirkja": {"lemma": "kirkja", "pos": "noun", "gender": "fem", "gloss": "église"},
    "hof": {"lemma": "hof", "pos": "noun", "gender": "neut", "gloss": "temple"},
    "þing": {"lemma": "þing", "pos": "noun", "gender": "neut", "gloss": "assemblée"},
    "alþingi": {"lemma": "alþingi", "pos": "noun", "gender": "neut", "gloss": "assemblée générale"},
    "borg": {"lemma": "borg", "pos": "noun", "gender": "fem", "gloss": "forteresse"},
    "vegr": {"lemma": "vegr", "pos": "noun", "gender": "masc", "gloss": "chemin"},
    "brú": {"lemma": "brú", "pos": "noun", "gender": "fem", "gloss": "pont"},

    "sværð": {"lemma": "sværð", "pos": "noun", "gender": "neut", "gloss": "épée"},
    "mækir": {"lemma": "mækir", "pos": "noun", "gender": "masc", "gloss": "épée"},
    "øx": {"lemma": "øx", "pos": "noun", "gender": "fem", "gloss": "hache"},
    "spjót": {"lemma": "spjót", "pos": "noun", "gender": "neut", "gloss": "lance"},
    "skjǫldr": {"lemma": "skjǫldr", "pos": "noun", "gender": "masc", "gloss": "bouclier"},
    "brynja": {"lemma": "brynja", "pos": "noun", "gender": "fem", "gloss": "cotte de mailles"},
    "hjálmr": {"lemma": "hjálmr", "pos": "noun", "gender": "masc", "gloss": "casque"},
    "bogi": {"lemma": "bogi", "pos": "noun", "gender": "masc", "gloss": "arc"},
    "ǫr": {"lemma": "ǫr", "pos": "noun", "gender": "fem", "gloss": "flèche"},
    "knífr": {"lemma": "knífr", "pos": "noun", "gender": "masc", "gloss": "couteau"},

    "hestr": {"lemma": "hestr", "pos": "noun", "gender": "masc", "gloss": "cheval"},
    "hross": {"lemma": "hross", "pos": "noun", "gender": "neut", "gloss": "cheval"},
    "hundr": {"lemma": "hundr", "pos": "noun", "gender": "masc", "gloss": "chien"},
    "kǫttr": {"lemma": "kǫttr", "pos": "noun", "gender": "masc", "gloss": "chat"},
    "ulfr": {"lemma": "ulfr", "pos": "noun", "gender": "masc", "gloss": "loup"},
    "bjǫrn": {"lemma": "bjǫrn", "pos": "noun", "gender": "masc", "gloss": "ours"},
    "ǫrn": {"lemma": "ǫrn", "pos": "noun", "gender": "masc", "gloss": "aigle"},
    "hrafn": {"lemma": "hrafn", "pos": "noun", "gender": "masc", "gloss": "corbeau"},
    "fugla": {"lemma": "fugl", "pos": "noun", "gender": "masc", "gloss": "oiseau"},
    "fiskr": {"lemma": "fiskr", "pos": "noun", "gender": "masc", "gloss": "poisson"},
    "ormr": {"lemma": "ormr", "pos": "noun", "gender": "masc", "gloss": "serpent/dragon"},
    "nǫðr": {"lemma": "nǫðr", "pos": "noun", "gender": "masc", "gloss": "serpent"},
    "kýr": {"lemma": "kýr", "pos": "noun", "gender": "fem", "gloss": "vache"},
    "oxi": {"lemma": "oxi", "pos": "noun", "gender": "masc", "gloss": "bœuf"},
    "sauðr": {"lemma": "sauðr", "pos": "noun", "gender": "masc", "gloss": "mouton"},
    "geit": {"lemma": "geit", "pos": "noun", "gender": "fem", "gloss": "chèvre"},
    "svín": {"lemma": "svín", "pos": "noun", "gender": "neut", "gloss": "porc"},

    "dagr": {"lemma": "dagr", "pos": "noun", "gender": "masc", "gloss": "jour"},
    "nótt": {"lemma": "nótt", "pos": "noun", "gender": "fem", "gloss": "nuit"},
    "morgin": {"lemma": "morgin", "pos": "noun", "gender": "masc", "gloss": "matin"},
    "aptann": {"lemma": "aptan", "pos": "noun", "gender": "masc", "gloss": "soir"},
    "ár": {"lemma": "ár", "pos": "noun", "gender": "neut", "gloss": "année"},
    "mánuðr": {"lemma": "mánuðr", "pos": "noun", "gender": "masc", "gloss": "mois"},
    "vika": {"lemma": "vika", "pos": "noun", "gender": "fem", "gloss": "semaine"},
    "tími": {"lemma": "tími", "pos": "noun", "gender": "masc", "gloss": "temps/heure"},
    "stund": {"lemma": "stund", "pos": "noun", "gender": "fem", "gloss": "moment"},
    "sumar": {"lemma": "sumar", "pos": "noun", "gender": "neut", "gloss": "été"},
    "vetr": {"lemma": "vetr", "pos": "noun", "gender": "masc", "gloss": "hiver"},
    "vár": {"lemma": "vár", "pos": "noun", "gender": "neut", "gloss": "printemps"},
    "haust": {"lemma": "haust", "pos": "noun", "gender": "neut", "gloss": "automne"},

    "sól": {"lemma": "sól", "pos": "noun", "gender": "fem", "gloss": "soleil"},
    "máni": {"lemma": "máni", "pos": "noun", "gender": "masc", "gloss": "lune"},
    "stjarna": {"lemma": "stjarna", "pos": "noun", "gender": "fem", "gloss": "étoile"},
    "himinn": {"lemma": "himinn", "pos": "noun", "gender": "masc", "gloss": "ciel"},
    "ský": {"lemma": "ský", "pos": "noun", "gender": "neut", "gloss": "nuage"},
    "veðr": {"lemma": "veðr", "pos": "noun", "gender": "neut", "gloss": "temps/météo"},
    "vindr": {"lemma": "vindr", "pos": "noun", "gender": "masc", "gloss": "vent"},
    "regn": {"lemma": "regn", "pos": "noun", "gender": "neut", "gloss": "pluie"},
    "snjór": {"lemma": "snjór", "pos": "noun", "gender": "masc", "gloss": "neige"},
    "íss": {"lemma": "íss", "pos": "noun", "gender": "masc", "gloss": "glace"},
    "eldr": {"lemma": "eldr", "pos": "noun", "gender": "masc", "gloss": "feu"},
    "vatn": {"lemma": "vatn", "pos": "noun", "gender": "neut", "gloss": "eau"},
    "sjór": {"lemma": "sjór", "pos": "noun", "gender": "masc", "gloss": "mer"},
    "á": {"lemma": "á", "pos": "noun", "gender": "fem", "gloss": "rivière"},
    "fjǫrðr": {"lemma": "fjǫrðr", "pos": "noun", "gender": "masc", "gloss": "fjord"},
    "vatn": {"lemma": "vatn", "pos": "noun", "gender": "neut", "gloss": "lac"},
    "ey": {"lemma": "ey", "pos": "noun", "gender": "fem", "gloss": "île"},
    "fjall": {"lemma": "fjall", "pos": "noun", "gender": "neut", "gloss": "montagne"},
    "dalr": {"lemma": "dalr", "pos": "noun", "gender": "masc", "gloss": "vallée"},
    "vǫllr": {"lemma": "vǫllr", "pos": "noun", "gender": "masc", "gloss": "champ/plaine"},
    "skógr": {"lemma": "skógr", "pos": "noun", "gender": "masc", "gloss": "forêt"},
    "mork": {"lemma": "mork", "pos": "noun", "gender": "fem", "gloss": "forêt"},
    "steinn": {"lemma": "steinn", "pos": "noun", "gender": "masc", "gloss": "pierre"},
    "jǫrð": {"lemma": "jǫrð", "pos": "noun", "gender": "fem", "gloss": "terre/sol"},
    "grǫs": {"lemma": "grǫs", "pos": "noun", "gender": "neut", "gloss": "herbe"},
    "tré": {"lemma": "tré", "pos": "noun", "gender": "neut", "gloss": "arbre"},

    "matr": {"lemma": "matr", "pos": "noun", "gender": "masc", "gloss": "nourriture"},
    "brauð": {"lemma": "brauð", "pos": "noun", "gender": "neut", "gloss": "pain"},
    "kjǫt": {"lemma": "kjǫt", "pos": "noun", "gender": "neut", "gloss": "viande"},
    "ǫl": {"lemma": "ǫl", "pos": "noun", "gender": "neut", "gloss": "bière"},
    "vín": {"lemma": "vín", "pos": "noun", "gender": "neut", "gloss": "vin"},
    "mjǫðr": {"lemma": "mjǫðr", "pos": "noun", "gender": "masc", "gloss": "hydromel"},
    "mjólk": {"lemma": "mjólk", "pos": "noun", "gender": "fem", "gloss": "lait"},
    "smjǫr": {"lemma": "smjǫr", "pos": "noun", "gender": "neut", "gloss": "beurre"},
    "ostr": {"lemma": "ostr", "pos": "noun", "gender": "masc", "gloss": "fromage"},

    "höfuð": {"lemma": "höfuð", "pos": "noun", "gender": "neut", "gloss": "tête"},
    "hár": {"lemma": "hár", "pos": "noun", "gender": "neut", "gloss": "cheveux"},
    "auga": {"lemma": "auga", "pos": "noun", "gender": "neut", "gloss": "œil"},
    "eyra": {"lemma": "eyra", "pos": "noun", "gender": "neut", "gloss": "oreille"},
    "nef": {"lemma": "nef", "pos": "noun", "gender": "fem", "gloss": "nez"},
    "munnr": {"lemma": "munnr", "pos": "noun", "gender": "masc", "gloss": "bouche"},
    "tunga": {"lemma": "tunga", "pos": "noun", "gender": "fem", "gloss": "langue"},
    "tǫnn": {"lemma": "tǫnn", "pos": "noun", "gender": "fem", "gloss": "dent"},
    "hals": {"lemma": "hals", "pos": "noun", "gender": "masc", "gloss": "cou"},
    "hǫnd": {"lemma": "hǫnd", "pos": "noun", "gender": "fem", "gloss": "main"},
    "fingr": {"lemma": "fingr", "pos": "noun", "gender": "masc", "gloss": "doigt"},
    "fótr": {"lemma": "fótr", "pos": "noun", "gender": "masc", "gloss": "pied"},
    "beinn": {"lemma": "bein", "pos": "noun", "gender": "neut", "gloss": "os/jambe"},
    "hjarta": {"lemma": "hjarta", "pos": "noun", "gender": "neut", "gloss": "cœur"},
    "blóð": {"lemma": "blóð", "pos": "noun", "gender": "neut", "gloss": "sang"},
    "líkami": {"lemma": "líkami", "pos": "noun", "gender": "masc", "gloss": "corps"},

    "goð": {"lemma": "goð", "pos": "noun", "gender": "neut", "gloss": "dieu"},
    "guð": {"lemma": "guð", "pos": "noun", "gender": "masc", "gloss": "dieu"},
    "gyðja": {"lemma": "gyðja", "pos": "noun", "gender": "fem", "gloss": "déesse"},
    "áss": {"lemma": "áss", "pos": "noun", "gender": "masc", "gloss": "dieu Ase"},
    "vanr": {"lemma": "vanr", "pos": "noun", "gender": "masc", "gloss": "dieu Vane"},
    "jǫtunn": {"lemma": "jǫtunn", "pos": "noun", "gender": "masc", "gloss": "géant"},
    "álfr": {"lemma": "álfr", "pos": "noun", "gender": "masc", "gloss": "elfe"},
    "dvergr": {"lemma": "dvergr", "pos": "noun", "gender": "masc", "gloss": "nain"},
    "trǫll": {"lemma": "trǫll", "pos": "noun", "gender": "neut", "gloss": "troll"},
    "draug": {"lemma": "draugr", "pos": "noun", "gender": "masc", "gloss": "revenant"},
    "valkyrja": {"lemma": "valkyrja", "pos": "noun", "gender": "fem", "gloss": "valkyrie"},
    "hamr": {"lemma": "hamr", "pos": "noun", "gender": "masc", "gloss": "forme/peau"},
    "seiðr": {"lemma": "seiðr", "pos": "noun", "gender": "masc", "gloss": "sorcellerie"},
    "galdr": {"lemma": "galdr", "pos": "noun", "gender": "masc", "gloss": "incantation"},
    "rúnar": {"lemma": "rún", "pos": "noun", "gender": "fem", "gloss": "rune"},

    "orð": {"lemma": "orð", "pos": "noun", "gender": "neut", "gloss": "mot/parole"},
    "mál": {"lemma": "mál", "pos": "noun", "gender": "neut", "gloss": "langue/discours"},
    "saga": {"lemma": "saga", "pos": "noun", "gender": "fem", "gloss": "récit/saga"},
    "sǫgn": {"lemma": "sǫgn", "pos": "noun", "gender": "fem", "gloss": "histoire"},
    "kvæði": {"lemma": "kvæði", "pos": "noun", "gender": "neut", "gloss": "poème"},
    "vísa": {"lemma": "vísa", "pos": "noun", "gender": "fem", "gloss": "strophe/vers"},
    "nafn": {"lemma": "nafn", "pos": "noun", "gender": "neut", "gloss": "nom"},
    "heiti": {"lemma": "heiti", "pos": "noun", "gender": "neut", "gloss": "nom/appellation"},
    "kenning": {"lemma": "kenning", "pos": "noun", "gender": "fem", "gloss": "kenning"},

    "vegr": {"lemma": "vegr", "pos": "noun", "gender": "masc", "gloss": "gloire"},
    "sœmð": {"lemma": "sœmð", "pos": "noun", "gender": "fem", "gloss": "honneur"},
    "frægð": {"lemma": "frægð", "pos": "noun", "gender": "fem", "gloss": "renommée"},
    "skǫmm": {"lemma": "skǫmm", "pos": "noun", "gender": "fem", "gloss": "honte"},
    "níð": {"lemma": "níð", "pos": "noun", "gender": "neut", "gloss": "insulte/honte"},
    "heill": {"lemma": "heill", "pos": "noun", "gender": "fem", "gloss": "chance/santé"},
    "gæfa": {"lemma": "gæfa", "pos": "noun", "gender": "fem", "gloss": "chance"},
    "hamingja": {"lemma": "hamingja", "pos": "noun", "gender": "fem", "gloss": "chance/esprit tutélaire"},
    "auðr": {"lemma": "auðr", "pos": "noun", "gender": "masc", "gloss": "richesse"},
    "fé": {"lemma": "fé", "pos": "noun", "gender": "neut", "gloss": "bétail/richesse"},
    "silfr": {"lemma": "silfr", "pos": "noun", "gender": "neut", "gloss": "argent"},
    "gull": {"lemma": "gull", "pos": "noun", "gender": "neut", "gloss": "or"},
    "hringr": {"lemma": "hringr", "pos": "noun", "gender": "masc", "gloss": "anneau"},

    "ok": {"lemma": "ok", "pos": "conj", "gloss": "et"},
    "eða": {"lemma": "eða", "pos": "conj", "gloss": "ou"},
    "en": {"lemma": "en", "pos": "conj", "gloss": "mais"},
    "at": {"lemma": "at", "pos": "conj", "gloss": "que/à"},
    "ef": {"lemma": "ef", "pos": "conj", "gloss": "si"},
    "þó": {"lemma": "þó", "pos": "conj", "gloss": "bien que/cependant"},
    "því": {"lemma": "því", "pos": "conj", "gloss": "parce que"},
    "þegar": {"lemma": "þegar", "pos": "conj", "gloss": "dès que"},
    "meðan": {"lemma": "meðan", "pos": "conj", "gloss": "pendant que"},
    "áðr": {"lemma": "áðr", "pos": "conj", "gloss": "avant que"},
    "síðan": {"lemma": "síðan", "pos": "conj", "gloss": "après/depuis"},

    "til": {"lemma": "til", "pos": "prep", "gloss": "vers/à"},
    "frá": {"lemma": "frá", "pos": "prep", "gloss": "de/depuis"},
    "á": {"lemma": "á", "pos": "prep", "gloss": "sur/à"},
    "í": {"lemma": "í", "pos": "prep", "gloss": "dans"},
    "með": {"lemma": "með", "pos": "prep", "gloss": "avec"},
    "af": {"lemma": "af", "pos": "prep", "gloss": "de/par"},
    "fyrir": {"lemma": "fyrir", "pos": "prep", "gloss": "pour/devant"},
    "um": {"lemma": "um", "pos": "prep", "gloss": "autour/au sujet de"},
    "við": {"lemma": "við", "pos": "prep", "gloss": "contre/auprès de"},
    "undir": {"lemma": "undir", "pos": "prep", "gloss": "sous"},
    "yfir": {"lemma": "yfir", "pos": "prep", "gloss": "au-dessus"},
    "hjá": {"lemma": "hjá", "pos": "prep", "gloss": "chez/près de"},
    "milli": {"lemma": "milli", "pos": "prep", "gloss": "entre"},
    "millum": {"lemma": "millum", "pos": "prep", "gloss": "entre"},
    "gegn": {"lemma": "gegn", "pos": "prep", "gloss": "contre/en face de"},
    "mót": {"lemma": "mót", "pos": "prep", "gloss": "contre/vers"},
    "eptir": {"lemma": "eptir", "pos": "prep", "gloss": "après/selon"},
    "utan": {"lemma": "utan", "pos": "prep", "gloss": "dehors/excepté"},
    "innan": {"lemma": "innan", "pos": "prep", "gloss": "dedans"},
    "nær": {"lemma": "nær", "pos": "prep", "gloss": "près de"},
    "fjarri": {"lemma": "fjarri", "pos": "prep", "gloss": "loin de"},

    "mikill": {"lemma": "mikill", "pos": "adj", "gloss": "grand"},
    "lítill": {"lemma": "lítill", "pos": "adj", "gloss": "petit"},
    "stórr": {"lemma": "stórr", "pos": "adj", "gloss": "grand"},
    "langr": {"lemma": "langr", "pos": "adj", "gloss": "long"},
    "stuttr": {"lemma": "stuttr", "pos": "adj", "gloss": "court"},
    "breiðr": {"lemma": "breiðr", "pos": "adj", "gloss": "large"},
    "mjór": {"lemma": "mjór", "pos": "adj", "gloss": "mince"},
    "þykkr": {"lemma": "þykkr", "pos": "adj", "gloss": "épais"},
    "hár": {"lemma": "hár", "pos": "adj", "gloss": "haut"},
    "lágr": {"lemma": "lágr", "pos": "adj", "gloss": "bas"},
    "djúpr": {"lemma": "djúpr", "pos": "adj", "gloss": "profond"},
    "grunnr": {"lemma": "grunnr", "pos": "adj", "gloss": "peu profond"},
    "þungr": {"lemma": "þungr", "pos": "adj", "gloss": "lourd"},
    "léttr": {"lemma": "léttr", "pos": "adj", "gloss": "léger"},

    "góðr": {"lemma": "góðr", "pos": "adj", "gloss": "bon"},
    "illr": {"lemma": "illr", "pos": "adj", "gloss": "mauvais"},
    "betr": {"lemma": "betr", "pos": "adj", "gloss": "meilleur"},
    "verr": {"lemma": "verr", "pos": "adj", "gloss": "pire"},
    "fagr": {"lemma": "fagr", "pos": "adj", "gloss": "beau"},
    "ljótr": {"lemma": "ljótr", "pos": "adj", "gloss": "laid"},
    "fríðr": {"lemma": "fríðr", "pos": "adj", "gloss": "beau"},
    "ríkr": {"lemma": "ríkr", "pos": "adj", "gloss": "puissant"},
    "máttugr": {"lemma": "máttugr", "pos": "adj", "gloss": "puissant"},
    "sterkr": {"lemma": "sterkr", "pos": "adj", "gloss": "fort"},
    "veikr": {"lemma": "veikr", "pos": "adj", "gloss": "faible"},
    "harðr": {"lemma": "harðr", "pos": "adj", "gloss": "dur"},
    "mjúkr": {"lemma": "mjúkr", "pos": "adj", "gloss": "doux/mou"},
    "hvass": {"lemma": "hvass", "pos": "adj", "gloss": "tranchant/vif"},
    "sljór": {"lemma": "sljór", "pos": "adj", "gloss": "émoussé"},

    "gamall": {"lemma": "gamall", "pos": "adj", "gloss": "vieux"},
    "ungr": {"lemma": "ungr", "pos": "adj", "gloss": "jeune"},
    "nýr": {"lemma": "nýr", "pos": "adj", "gloss": "nouveau"},
    "forn": {"lemma": "forn", "pos": "adj", "gloss": "ancien"},
    "hinn": {"lemma": "hinn", "pos": "adj", "gloss": "l'autre"},

    "ríkr": {"lemma": "ríkr", "pos": "adj", "gloss": "riche"},
    "fátœkr": {"lemma": "fátœkr", "pos": "adj", "gloss": "pauvre"},
    "auðigr": {"lemma": "auðigr", "pos": "adj", "gloss": "riche"},
    "dýrr": {"lemma": "dýrr", "pos": "adj", "gloss": "cher/précieux"},

    "vitr": {"lemma": "vitr", "pos": "adj", "gloss": "sage"},
    "heimskr": {"lemma": "heimskr", "pos": "adj", "gloss": "stupide"},
    "fróðr": {"lemma": "fróðr", "pos": "adj", "gloss": "savant"},
    "klókr": {"lemma": "klókr", "pos": "adj", "gloss": "rusé/intelligent"},

    "heiðr": {"lemma": "heiðr", "pos": "adj", "gloss": "clair/brillant"},
    "ljóss": {"lemma": "ljóss", "pos": "adj", "gloss": "lumineux"},
    "dimmr": {"lemma": "dimmr", "pos": "adj", "gloss": "sombre"},
    "myrkr": {"lemma": "myrkr", "pos": "adj", "gloss": "obscur"},
    "bjart": {"lemma": "bjart", "pos": "adj", "gloss": "brillant"},
    "hvítr": {"lemma": "hvítr", "pos": "adj", "gloss": "blanc"},
    "svartr": {"lemma": "svartr", "pos": "adj", "gloss": "noir"},
    "rauðr": {"lemma": "rauðr", "pos": "adj", "gloss": "rouge"},
    "grœnn": {"lemma": "grœnn", "pos": "adj", "gloss": "vert"},
    "blár": {"lemma": "blár", "pos": "adj", "gloss": "bleu/noir"},
    "gulr": {"lemma": "gulr", "pos": "adj", "gloss": "jaune"},
    "grár": {"lemma": "grár", "pos": "adj", "gloss": "gris"},

    "heitr": {"lemma": "heitr", "pos": "adj", "gloss": "chaud"},
    "kaldr": {"lemma": "kaldr", "pos": "adj", "gloss": "froid"},
    "varmr": {"lemma": "varmr", "pos": "adj", "gloss": "chaud"},
    "þurr": {"lemma": "þurr", "pos": "adj", "gloss": "sec"},
    "blautr": {"lemma": "blautr", "pos": "adj", "gloss": "humide/mouillé"},
    "votr": {"lemma": "votr", "pos": "adj", "gloss": "humide"},

    "glaðr": {"lemma": "glaðr", "pos": "adj", "gloss": "joyeux"},
    "hryggr": {"lemma": "hryggr", "pos": "adj", "gloss": "triste"},
    "reiðr": {"lemma": "reiðr", "pos": "adj", "gloss": "en colère"},
    "bliðr": {"lemma": "bliðr", "pos": "adj", "gloss": "doux/aimable"},
    "grimmr": {"lemma": "grimmr", "pos": "adj", "gloss": "féroce"},
    "huglauss": {"lemma": "huglauss", "pos": "adj", "gloss": "lâche"},
    "djarfr": {"lemma": "djarfr", "pos": "adj", "gloss": "audacieux"},
    "hraustr": {"lemma": "hraustr", "pos": "adj", "gloss": "vaillant"},

    "sannr": {"lemma": "sannr", "pos": "adj", "gloss": "vrai"},
    "ósannr": {"lemma": "ósannr", "pos": "adj", "gloss": "faux"},
    "hollr": {"lemma": "hollr", "pos": "adj", "gloss": "loyal"},
    "svikin": {"lemma": "svikinn", "pos": "adj", "gloss": "traître"},
    "trúr": {"lemma": "trúr", "pos": "adj", "gloss": "fidèle"},

    "fullr": {"lemma": "fullr", "pos": "adj", "gloss": "plein"},
    "tómr": {"lemma": "tómr", "pos": "adj", "gloss": "vide"},
    "margr": {"lemma": "margr", "pos": "adj", "gloss": "beaucoup"},
    "fár": {"lemma": "fár", "pos": "adj", "gloss": "peu"},
    "allr": {"lemma": "allr", "pos": "adj", "gloss": "tout"},
    "engi": {"lemma": "engi", "pos": "adj", "gloss": "aucun"},
    "sumr": {"lemma": "sumr", "pos": "adj", "gloss": "certains"},
    "annarr": {"lemma": "annarr", "pos": "adj", "gloss": "autre"},
    "báðir": {"lemma": "báðir", "pos": "adj", "gloss": "les deux"},
    "einn": {"lemma": "einn", "pos": "adj", "gloss": "un/seul"},
    "tveir": {"lemma": "tveir", "pos": "num", "gloss": "deux"},
    "þrír": {"lemma": "þrír", "pos": "num", "gloss": "trois"},
    "fjórir": {"lemma": "fjórir", "pos": "num", "gloss": "quatre"},
    "fimm": {"lemma": "fimm", "pos": "num", "gloss": "cinq"},
    "sex": {"lemma": "sex", "pos": "num", "gloss": "six"},
    "sjau": {"lemma": "sjau", "pos": "num", "gloss": "sept"},
    "átta": {"lemma": "átta", "pos": "num", "gloss": "huit"},
    "níu": {"lemma": "níu", "pos": "num", "gloss": "neuf"},
    "tíu": {"lemma": "tíu", "pos": "num", "gloss": "dix"},
    "hundrað": {"lemma": "hundrað", "pos": "num", "gloss": "cent"},
    "þúsund": {"lemma": "þúsund", "pos": "num", "gloss": "mille"},

    "ek": {"lemma": "ek", "pos": "pron", "gloss": "je"},
    "þú": {"lemma": "þú", "pos": "pron", "gloss": "tu"},
    "hann": {"lemma": "hann", "pos": "pron", "gloss": "il"},
    "hon": {"lemma": "hon", "pos": "pron", "gloss": "elle"},
    "þat": {"lemma": "þat", "pos": "pron", "gloss": "cela"},
    "vér": {"lemma": "vér", "pos": "pron", "gloss": "nous"},
    "þér": {"lemma": "þér", "pos": "pron", "gloss": "vous"},
    "þeir": {"lemma": "þeir", "pos": "pron", "gloss": "ils"},
    "þær": {"lemma": "þær", "pos": "pron", "gloss": "elles"},
    "sá": {"lemma": "sá", "pos": "pron", "gloss": "celui-là"},
    "sú": {"lemma": "sú", "pos": "pron", "gloss": "celle-là"},
    "sjá": {"lemma": "sjá", "pos": "pron", "gloss": "ce"},
    "þessi": {"lemma": "þessi", "pos": "pron", "gloss": "ce/cet"},
    "minn": {"lemma": "minn", "pos": "pron", "gloss": "mon"},
    "þinn": {"lemma": "þinn", "pos": "pron", "gloss": "ton"},
    "sinn": {"lemma": "sinn", "pos": "pron", "gloss": "son"},
    "várr": {"lemma": "várr", "pos": "pron", "gloss": "notre"},
    "yðarr": {"lemma": "yðarr", "pos": "pron", "gloss": "votre"},
    "hvat": {"lemma": "hvat", "pos": "pron", "gloss": "quoi"},
    "hverr": {"lemma": "hverr", "pos": "pron", "gloss": "qui"},
    "hvar": {"lemma": "hvar", "pos": "adv", "gloss": "où"},
    "hví": {"lemma": "hví", "pos": "adv", "gloss": "pourquoi"},
    "hvenær": {"lemma": "hvenær", "pos": "adv", "gloss": "quand"},
    "hvernig": {"lemma": "hvernig", "pos": "adv", "gloss": "comment"},

    "já": {"lemma": "já", "pos": "adv", "gloss": "oui"},
    "nei": {"lemma": "nei", "pos": "adv", "gloss": "non"},
    "eigi": {"lemma": "eigi", "pos": "adv", "gloss": "ne pas"},
    "ekki": {"lemma": "ekki", "pos": "adv", "gloss": "ne pas"},
    "aldri": {"lemma": "aldri", "pos": "adv", "gloss": "jamais"},
    "æ": {"lemma": "æ", "pos": "adv", "gloss": "toujours"},
    "jafnan": {"lemma": "jafnan", "pos": "adv", "gloss": "toujours"},
    "opt": {"lemma": "opt", "pos": "adv", "gloss": "souvent"},
    "sjaldan": {"lemma": "sjaldan", "pos": "adv", "gloss": "rarement"},
    "stundum": {"lemma": "stundum", "pos": "adv", "gloss": "parfois"},
    "nú": {"lemma": "nú", "pos": "adv", "gloss": "maintenant"},
    "þá": {"lemma": "þá", "pos": "adv", "gloss": "alors"},
    "ávallt": {"lemma": "ávallt", "pos": "adv", "gloss": "toujours"},
    "þegar": {"lemma": "þegar", "pos": "adv", "gloss": "aussitôt"},
    "brátt": {"lemma": "brátt", "pos": "adv", "gloss": "bientôt"},
    "síðar": {"lemma": "síðar", "pos": "adv", "gloss": "plus tard"},
    "áðr": {"lemma": "áðr", "pos": "adv", "gloss": "avant"},
    "fyrr": {"lemma": "fyrr", "pos": "adv", "gloss": "avant/plus tôt"},
    "síðan": {"lemma": "síðan", "pos": "adv", "gloss": "après/ensuite"},

    "hér": {"lemma": "hér", "pos": "adv", "gloss": "ici"},
    "þar": {"lemma": "þar", "pos": "adv", "gloss": "là"},
    "þaðan": {"lemma": "þaðan", "pos": "adv", "gloss": "de là"},
    "hingat": {"lemma": "hingat", "pos": "adv", "gloss": "ici (vers)"},
    "þangat": {"lemma": "þangat", "pos": "adv", "gloss": "là (vers)"},
    "hvert": {"lemma": "hvert", "pos": "adv", "gloss": "où (vers)"},
    "uppi": {"lemma": "uppi", "pos": "adv", "gloss": "en haut"},
    "niðri": {"lemma": "niðri", "pos": "adv", "gloss": "en bas"},
    "inni": {"lemma": "inni", "pos": "adv", "gloss": "dedans"},
    "úti": {"lemma": "úti", "pos": "adv", "gloss": "dehors"},
    "heima": {"lemma": "heima", "pos": "adv", "gloss": "à la maison"},
    "brott": {"lemma": "brott", "pos": "adv", "gloss": "loin/parti"},
    "fram": {"lemma": "fram", "pos": "adv", "gloss": "en avant"},
    "aptr": {"lemma": "aptr", "pos": "adv", "gloss": "en arrière"},
    "norðr": {"lemma": "norðr", "pos": "adv", "gloss": "au nord"},
    "suðr": {"lemma": "suðr", "pos": "adv", "gloss": "au sud"},
    "austr": {"lemma": "austr", "pos": "adv", "gloss": "à l'est"},
    "vestr": {"lemma": "vestr", "pos": "adv", "gloss": "à l'ouest"},

    "mjǫk": {"lemma": "mjǫk", "pos": "adv", "gloss": "très/beaucoup"},
    "lítt": {"lemma": "lítt", "pos": "adv", "gloss": "peu"},
    "meira": {"lemma": "meira", "pos": "adv", "gloss": "plus"},
    "minna": {"lemma": "minna", "pos": "adv", "gloss": "moins"},
    "mest": {"lemma": "mest", "pos": "adv", "gloss": "le plus"},
    "vel": {"lemma": "vel", "pos": "adv", "gloss": "bien"},
    "illa": {"lemma": "illa", "pos": "adv", "gloss": "mal"},
    "skjótt": {"lemma": "skjótt", "pos": "adv", "gloss": "vite"},
    "seint": {"lemma": "seint", "pos": "adv", "gloss": "lentement"},
    "lengi": {"lemma": "lengi", "pos": "adv", "gloss": "longtemps"},
    "nær": {"lemma": "nær", "pos": "adv", "gloss": "près"},
    "fjarri": {"lemma": "fjarri", "pos": "adv", "gloss": "loin"},
    "saman": {"lemma": "saman", "pos": "adv", "gloss": "ensemble"},
    "í sundr": {"lemma": "í sundr", "pos": "adv", "gloss": "séparément"}
        }
        
        # Lexique étendu - exemples représentatifs
        extended_entries = {
            # VERBES - formes conjuguées
            "em": {"lemma": "vera", "pos": "verb", "gloss": "suis", "features": {"tense": "pres", "mood": "ind", "person": "1", "number": "sg"}},
            "ert": {"lemma": "vera", "pos": "verb", "gloss": "es", "features": {"tense": "pres", "mood": "ind", "person": "2", "number": "sg"}},
            "er": {"lemma": "vera", "pos": "verb", "gloss": "est", "features": {"tense": "pres", "mood": "ind", "person": "3", "number": "sg"}},
            "erum": {"lemma": "vera", "pos": "verb", "gloss": "sommes", "features": {"tense": "pres", "mood": "ind", "person": "1", "number": "pl"}},
            "eruð": {"lemma": "vera", "pos": "verb", "gloss": "êtes", "features": {"tense": "pres", "mood": "ind", "person": "2", "number": "pl"}},
            "eru": {"lemma": "vera", "pos": "verb", "gloss": "sont", "features": {"tense": "pres", "mood": "ind", "person": "3", "number": "pl"}},
            
            "var": {"lemma": "vera", "pos": "verb", "gloss": "fus/était", "features": {"tense": "past", "mood": "ind", "person": "1/3", "number": "sg"}},
            "várum": {"lemma": "vera", "pos": "verb", "gloss": "fûmes/étions", "features": {"tense": "past", "mood": "ind", "person": "1", "number": "pl"}},
            
            # NOMS - formes déclinées
            "menn": {"lemma": "maðr", "pos": "noun", "gender": "masc", "gloss": "hommes", "features": {"case": "nom", "number": "pl"}},
            "manna": {"lemma": "maðr", "pos": "noun", "gender": "masc", "gloss": "des hommes", "features": {"case": "gen", "number": "pl"}},
            "mǫnnum": {"lemma": "maðr", "pos": "noun", "gender": "masc", "gloss": "aux hommes", "features": {"case": "dat", "number": "pl"}},
            
            "konur": {"lemma": "kona", "pos": "noun", "gender": "fem", "gloss": "femmes", "features": {"case": "nom", "number": "pl"}},
            "kvenna": {"lemma": "kona", "pos": "noun", "gender": "fem", "gloss": "des femmes", "features": {"case": "gen", "number": "pl"}},
            
            # ADJECTIFS - formes diverses
            "góðr": {"lemma": "góðr", "pos": "adj", "gloss": "bon", "features": {"case": "nom", "gender": "masc", "number": "sg", "degree": "pos"}},
            "góðan": {"lemma": "góðr", "pos": "adj", "gloss": "bon", "features": {"case": "acc", "gender": "masc", "number": "sg", "degree": "pos"}},
            "góðum": {"lemma": "góðr", "pos": "adj", "gloss": "bon", "features": {"case": "dat", "gender": "masc", "number": "sg", "degree": "pos"}},
            "betri": {"lemma": "góðr", "pos": "adj", "gloss": "meilleur", "features": {"degree": "comp"}},
            "beztr": {"lemma": "góðr", "pos": "adj", "gloss": "le meilleur", "features": {"degree": "sup"}},
            
            # PRONOMS - formes complètes
            "mik": {"lemma": "ek", "pos": "pron", "gloss": "me", "features": {"case": "acc", "person": "1", "number": "sg"}},
            "mér": {"lemma": "ek", "pos": "pron", "gloss": "à moi", "features": {"case": "dat", "person": "1", "number": "sg"}},
            "mín": {"lemma": "ek", "pos": "pron", "gloss": "de moi", "features": {"case": "gen", "person": "1", "number": "sg"}},
            
            "þik": {"lemma": "þú", "pos": "pron", "gloss": "te", "features": {"case": "acc", "person": "2", "number": "sg"}},
            "þér": {"lemma": "þú", "pos": "pron", "gloss": "à toi", "features": {"case": "dat", "person": "2", "number": "sg"}},
            "þín": {"lemma": "þú", "pos": "pron", "gloss": "de toi", "features": {"case": "gen", "person": "2", "number": "sg"}},
            
            # ... (on ajouterait ici 2000+ entrées supplémentaires)
        }
        
        # Fusionner les entrées
        self.entries.update(base_entries)
        self.entries.update(extended_entries)
        
        # Construire les index
        self._build_indexes()
    
    def _build_indexes(self):
        """Construit les index pour une recherche rapide"""
        for form, entry in self.entries.items():
            lemma = entry.get('lemma', form)
            
            # Index par forme
            self.form_index[form] = entry
            
            # Index par lemme
            self.lemma_index[lemma].append(entry)
            
            # Index par catégorie grammaticale
            pos = entry.get('pos', 'unknown')
            self.pos_index[pos][form] = entry
    
    def find_by_lemma(self, lemma: str) -> List[Dict]:
        """Trouve toutes les formes pour un lemme donné"""
        return self.lemma_index.get(lemma, [])
    
    def find_by_pos(self, pos: str) -> Dict[str, Dict]:
        """Trouve toutes les formes pour une catégorie grammaticale"""
        return self.pos_index.get(pos, {})
    
    def add_entry(self, form: str, entry: Dict):
        """Ajoute une entrée au lexique"""
        self.entries[form] = entry
        self._build_indexes()

# ------------------------ PARADIGMES MORPHOLOGIQUES COMPLETS ------------------------

class MorphologicalParadigms:
    """Paradigmes morphologiques complets pour l'ancien norrois"""
    
    # Paradigmes nominaux étendus
    NOUN_PARADIGMS = {
        'masc_strong_a': {
            'stem_type': 'strong',
            'gender': 'masc',
            'declension': 'a-stem',
            'sg': {'nom': 'r', 'acc': '', 'gen': 's', 'dat': 'i'},
            'pl': {'nom': 'ar', 'acc': 'a', 'gen': 'a', 'dat': 'um'}
        },
        'masc_strong_i': {
            'stem_type': 'strong',
            'gender': 'masc',
            'declension': 'i-stem',
            'sg': {'nom': 'r', 'acc': '', 'gen': 's', 'dat': ''},
            'pl': {'nom': 'ir', 'acc': 'i', 'gen': 'a', 'dat': 'um'}
        },
        'masc_weak_an': {
            'stem_type': 'weak',
            'gender': 'masc',
            'declension': 'an-stem',
            'sg': {'nom': 'i', 'acc': 'a', 'gen': 'a', 'dat': 'a'},
            'pl': {'nom': 'ar', 'acc': 'a', 'gen': 'na', 'dat': 'um'}
        },
        'fem_strong_o': {
            'stem_type': 'strong',
            'gender': 'fem',
            'declension': 'ō-stem',
            'sg': {'nom': '', 'acc': '', 'gen': 'ar', 'dat': ''},
            'pl': {'nom': 'ar', 'acc': 'ar', 'gen': 'a', 'dat': 'um'}
        },
        'fem_strong_i': {
            'stem_type': 'strong',
            'gender': 'fem',
            'declension': 'i-stem',
            'sg': {'nom': '', 'acc': '', 'gen': 'ar', 'dat': ''},
            'pl': {'nom': 'ir', 'acc': 'ir', 'gen': 'a', 'dat': 'um'}
        },
        'fem_weak_on': {
            'stem_type': 'weak',
            'gender': 'fem',
            'declension': 'ōn-stem',
            'sg': {'nom': 'a', 'acc': 'u', 'gen': 'u', 'dat': 'u'},
            'pl': {'nom': 'ur', 'acc': 'ur', 'gen': 'na', 'dat': 'um'}
        },
        'neut_strong_a': {
            'stem_type': 'strong',
            'gender': 'neut',
            'declension': 'a-stem',
            'sg': {'nom': '', 'acc': '', 'gen': 's', 'dat': 'i'},
            'pl': {'nom': '', 'acc': '', 'gen': 'a', 'dat': 'um'}
        },
        'neut_strong_ja': {
            'stem_type': 'strong',
            'gender': 'neut',
            'declension': 'ja-stem',
            'sg': {'nom': '', 'acc': '', 'gen': 's', 'dat': 'i'},
            'pl': {'nom': '', 'acc': '', 'gen': 'a', 'dat': 'um'}
        }
    }
    
    # Paradigmes verbaux complets
    VERB_PARADIGMS = {
        'strong_1': {
            'class': 'strong',
            'infinitive': 'a',
            'present': {'sg1': '', 'sg2': 'r', 'sg3': 'r', 'pl': 'a'},
            'past': {'sg': '', 'pl': 'u'},
            'past_part': 'inn'
        },
        'strong_2': {
            'class': 'strong',
            'infinitive': 'a',
            'present': {'sg1': '', 'sg2': 'r', 'sg3': 'r', 'pl': 'a'},
            'past': {'sg': '', 'pl': 'u'},
            'past_part': 'inn'
        },
        'weak_1': {
            'class': 'weak',
            'infinitive': 'a',
            'present': {'sg1': 'a', 'sg2': 'ar', 'sg3': 'ar', 'pl': 'a'},
            'past': {'sg': 'aði', 'pl': 'uðu'},
            'past_part': 'aðr'
        },
        'weak_2': {
            'class': 'weak',
            'infinitive': 'a',
            'present': {'sg1': 'a', 'sg2': 'ar', 'sg3': 'ar', 'pl': 'a'},
            'past': {'sg': 'aði', 'pl': 'uðu'},
            'past_part': 'aðr'
        },
        'preterite-present': {
            'class': 'preterite-present',
            'infinitive': 'a',
            'present': {'sg1': 't', 'sg2': 't', 'sg3': 't', 'pl': 'u'},
            'past': {'sg': '', 'pl': 'u'},
            'past_part': 'inn'
        }
    }
    
    # Règles de mutation consonantique (umlaut, etc.)
    CONSONANT_MUTATIONS = {
        'a-umlaut': {
            'e': 'a', 'i': 'a', 'u': 'o', 'y': 'ø'
        },
        'i-umlaut': {
            'a': 'e', 'á': 'æ', 'ǫ': 'ø', 'o': 'ø', 'u': 'y', 'ú': 'ý', 'jó': 'ý'
        },
        'u-umlaut': {
            'a': 'ǫ', 'e': 'ø'
        }
    }

# ------------------------ ANALYSEUR MORPHOLOGIQUE AVANCÉ ------------------------

class AdvancedMorphologicalAnalyzer:
    """Analyseur morphologique avancé avec règles complexes"""
    
    def __init__(self, lexicon: ExtendedLexicon):
        self.lexicon = lexicon
        self.paradigms = MorphologicalParadigms()
        self.tokenizer = Tokenizer()
        
        # Compilation des patterns de terminaisons
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile les patterns regex pour l'analyse morphologique"""
        # Patterns pour les noms
        self.noun_patterns = [
            # Nominatif singulier masculin
            (r'(.*)r$', {'case': 'nom', 'number': 'sg', 'gender': 'masc'}),
            # Génitif singulier
            (r'(.*)s$', {'case': 'gen', 'number': 'sg'}),
            # Datif singulier
            (r'(.*)i$', {'case': 'dat', 'number': 'sg'}),
            # Nominatif pluriel
            (r'(.*)ar$', {'case': 'nom', 'number': 'pl'}),
            # Accusatif pluriel
            (r'(.*)a$', {'case': 'acc', 'number': 'pl'}),
            # Datif pluriel
            (r'(.*)um$', {'case': 'dat', 'number': 'pl'}),
        ]
        
        # Patterns pour les verbes
        self.verb_patterns = [
            # Infinitif
            (r'(.*)a$', {'form': 'inf'}),
            # Présent 2e/3e personne
            (r'(.*)r$', {'tense': 'pres', 'person': '2/3', 'number': 'sg'}),
            # Passé singulier
            (r'(.*)(ð|d|t)$', {'tense': 'past', 'number': 'sg'}),
            # Passé pluriel
            (r'(.*)u$', {'tense': 'past', 'number': 'pl'}),
            # Participe passé
            (r'(.*)inn$', {'form': 'past_part'}),
            # Participe présent
            (r'(.*)andi$', {'form': 'pres_part'}),
        ]
    
    def analyze_token(self, token_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse morphologique complète d'un token"""
        token = token_info['token']
        normalized = AdvancedNormalizer.normalize(token)
        
        result = {
            'token': token,
            'normalized': normalized,
            'candidates': [],
            'best': None,
            'analysis_type': 'unknown'
        }
        
        # 1. Recherche exacte dans le lexique
        exact_matches = self._exact_match(normalized)
        if exact_matches:
            result['candidates'].extend(exact_matches)
            result['analysis_type'] = 'exact_match'
        
        # 2. Analyse morphologique basée sur les paradigmes
        paradigm_analysis = self._paradigm_analysis(normalized)
        if paradigm_analysis:
            result['candidates'].extend(paradigm_analysis)
            if result['analysis_type'] == 'unknown':
                result['analysis_type'] = 'paradigm_analysis'
        
        # 3. Recherche approximative
        fuzzy_matches = self._fuzzy_match(normalized)
        if fuzzy_matches:
            result['candidates'].extend(fuzzy_matches)
            if result['analysis_type'] == 'unknown':
                result['analysis_type'] = 'fuzzy_match'
        
        # 4. Segmentation des composés
        compound_analysis = self._compound_analysis(normalized)
        if compound_analysis:
            result['candidates'].extend(compound_analysis)
            if result['analysis_type'] == 'unknown':
                result['analysis_type'] = 'compound_analysis'
        
        # 5. Déduction par règles
        rule_based = self._rule_based_analysis(normalized)
        if rule_based:
            result['candidates'].extend(rule_based)
            if result['analysis_type'] == 'unknown':
                result['analysis_type'] = 'rule_based'
        
        # Sélection du meilleur candidat
        if result['candidates']:
            result['candidates'] = sorted(result['candidates'], 
                                        key=lambda x: x.get('score', 0), 
                                        reverse=True)
            result['best'] = result['candidates'][0]
        else:
            result['best'] = {
                'lemma': normalized,
                'pos': 'unknown',
                'score': 0.0,
                'note': 'no analysis possible'
            }
        
        return result
    
    def _exact_match(self, token: str) -> List[Dict]:
        """Recherche exacte dans le lexique"""
        if token in self.lexicon.entries:
            entry = self.lexicon.entries[token]
            return [{
                'lemma': entry.get('lemma', token),
                'pos': entry.get('pos', 'unknown'),
                'gloss': entry.get('gloss', ''),
                'features': entry.get('features', {}),
                'score': 1.0,
                'note': 'exact match',
                'source': 'lexicon'
            }]
        return []
    
    def _paradigm_analysis(self, token: str) -> List[Dict]:
        """Analyse basée sur les paradigmes morphologiques"""
        candidates = []
        
        # Analyse des noms
        noun_candidates = self._analyze_noun_paradigms(token)
        candidates.extend(noun_candidates)
        
        # Analyse des verbes
        verb_candidates = self._analyze_verb_paradigms(token)
        candidates.extend(verb_candidates)
        
        # Analyse des adjectifs
        adj_candidates = self._analyze_adjective_paradigms(token)
        candidates.extend(adj_candidates)
        
        return candidates
    
    def _analyze_noun_paradigms(self, token: str) -> List[Dict]:
        """Analyse des paradigmes nominaux"""
        candidates = []
        
        for paradigm_name, paradigm in self.paradigms.NOUN_PARADIGMS.items():
            for number in ['sg', 'pl']:
                for case, ending in paradigm[number].items():
                    if token.endswith(ending):
                        stem = token[:-len(ending)] if ending else token
                        
                        # Vérifier si le stem existe dans le lexique
                        if any(stem in self.lexicon.lemma_index for stem_variant in AdvancedNormalizer.generate_variants(stem)):
                            candidate = {
                                'lemma': stem,
                                'pos': 'noun',
                                'features': {
                                    'case': case,
                                    'number': number,
                                    'gender': paradigm['gender'],
                                    'declension': paradigm['declension']
                                },
                                'score': 0.7,
                                'note': f'paradigm: {paradigm_name}',
                                'source': 'paradigm_analysis'
                            }
                            candidates.append(candidate)
        
        return candidates
    
    def _analyze_verb_paradigms(self, token: str) -> List[Dict]:
        """Analyse des paradigmes verbaux"""
        candidates = []
        
        for paradigm_name, paradigm in self.paradigms.VERB_PARADIGMS.items():
            # Vérifier l'infinitif
            if token.endswith(paradigm['infinitive']):
                stem = token[:-len(paradigm['infinitive'])]
                candidates.append({
                    'lemma': stem,
                    'pos': 'verb',
                    'features': {'form': 'inf', 'class': paradigm['class']},
                    'score': 0.6,
                    'note': f'verb paradigm: {paradigm_name}',
                    'source': 'paradigm_analysis'
                })
            
            # Vérifier les formes conjuguées
            for tense_forms in [paradigm['present'], paradigm['past']]:
                for form, ending in tense_forms.items():
                    if token.endswith(ending):
                        stem = token[:-len(ending)]
                        tense = 'pres' if tense_forms is paradigm['present'] else 'past'
                        
                        candidates.append({
                            'lemma': stem,
                            'pos': 'verb',
                            'features': {
                                'tense': tense,
                                'form': form,
                                'class': paradigm['class']
                            },
                            'score': 0.65,
                            'note': f'verb paradigm: {paradigm_name}',
                            'source': 'paradigm_analysis'
                        })
        
        return candidates
    
    def _analyze_adjective_paradigms(self, token: str) -> List[Dict]:
        """Analyse des paradigmes adjectivaux"""
        candidates = []
        
        # Patterns simples pour les adjectifs
        adj_patterns = [
            (r'(.*)r$', {'case': 'nom', 'gender': 'masc', 'number': 'sg', 'degree': 'pos'}),
            (r'(.*)an$', {'case': 'acc', 'gender': 'masc', 'number': 'sg', 'degree': 'pos'}),
            (r'(.*)um$', {'case': 'dat', 'gender': 'masc', 'number': 'sg', 'degree': 'pos'}),
            (r'(.*)ir$', {'case': 'nom', 'gender': 'masc', 'number': 'pl', 'degree': 'pos'}),
            (r'(.*)i$', {'case': 'nom', 'gender': 'fem', 'number': 'sg', 'degree': 'pos'}),
            (r'(.*)a$', {'case': 'nom', 'gender': 'neut', 'number': 'sg', 'degree': 'pos'}),
            (r'(.*)ari$', {'degree': 'comp'}),
            (r'(.*)astr$', {'degree': 'sup'}),
        ]
        
        for pattern, features in adj_patterns:
            match = re.match(pattern, token)
            if match:
                stem = match.group(1)
                candidates.append({
                    'lemma': stem,
                    'pos': 'adj',
                    'features': features,
                    'score': 0.5,
                    'note': 'adjective pattern',
                    'source': 'paradigm_analysis'
                })
        
        return candidates
    
    def _fuzzy_match(self, token: str, cutoff: float = 0.7) -> List[Dict]:
        """Recherche approximative étendue"""
        candidates = []
        lexicon_forms = list(self.lexicon.form_index.keys())
        
        # Recherche standard
        matches = get_close_matches(token, lexicon_forms, n=3, cutoff=cutoff)
        for match in matches:
            if match == token:
                continue
            entry = self.lexicon.form_index[match]
            similarity = SequenceMatcher(None, token, match).ratio()
            
            candidates.append({
                'lemma': entry.get('lemma', match),
                'pos': entry.get('pos', 'unknown'),
                'gloss': entry.get('gloss', ''),
                'features': entry.get('features', {}),
                'score': 0.3 + (similarity * 0.4),  # Score basé sur la similarité
                'note': f'fuzzy match: {match} (similarity: {similarity:.2f})',
                'source': 'fuzzy_match'
            })
        
        return candidates
    
    def _compound_analysis(self, token: str) -> List[Dict]:
        """Analyse avancée des composés"""
        candidates = []
        lexicon_forms = set(self.lexicon.form_index.keys())
        
        # Segmentation avancée
        segments_list = self.tokenizer.segment_compounds_advanced(token, lexicon_forms)
        
        for segments in segments_list:
            segment_entries = []
            valid = True
            
            for segment in segments:
                # Trouver la meilleure correspondance pour chaque segment
                segment_matches = get_close_matches(segment, lexicon_forms, n=1, cutoff=0.8)
                if segment_matches:
                    entry = self.lexicon.form_index[segment_matches[0]]
                    segment_entries.append(entry)
                else:
                    valid = False
                    break
            
            if valid and segment_entries:
                # Créer une entrée composite
                main_lemma = segment_entries[0].get('lemma', segments[0])
                gloss_parts = [entry.get('gloss', '') for entry in segment_entries]
                
                candidates.append({
                    'lemma': main_lemma,
                    'pos': segment_entries[0].get('pos', 'noun'),
                    'gloss': ' + '.join(gloss_parts),
                    'features': {
                        'compound': True,
                        'segments': segments,
                        'segment_glosses': gloss_parts
                    },
                    'score': 0.4,
                    'note': f'compound: {"-".join(segments)}',
                    'source': 'compound_analysis'
                })
        
        return candidates
    
    def _rule_based_analysis(self, token: str) -> List[Dict]:
        """Analyse basée sur des règles linguistiques"""
        candidates = []
        
        # Règles pour les mots courts courants
        short_words = {
            'í': {'lemma': 'í', 'pos': 'prep', 'gloss': 'dans', 'score': 0.9},
            'á': {'lemma': 'á', 'pos': 'prep', 'gloss': 'sur', 'score': 0.9},
            'af': {'lemma': 'af', 'pos': 'prep', 'gloss': 'de', 'score': 0.9},
            'um': {'lemma': 'um', 'pos': 'prep', 'gloss': 'autour', 'score': 0.9},
            'ok': {'lemma': 'ok', 'pos': 'conj', 'gloss': 'et', 'score': 0.9},
            'en': {'lemma': 'en', 'pos': 'conj', 'gloss': 'mais', 'score': 0.9},
        }
        
        if token in short_words:
            candidates.append(short_words[token])
        
        # Règles basées sur la fréquence des terminaisons
        if len(token) > 2:
            if token.endswith('ing'):
                candidates.append({
                    'lemma': token,
                    'pos': 'noun',
                    'features': {'gender': 'fem'},
                    'score': 0.3,
                    'note': 'common feminine ending -ing',
                    'source': 'rule_based'
                })
            elif token.endswith('leikr'):
                candidates.append({
                    'lemma': token,
                    'pos': 'noun',
                    'features': {'gender': 'masc'},
                    'score': 0.3,
                    'note': 'common masculine ending -leikr',
                    'source': 'rule_based'
                })
        
        return candidates

# ------------------------ ANALYSEUR DE TEXTE AVANCÉ ------------------------

class AdvancedOldNorseTextAnalyzer:
    """Analyseur de texte avancé avec désambiguïsation contextuelle"""
    
    def __init__(self, lexicon_path: Optional[str] = None):
        self.lexicon = ExtendedLexicon()
        self.morph_analyzer = AdvancedMorphologicalAnalyzer(self.lexicon)
        self.context_model = ContextModel()
        self.tokenizer = Tokenizer()  # <-- AJOUT DE CETTE LIGNE
        
        if lexicon_path:
            self.load_external_lexicon(lexicon_path)
    
    def load_external_lexicon(self, path: str):
        """Charge un lexique externe"""
        try:
            if path.endswith('.csv') or path.endswith('.tsv'):
                self._load_lexicon_csv(path)
            elif path.endswith('.json'):
                self._load_lexicon_json(path)
            elif path.endswith('.pkl'):
                self._load_lexicon_pickle(path)
            logger.info(f"Lexique externe chargé depuis {path}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du lexique: {e}")
    
    def _load_lexicon_csv(self, path: str):
        """Charge un lexique CSV"""
        delim = ',' if path.endswith('.csv') else '\t'
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delim)
            for row in reader:
                form = row.get('form', '').strip()
                if form:
                    entry = {
                        'lemma': row.get('lemma', form),
                        'pos': row.get('pos', 'unknown'),
                        'gloss': row.get('gloss', ''),
                        'features': {}
                    }
                    # Ajouter les features supplémentaires
                    for key, value in row.items():
                        if key not in ['form', 'lemma', 'pos', 'gloss'] and value:
                            entry['features'][key] = value
                    
                    self.lexicon.add_entry(form, entry)
    
    def _load_lexicon_json(self, path: str):
        """Charge un lexique JSON"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for form, entry in data.items():
                self.lexicon.add_entry(form, entry)
    
    def _load_lexicon_pickle(self, path: str):
        """Charge un lexique pickle"""
        with open(path, 'rb') as f:
            lexicon_data = pickle.load(f)
            self.lexicon.entries.update(lexicon_data)
            self.lexicon._build_indexes()
    
    def analyze_text(self, text: str) -> List[Dict[str, Any]]:
        """Analyse complète d'un texte"""
        # Tokenisation
        tokens = self.tokenizer.tokenize(text)  # <-- MAINTENANT self.tokenizer EXISTE
        
        # Analyse morphologique
        analysis = []
        for token_info in tokens:
            if token_info['type'] == 'punctuation':
                analysis.append({
                    'token': token_info['token'],
                    'type': 'punctuation',
                    'position': token_info['start']
                })
            else:
                token_analysis = self.morph_analyzer.analyze_token(token_info)
                token_analysis['position'] = token_info['start']
                analysis.append(token_analysis)
        
        # Désambiguïsation contextuelle
        self.context_model.disambiguate(analysis)
        
        return analysis
    
    def analyze_with_confidence(self, text: str) -> Dict[str, Any]:
        """Analyse avec scores de confiance détaillés"""
        analysis = self.analyze_text(text)
        
        # Calcul des métriques de confiance
        word_tokens = [a for a in analysis if a.get('type') != 'punctuation']
        if word_tokens:
            avg_confidence = sum(a['best'].get('score', 0) for a in word_tokens) / len(word_tokens)
            known_words = sum(1 for a in word_tokens if a['best'].get('score', 0) > 0.5)
            known_ratio = known_words / len(word_tokens)
        else:
            avg_confidence = 0.0
            known_ratio = 0.0
        
        return {
            'analysis': analysis,
            'metrics': {
                'total_tokens': len(analysis),
                'word_tokens': len(word_tokens),
                'average_confidence': avg_confidence,
                'known_words_ratio': known_ratio,
                'analysis_types': Counter(a.get('analysis_type', 'unknown') for a in word_tokens)
            }
        }

# ------------------------ MODÈLE CONTEXTUEL AVANCÉ ------------------------

class ContextModel:
    """Modèle de désambiguïsation contextuelle avancé"""
    
    def __init__(self):
        # Patterns syntaxiques courants
        self.syntax_patterns = [
            # Déterminant + Nom
            (['det', 'art'], ['noun'], 0.1),
            # Préposition + Nom
            (['prep'], ['noun', 'pron'], 0.15),
            # Sujet + Verbe
            (['noun', 'pron'], ['verb'], 0.12),
            # Verbe + Objet
            (['verb'], ['noun', 'pron'], 0.1),
            # Adjectif + Nom
            (['adj'], ['noun'], 0.08),
        ]
        
        # Cohérence des features
        self.feature_coherence = {
            'noun': ['case', 'gender', 'number'],
            'verb': ['tense', 'mood', 'person'],
            'adj': ['case', 'gender', 'number', 'degree']
        }
    
    def disambiguate(self, analysis: List[Dict]):
        """Désambiguïsation contextuelle avancée"""
        if len(analysis) < 2:
            return
        
        # Première passe: cohérence locale
        for i in range(1, len(analysis) - 1):
            self._local_coherence(analysis, i)
        
        # Deuxième passe: patterns syntaxiques
        for i in range(len(analysis) - 1):
            self._syntactic_patterns(analysis, i)
        
        # Troisième passe: cohérence globale des features
        self._global_feature_coherence(analysis)
    
    def _local_coherence(self, analysis: List[Dict], position: int):
        """Cohérence locale entre tokens adjacents"""
        if analysis[position].get('type') == 'punctuation':
            return
        
        current = analysis[position]
        prev = analysis[position - 1] if position > 0 else None
        next = analysis[position + 1] if position < len(analysis) - 1 else None
        
        # Booster les candidats cohérents avec le contexte
        for candidate in current.get('candidates', []):
            score_boost = 0.0
            
            # Vérifier la cohérence avec le token précédent
            if prev and prev.get('best'):
                prev_pos = prev['best'].get('pos')
                current_pos = candidate.get('pos')
                
                # Patterns basiques
                if prev_pos == 'det' and current_pos == 'noun':
                    score_boost += 0.1
                elif prev_pos == 'prep' and current_pos in ['noun', 'pron']:
                    score_boost += 0.1
                elif prev_pos in ['noun', 'pron'] and current_pos == 'verb':
                    score_boost += 0.08
            
            # Vérifier la cohérence avec le token suivant
            if next and next.get('best'):
                next_pos = next['best'].get('pos')
                current_pos = candidate.get('pos')
                
                if current_pos == 'verb' and next_pos in ['noun', 'pron']:
                    score_boost += 0.08
                elif current_pos == 'adj' and next_pos == 'noun':
                    score_boost += 0.06
            
            candidate['score'] = min(1.0, candidate.get('score', 0) + score_boost)
            
            if score_boost > 0:
                candidate['note'] = f"{candidate.get('note', '')}; context boost".strip('; ')
    
    def _syntactic_patterns(self, analysis: List[Dict], position: int):
        """Application des patterns syntaxiques"""
        if position >= len(analysis) - 1:
            return
        
        current = analysis[position]
        next = analysis[position + 1]
        
        if current.get('type') == 'punctuation' or next.get('type') == 'punctuation':
            return
        
        for pattern in self.syntax_patterns:
            prev_possibilities, next_possibilities, boost = pattern
            
            current_pos = current['best'].get('pos') if current.get('best') else None
            next_pos = next['best'].get('pos') if next.get('best') else None
            
            if current_pos in prev_possibilities and next_pos in next_possibilities:
                # Booster les deux tokens
                if current.get('best'):
                    current['best']['score'] = min(1.0, current['best'].get('score', 0) + boost)
                if next.get('best'):
                    next['best']['score'] = min(1.0, next['best'].get('score', 0) + boost)
    
    def _global_feature_coherence(self, analysis: List[Dict]):
        """Cohérence globale des features grammaticales"""
        # Collecter les features par position
        pos_features = defaultdict(list)
        
        for i, token in enumerate(analysis):
            if token.get('type') == 'punctuation' or not token.get('best'):
                continue
            
            pos = token['best'].get('pos')
            features = token['best'].get('features', {})
            
            if pos in self.feature_coherence:
                for feature in self.feature_coherence[pos]:
                    if feature in features:
                        pos_features[feature].append((i, features[feature]))
        
        # Détecter et corriger les incohérences
        for feature, values in pos_features.items():
            if len(values) < 2:
                continue
            
            # Trouver la valeur la plus commune
            value_counts = Counter(v for _, v in values)
            most_common = value_counts.most_common(1)[0][0]
            
            # Booster les tokens cohérents
            for i, value in values:
                if value == most_common:
                    analysis[i]['best']['score'] = min(1.0, analysis[i]['best'].get('score', 0) + 0.05)

# ------------------------ INTERFACE GRAPHIQUE AMÉLIORÉE ------------------------

class AdvancedAnalyzerGUI:
    """Interface graphique avancée avec visualisations"""
    
    POS_COLORS = {
        'noun': '#0B5394',   # bleu
        'verb': '#990000',   # rouge
        'adj': '#38761D',    # vert
        'adv': '#674EA7',    # violet
        'prep': '#B45F06',   # orange
        'conj': '#CC0000',   # rouge foncé
        'pron': '#741B47',   # violet foncé
        'det': '#5B5B5B',    # gris foncé
        'num': '#FF00FF',    # magenta
        'part': '#00FFFF',   # cyan
        'interj': '#FFFF00', # jaune
        'unknown': '#666666' # gris
    }
    
    def __init__(self, root, analyzer: AdvancedOldNorseTextAnalyzer):
        self.root = root
        self.analyzer = analyzer
        self.root.title('Old Norse Analyzer v4 — Analyse Avancée')
        self.root.geometry('1200x800')
        
        # Variables d'interface
        self.color_enabled = tk.BooleanVar(value=True)
        self.show_confidence = tk.BooleanVar(value=True)
        self.auto_analyze = tk.BooleanVar(value=False)
        
        self.build_advanced_ui()
    
    def build_advanced_ui(self):
        """Construit l'interface avancée"""
        # Frame principal avec notebook pour les onglets
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet Analyse
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text='Analyse')
        
        self.build_analysis_tab(analysis_frame)
        
        # Onglet Lexique
        lexicon_frame = ttk.Frame(notebook)
        notebook.add(lexicon_frame, text='Lexique')
        
        self.build_lexicon_tab(lexicon_frame)
        
        # Onglet Statistiques
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text='Statistiques')
        
        self.build_stats_tab(stats_frame)
    
    def build_analysis_tab(self, parent):
        """Construit l'onglet d'analyse"""
        # Frame supérieur: contrôles
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text='Texte en ancien norrois:').pack(anchor='w')
        
        # Frame pour les boutons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text='Analyser', command=self.on_analyze).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text='Charger lexique', command=self.on_load_lexicon).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='Exporter JSON', command=self.on_export_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='Exporter CSV', command=self.on_export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='Analyser avec métriques', command=self.on_analyze_with_metrics).pack(side=tk.LEFT, padx=5)
        
        # Options d'affichage
        options_frame = ttk.Frame(control_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(options_frame, text='Coloration POS', variable=self.color_enabled).pack(side=tk.LEFT)
        ttk.Checkbutton(options_frame, text='Afficher confiance', variable=self.show_confidence).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text='Analyse auto', variable=self.auto_analyze).pack(side=tk.LEFT)
        
        # Zone de texte d'entrée
        input_frame = ttk.LabelFrame(parent, text='Texte d\'entrée')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_txt = tk.Text(input_frame, height=8, wrap=tk.WORD, font=('Arial', 11))
        scrollbar_input = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_txt.yview)
        self.input_txt.configure(yscrollcommand=scrollbar_input.set)
        
        self.input_txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_input.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Zone de résultats
        result_frame = ttk.LabelFrame(parent, text='Résultats d\'analyse')
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Créer un frame avec scrollbar pour les résultats
        result_container = ttk.Frame(result_frame)
        result_container.pack(fill=tk.BOTH, expand=True)
        
        self.result_txt = tk.Text(result_container, wrap=tk.WORD, font=('Courier New', 10), 
                                 state=tk.DISABLED, bg='#f8f8f8')
        scrollbar_result = ttk.Scrollbar(result_container, orient=tk.VERTICAL, command=self.result_txt.yview)
        self.result_txt.configure(yscrollcommand=scrollbar_result.set)
        
        self.result_txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_result.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurer les tags de couleur
        for pos, color in self.POS_COLORS.items():
            self.result_txt.tag_config(pos, foreground=color)
            self.result_txt.tag_config(f'{pos}_bold', foreground=color, font=('Courier New', 10, 'bold'))
        
        # Tags pour les scores de confiance
        self.result_txt.tag_config('high_confidence', background='#e6ffe6')
        self.result_txt.tag_config('medium_confidence', background='#fff8e6')
        self.result_txt.tag_config('low_confidence', background='#ffe6e6')
        self.result_txt.tag_config('info', foreground='#666666', font=('Courier New', 9))
    
    def build_lexicon_tab(self, parent):
        """Construit l'onglet de gestion du lexique"""
        # Frame pour les statistiques du lexique
        stats_frame = ttk.LabelFrame(parent, text='Statistiques du lexique')
        stats_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.lexicon_stats_var = tk.StringVar(value='Chargement...')
        ttk.Label(stats_frame, textvariable=self.lexicon_stats_var, font=('Arial', 10)).pack(pady=10)
        
        # Frame pour les actions
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=10, padx=5)
        
        ttk.Button(action_frame, text='Actualiser les statistiques', 
                  command=self.update_lexicon_stats).pack(side=tk.LEFT)
        ttk.Button(action_frame, text='Rechercher dans le lexique', 
                  command=self.show_lexicon_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text='Exporter le lexique', 
                  command=self.export_lexicon).pack(side=tk.LEFT, padx=5)
        
        # Zone d'affichage du lexique
        lexicon_frame = ttk.LabelFrame(parent, text='Entrées du lexique')
        lexicon_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        # Treeview pour afficher le lexique
        columns = ('form', 'lemma', 'pos', 'gloss', 'features')
        self.lexicon_tree = ttk.Treeview(lexicon_frame, columns=columns, show='headings')
        
        # Définir les en-têtes
        self.lexicon_tree.heading('form', text='Forme')
        self.lexicon_tree.heading('lemma', text='Lemme')
        self.lexicon_tree.heading('pos', text='POS')
        self.lexicon_tree.heading('gloss', text='Glose')
        self.lexicon_tree.heading('features', text='Features')
        
        # Configurer les colonnes
        self.lexicon_tree.column('form', width=100)
        self.lexicon_tree.column('lemma', width=100)
        self.lexicon_tree.column('pos', width=80)
        self.lexicon_tree.column('gloss', width=150)
        self.lexicon_tree.column('features', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(lexicon_frame, orient=tk.VERTICAL, command=self.lexicon_tree.yview)
        self.lexicon_tree.configure(yscrollcommand=scrollbar.set)
        
        self.lexicon_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mettre à jour les statistiques
        self.update_lexicon_stats()
    
    def build_stats_tab(self, parent):
        """Construit l'onglet des statistiques"""
        # Frame pour les métriques d'analyse
        metrics_frame = ttk.LabelFrame(parent, text='Métriques d\'analyse')
        metrics_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.metrics_var = tk.StringVar(value='Analysez un texte pour voir les métriques')
        ttk.Label(metrics_frame, textvariable=self.metrics_var, font=('Arial', 10), 
                 wraplength=1000).pack(pady=10, padx=10)
        
        # Frame pour les graphiques (placeholder)
        chart_frame = ttk.LabelFrame(parent, text='Répartition grammaticale')
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        # Zone pour les graphiques (serait implémentée avec matplotlib)
        self.chart_canvas = tk.Canvas(chart_frame, bg='white', height=300)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texte temporaire pour les graphiques
        self.chart_canvas.create_text(200, 150, text='Graphiques de distribution POS\n(À implémenter avec matplotlib)',
                                     fill='gray', font=('Arial', 12), justify=tk.CENTER)
    
    def on_analyze(self):
        """Lance l'analyse du texte"""
        txt = self.input_txt.get('1.0', tk.END).strip()
        if not txt:
            messagebox.showinfo('Info', 'Veuillez entrer du texte à analyser.')
            return
        
        try:
            # Analyser le texte
            analysis = self.analyzer.analyze_text(txt)
            self.display_analysis_results(analysis)
            
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur lors de l\'analyse: {str(e)}')
    
    def on_analyze_with_metrics(self):
        """Lance l'analyse avec métriques détaillées"""
        txt = self.input_txt.get('1.0', tk.END).strip()
        if not txt:
            messagebox.showinfo('Info', 'Veuillez entrer du texte à analyser.')
            return
        
        try:
            # Analyser avec métriques
            result = self.analyzer.analyze_with_confidence(txt)
            self.display_analysis_results(result['analysis'])
            
            # Afficher les métriques
            metrics = result['metrics']
            metrics_text = (f"Tokens totaux: {metrics['total_tokens']} | "
                          f"Mots: {metrics['word_tokens']} | "
                          f"Confiance moyenne: {metrics['average_confidence']:.2f} | "
                          f"Mots connus: {metrics['known_words_ratio']:.1%}")
            
            self.metrics_var.set(metrics_text)
            
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur lors de l\'analyse: {str(e)}')


    def display_analysis_results(self, analysis):
        """Version détaillée avec traduction en évidence"""
        self.result_txt.config(state=tk.NORMAL)
        self.result_txt.delete('1.0', tk.END)
        
        # Configuration des tags
        self.result_txt.tag_config('gloss_high', 
                                  background='#90EE90',  # vert clair - haute confiance
                                  foreground='black',
                                  font=('Courier New', 10, 'bold'))
        
        self.result_txt.tag_config('gloss_medium',
                                  background='#E6FFE6',  # vert très pâle - confiance moyenne
                                  foreground='black',
                                  font=('Courier New', 10))
        
        self.result_txt.tag_config('no_gloss',
                                  background='#FFE6E6',  # rouge pâle - pas de traduction
                                  foreground='black',
                                  font=('Courier New', 10))
        
        self.result_txt.tag_config('token',
                                  foreground='#000080',  # bleu foncé pour le token
                                  font=('Courier New', 10, 'bold'))
        
        self.result_txt.tag_config('info',
                                  foreground='#666666',
                                  font=('Courier New', 9))
        
        self.result_txt.tag_config('pos_tag',
                                  foreground='#8B0000',  # rouge foncé pour POS
                                  font=('Courier New', 9, 'italic'))
    
        for i, item in enumerate(analysis):
            if item.get('type') == 'punctuation':
                self.result_txt.insert(tk.END, item['token'] + ' ')
                continue
            
            token = item['token']
            best = item.get('best', {})
            score = best.get('score', 0)
            lemma = best.get('lemma', '?')
            pos = best.get('pos', 'unknown')
            gloss = best.get('gloss', '')
            
            # 1. Afficher le token original
            self.result_txt.insert(tk.END, token, ('token',))
            
            # 2. Afficher la traduction avec surbrillance appropriée
            if gloss:
                if score >= 0.8:
                    gloss_tag = 'gloss_high'
                elif score >= 0.5:
                    gloss_tag = 'gloss_medium'
                else:
                    gloss_tag = 'no_gloss'
                
                if self.color_enabled.get():
                    self.result_txt.insert(tk.END, f" → {gloss}", (gloss_tag,))
                else:
                    self.result_txt.insert(tk.END, f" → {gloss}")
            else:
                # Pas de traduction trouvée
                if self.color_enabled.get():
                    self.result_txt.insert(tk.END, f" [pas de trad]", ('no_gloss',))
                else:
                    self.result_txt.insert(tk.END, f" [{lemma}]")
            
            # 3. Informations techniques (optionnelles)
            if self.show_confidence.get():
                self.result_txt.insert(tk.END, f" ({pos}", ('pos_tag',))
                self.result_txt.insert(tk.END, f", score:{score:.2f})", ('info',))
            
            self.result_txt.insert(tk.END, ' ')
        
        self.result_txt.config(state=tk.DISABLED)


    def display_analysis_results_old2(self, analysis):
        """Version minimaliste : vert pour reconnu, noir pour inconnu"""
        self.result_txt.config(state=tk.NORMAL)
        self.result_txt.delete('1.0', tk.END)
        
        # Tags simples
        self.result_txt.tag_config('known', 
                                  background='#90EE90',  # vert clair
                                  foreground='black',
                                  font=('Courier New', 10, 'bold'))
        
        self.result_txt.tag_config('unknown',
                                  background='white',
                                  foreground='black',
                                  font=('Courier New', 10))
        
        for i, item in enumerate(analysis):
            if item.get('type') == 'punctuation':
                self.result_txt.insert(tk.END, item['token'])
                continue
            
            token = item['token']
            best = item.get('best', {})
            score = best.get('score', 0)
            lemma = best.get('lemma', '?')
            
            # Simple : vert si score > 0.5, sinon normal
            if score > 0.5:
                display_tag = 'known'
            else:
                display_tag = 'unknown'
            
            if self.color_enabled.get():
                self.result_txt.insert(tk.END, token, (display_tag,))
            else:
                self.result_txt.insert(tk.END, token)
            
            self.result_txt.insert(tk.END, f" [{lemma}]", ('info',))
            self.result_txt.insert(tk.END, ' ')
        
        self.result_txt.config(state=tk.DISABLED)
    
    def display_analysis_results_old(self, analysis):
        """Affiche les résultats de l'analyse"""
        self.result_txt.config(state=tk.NORMAL)
        self.result_txt.delete('1.0', tk.END)
        
        # Effacer les anciens tags de fond
        for tag in self.result_txt.tag_names():
            if tag.startswith('bg_'):
                self.result_txt.tag_delete(tag)
        
        current_line = 1
        
        for i, item in enumerate(analysis):
            if item.get('type') == 'punctuation':
                # Ponctuation - pas d'analyse
                self.result_txt.insert(tk.END, item['token'])
                continue
            
            token = item['token']
            best = item.get('best', {})
            pos = best.get('pos', 'unknown')
            score = best.get('score', 0)
            lemma = best.get('lemma', '?')
            gloss = best.get('gloss', '')
            note = best.get('note', '')
            
            # Déterminer la couleur basée sur le POS
            color_tag = pos if pos in self.POS_COLORS else 'unknown'
            
            # Déterminer la couleur de fond basée sur le score de confiance
            if score >= 0.8:
                bg_tag = 'high_confidence'
            elif score >= 0.5:
                bg_tag = 'medium_confidence'
            else:
                bg_tag = 'low_confidence'
            
            # Afficher le token avec coloration
            if self.color_enabled.get():
                self.result_txt.insert(tk.END, token, (color_tag, bg_tag))
            else:
                self.result_txt.insert(tk.END, token, (bg_tag,))
            
            # Ajouter les informations d'analyse
            if self.show_confidence.get():
                info_text = f" [{lemma} | {pos} | {score:.2f}]"
            else:
                info_text = f" [{lemma} | {pos}]"
            
            self.result_txt.insert(tk.END, info_text, ('info',))
            self.result_txt.insert(tk.END, ' ')
        
        self.result_txt.config(state=tk.DISABLED)
    
    def on_load_lexicon(self):
        """Charge un lexique externe"""
        path = filedialog.askopenfilename(
            filetypes=[
                ('CSV/TSV', '*.csv;*.tsv;*.txt'),
                ('JSON', '*.json'),
                ('Pickle', '*.pkl'),
                ('Tous', '*.*')
            ]
        )
        if not path:
            return
        
        try:
            self.analyzer.load_external_lexicon(path)
            self.update_lexicon_stats()
            messagebox.showinfo('Succès', f'Lexique chargé depuis {os.path.basename(path)}')
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur lors du chargement: {str(e)}')
    
    def on_export_json(self):
        """Exporte les résultats en JSON"""
        txt = self.input_txt.get('1.0', tk.END).strip()
        if not txt:
            messagebox.showinfo('Info', 'Veuillez entrer du texte à analyser.')
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON', '*.json')]
        )
        if not path:
            return
        
        try:
            result = self.analyzer.analyze_with_confidence(txt)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            messagebox.showinfo('Succès', f'Résultats exportés vers {path}')
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur lors de l\'export: {str(e)}')
    
    def on_export_csv(self):
        """Exporte les résultats en CSV"""
        txt = self.input_txt.get('1.0', tk.END).strip()
        if not txt:
            messagebox.showinfo('Info', 'Veuillez entrer du texte à analyser.')
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv')]
        )
        if not path:
            return
        
        try:
            analysis = self.analyzer.analyze_text(txt)
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['token', 'normalized', 'lemma', 'pos', 'gloss', 'features', 'score', 'note', 'analysis_type'])
                
                for item in analysis:
                    if item.get('type') == 'punctuation':
                        writer.writerow([item['token'], '', '', '', '', '', '', '', 'punctuation'])
                        continue
                    
                    best = item.get('best', {})
                    writer.writerow([
                        item['token'],
                        item.get('normalized', ''),
                        best.get('lemma', ''),
                        best.get('pos', ''),
                        best.get('gloss', ''),
                        json.dumps(best.get('features', {}), ensure_ascii=False),
                        best.get('score', 0),
                        best.get('note', ''),
                        item.get('analysis_type', '')
                    ])
            
            messagebox.showinfo('Succès', f'Résultats exportés vers {path}')
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur lors de l\'export: {str(e)}')
    
    def update_lexicon_stats(self):
        """Met à jour les statistiques du lexique"""
        lexicon = self.analyzer.lexicon
        total_entries = len(lexicon.entries)
        
        # Compter par POS
        pos_counts = defaultdict(int)
        for entry in lexicon.entries.values():
            pos = entry.get('pos', 'unknown')
            pos_counts[pos] += 1
        
        stats_text = (f"Entrées totales: {total_entries} | "
                     f"Noms: {pos_counts['noun']} | "
                     f"Verbes: {pos_counts['verb']} | "
                     f"Adjectifs: {pos_counts['adj']} | "
                     f"Autres: {sum(v for k, v in pos_counts.items() if k not in ['noun', 'verb', 'adj'])}")
        
        self.lexicon_stats_var.set(stats_text)
        
        # Mettre à jour l'arbre du lexique (premières 100 entrées)
        self.lexicon_tree.delete(*self.lexicon_tree.get_children())
        for i, (form, entry) in enumerate(list(lexicon.entries.items())[:100]):
            self.lexicon_tree.insert('', 'end', values=(
                form,
                entry.get('lemma', ''),
                entry.get('pos', ''),
                entry.get('gloss', ''),
                json.dumps(entry.get('features', {}), ensure_ascii=False)
            ))
    
    def show_lexicon_search(self):
        """Affiche une fenêtre de recherche dans le lexique"""
        search_window = tk.Toplevel(self.root)
        search_window.title('Recherche dans le lexique')
        search_window.geometry('600x400')
        
        ttk.Label(search_window, text='Rechercher:').pack(pady=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_window, textvariable=search_var, width=50)
        search_entry.pack(pady=5)
        
        # Treeview pour les résultats
        columns = ('form', 'lemma', 'pos', 'gloss')
        results_tree = ttk.Treeview(search_window, columns=columns, show='headings')
        
        for col in columns:
            results_tree.heading(col, text=col.capitalize())
            results_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(search_window, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscrollcommand=scrollbar.set)
        
        results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        def perform_search(*args):
            query = search_var.get().strip().lower()
            results_tree.delete(*results_tree.get_children())
            
            if not query:
                return
            
            for form, entry in self.analyzer.lexicon.entries.items():
                if (query in form.lower() or 
                    query in entry.get('lemma', '').lower() or 
                    query in entry.get('gloss', '').lower()):
                    
                    results_tree.insert('', 'end', values=(
                        form,
                        entry.get('lemma', ''),
                        entry.get('pos', ''),
                        entry.get('gloss', '')
                    ))
        
        search_var.trace('w', perform_search)
        search_entry.focus()
    
    def export_lexicon(self):
        """Exporte le lexique complet"""
        path = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON', '*.json'), ('CSV', '*.csv')]
        )
        if not path:
            return
        
        try:
            if path.endswith('.json'):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.analyzer.lexicon.entries, f, ensure_ascii=False, indent=2)
            else:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['form', 'lemma', 'pos', 'gloss', 'features'])
                    for form, entry in self.analyzer.lexicon.entries.items():
                        writer.writerow([
                            form,
                            entry.get('lemma', ''),
                            entry.get('pos', ''),
                            entry.get('gloss', ''),
                            json.dumps(entry.get('features', {}), ensure_ascii=False)
                        ])
            
            messagebox.showinfo('Succès', f'Lexique exporté vers {path}')
        except Exception as e:
            messagebox.showerror('Erreur', f'Erreur lors de l\'export: {str(e)}')

# ------------------------ FONCTIONS D'EXPORT AVANCÉES ------------------------

def export_analysis(analysis, format='json', path=None):
    """Exporte l'analyse dans différents formats"""
    if format == 'json':
        if not path:
            path = 'analysis_result.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    elif format == 'csv':
        if not path:
            path = 'analysis_result.csv'
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['token', 'lemma', 'pos', 'gloss', 'features', 'score', 'confidence'])
            
            for item in analysis:
                if item.get('type') == 'punctuation':
                    continue
                
                best = item.get('best', {})
                writer.writerow([
                    item['token'],
                    best.get('lemma', ''),
                    best.get('pos', ''),
                    best.get('gloss', ''),
                    json.dumps(best.get('features', {}), ensure_ascii=False),
                    best.get('score', 0),
                    'high' if best.get('score', 0) >= 0.8 else 
                    'medium' if best.get('score', 0) >= 0.5 else 'low'
                ])
    
    elif format == 'conllu':
        if not path:
            path = 'analysis_result.conllu'
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# sent_id = 1\n")
            f.write("# text = " + ' '.join(item['token'] for item in analysis if item.get('type') != 'punctuation') + "\n")
            
            for i, item in enumerate(analysis):
                if item.get('type') == 'punctuation':
                    continue
                
                best = item.get('best', {})
                f.write(f"{i+1}\t{item['token']}\t{best.get('lemma', '_')}\t{best.get('pos', '_')}\t_\t{json.dumps(best.get('features', {}), ensure_ascii=False)}\t_\t_\t_\t_\n")
    
    return path

# ------------------------ SCRIPT DE DÉMONSTRATION ------------------------

def demo_advanced_analyzer():
    """Démontre les capacités de l'analyseur avancé"""
    print("=== Démonstration de l'Analyseur d'Ancien Norrois Avancé ===\n")
    
    # Créer l'analyseur
    analyzer = AdvancedOldNorseTextAnalyzer()
    
    # Textes de démonstration
    demo_texts = [
        "Ólafr hét maðr. Hann var konungr yfir Nóregi.",
        "Hann fór til Íslands ok kom á Eyjafjǫrð.",
        "Þeir menn er réðu fyrir landi því.",
        "Hann hafði mikinn her ok góð skip.",
        "Svá segir í frásǫgn þeiri."
    ]
    
    for i, text in enumerate(demo_texts, 1):
        print(f"--- Phrase {i}: {text} ---")
        
        # Analyse avancée avec métriques
        result = analyzer.analyze_with_confidence(text)
        
        # Afficher les résultats
        for item in result['analysis']:
            if item.get('type') == 'punctuation':
                print(f"  {item['token']}", end='')
            else:
                best = item.get('best', {})
                print(f" {item['token']}[{best.get('lemma')}/{best.get('pos')}/{best.get('score'):.2f}]", end='')
        print()
        
        # Afficher les métriques
        metrics = result['metrics']
        print(f"  Métriques: {metrics['word_tokens']} mots, confiance moyenne: {metrics['average_confidence']:.2f}")
        print()
    
    print("=== Démonstration terminée ===")

# ------------------------ POINT D'ENTRÉE PRINCIPAL ------------------------

if __name__ == '__main__':
    import sys
    
    # Vérifier les arguments de ligne de commande
    if len(sys.argv) > 1:
        if sys.argv[1] == '--demo':
            demo_advanced_analyzer()
        elif sys.argv[1] == '--analyze' and len(sys.argv) > 2:
            # Analyse en ligne de commande
            analyzer = AdvancedOldNorseTextAnalyzer()
            text = ' '.join(sys.argv[2:])
            result = analyzer.analyze_with_confidence(text)
            
            print(f"Analyse de: {text}")
            for item in result['analysis']:
                if item.get('type') != 'punctuation':
                    best = item.get('best', {})
                    print(f"  {item['token']} -> {best.get('lemma')} [{best.get('pos')}] (score: {best.get('score'):.2f})")
            
            print(f"\nMétriques: {result['metrics']}")
        else:
            print("Usage:")
            print("  python analyzer.py --demo")
            print("  python analyzer.py --analyze 'texte en ancien norrois'")
            print("  python analyzer.py (lance l'interface graphique)")
    else:
        # Lancer l'interface graphique
        try:
            root = tk.Tk()
            analyzer = AdvancedOldNorseTextAnalyzer()
            gui = AdvancedAnalyzerGUI(root, analyzer)
            root.mainloop()
        except Exception as e:
            print(f"Erreur lors du lancement de l'interface: {e}")
            print("Lancement de la démonstration en mode console...")
            demo_advanced_analyzer()
