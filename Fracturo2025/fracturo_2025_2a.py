#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FracturoScript 2025 — Version Étendue
Un outil pédagogique pour détecter, analyser et déconstruire 
les virus linguistiques de notre époque.

Exécutable sur n'importe quel Python 3.6+.
Aucune dépendance externe.
"""

import json
import random
import argparse
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import textwrap
import hashlib

# Chemins
SCRIPT_DIR = Path(__file__).parent
LEXICON_PATH = SCRIPT_DIR / "lexicon_2025.json"
OUTPUT_DIR = SCRIPT_DIR / "output"
HISTORY_PATH = SCRIPT_DIR / "history.jsonl"
COLLECTIONS_PATH = SCRIPT_DIR / "collections.json"
OUTPUT_DIR.mkdir(exist_ok=True)

# Configuration d'affichage
class Colors:
    """Codes ANSI pour la colorisation (désactivable)"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @classmethod
    def disable(cls):
        cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = ''
        cls.YELLOW = cls.RED = cls.BOLD = cls.UNDERLINE = cls.END = ''

# ---------------------------
# Chargement du lexique
# ---------------------------
def load_lexicon():
    """Charge le lexique de virus linguistiques"""
    try:
        with open(LEXICON_PATH, "r", encoding="utf-8") as f:
            lexicon = json.load(f)
        # Ajoute un ID unique à chaque virus
        for i, virus in enumerate(lexicon):
            if 'id' not in virus:
                virus['id'] = hashlib.md5(virus['payload'].encode()).hexdigest()[:8]
        return lexicon
    except FileNotFoundError:
        print(f"❌ Erreur: Fichier {LEXICON_PATH} introuvable")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {e}")
        sys.exit(1)

# ---------------------------
# Système de filtrage avancé
# ---------------------------
class VirusFilter:
    """Filtre les virus selon différents critères"""
    
    @staticmethod
    def by_emotional_charge(lexicon, min_charge=0, max_charge=10):
        return [v for v in lexicon 
                if min_charge <= v['emotional_charge'] <= max_charge]
    
    @staticmethod
    def by_replication(lexicon, min_rep=0, max_rep=10):
        return [v for v in lexicon 
                if min_rep <= v['replication_potential'] <= max_rep]
    
    @staticmethod
    def by_origin(lexicon, origin_keyword):
        keyword = origin_keyword.lower()
        return [v for v in lexicon 
                if keyword in v['origin'].lower()]
    
    @staticmethod
    def by_strategy(lexicon, strategy_keyword):
        keyword = strategy_keyword.lower()
        return [v for v in lexicon 
                if keyword in v['anti_narrative_strategy'].lower()]
    
    @staticmethod
    def most_dangerous(lexicon, top_n=5):
        """Les virus les plus dangereux (charge émotionnelle × réplication)"""
        scored = [(v, v['emotional_charge'] * v['replication_potential']) 
                  for v in lexicon]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [v for v, _ in scored[:top_n]]
    
    @staticmethod
    def by_keyword(lexicon, keyword):
        """Recherche dans tous les champs textuels"""
        keyword = keyword.lower()
        return [v for v in lexicon if any(
            keyword in str(v.get(field, '')).lower() 
            for field in ['payload', 'origin', 'mechanism', 
                         'countermeasure', 'anti_narrative_strategy']
        )]

# ---------------------------
# Système d'analyse statistique
# ---------------------------
class VirusAnalyzer:
    """Analyse statistique du lexique"""
    
    def __init__(self, lexicon):
        self.lexicon = lexicon
    
    def global_stats(self):
        """Statistiques globales"""
        total = len(self.lexicon)
        avg_emotion = sum(v['emotional_charge'] for v in self.lexicon) / total
        avg_replication = sum(v['replication_potential'] for v in self.lexicon) / total
        
        origins = [v['origin'] for v in self.lexicon]
        strategies = [v['anti_narrative_strategy'] for v in self.lexicon]
        
        return {
            'total': total,
            'avg_emotional_charge': round(avg_emotion, 2),
            'avg_replication': round(avg_replication, 2),
            'unique_origins': len(set(origins)),
            'unique_strategies': len(set(strategies)),
            'most_common_origin': Counter(origins).most_common(1)[0] if origins else None,
            'most_common_strategy': Counter(strategies).most_common(1)[0] if strategies else None
        }
    
    def distribution_report(self):
        """Distribution des charges émotionnelles et potentiels de réplication"""
        emotion_dist = defaultdict(int)
        replication_dist = defaultdict(int)
        
        for v in self.lexicon:
            emotion_dist[v['emotional_charge']] += 1
            replication_dist[v['replication_potential']] += 1
        
        return {
            'emotional_charge': dict(emotion_dist),
            'replication_potential': dict(replication_dist)
        }
    
    def origin_analysis(self):
        """Analyse par origine"""
        by_origin = defaultdict(list)
        for v in self.lexicon:
            by_origin[v['origin']].append(v)
        
        return {
            origin: {
                'count': len(viruses),
                'avg_danger': round(sum(v['emotional_charge'] * v['replication_potential'] 
                                      for v in viruses) / len(viruses), 2)
            }
            for origin, viruses in by_origin.items()
        }
    
    def strategy_analysis(self):
        """Analyse par stratégie anti-narrative"""
        by_strategy = defaultdict(list)
        for v in self.lexicon:
            by_strategy[v['anti_narrative_strategy']].append(v)
        
        return {
            strategy: len(viruses)
            for strategy, viruses in sorted(by_strategy.items(), 
                                          key=lambda x: len(x[1]), 
                                          reverse=True)
        }

