#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEME-FORGERY ENGINE v2.0 - ULTRA ENHANCED
Système avancé de forge mémétique basé sur la Bible du Programme
Chargement JSON + CLI complète + Extensions AR
"""

import argparse
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random
import requests
from io import BytesIO
import hashlib
from datetime import datetime
import os
import sys
from pathlib import Path
import qrcode
import feedparser
from urllib.parse import quote

class AdvancedMemeForge:
    def __init__(self, config_dir="./config"):
        self.config_dir = Path(config_dir)
        self.load_configurations()
        self.setup_glitch_luts()
        
    def load_configurations(self):
        """Charge toutes les configurations depuis les fichiers JSON"""
        try:
            # Configuration des runes
            with open(self.config_dir / "runes.json", 'r', encoding='utf-8') as f:
                self.runes_config = json.load(f)
            
            # Archétypes mémétiques
            with open(self.config_dir / "archetypes.json", 'r', encoding='utf-8') as f:
                self.archetypes_config = json.load(f)
            
            # Templates de narratives
            with open(self.config_dir / "narratives.json", 'r', encoding='utf-8') as f:
                self.narratives_config = json.load(f)
            
            # Effets glitch avancés
            with open(self.config_dir / "glitch_effects.json", 'r', encoding='utf-8') as f:
                self.glitch_config = json.load(f)
            
            # Sources d'images et APIs
            with open(self.config_dir / "sources.json", 'r', encoding='utf-8') as f:
                self.sources_config = json.load(f)
                
            print("✅ Configurations chargées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur chargement config: {e}")
            self.load_fallback_config()
    
    def load_fallback_config(self):
        """Configuration de fallback si fichiers manquants"""
        self.runes_config = {
            "runes": {
                "ᚨ": {"name": "Ansuz", "effect": "communication_divine", "frequency": "14.225"},
                "ᛒ": {"name": "Berkano", "effect": "naissance_transformation", "frequency": "14.100"},
                "ᚠ": {"name": "Fehu", "effect": "richesse_assignation", "frequency": "14.300"},
                "ᛉ": {"name": "Algiz", "effect": "protection_fusion", "frequency": "14.175"}
            }
        }
        
        self.archetypes_config = {
            "archetypes": {
                "glitch": {
                    "keywords": ["corruption", "fracture", "erreur_systeme", "bug_feature"],
                    "color_palette": ["#ff0000", "#00ffff", "#ffff00", "#0000ff"],
                    "intensity": 2.5
                },
                "resistance": {
                    "keywords": ["rebellion_analog", "silence", "memoire", "effacement"],
                    "color_palette": ["#8b4513", "#2f4f4f", "#696969", "#f5f5dc"],
                    "intensity": 1.8
                }
            }
        }
    
    def setup_glitch_luts(self):
        """Initialise les tables de lookup pour effets glitch avancés"""
        self.channel_shift_lut = {
            "subtle": {"x_shift": (2, 5), "y_shift": (1, 3)},
            "medium": {"x_shift": (5, 12), "y_shift": (3, 8)},
            "extreme": {"x_shift": (10, 25), "y_shift": (5, 15)}
        }
        
        self.data_bending_patterns = [
            lambda x: x ^ 0x15,
            lambda x: (x + 47) % 256,
            lambda x: x ^ (x >> 3),
            lambda x: (x * 13) % 256
        ]
    
    def parse_arguments(self):
        """Parse les arguments de ligne de commande"""
        parser = argparse.ArgumentParser(
            description="MEME-FORGERY ENGINE v2.0 - Système avancé de forge mémétique",
            epilog="Exemple: python meme_forge.py -i input.jpg -a glitch -r ᚨ -g 3 --ar --news --output meme_result"
        )
        
        # Arguments principaux
        parser.add_argument("-i", "--input", help="Image source (URL ou chemin local)")
        parser.add_argument("-t", "--text", help="Texte personnalisé pour le mème")
        parser.add_argument("-a", "--archetype", choices=list(self.archetypes_config["archetypes"].keys()), 
                          help="Archétype mémétique à utiliser")
        parser.add_argument("-r", "--rune", help="Rune spécifique à incorporer")
        
        # Paramètres de traitement
        parser.add_argument("-g", "--glitch", type=int, choices=[1, 2, 3], default=2,
                          help="Niveau de glitch (1=subtle, 2=medium, 3=extreme)")
        parser.add_argument("--glitch-style", choices=list(self.channel_shift_lut.keys()), 
                          default="medium", help="Style d'effet glitch")
        
        # Fonctionnalités avancées
        parser.add_argument("--ar", action="store_true", help="Ajouter un QR code AR")
        parser.add_argument("--ar-url", help="URL personnalisée pour le QR code AR")
        parser.add_argument("--news", action="store_true", 
                          help="Générer basé sur l'actualité du jour")
        parser.add_argument("--batch", type=int, help="Générer un lot de N mèmes")
        parser.add_argument("--theme", help="Thème spécifique pour la génération")
        
        # Sortie
        parser.add_argument("-o", "--output", help="Préfixe du fichier de sortie")
        parser.add_argument("--format", choices=["png", "jpg", "webp"], default="png",
                          help="Format de sortie")
        parser.add_argument("--quality", type=int, default=85, 
                          help="Qualité pour JPEG/WEBP (1-100)")
        
        # Métadonnées
        parser.add_argument("--metadata", action="store_true", 
                          help="Générer un fichier JSON de métadonnées")
        parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
        
        return parser.parse_args()
    
    def load_image_source(self, source):
        """Charge une image depuis diverses sources"""
        if source.startswith('http'):
            if self.args.verbose:
                print(f"🌐 Chargement depuis URL: {source}")
            response = requests.get(source, timeout=10)
            return Image.open(BytesIO(response.content))
        else:
            if self.args.verbose:
                print(f"📁 Chargement depuis fichier: {source}")
            return Image.open(source)
    
    def apply_advanced_glitch(self, image, level, style):
        """Applique des effets glitch avancés"""
        img_array = np.array(image)
        
        # Application des patterns de data bending
        bending_pattern = random.choice(self.data_bending_patterns)
        bending_mask = np.random.random(img_array.shape[:2]) < 0.1
        img_array[bending_mask] = bending_pattern(img_array[bending_mask])
        
        # Décalage de canaux RGB
        shifts = self.channel_shift_lut[style]
        shift_x = random.randint(*shifts["x_shift"])
        shift_y = random.randint(*shifts["y_shift"])
        
        # Créer une version décalée
        shifted = np.roll(img_array, shift_x, axis=1)
        shifted = np.roll(shifted, shift_y, axis=0)
        
        # Fusion avec l'original selon le niveau
        alpha = level / 3.0
        glitched = (img_array * (1 - alpha) + shifted * alpha).astype(np.uint8)
        
        # Ajouter du bruit scanline
        if level >= 2:
            scanline_freq = random.randint(3, 8)
            for y in range(0, glitched.shape[0], scanline_freq):
                glitched[y:y+1] = glitched[y:y+1] ^ 0x30
        
        return Image.fromarray(glitched)
    
    def generate_archetypal_narrative(self, archetype, theme=None):
        """Génère un narrative basé sur l'archétype"""
        archetype_data = self.archetypes_config["archetypes"][archetype]
        
        if theme and theme in self.narratives_config.get("themes", {}):
            templates = self.narratives_config["themes"][theme]
        else:
            templates = self.narratives_config.get("templates", {}).get(archetype, [])
        
        if not templates:
            # Fallback templates
            templates = [
                "What if {concept} was never what we thought?",
                "The secret truth about {concept} they don't want you to know",
                "How {concept} is rewriting reality itself"
            ]
        
        concepts = self.narratives_config.get("concepts", ["reality", "consciousness", "time", "memory"])
        template = random.choice(templates)
        concept = random.choice(concepts)
        
        narrative = template.format(concept=concept, archetype=archetype)
        
        # Calcul du potentiel viral basé sur la complexité
        complexity = len(narrative) / 150
        virality = min(1.0, complexity * 0.6 + random.uniform(0.2, 0.4))
        
        return narrative, virality
    
    def get_current_news_headline(self):
        """Récupère un titre d'actualité du jour"""
        try:
            news_source = random.choice(self.sources_config.get("news_feeds", [
                "https://feeds.bbci.co.uk/news/rss.xml",
                "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
            ]))
            
            feed = feedparser.parse(news_source)
            if feed.entries:
                headline = random.choice(feed.entries[:10]).title
                return f"{headline} - or is this just a narrative glitch?"
        except:
            pass
        
        return "Reality is fracturing at the seams - are you paying attention?"
    
    def add_ar_qr_code(self, image, custom_url=None):
        """Ajoute un QR code de réalité augmentée"""
        if custom_url:
            ar_content = custom_url
        else:
            # Générer un contenu AR mystérieux
            ar_templates = [
                "https://example.com/ar/{}".format(hashlib.md5(str(random.random()).encode()).hexdigest()[:8]),
                "data:text/plain;base64,{}".format(quote("The truth is in the glitch")),
                "geo:{},{};u=10".format(random.uniform(48.0, 49.0), random.uniform(-1.0, 1.0))
            ]
            ar_content = random.choice(ar_templates)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=2,
        )
        qr.add_data(ar_content)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="white", back_color="black")
        
        # Redimensionner et positionner
        qr_size = min(image.width, image.height) // 6
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)
        
        # Position aléatoire mais visible
        pos_x = random.randint(20, image.width - qr_size - 20)
        pos_y = random.randint(20, image.height - qr_size - 20)
        
        image.paste(qr_img, (pos_x, pos_y))
        return image, ar_content
    
    def create_advanced_meme(self, args):
        """Crée un mème avancé avec toutes les fonctionnalités"""
        self.args = args
        
        # Charger l'image source
        if args.input:
            try:
                image = self.load_image_source(args.input)
            except:
                if args.verbose:
                    print("❌ Erreur chargement image, génération d'art glitch...")
                image = self.generate_glitch_art()
        else:
            image = self.generate_glitch_art()
        
        # Générer le narrative
        if args.text:
            narrative = args.text
        elif args.news:
            narrative = self.get_current_news_headline()
        else:
            narrative, virality = self.generate_archetypal_narrative(
                args.archetype or random.choice(list(self.archetypes_config["archetypes"].keys())),
                args.theme
            )
        
        # Appliquer les effets glitch
        if args.verbose:
            print(f"🎨 Application glitch niveau {args.glitch} ({args.glitch_style})...")
        
        image = self.apply_advanced_glitch(image, args.glitch, args.glitch_style)
        
        # Ajouter QR code AR si demandé
        ar_content = None
        if args.ar:
            if args.verbose:
                print("📱 Ajout QR code AR...")
            image, ar_content = self.add_ar_qr_code(image, args.ar_url)
        
        # Superposer le texte
        image = self.overlay_advanced_text(image, narrative, args.archetype)
        
        # Préparer les métadonnées
        rune_used = args.rune or random.choice(list(self.runes_config["runes"].keys()))
        rune_data = self.runes_config["runes"].get(rune_used, {})
        
        metadata = {
            "narrative": narrative,
            "archetype": args.archetype,
            "rune": rune_used,
            "rune_data": rune_data,
            "glitch_level": args.glitch,
            "glitch_style": args.glitch_style,
            "ar_content": ar_content,
            "timestamp": datetime.now().isoformat(),
            "version": "2.0",
            "generator": "MemeForge-Advanced"
        }
        
        return image, metadata
    
    def overlay_advanced_text(self, image, text, archetype):
        """Superpose du texte avec style avancé"""
        draw = ImageDraw.Draw(image)
        
        # Configuration du style basé sur l'archétype
        archetype_data = self.archetypes_config["archetypes"].get(archetype, {})
        colors = archetype_data.get("color_palette", ["#ffffff", "#ff0000", "#00ffff"])
        
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            except:
                font = ImageFont.load_default()
        
        # Préparer le texte avec wrapper
        max_width = image.width - 40
        lines = textwrap.wrap(text, width=30)
        
        # Position dynamique
        total_text_height = len(lines) * 35
        y_position = random.randint(20, image.height - total_text_height - 20)
        
        for i, line in enumerate(lines):
            # Effet de décalage glitch
            color = random.choice(colors)
            shadow_color = (0, 0, 0)
            
            # Multiple shadows pour effet glitch
            for offset_x, offset_y in [(2, 2), (-1, -1), (1, -1)]:
                draw.text((20 + offset_x, y_position + offset_y), line, shadow_color, font=font)
            
            draw.text((20, y_position), line, color, font=font)
            y_position += 35
        
        return image
    
    def generate_glitch_art(self, width=800, height=600):
        """Génère de l'art glitch algorithmique avancé"""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        # Pattern fractal complexe
        for x in range(width):
            for y in range(height):
                r = int(128 + 128 * np.sin(x * 0.01 + y * 0.005) * np.cos(y * 0.008))
                g = int(128 + 128 * np.sin(x * 0.015) * np.cos(y * 0.012 + x * 0.003))
                b = int(128 + 128 * np.sin(x * 0.008 + y * 0.01) * np.cos(y * 0.015))
                
                # Zones de corruption aléatoires
                if random.random() < 0.05:
                    corruption_type = random.choice(["shift", "invert", "noise"])
                    if corruption_type == "shift":
                        r, g, b = g, b, r
                    elif corruption_type == "invert":
                        r, g, b = 255 - r, 255 - g, 255 - b
                    else:
                        r = random.randint(0, 255)
                        g = random.randint(0, 255)
                        b = random.randint(0, 255)
                
                pixels[x, y] = (r, g, b)
        
        return image
    
    def save_results(self, image, metadata, args):
        """Sauvegarde l'image et les métadonnées"""
        # Générer le nom de fichier
        if args.output:
            base_name = args.output
        else:
            narrative_hash = hashlib.md5(metadata["narrative"].encode()).hexdigest()[:8]
            base_name = f"meme_{narrative_hash}"
        
        filename = f"{base_name}.{args.format}"
        
        # Sauvegarde de l'image
        save_kwargs = {}
        if args.format in ["jpg", "webp"]:
            save_kwargs["quality"] = args.quality
        
        image.save(filename, **save_kwargs)
        
        # Sauvegarde des métadonnées si demandé
        if args.metadata:
            metadata_file = f"{base_name}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return filename, metadata
    
    def batch_generate(self, count, args):
        """Génère un lot de mèmes"""
        results = []
        
        for i in range(count):
            if args.verbose:
                print(f"🔮 Génération mème {i+1}/{count}...")
            
            # Modifier légèrement les args pour chaque génération
            batch_args = argparse.Namespace(**vars(args))
            batch_args.output = f"{args.output or 'batch'}_{i+1}"
            batch_args.glitch = random.choice([1, 2, 3])
            batch_args.archetype = random.choice(list(self.archetypes_config["archetypes"].keys()))
            
            image, metadata = self.create_advanced_meme(batch_args)
            filename, _ = self.save_results(image, metadata, batch_args)
            
            results.append({
                "filename": filename,
                "metadata": metadata
            })
        
        return results

