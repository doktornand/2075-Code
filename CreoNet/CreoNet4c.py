# █████████████████████████████████████████████████████████████████████████████
# █  CREONET vΩ.3 — Système Multi-Profils ACTIF                              █
# █████████████████████████████████████████████████████████████████████████████

import json
import os
import random
import re
from typing import Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "core": os.path.join(BASE_DIR, "creo_lexicon_core.json"),
    "creole": os.path.join(BASE_DIR, "creo_lexicon_creole.json"),
    "french": os.path.join(BASE_DIR, "creo_lexicon_french.json"),
    "english": os.path.join(BASE_DIR, "creo_lexicon_english.json"),
    "slang": os.path.join(BASE_DIR, "creo_lexicon_slang.json"),
    "dreams": os.path.join(BASE_DIR, "creo_lexicon_dreams.json"),
    "config": os.path.join(BASE_DIR, "creo_config.json"),
    "profiles": os.path.join(BASE_DIR, "language_profiles.json")
}

def load_json(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def remove_accents(s: str) -> str:
    replacements = {
        "é":"e","è":"e","ê":"e","ë":"e","à":"a","â":"a","ä":"a",
        "î":"i","ï":"i","í":"i","ô":"o","ö":"o","ù":"u","û":"u","ü":"u",
        "ç":"c","œ":"oe","æ":"ae","ñ":"n"
    }
    for a, b in replacements.items():
        s = s.replace(a, b)
    return s

def creofy_word(word: str, style: str = "street") -> str:
    """Transforme un mot selon les règles CréoNeurales + style"""
    if word.isdigit():
        return "n" + word
    if len(word) <= 2:
        return word
    
    # Applique des transformations selon le style
    w = word.lower()
    
    if style == "street":
        w = re.sub(r'[aeiou]{2,}', lambda m: m.group(0)[0], w)
        w = w.replace("th", "d").replace("ph", "f")
        if random.random() < 0.15:
            w = w + random.choice(["z", "x", ""])
    
    elif style == "ritual":
        if random.random() < 0.3:
            w = "ghost." + w
        if len(w) > 4:
            w = w[:3] + "." + w[3:]
    
    # Évite de trop transformer les mots courts
    if len(w) <= 3:
        return w
        
    return w

def simple_tokenize(text: str) -> List[str]:
    text = text.replace("'", " ").replace("'", " ")
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)

def is_punctuation(tok: str) -> bool:
    return re.fullmatch(r"[^\w\s]", tok) is not None

class CreoNetTranslator:
    def __init__(self):
        self.load_all_resources()
        
    def load_all_resources(self):
        self.lookup = self.build_master_lookup()
        self.config = load_json(FILES["config"])
        profiles_data = load_json(FILES["profiles"])
        self.profiles = profiles_data.get("language_profiles", {
            "gwadar": {"creole": 0.3, "french": 0.2, "english": 0.4, "code": 0.1}
        })
        
        # Chargement individuel des lexiques
        self.lexicons = {
            "creole": self.flatten_lexicon(load_json(FILES["creole"])),
            "french": self.flatten_lexicon(load_json(FILES["french"])),
            "english": self.flatten_lexicon(load_json(FILES["english"])),
            "core": self.flatten_lexicon(load_json(FILES["core"]))
        }
    
    def flatten_lexicon(self, data: dict) -> Dict[str, str]:
        flat = {}
        for category in data.values():
            if isinstance(category, dict):
                flat.update(category)
        return flat
    
    def build_master_lookup(self) -> Dict[str, str]:
        lookup = {}
        for name in ["creole", "french", "core", "slang", "dreams", "english"]:
            data = load_json(FILES[name])
            for category_dict in data.values():
                if isinstance(category_dict, dict):
                    lookup.update(category_dict)
        return lookup
    
    def get_language_weights(self, profile: str) -> Dict[str, float]:
        return self.profiles.get(profile, self.profiles["gwadar"])
    
    def find_best_translation(self, word: str, weights: Dict[str, float], style: str) -> str:
        """Trouve la meilleure traduction selon les poids linguistiques"""
        word_lower = word.lower()
        word_clean = remove_accents(word_lower)
        
        # 1. Cherche une traduction exacte dans les lexiques prioritaires
        candidates = []
        
        # Parcours par ordre de poids décroissant
        sorted_langs = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        
        for lang, weight in sorted_langs:
            if lang in self.lexicons:
                lexicon = self.lexicons[lang]
                # Cherche le mot exact
                if word_lower in lexicon:
                    candidates.append((weight * 1.0, lexicon[word_lower]))
                elif word_clean in lexicon:
                    candidates.append((weight * 0.9, lexicon[word_clean]))
        
        # 2. Si pas de candidats, applique les règles CréoNeurales
        if not candidates:
            return creofy_word(word, style)
        
        # 3. Choisit le meilleur candidat avec un peu d'aléatoire
        best_candidate = max(candidates, key=lambda x: x[0] * random.uniform(0.8, 1.2))
        return best_candidate[1]
    
    def apply_regional_syntax(self, tokens: List[str], weights: Dict[str, float]) -> List[str]:
        """Applique des règles de syntaxe régionales"""
        result = []
        i = 0
        
        while i < len(tokens):
            current = tokens[i]
            
            # RÈGLES CRÉOLES (Port-au-Prince, Lagos)
            if weights["creole"] > 0.4:
                # "je" → "mwen" en début de phrase
                if current == "je" and (i == 0 or result[-1] in ["", "//"]):
                    result.append("mwen")
                    i += 1
                    continue
                    
                # "ne...pas" → "pa"
                if current in ["ne", "pas"]:
                    if "pa" not in result[-2:]:
                        result.append("pa")
                    i += 1
                    continue
            
            # RÈGLES FRANÇAISES (Djibouti, Abidjan)  
            elif weights["french"] > 0.4:
                # Garde plus de structure française
                if current in ["le", "la", "les", "un", "une", "des"]:
                    result.append(current)
                    i += 1
                    continue
            
            # RÈGLES ANGLAISES (Gwadar)
            elif weights["english"] > 0.4:
                # Simplification anglo-saxonne
                if current in ["le", "la"]:
                    result.append("the")
                    i += 1
                    continue
                elif current in ["de", "du", "des"]:
                    result.append("of")
                    i += 1
                    continue
            
            # Mot normal
            result.append(current)
            i += 1
        
        return result