# ---------------------------
# Générateur de virus personnalisés
# ---------------------------
class VirusGenerator:
    """Génère de nouveaux virus par combinaison"""
    
    def __init__(self, lexicon):
        self.lexicon = lexicon
    
    def hybrid_virus(self, virus1, virus2):
        """Crée un virus hybride à partir de deux virus"""
        return {
            'payload': f"{virus1['payload']} {virus2['payload']}",
            'origin': f"Hybride: {virus1['origin']} + {virus2['origin']}",
            'emotional_charge': (virus1['emotional_charge'] + virus2['emotional_charge']) // 2,
            'replication_potential': max(virus1['replication_potential'], 
                                        virus2['replication_potential']),
            'paleo_symbol': f"{virus1['paleo_symbol']}{virus2['paleo_symbol']}",
            'anti_narrative_strategy': f"{virus1['anti_narrative_strategy']} + {virus2['anti_narrative_strategy']}",
            'mechanism': f"Combine: {virus1['mechanism']} ET {virus2['mechanism']}",
            'countermeasure': f"{virus1['countermeasure']} • {virus2['countermeasure']}",
            'id': 'hybrid',
            'hybrid': True
        }
    
    def mutate_virus(self, virus):
        """Mute légèrement un virus"""
        mutated = virus.copy()
        mutations = [
            lambda v: {**v, 'emotional_charge': min(10, v['emotional_charge'] + 1)},
            lambda v: {**v, 'replication_potential': min(10, v['replication_potential'] + 1)},
            lambda v: {**v, 'payload': v['payload'].replace('.', '...').replace('?', '...')},
        ]
        return random.choice(mutations)(mutated)

# ---------------------------
# Système d'historique
# ---------------------------
class VirusHistory:
    """Gère l'historique des virus générés"""
    
    @staticmethod
    def log_generation(virus, context=None):
        """Enregistre une génération dans l'historique"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'virus_id': virus.get('id', 'unknown'),
            'payload': virus['payload'],
            'context': context or {}
        }
        
        with open(HISTORY_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    @staticmethod
    def get_history(limit=None):
        """Récupère l'historique"""
        if not HISTORY_PATH.exists():
            return []
        
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            entries = [json.loads(line) for line in f]
        
        return entries[-limit:] if limit else entries
    
    @staticmethod
    def stats():
        """Statistiques de l'historique"""
        history = VirusHistory.get_history()
        if not history:
            return {'total': 0}
        
        virus_counts = Counter(e['virus_id'] for e in history)
        dates = [datetime.fromisoformat(e['timestamp']).date() for e in history]
        
        return {
            'total_generations': len(history),
            'most_generated': virus_counts.most_common(3),
            'first_use': min(dates).isoformat(),
            'last_use': max(dates).isoformat(),
            'unique_viruses': len(virus_counts)
        }