def main():
    forge = AdvancedMemeForge()
    args = forge.parse_arguments()
    
    print("""
    🧠 MEME-FORGERY ENGINE v2.0
    === Système Avancé de Forge Mémétique ===
    """)
    
    try:
        if args.batch:
            if args.verbose:
                print(f"🔮 Lancement génération de {args.batch} mèmes...")
            
            results = forge.batch_generate(args.batch, args)
            
            print(f"\n✅ Génération terminée ! {len(results)} mèmes créés:")
            for result in results:
                print(f"   📁 {result['filename']}")
                print(f"   📝 {result['metadata']['narrative'][:60]}...")
        
        else:
            if args.verbose:
                print("🔮 Création d'un mème unique...")
            
            image, metadata = forge.create_advanced_meme(args)
            filename, _ = forge.save_results(image, metadata, args)
            
            print(f"\n✅ Mème créé avec succès: {filename}")
            print(f"📝 Narrative: {metadata['narrative']}")
            print(f"🪶 Rune: {metadata['rune']} ({metadata['rune_data'].get('name', 'unknown')})")
            print(f"🎨 Glitch: niveau {metadata['glitch_level']} ({metadata['glitch_style']})")
            
            if metadata['ar_content']:
                print(f"📱 AR: {metadata['ar_content']}")
    
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