def creonet_translate(
    text: str,
    mood: str = "neutre",
    style: str = "street", 
    city_profile: str = "gwadar",
    seed: Optional[int] = None,
    conserve_punct: bool = False
) -> str:
    if seed is not None:
        random.seed(seed)
        
    translator = CreoNetTranslator()
    weights = translator.get_language_weights(city_profile)
    
    # Tokenisation
    tokens = simple_tokenize(text)
    
    # Traduction mot à mot avec les poids régionaux
    mapped = []
    for token in tokens:
        if is_punctuation(token) and not conserve_punct:
            continue
            
        translated = translator.find_best_translation(token, weights, style)
        mapped.append(translated)
    
    # Application de la syntaxe régionale
    mapped = translator.apply_regional_syntax(mapped, weights)
    
    # AJOUTS SPÉCIFIQUES PAR VILLE
    final_tokens = []
    
    # Port-au-Prince: plus de particules créoles
    if city_profile == "port_au_prince":
        for token in mapped:
            final_tokens.append(token)
            if random.random() < 0.25:
                final_tokens.append(random.choice(["wi", "non", "tèlman", "vre"]))
    
    # Gwadar: plus de code et d'anglais
    elif city_profile == "gwadar":
        for token in mapped:
            final_tokens.append(token)
            if random.random() < 0.2:
                final_tokens.append(random.choice(["data", "net", "node", "stream"]))
    
    # Djibouti: structure plus française
    elif city_profile == "djibouti":
        final_tokens = mapped  # Garde la structure originale
        if random.random() < 0.3:
            final_tokens.insert(0, "alors")
    
    else:
        final_tokens = mapped
    
    # DENSITÉ DE PARTICULES selon le style
    density = 0.25 if style in ("street", "hacker") else 0.1
    out = []
    for token in final_tokens:
        out.append(token)
        if random.random() < density:
            particles = translator.config.get("particles", ["yo", "mi", "dat", "we", "no"])
            out.append(random.choice(particles))
    
    # TAGS D'ÉMOTION
    emotion_tags = translator.config.get("emotion_tags", {}).get(mood, ["<null>"])
    if random.random() < 0.4:
        out.append(random.choice(emotion_tags))
    
    # SÉPARATEURS
    separators = translator.config.get("separators", {"street": " / "})
    sep = separators.get(style, " / ")
    
    result = sep.join(out)
    
    # EFFETS SPÉCIAUX PAR VILLE
    if city_profile == "port_au_prince" and random.random() < 0.3:
        result = result + " // sak pase"
    elif city_profile == "naples" and random.random() < 0.2:
        result = "🇮🇹 " + result
    elif city_profile == "djibouti" and random.random() < 0.2:
        result = result + " // wallahi"
    
    # POST-PROCESSING
    if style in ("ritual", "liturgical"):
        result = result.upper()
    
    result = re.sub(r'( {0,}// {0,})+', ' // ', result)
    result = re.sub(r'( {0,}/ {0,})+', ' / ', result)
    
    return result

# API pour GUI
def get_city_profiles():
    translator = CreoNetTranslator()
    return list(translator.profiles.keys())

def get_emotion_tags():
    config = load_json(FILES["config"])
    return config.get("emotion_tags", {"neutre": ["<null>"]})

def get_styles():
    config = load_json(FILES["config"])
    separators = config.get("separators", {"street": " / "})
    return list(separators.keys())