# ---------------------------
# Système de collections personnalisées
# ---------------------------
class VirusCollection:
    """Gère des collections personnalisées de virus"""
    
    @staticmethod
    def load_collections():
        """Charge les collections existantes"""
        if not COLLECTIONS_PATH.exists():
            return {}
        with open(COLLECTIONS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_collections(collections):
        """Sauvegarde les collections"""
        with open(COLLECTIONS_PATH, 'w', encoding='utf-8') as f:
            json.dump(collections, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def add_to_collection(collection_name, virus_id):
        """Ajoute un virus à une collection"""
        collections = VirusCollection.load_collections()
        if collection_name not in collections:
            collections[collection_name] = {
                'created': datetime.now().isoformat(),
                'viruses': []
            }
        
        if virus_id not in collections[collection_name]['viruses']:
            collections[collection_name]['viruses'].append(virus_id)
            VirusCollection.save_collections(collections)
            return True
        return False
    
    @staticmethod
    def list_collections():
        """Liste toutes les collections"""
        return VirusCollection.load_collections()
    
    @staticmethod
    def get_collection(collection_name, lexicon):
        """Récupère les virus d'une collection"""
        collections = VirusCollection.load_collections()
        if collection_name not in collections:
            return []
        
        virus_ids = collections[collection_name]['viruses']
        return [v for v in lexicon if v['id'] in virus_ids]

# ---------------------------
# Affichage amélioré
# ---------------------------
class VirusDisplay:
    """Gestion avancée de l'affichage"""
    
    @staticmethod
    def compact(virus):
        """Affichage compact sur une ligne"""
        danger = virus['emotional_charge'] * virus['replication_potential']
        danger_indicator = '🔴' if danger > 70 else '🟠' if danger > 40 else '🟢'
        return f"{danger_indicator} « {virus['payload']} » — {virus['origin']}"
    
    @staticmethod
    def detailed(virus):
        """Affichage détaillé et formaté"""
        print("\n" + "━" * 70)
        print(f"{Colors.BOLD}{Colors.RED}🧠 VIRUS LINGUISTIQUE • 2025{Colors.END}")
        print("━" * 70)
        
        # Indicateur de danger
        danger = virus['emotional_charge'] * virus['replication_potential']
        danger_level = "CRITIQUE" if danger > 70 else "ÉLEVÉ" if danger > 40 else "MODÉRÉ"
        danger_color = Colors.RED if danger > 70 else Colors.YELLOW if danger > 40 else Colors.GREEN
        
        print(f"\n{Colors.BOLD}Niveau de danger: {danger_color}{danger_level} ({danger}/100){Colors.END}\n")
        
        # Informations principales
        print(f"{Colors.CYAN}💬 Payload{Colors.END}")
        print(f"   {Colors.BOLD}{virus['payload']}{Colors.END}")
        
        print(f"\n{Colors.CYAN}📍 Origine{Colors.END}")
        print(f"   {virus['origin']}")
        
        print(f"\n{Colors.CYAN}🪨 Symbole{Colors.END}")
        print(f"   {virus['paleo_symbol']} (symbole paléolithique)")
        
        # Métriques
        print(f"\n{Colors.CYAN}📊 Métriques{Colors.END}")
        print(f"   Charge émotionnelle:  {VirusDisplay._bar(virus['emotional_charge'], 10)} {virus['emotional_charge']}/10")
        print(f"   Potentiel réplication: {VirusDisplay._bar(virus['replication_potential'], 10)} {virus['replication_potential']}/10")
        
        # Stratégie
        print(f"\n{Colors.CYAN}🌀 Stratégie anti-narrative{Colors.END}")
        print(f"   {virus['anti_narrative_strategy']}")
        
        # Mécanisme
        print(f"\n{Colors.CYAN}🔬 Mécanisme de fonctionnement{Colors.END}")
        wrapped = textwrap.fill(virus['mechanism'], width=65, initial_indent='   ', subsequent_indent='   ')
        print(wrapped)
        
        # Contre-mesure
        print(f"\n{Colors.CYAN}🛡️  Contre-mesure suggérée{Colors.END}")
        print(f"   {Colors.GREEN}{virus['countermeasure']}{Colors.END}")
        
        # ID
        if 'id' in virus:
            print(f"\n{Colors.CYAN}🔑 ID{Colors.END}: {virus['id']}")
        
        print("\n" + "━" * 70 + "\n")
    
    @staticmethod
    def _bar(value, max_value):
        """Crée une barre de progression ASCII"""
        filled = int((value / max_value) * 10)
        return '█' * filled + '░' * (10 - filled)
    
    @staticmethod
    def table(viruses, fields=['payload', 'origin', 'emotional_charge', 'replication_potential']):
        """Affichage tabulaire"""
        if not viruses:
            print("Aucun virus à afficher")
            return
        
        # En-têtes
        headers = {
            'payload': 'Payload',
            'origin': 'Origine',
            'emotional_charge': 'Émotion',
            'replication_potential': 'Réplication',
            'anti_narrative_strategy': 'Stratégie'
        }
        
        print("\n" + "─" * 120)
        header_line = " | ".join(headers[f] for f in fields if f in headers)
        print(header_line)
        print("─" * 120)
        
        for virus in viruses:
            values = []
            for field in fields:
                value = str(virus.get(field, ''))
                if field == 'payload':
                    value = value[:60] + '...' if len(value) > 60 else value
                elif field == 'origin':
                    value = value[:30] + '...' if len(value) > 30 else value
                values.append(value)
            print(" | ".join(values))
        
        print("─" * 120 + "\n")

# ---------------------------
# Système de recommandation
# ---------------------------
class VirusRecommender:
    """Recommande des virus basés sur l'historique"""
    
    def __init__(self, lexicon):
        self.lexicon = lexicon
    
    def recommend_similar(self, virus, n=3):
        """Recommande des virus similaires"""
        # Calcul de similarité simple basé sur les métriques
        similarities = []
        for v in self.lexicon:
            if v['id'] == virus['id']:
                continue
            
            # Distance euclidienne normalisée
            emotion_diff = abs(v['emotional_charge'] - virus['emotional_charge']) / 10
            replication_diff = abs(v['replication_potential'] - virus['replication_potential']) / 10
            
            # Similarité d'origine (booléenne)
            origin_match = 1 if v['origin'] == virus['origin'] else 0
            
            similarity = 1 - ((emotion_diff + replication_diff) / 2) + (origin_match * 0.2)
            similarities.append((v, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [v for v, _ in similarities[:n]]
    
    def recommend_complementary(self, virus, n=3):
        """Recommande des virus complémentaires (différentes stratégies)"""
        different_strategy = [
            v for v in self.lexicon 
            if v['anti_narrative_strategy'] != virus['anti_narrative_strategy']
        ]
        return random.sample(different_strategy, min(n, len(different_strategy)))

# ---------------------------
# Mode interactif
# ---------------------------
class InteractiveMode:
    """Mode interactif pour explorer le lexique"""
    
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.current_virus = None
        self.analyzer = VirusAnalyzer(lexicon)
        self.recommender = VirusRecommender(lexicon)
        self.generator = VirusGenerator(lexicon)
    
    def run(self):
        """Lance le mode interactif"""
        print(f"\n{Colors.BOLD}═══════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BOLD}{Colors.RED}   🧠 FracturoScript 2025 — Mode Interactif{Colors.END}")
        print(f"{Colors.BOLD}═══════════════════════════════════════════════════════{Colors.END}\n")
        print(f"Lexique chargé: {len(self.lexicon)} virus linguistiques")
        print("Tapez 'help' pour voir les commandes disponibles\n")
        
        while True:
            try:
                cmd = input(f"{Colors.CYAN}fracturo>{Colors.END} ").strip().lower()
                
                if not cmd:
                    continue
                elif cmd in ['quit', 'exit', 'q']:
                    print("Au revoir! 👋")
                    break
                elif cmd == 'help':
                    self._show_help()
                elif cmd == 'random':
                    self._random_virus()
                elif cmd == 'stats':
                    self._show_stats()
                elif cmd.startswith('filter '):
                    self._filter_command(cmd)
                elif cmd == 'dangerous':
                    self._show_dangerous()
                elif cmd.startswith('search '):
                    self._search_command(cmd)
                elif cmd == 'similar' and self.current_virus:
                    self._show_similar()
                elif cmd == 'complementary' and self.current_virus:
                    self._show_complementary()
                elif cmd == 'history':
                    self._show_history()
                elif cmd == 'collections':
                    self._show_collections()
                elif cmd.startswith('save '):
                    self._save_to_collection(cmd)
                elif cmd == 'hybrid' and self.current_virus:
                    self._create_hybrid()
                elif cmd == 'mutate' and self.current_virus:
                    self._mutate_current()
                else:
                    print(f"❌ Commande inconnue: {cmd}")
                    print("   Tapez 'help' pour voir les commandes")
                
            except KeyboardInterrupt:
                print("\n\nInterrompu. Tapez 'quit' pour quitter.")
            except Exception as e:
                print(f"❌ Erreur: {e}")
    
    def _show_help(self):
        """Affiche l'aide"""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║                   COMMANDES DISPONIBLES                     ║
╠════════════════════════════════════════════════════════════╣
║ random           │ Affiche un virus aléatoire               ║
║ dangerous        │ Top 5 des virus les plus dangereux       ║
║ stats            │ Statistiques globales                     ║
║ history          │ Historique des générations                ║
║ search <mot>     │ Recherche par mot-clé                     ║
║ filter <critère> │ Filtre les virus                          ║
║                  │   emotion:min-max, replication:min-max    ║
║                  │   origin:<mot>, strategy:<mot>            ║
║ collections      │ Liste les collections sauvegardées        ║
║ save <nom>       │ Sauvegarde le virus actuel                ║
║ similar          │ Virus similaires au virus actuel          ║
║ complementary    │ Virus complémentaires                     ║
║ hybrid           │ Crée un hybride (nécessite 2 virus)      ║
║ mutate           │ Mute le virus actuel                      ║
║ help             │ Affiche cette aide                        ║
║ quit / exit / q  │ Quitte le mode interactif                 ║
╚════════════════════════════════════════════════════════════╝
        """
        print(help_text)
    
    def _random_virus(self):
        """Affiche un virus aléatoire"""
        self.current_virus = random.choice(self.lexicon)
        VirusDisplay.detailed(self.current_virus)
        VirusHistory.log_generation(self.current_virus, {'mode': 'interactive'})
    
    def _show_stats(self):
        """Affiche les statistiques"""
        stats = self.analyzer.global_stats()
        print(f"\n{Colors.BOLD}📊 STATISTIQUES GLOBALES{Colors.END}\n")
        print(f"Total de virus:              {stats['total']}")
        print(f"Charge émotionnelle moyenne: {stats['avg_emotional_charge']}/10")
        print(f"Réplication moyenne:         {stats['avg_replication']}/10")
        print(f"Origines uniques:            {stats['unique_origins']}")
        print(f"Stratégies uniques:          {stats['unique_strategies']}")
        if stats['most_common_origin']:
            print(f"Origine la plus fréquente:   {stats['most_common_origin'][0]} ({stats['most_common_origin'][1]}x)")
        print()
    
    def _filter_command(self, cmd):
        """Gère les commandes de filtrage"""
        parts = cmd.split(' ', 1)
        if len(parts) < 2:
            print("Usage: filter emotion:5-8, filter origin:gig, etc.")
            return
        
        criterion = parts[1]
        
        if ':' not in criterion:
            print("Format incorrect. Exemple: filter emotion:5-8")
            return
        
        filter_type, value = criterion.split(':', 1)
        
        if filter_type == 'emotion':
            try:
                min_val, max_val = map(int, value.split('-'))
                results = VirusFilter.by_emotional_charge(self.lexicon, min_val, max_val)
            except ValueError:
                print("Format incorrect pour emotion. Exemple: emotion:5-8")
                return
        elif filter_type == 'replication':
            try:
                min_val, max_val = map(int, value.split('-'))
                results = VirusFilter.by_replication(self.lexicon, min_val, max_val)
            except ValueError:
                print("Format incorrect pour replication. Exemple: replication:7-9")
                return
        elif filter_type == 'origin':
            results = VirusFilter.by_origin(self.lexicon, value)
        elif filter_type == 'strategy':
            results = VirusFilter.by_strategy(self.lexicon, value)
        else:
            print(f"Type de filtre inconnu: {filter_type}")
            return
        
        print(f"\n{len(results)} résultat(s):\n")
        for virus in results[:10]:  # Limite à 10
            print(VirusDisplay.compact(virus))
        
        if len(results) > 10:
            print(f"\n... et {len(results) - 10} autres")
    
    def _show_dangerous(self):
        """Affiche les virus les plus dangereux"""
        dangerous = VirusFilter.most_dangerous(self.lexicon, 5)
        print(f"\n{Colors.BOLD}{Colors.RED}⚠️  TOP 5 DES VIRUS LES PLUS DANGEREUX{Colors.END}\n")
        for i, virus in enumerate(dangerous, 1):
            danger = virus['emotional_charge'] * virus['replication_potential']
            print(f"{i}. {VirusDisplay.compact(virus)} [Danger: {danger}/100]")
        print()
    
    def _search_command(self, cmd):
        """Recherche par mot-clé"""
        keyword = cmd.split(' ', 1)[1] if ' ' in cmd else ''
        if not keyword:
            print("Usage: search <mot-clé>")
            return
        
        results = VirusFilter.by_keyword(self.lexicon, keyword)
        print(f"\n{len(results)} résultat(s) pour '{keyword}':\n")
        for virus in results[:10]:
            print(VirusDisplay.compact(virus))
        
        if len(results) > 10:
            print(f"\n... et {len(results) - 10} autres")
    
    def _show_similar(self):
        """Affiche les virus similaires"""
        similar = self.recommender.recommend_similar(self.current_virus, 3)
        print(f"\n{Colors.BOLD}🔗 VIRUS SIMILAIRES{Colors.END}\n")
        for virus in similar:
            print(VirusDisplay.compact(virus))
        print()
    
    def _show_complementary(self):
        """Affiche les virus complémentaires"""
        complementary = self.recommender.recommend_complementary(self.current_virus, 3)
        print(f"\n{Colors.BOLD}🔄 VIRUS COMPLÉMENTAIRES{Colors.END}\n")
        for virus in complementary:
            print(VirusDisplay.compact(virus))
        print()
    
    def _show_history(self):
        """Affiche l'historique"""
        stats = VirusHistory.stats()
        print(f"\n{Colors.BOLD}📜 HISTORIQUE{Colors.END}\n")
        
        if stats['total_generations'] == 0:
            print("Aucune génération enregistrée")
            return
        
        print(f"Total de générations: {stats['total_generations']}")
        print(f"Virus uniques:        {stats['unique_viruses']}")
        print(f"Première utilisation: {stats['first_use']}")
        print(f"Dernière utilisation: {stats['last_use']}")
        print(f"\nPlus générés:")
        for virus_id, count in stats['most_generated']:
            print(f"  • {virus_id}: {count}x")
        print()
    
    def _show_collections(self):
        """Affiche les collections"""
        collections = VirusCollection.list_collections()
        print(f"\n{Colors.BOLD}📚 COLLECTIONS{Colors.END}\n")
        
        if not collections:
            print("Aucune collection sauvegardée")
            return
        
        for name, data in collections.items():
            print(f"• {name}: {len(data['viruses'])} virus")
            print(f"  Créée le: {data['created'][:10]}")
        print()
    
    def _save_to_collection(self, cmd):
        """Sauvegarde dans une collection"""
        if not self.current_virus:
            print("❌ Aucun virus actuel. Générez-en un d'abord (random)")
            return
        
        parts = cmd.split(' ', 1)
        if len(parts) < 2:
            print("Usage: save <nom_collection>")
            return
        
        collection_name = parts[1]
        success = VirusCollection.add_to_collection(collection_name, self.current_virus['id'])
        
        if success:
            print(f"✅ Virus sauvegardé dans la collection '{collection_name}'")
        else:
            print(f"ℹ️  Ce virus existe déjà dans '{collection_name}'")
    
    def _create_hybrid(self):
        """Crée un virus hybride"""
        print("\nSélectionnez un second virus pour créer un hybride:")
        virus2 = random.choice(self.lexicon)
        print(f"Second virus: {VirusDisplay.compact(virus2)}\n")
        
        hybrid = self.generator.hybrid_virus(self.current_virus, virus2)
        self.current_virus = hybrid
        VirusDisplay.detailed(hybrid)
    
    def _mutate_current(self):
        """Mute le virus actuel"""
        mutated = self.generator.mutate_virus(self.current_virus)
        self.current_virus = mutated
        print("\n🧬 Virus muté:")
        VirusDisplay.detailed(mutated)

# ---------------------------
# Mode comparaison
# ---------------------------
class VirusComparator:
    """Compare plusieurs virus"""
    
    @staticmethod
    def compare(virus1, virus2):
        """Compare deux virus"""
        print(f"\n{Colors.BOLD}⚖️  COMPARAISON DE VIRUS{Colors.END}\n")
        
        fields = [
            ('Payload', 'payload'),
            ('Origine', 'origin'),
            ('Charge émotionnelle', 'emotional_charge'),
            ('Potentiel réplication', 'replication_potential'),
            ('Stratégie', 'anti_narrative_strategy')
        ]
        
        for label, field in fields:
            v1_val = virus1.get(field, 'N/A')
            v2_val = virus2.get(field, 'N/A')
            
            print(f"{Colors.CYAN}{label}{Colors.END}")
            print(f"  Virus 1: {v1_val}")
            print(f"  Virus 2: {v2_val}")
            
            if field in ['emotional_charge', 'replication_potential']:
                diff = int(v1_val) - int(v2_val)
                if diff > 0:
                    print(f"  → Virus 1 plus élevé (+{diff})")
                elif diff < 0:
                    print(f"  → Virus 2 plus élevé (+{abs(diff)})")
                else:
                    print(f"  → Égalité")
            print()
        
        # Indice de danger
        danger1 = virus1['emotional_charge'] * virus1['replication_potential']
        danger2 = virus2['emotional_charge'] * virus2['replication_potential']
        
        print(f"{Colors.BOLD}Indice de danger:{Colors.END}")
        print(f"  Virus 1: {danger1}/100")
        print(f"  Virus 2: {danger2}/100")
        
        if danger1 > danger2:
            print(f"  {Colors.RED}→ Virus 1 est plus dangereux{Colors.END}")
        elif danger2 > danger1:
            print(f"  {Colors.RED}→ Virus 2 est plus dangereux{Colors.END}")
        else:
            print(f"  → Dangerosité égale")
        print()

# ---------------------------
# Export avancé
# ---------------------------
class VirusExporter:
    """Exporte les virus dans différents formats"""
    
    @staticmethod
    def to_json(virus, filepath):
        """Export JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(virus, f, ensure_ascii=False, indent=2)
        return filepath
    
    @staticmethod
    def to_markdown(virus, filepath):
        """Export Markdown"""
        md_content = f"""# Virus Linguistique

## {virus['payload']}

**Origine:** {virus['origin']}

**Symbole:** {virus['paleo_symbol']}

### Métriques

- Charge émotionnelle: {virus['emotional_charge']}/10
- Potentiel de réplication: {virus['replication_potential']}/10
- Indice de danger: {virus['emotional_charge'] * virus['replication_potential']}/100

### Stratégie anti-narrative

{virus['anti_narrative_strategy']}

### Mécanisme

{virus['mechanism']}

### Contre-mesure

> {virus['countermeasure']}

---

*Généré par FracturoScript 2025 le {datetime.now().strftime('%Y-%m-%d à %H:%M')}*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        return filepath
    
    @staticmethod
    def to_html(virus, filepath):
        """Export HTML"""
        danger = virus['emotional_charge'] * virus['replication_potential']
        danger_color = '#dc3545' if danger > 70 else '#ffc107' if danger > 40 else '#28a745'
        
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virus Linguistique - {virus['payload'][:50]}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid {danger_color};
            padding-bottom: 10px;
        }}
        .payload {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin: 20px 0;
            padding: 15px;
            background: #ecf0f1;
            border-left: 5px solid {danger_color};
        }}
        .metrics {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }}
        .metric {{
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: {danger_color};
        }}
        .section {{
            margin: 25px 0;
        }}
        .section-title {{
            font-size: 1.2em;
            color: #2c3e50;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        .countermeasure {{
            background: #d4edda;
            border-left: 5px solid #28a745;
            padding: 15px;
            font-style: italic;
            margin: 15px 0;
        }}
        .symbol {{
            font-size: 3em;
            text-align: center;
            margin: 20px 0;
        }}
        footer {{
            margin-top: 30px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Virus Linguistique</h1>
        
        <div class="payload">
            « {virus['payload']} »
        </div>
        
        <div class="symbol">{virus['paleo_symbol']}</div>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Charge émotionnelle</div>
                <div class="metric-value">{virus['emotional_charge']}/10</div>
            </div>
            <div class="metric">
                <div class="metric-label">Potentiel de réplication</div>
                <div class="metric-value">{virus['replication_potential']}/10</div>
            </div>
            <div class="metric">
                <div class="metric-label">Origine</div>
                <div style="font-size: 1em; color: #555;">{virus['origin']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Indice de danger</div>
                <div class="metric-value">{danger}/100</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">🌀 Stratégie anti-narrative</div>
            <p>{virus['anti_narrative_strategy']}</p>
        </div>
        
        <div class="section">
            <div class="section-title">🔬 Mécanisme de fonctionnement</div>
            <p>{virus['mechanism']}</p>
        </div>
        
        <div class="section">
            <div class="section-title">🛡️ Contre-mesure</div>
            <div class="countermeasure">
                {virus['countermeasure']}
            </div>
        </div>
        
        <footer>
            Généré par FracturoScript 2025<br>
            {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        </footer>
    </div>
</body>
</html>"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath
    
    @staticmethod
    def batch_export(viruses, format='json'):
        """Export de plusieurs virus"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f"batch_{timestamp}.{format}"
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(viruses, f, ensure_ascii=False, indent=2)
        elif format == 'csv':
            # Export CSV simple sans dépendances
            with open(output_path, 'w', encoding='utf-8') as f:
                # En-têtes
                headers = ['payload', 'origin', 'emotional_charge', 'replication_potential', 
                          'anti_narrative_strategy', 'mechanism', 'countermeasure']
                f.write(','.join(headers) + '\n')
                
                # Données
                for virus in viruses:
                    row = [str(virus.get(h, '')).replace(',', ';').replace('\n', ' ') 
                          for h in headers]
                    f.write(','.join(row) + '\n')
        
        return output_path

# ---------------------------
# Générateur de rapports
# ---------------------------
class ReportGenerator:
    """Génère des rapports d'analyse"""
    
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.analyzer = VirusAnalyzer(lexicon)
    
    def full_report(self):
        """Génère un rapport complet"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = OUTPUT_DIR / f"rapport_{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT D'ANALYSE - FRACTURO 2025\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
            f.write(f"Lexique: {len(self.lexicon)} virus linguistiques\n\n")
            
            # Statistiques globales
            stats = self.analyzer.global_stats()
            f.write("-" * 80 + "\n")
            f.write("STATISTIQUES GLOBALES\n")
            f.write("-" * 80 + "\n")
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            # Distribution
            dist = self.analyzer.distribution_report()
            f.write("-" * 80 + "\n")
            f.write("DISTRIBUTION DES CHARGES ÉMOTIONNELLES\n")
            f.write("-" * 80 + "\n")
            for charge, count in sorted(dist['emotional_charge'].items()):
                bar = '█' * count
                f.write(f"{charge}/10: {bar} ({count})\n")
            f.write("\n")
            
            f.write("-" * 80 + "\n")
            f.write("DISTRIBUTION DU POTENTIEL DE RÉPLICATION\n")
            f.write("-" * 80 + "\n")
            for rep, count in sorted(dist['replication_potential'].items()):
                bar = '█' * count
                f.write(f"{rep}/10: {bar} ({count})\n")
            f.write("\n")
            
            # Analyse par origine
            origin_analysis = self.analyzer.origin_analysis()
            f.write("-" * 80 + "\n")
            f.write("ANALYSE PAR ORIGINE\n")
            f.write("-" * 80 + "\n")
            for origin, data in sorted(origin_analysis.items(), 
                                      key=lambda x: x[1]['avg_danger'], 
                                      reverse=True):
                f.write(f"\n{origin}\n")
                f.write(f"  Nombre: {data['count']}\n")
                f.write(f"  Danger moyen: {data['avg_danger']}/100\n")
            f.write("\n")
            
            # Top dangereux
            dangerous = VirusFilter.most_dangerous(self.lexicon, 10)
            f.write("-" * 80 + "\n")
            f.write("TOP 10 DES VIRUS LES PLUS DANGEREUX\n")
            f.write("-" * 80 + "\n")
            for i, virus in enumerate(dangerous, 1):
                danger = virus['emotional_charge'] * virus['replication_potential']
                f.write(f"\n{i}. {virus['payload']}\n")
                f.write(f"   Origine: {virus['origin']}\n")
                f.write(f"   Danger: {danger}/100\n")
            
        return report_path

# ---------------------------
# CLI principal amélioré
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="FracturoScript 2025 — Détecteur de virus linguistiques actuels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s --random                           # Affiche un virus aléatoire
  %(prog)s --dangerous 5                      # Top 5 des plus dangereux
  %(prog)s --filter emotion:7-9               # Filtre par charge émotionnelle
  %(prog)s --search "burnout"                 # Recherche par mot-clé
  %(prog)s --interactive                      # Mode interactif
  %(prog)s --stats                            # Statistiques globales
  %(prog)s --export html --count 5            # Exporte 5 virus en HTML
  %(prog)s --report                           # Génère un rapport complet
        """
    )
    
    # Arguments de base
    parser.add_argument("--count", type=int, default=1, 
                       help="Nombre de virus à afficher")
    parser.add_argument("--seed", type=int, default=None, 
                       help="Graine aléatoire pour reproductibilité")
    parser.add_argument("--no-color", action="store_true",
                       help="Désactive les couleurs")
    
    # Modes d'affichage
    display_group = parser.add_argument_group('Affichage')
    display_group.add_argument("--random", action="store_true",
                              help="Affiche des virus aléatoires")
    display_group.add_argument("--compact", action="store_true",
                              help="Affichage compact (une ligne)")
    display_group.add_argument("--detailed", action="store_true",
                              help="Affichage détaillé (défaut)")
    display_group.add_argument("--table", action="store_true",
                              help="Affichage tabulaire")
    
    # Filtres
    filter_group = parser.add_argument_group('Filtres')
    filter_group.add_argument("--filter", type=str,
                             help="Filtre: emotion:min-max, replication:min-max, origin:mot, strategy:mot")
    filter_group.add_argument("--dangerous", type=int, metavar='N',
                             help="Affiche les N virus les plus dangereux")
    filter_group.add_argument("--search", type=str,
                             help="Recherche par mot-clé dans tous les champs")
    
    # Analyse
    analysis_group = parser.add_argument_group('Analyse')
    analysis_group.add_argument("--stats", action="store_true",
                               help="Affiche les statistiques globales")
    analysis_group.add_argument("--distribution", action="store_true",
                               help="Affiche la distribution des métriques")
    analysis_group.add_argument("--origins", action="store_true",
                               help="Analyse par origine")
    analysis_group.add_argument("--strategies", action="store_true",
                               help="Analyse par stratégie")
    
    # Export
    export_group = parser.add_argument_group('Export')
    export_group.add_argument("--export", choices=['json', 'markdown', 'html', 'csv'],
                             help="Format d'export")
    export_group.add_argument("--report", action="store_true",
                             help="Génère un rapport complet")
    
    # Historique et collections
    history_group = parser.add_argument_group('Historique et collections')
    history_group.add_argument("--history", action="store_true",
                              help="Affiche l'historique des générations")
    history_group.add_argument("--collections", action="store_true",
                              help="Liste les collections sauvegardées")
    history_group.add_argument("--collection", type=str,
                              help="Affiche une collection spécifique")
    
    # Modes spéciaux
    special_group = parser.add_argument_group('Modes spéciaux')
    special_group.add_argument("--interactive", "-i", action="store_true",
                              help="Lance le mode interactif")
    special_group.add_argument("--compare", nargs=2, type=int,
                              help="Compare deux virus par index")
    special_group.add_argument("--hybrid", nargs=2, type=int,
                              help="Crée un virus hybride à partir de deux index")
    
    args = parser.parse_args()
    
    # Désactive les couleurs si demandé
    if args.no_color:
        Colors.disable()
    
    # Charge le lexique
    lexicon = load_lexicon()
    print(f"{Colors.GREEN}✓{Colors.END} Lexique 2025 chargé ({len(lexicon)} virus)\n")
    
    # Mode interactif
    if args.interactive:
        interactive = InteractiveMode(lexicon)
        interactive.run()
        return
    
    # Historique
    if args.history:
        stats = VirusHistory.stats()
        print(f"{Colors.BOLD}📜 HISTORIQUE{Colors.END}\n")
        if stats['total_generations'] == 0:
            print("Aucune génération enregistrée")
        else:
            print(f"Total: {stats['total_generations']} générations")
            print(f"Virus uniques: {stats['unique_viruses']}")
            print(f"Période: {stats['first_use']} → {stats['last_use']}")
            print("\nPlus générés:")
            for virus_id, count in stats['most_generated']:
                print(f"  • {virus_id}: {count}x")
        return
    
    # Collections
    if args.collections:
        collections = VirusCollection.list_collections()
        print(f"{Colors.BOLD}📚 COLLECTIONS{Colors.END}\n")
        if not collections:
            print("Aucune collection sauvegardée")
        else:
            for name, data in collections.items():
                print(f"• {name}: {len(data['viruses'])} virus (créée le {data['created'][:10]})")
        return
    
    if args.collection:
        viruses = VirusCollection.get_collection(args.collection, lexicon)
        if not viruses:
            print(f"❌ Collection '{args.collection}' introuvable ou vide")
            return
        print(f"\n{Colors.BOLD}📚 Collection: {args.collection}{Colors.END}\n")
        for virus in viruses:
            print(VirusDisplay.compact(virus))
        return
    
    # Statistiques
    analyzer = VirusAnalyzer(lexicon)
    
    if args.stats:
        stats = analyzer.global_stats()
        print(f"{Colors.BOLD}📊 STATISTIQUES GLOBALES{Colors.END}\n")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        return
    
    if args.distribution:
        dist = analyzer.distribution_report()
        print(f"{Colors.BOLD}📊 DISTRIBUTION{Colors.END}\n")
        print("Charge émotionnelle:")
        for charge, count in sorted(dist['emotional_charge'].items()):
            bar = '█' * count
            print(f"  {charge}/10: {bar} ({count})")
        print("\nPotentiel de réplication:")
        for rep, count in sorted(dist['replication_potential'].items()):
            bar = '█' * count
            print(f"  {rep}/10: {bar} ({count})")
        return
    
    if args.origins:
        origins = analyzer.origin_analysis()
        print(f"{Colors.BOLD}📍 ANALYSE PAR ORIGINE{Colors.END}\n")
        for origin, data in sorted(origins.items(), key=lambda x: x[1]['avg_danger'], reverse=True):
            print(f"{origin}")
            print(f"  Nombre: {data['count']}, Danger moyen: {data['avg_danger']}/100")
        return
    
    if args.strategies:
        strategies = analyzer.strategy_analysis()
        print(f"{Colors.BOLD}🌀 ANALYSE PAR STRATÉGIE{Colors.END}\n")
        for strategy, count in list(strategies.items())[:15]:
            print(f"{strategy}: {count}")
        return
    
    # Rapport
    if args.report:
        generator = ReportGenerator(lexicon)
        report_path = generator.full_report()
        print(f"✅ Rapport généré: {report_path}")
        return
    
    # Comparaison
    if args.compare:
        idx1, idx2 = args.compare
        if 0 <= idx1 < len(lexicon) and 0 <= idx2 < len(lexicon):
            VirusComparator.compare(lexicon[idx1], lexicon[idx2])
        else:
            print(f"❌ Index invalides (0-{len(lexicon)-1})")
        return
    
    # Hybride
    if args.hybrid:
        idx1, idx2 = args.hybrid
        if 0 <= idx1 < len(lexicon) and 0 <= idx2 < len(lexicon):
            generator = VirusGenerator(lexicon)
            hybrid = generator.hybrid_virus(lexicon[idx1], lexicon[idx2])
            VirusDisplay.detailed(hybrid)
        else:
            print(f"❌ Index invalides (0-{len(lexicon)-1})")
        return
    
    # Sélection des virus à afficher
    selected_viruses = []
    
    if args.filter:
        # Parsing du filtre
        if ':' in args.filter:
            filter_type, value = args.filter.split(':', 1)
            
            if filter_type == 'emotion':
                min_val, max_val = map(int, value.split('-'))
                selected_viruses = VirusFilter.by_emotional_charge(lexicon, min_val, max_val)
            elif filter_type == 'replication':
                min_val, max_val = map(int, value.split('-'))
                selected_viruses = VirusFilter.by_replication(lexicon, min_val, max_val)
            elif filter_type == 'origin':
                selected_viruses = VirusFilter.by_origin(lexicon, value)
            elif filter_type == 'strategy':
                selected_viruses = VirusFilter.by_strategy(lexicon, value)
        
        print(f"Filtre appliqué: {len(selected_viruses)} résultat(s)\n")
    
    elif args.search:
        selected_viruses = VirusFilter.by_keyword(lexicon, args.search)
        print(f"Recherche '{args.search}': {len(selected_viruses)} résultat(s)\n")
    
    elif args.dangerous:
        selected_viruses = VirusFilter.most_dangerous(lexicon, args.dangerous)
        print(f"Top {args.dangerous} des virus les plus dangereux:\n")
    
    elif args.random or not any([args.filter, args.search, args.dangerous]):
        # Par défaut: sélection aléatoire
        if args.seed:
            random.seed(args.seed)
        selected_viruses = [random.choice(lexicon) for _ in range(args.count)]
    
    # Limitation du nombre
    if args.count and len(selected_viruses) > args.count:
        selected_viruses = selected_viruses[:args.count]
    
    # Affichage
    if args.table:
        VirusDisplay.table(selected_viruses)
    elif args.compact:
        for virus in selected_viruses:
            print(VirusDisplay.compact(virus))
    else:
        # Détaillé par défaut
        for virus in selected_viruses:
            VirusDisplay.detailed(virus)
            VirusHistory.log_generation(virus, {'mode': 'cli'})
    
    # Export
    if args.export and selected_viruses:
        exporter = VirusExporter()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if len(selected_viruses) == 1:
            virus = selected_viruses[0]
            if args.export == 'json':
                path = OUTPUT_DIR / f"virus_{timestamp}.json"
                exporter.to_json(virus, path)
            elif args.export == 'markdown':
                path = OUTPUT_DIR / f"virus_{timestamp}.md"
                exporter.to_markdown(virus, path)
            elif args.export == 'html':
                path = OUTPUT_DIR / f"virus_{timestamp}.html"
                exporter.to_html(virus, path)
            print(f"\n✅ Exporté: {path}")
        else:
            path = exporter.batch_export(selected_viruses, args.export)
            print(f"\n✅ Batch exporté: {path}")

if __name__ == "__main__":
    main()