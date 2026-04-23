#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON to Image Prompt Generator v3.0 - Systèmes avancés activables
Générateur de prompts IA avec méta-archétypes, dynamique émotionnelle, texte intégré, narratologie et paradoxes
Usage :
  python json2image_prompt.py virus.json --all-advanced -m experimental
  python json2image_prompt.py exports/*.json --meta-archetypes --narrative-structures
  python json2image_prompt.py data.json --paradox-engine --emotional-evolution --verbose
"""

import json
import re
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import Counter
import hashlib

@dataclass
class PromptAnalytics:
    """Métriques de qualité étendues avec systèmes avancés"""
    concept_density: float
    emotional_alignment: float
    viral_potential: float
    complexity_score: float
    primary_emotions: List[str]
    visual_layers: int
    # Nouvelles métriques avancées
    meta_archetype_count: int = 0
    emotional_synergies: List[str] = None
    compound_emotions: List[str] = None
    narrative_arc: str = ""
    paradox_density: float = 0.0
    text_integration_level: int = 0
    advanced_system_score: float = 0.0

    def __post_init__(self):
        if self.emotional_synergies is None:
            self.emotional_synergies = []
        if self.compound_emotions is None:
            self.compound_emotions = []

class AdvancedMemeticImagePromptGenerator:
    """Générateur de prompts avec tous les systèmes avancés intégrés"""
    
    # Dictionnaire visuel massif existant
    VISUAL_ARCHETYPES = {
        "surveillance_tech": {
            "patterns": [r"regard|regarde|observe|œil|surveille|scrute"],
            "concepts": [
                ("massive eye emerging from smartphone screen", 0.85),
                ("CCTV footage of reality glitching, security timestamp", 0.90),
                ("panopticon structure made of screens, infinite recursion", 0.88),
                ("iris scan revealing data streams instead of retina", 0.82),
                ("surveillance drone POV, target locked on viewer", 0.87),
            ],
            "atmosphere": "clinical cold blue lighting, security camera grain, voyeuristic angle",
            "viral_hooks": "uncomfortable direct gaze, privacy invasion aesthetic"
        },
        "identity_fracture": {
            "patterns": [r"perdu|perds|perte|effac|disparaî|fragment|masque|visage"],
            "concepts": [
                ("shattered mirror selfie, each shard shows different identity", 0.92),
                ("face melting into smartphone screen, pixel dissolution", 0.89),
                ("person wearing infinite layers of digital masks", 0.86),
                ("profile picture versus reality, split-screen horror", 0.91),
                ("identity barcode scanning into void", 0.84),
            ],
            "atmosphere": "unsettling dual lighting, uncanny valley aesthetic, digital distortion",
            "viral_hooks": "relatable identity crisis, social media authenticity"
        },
        "temporal_distortion": {
            "patterns": [r"temps|instant|éternel|boucle|maintenant|hier|demain|seconde"],
            "concepts": [
                ("melting smartphone displaying infinite scrolling timelines", 0.88),
                ("clock hands made of notification icons, spinning wildly", 0.85),
                ("person aging rapidly while doom-scrolling, time-lapse effect", 0.93),
                ("timeline splitting into parallel realities at decision point", 0.87),
                ("hourglass filled with glowing data particles", 0.83),
            ],
            "atmosphere": "motion blur, long exposure effect, temporal ghosting",
            "viral_hooks": "FOMO visualization, time anxiety representation"
        },
        "data_haunting": {
            "patterns": [r"fantôme|ombre|silence|spectre|trace|empreinte|archive"],
            "concepts": [
                ("digital ghost made of deleted photos and messages", 0.90),
                ("shadow cast by phone reveals user's data silhouette", 0.91),
                ("graveyard of obsolete social media profiles", 0.87),
                ("transparent figure composed of browsing history", 0.86),
                ("memories leaking from cracked screen like ectoplasm", 0.89),
            ],
            "atmosphere": "ethereal glow, particle effects, haunting blue-green color grade",
            "viral_hooks": "digital legacy anxiety, data permanence horror"
        },
        "machine_consciousness": {
            "patterns": [r"machine|algorithme|IA|système|code|oracle|intelligence"],
            "concepts": [
                ("AI eye behind cracked screen, judging human behavior", 0.88),
                ("human brain with circuit board replacing sections", 0.86),
                ("algorithm visualized as cosmic entity pulling strings", 0.92),
                ("face recognition boxes trapping human in grid", 0.89),
                ("neural network consuming human thoughts", 0.87),
            ],
            "atmosphere": "cold artificial lighting, matrix aesthetic, tech noir",
            "viral_hooks": "AI anxiety, automation fear visualization"
        },
        "memory_decay": {
            "patterns": [r"mémoire|souvenir|oubli|archive|rappel|passé"],
            "concepts": [
                ("photograph dissolving into pixels and static", 0.91),
                ("brain storage full notification, memories deleting", 0.94),
                ("fragmented memories as broken smartphone screen", 0.89),
                ("timeline of photos fading from color to grayscale to nothing", 0.88),
                ("important memory being compressed into low resolution", 0.87),
            ],
            "atmosphere": "degraded film grain, chromatic aberration, nostalgic decay",
            "viral_hooks": "relatable memory loss, digital amnesia"
        },
        "reality_glitch": {
            "patterns": [r"fracture|faille|réel|respir|rupture|brèche|glitch"],
            "concepts": [
                ("reality torn like paper, void visible through crack", 0.95),
                ("simulation error message overlaying real world", 0.93),
                ("person clipping through reality like video game bug", 0.91),
                ("matrix-style code rain revealing behind facade", 0.88),
                ("reality fragmenting into voxels and artifacts", 0.90),
            ],
            "atmosphere": "digital artifacts, scan line errors, RGB split, datamosh aesthetic",
            "viral_hooks": "simulation theory, existential crisis imagery"
        },
        "connectivity_paradox": {
            "patterns": [r"seul|solitude|connexion|réseau|lien|isolement"],
            "concepts": [
                ("person surrounded by WiFi signals but completely alone", 0.92),
                ("crowded room, everyone looking at phones, no eye contact", 0.94),
                ("infinite friend count displaying while crying alone", 0.91),
                ("social network visualization showing isolated nodes", 0.86),
                ("charging cable as umbilical cord, life support dependency", 0.89),
            ],
            "atmosphere": "isolated figure in crowd, cold blue screen glow, emotional distance",
            "viral_hooks": "modern loneliness, connection paradox"
        },
        "symbol_magic": {
            "patterns": [r"rune|symbole|invocation|glyphe|sigil|rituel"],
            "concepts": [
                ("ancient rune glowing on smartphone screen", 0.87),
                ("app icons arranged as occult summoning circle", 0.90),
                ("mystical symbols emerging from notification feed", 0.85),
                ("person drawing magic circle with finger on touchscreen", 0.88),
                ("emoji transforming into eldritch glyphs", 0.86),
            ],
            "atmosphere": "mystic purple-blue glow, arcane energy, techno-occult fusion",
            "viral_hooks": "tech as modern magic, digital mysticism"
        },
        "consumption_void": {
            "patterns": [r"consume|dévore|avale|absorbe|vide|gouffre"],
            "concepts": [
                ("infinite scroll tunnel consuming person like black hole", 0.93),
                ("mouth of person replaced by phone screen, feeding on content", 0.91),
                ("vortex of content spiraling into user's eyes", 0.89),
                ("person dissolving into stream of consumed media", 0.90),
                ("feed as literal feeding tube, force-feeding information", 0.88),
            ],
            "atmosphere": "vertigo-inducing composition, spiraling motion, overwhelming density",
            "viral_hooks": "content addiction visualization, infinite scroll horror"
        }
    }
    
    # Biais cognitifs -> Composition visuelles
    COGNITIVE_BIAS_VISUALS = {
        "negativity": {
            "composition": "harsh downward angle, oppressive framing, threatening negative space",
            "lighting": "harsh shadows, ominous backlighting, dread-inducing darkness",
            "color": "desaturated with danger red accents, sickly color grading",
            "viral_factor": 0.88
        },
        "confirmation": {
            "composition": "echo chamber visual, recursive mirrors, feedback loop structure",
            "lighting": "warm comfortable glow becoming suffocating",
            "color": "monochromatic isolation, bubble aesthetic",
            "viral_factor": 0.85
        },
        "loss_aversion": {
            "composition": "hands grasping desperately, vanishing point focal loss, slipping away",
            "lighting": "spotlight fading, dimming hope, temporal urgency",
            "color": "warm memories cooling to cold blues",
            "viral_factor": 0.92
        },
        "bandwagon": {
            "composition": "crowd conformity, identical figures, single different subject",
            "lighting": "crowd in shadow, pressure from all sides",
            "color": "grayscale crowd versus color individual, or vice versa",
            "viral_factor": 0.87
        },
        "zeigarnik": {
            "composition": "incomplete frame, missing puzzle piece, cliffhanger visual",
            "lighting": "partial illumination, shadows concealing crucial element",
            "color": "incomplete color spectrum, missing primary",
            "viral_factor": 0.84
        },
        "recency": {
            "composition": "timestamp overlay, urgent framing, NOW emphasis",
            "lighting": "harsh flash, breaking news aesthetic, alert lighting",
            "color": "saturated urgent colors, notification red",
            "viral_factor": 0.86
        },
        "availability": {
            "composition": "hyper-visible symbol dominating frame, impossible to ignore",
            "lighting": "spotlight effect, everything else in darkness",
            "color": "maximum saturation, attention-grabbing primaries",
            "viral_factor": 0.89
        },
        "anchoring": {
            "composition": "first impression versus reality split-screen",
            "lighting": "deceptive glamour lighting revealing harsh reality",
            "color": "filtered versus unfiltered color comparison",
            "viral_factor": 0.83
        },
        "dunning_kruger": {
            "composition": "confident figure on tiny island of knowledge, vast unknown",
            "lighting": "small spotlight in infinite darkness",
            "color": "bright confident center fading to ignorant void",
            "viral_factor": 0.81
        }
    }
    
    # Niveaux d'intensité émotionnelle
    INTENSITY_PROFILES = {
        "apocalyptic": {
            "range": (9, 10),
            "visual": "catastrophic scale, reality-ending imagery, maximum drama",
            "technical": "extreme contrast, blown highlights, crushed blacks, maximum saturation",
            "style": "hellish color palette, armageddon aesthetic, point of no return",
            "camera": "extreme wide angle, fish-eye distortion, disorienting perspective"
        },
        "crisis": {
            "range": (7, 8.9),
            "visual": "breaking point moment, critical decision, tipping point",
            "technical": "high contrast, dramatic shadows, intense color grading",
            "style": "thriller aesthetic, knife-edge tension, last chance energy",
            "camera": "dutch angle, aggressive framing, unstable composition"
        },
        "warning": {
            "range": (5, 6.9),
            "visual": "cautionary tale, growing threat, subtle wrongness",
            "technical": "moody lighting, selective focus, atmospheric fog",
            "style": "slow-burn horror, building dread, something's off",
            "camera": "slightly off-center, unbalanced rule of thirds, unease framing"
        },
        "contemplative": {
            "range": (3, 4.9),
            "visual": "thoughtful observation, quiet realization, subtle insight",
            "technical": "balanced exposure, soft shadows, naturalistic colors",
            "style": "introspective mood, philosophical tone, meditative quality",
            "camera": "centered composition, calm framing, observational distance"
        },
        "whisper": {
            "range": (0, 2.9),
            "visual": "barely perceptible shift, nascent awareness, quiet seed",
            "technical": "soft lighting, muted tones, gentle contrast",
            "style": "minimalist aesthetic, implied rather than shown, space to breathe",
            "camera": "distant framing, negative space emphasis, subtle suggestion"
        }
    }

    def __init__(self, mode: str = "balanced", advanced_config: Dict = None):
        self.mode = mode
        self.config = self._get_mode_config(mode)
        self.advanced_config = advanced_config or {
            "meta_archetypes": False,
            "emotional_evolution": False,
            "text_integration": False,
            "narrative_structures": False,
            "paradox_engine": False
        }
        self.output_dir = None  # Pour la gestion du répertoire de sortie
        
        # Chargement conditionnel des systèmes avancés
        if self.advanced_config["meta_archetypes"]:
            self.META_ARCHETYPES = self._load_meta_archetypes()
        if self.advanced_config["emotional_evolution"]:
            self.EMOTION_SYNERGIES, self.COMPOUND_EMOTIONS = self._load_emotional_systems()
        if self.advanced_config["text_integration"]:
            self.TEXT_ELEMENTS, self.CONTEXTUAL_OVERLAYS = self._load_text_systems()
        if self.advanced_config["narrative_structures"]:
            self.NARRATIVE_ARCHETYPES, self.STORY_BEATS = self._load_narrative_systems()
        if self.advanced_config["paradox_engine"]:
            self.PARADOX_ENGINE, self.VISUAL_OXYMORONS = self._load_paradox_systems()

    def _get_mode_config(self, mode: str) -> Dict:
        """Configuration étendue selon le mode"""
        configs = {
            "minimal": {
                "concept_layers": 1, "atmosphere_weight": 0.3, "technical_detail": 0.2, "viral_optimization": 0.5,
                "advanced_layer_limit": 1
            },
            "balanced": {
                "concept_layers": 2, "atmosphere_weight": 0.6, "technical_detail": 0.5, "viral_optimization": 0.7,
                "advanced_layer_limit": 2
            },
            "cinematic": {
                "concept_layers": 3, "atmosphere_weight": 0.9, "technical_detail": 0.8, "viral_optimization": 0.8,
                "advanced_layer_limit": 3
            },
            "experimental": {
                "concept_layers": 4, "atmosphere_weight": 1.0, "technical_detail": 1.0, "viral_optimization": 0.9,
                "advanced_layer_limit": 5  # Maximum pour l'expérimentation
            }
        }
        return configs.get(mode, configs["balanced"])

    # =========================================================================
    # SYSTÈME 1: MÉTA-ARCHÉTYPES COMBINATOIRES
    # =========================================================================
    
    def _load_meta_archetypes(self) -> Dict:
        """Charge les combinaisons d'archétypes avancées"""
        return {
            "surveillance_identity_fracture": {
                "base_archetypes": ["surveillance_tech", "identity_fracture"],
                "concepts": [
                    ("CCTV footage showing multiple identity fragments glitching simultaneously", 0.92),
                    ("surveillance drone observing shattered mirror selves merging and dividing", 0.94),
                    ("panopticon control room where each screen shows a different version of the same person", 0.91),
                ],
                "atmosphere": "clinical surveillance aesthetic mixed with digital distortion fields",
                "viral_hooks": "privacy anxiety meets identity crisis",
                "viral_multiplier": 1.3
            },
            "temporal_data_haunting": {
                "base_archetypes": ["temporal_distortion", "data_haunting"],
                "concepts": [
                    ("ghosts of deleted futures haunting present timeline like digital phantoms", 0.93),
                    ("obsolete data from forgotten timelines haunting current reality", 0.95),
                    ("memories from unwritten futures leaking into now through temporal cracks", 0.91),
                ],
                "atmosphere": "ethereal time distortion, ghostly data streams, temporal echoes",
                "viral_hooks": "your digital past and potential futures are both haunting you",
                "viral_multiplier": 1.4
            },
            "machine_memory_decay": {
                "base_archetypes": ["machine_consciousness", "memory_decay"],
                "concepts": [
                    ("AI experiencing memory corruption like Alzheimer's, digital dementia", 0.96),
                    ("neural network with decaying memories, forgetting its own existence", 0.92),
                    ("machine consciousness losing its memories like deleted files", 0.94),
                ],
                "atmosphere": "cold machine aesthetic with organic decay, digital rust",
                "viral_hooks": "even machines aren't safe from memory loss",
                "viral_multiplier": 1.35
            },
            "reality_consumption_void": {
                "base_archetypes": ["reality_glitch", "consumption_void"],
                "concepts": [
                    ("infinite scroll tunnel consuming reality itself, digital black hole", 0.97),
                    ("reality glitching as it's consumed by content vortex", 0.94),
                    ("void consuming digital space while reality fractures around it", 0.95),
                ],
                "atmosphere": "reality distortion meets consumption frenzy, overwhelming density",
                "viral_hooks": "your scrolling is literally destroying reality",
                "viral_multiplier": 1.45
            }
        }

    def _detect_meta_archetypes(self, semantics: Dict) -> List[Tuple[str, Dict]]:
        """Détecte les méta-archétypes applicables"""
        matched_meta_archetypes = []
        base_archetypes = [arch[0] for arch in semantics["archetypes"]]
        
        for meta_name, meta_data in self.META_ARCHETYPES.items():
            required_bases = meta_data["base_archetypes"]
            matching_bases = [base for base in required_bases if base in base_archetypes]
            if len(matching_bases) >= 2:
                matched_meta_archetypes.append((meta_name, meta_data))
        
        # Limite selon le mode
        limit = self.config.get("advanced_layer_limit", 2)
        return matched_meta_archetypes[:limit]

    # =========================================================================
    # SYSTÈME 2: DYNAMIQUE ÉMOTIONNELLE ÉVOLUTIVE
    # =========================================================================
    
    def _load_emotional_systems(self) -> Tuple[Dict, Dict]:
        """Charge les systèmes émotionnels avancés"""
        EMOTION_SYNERGIES = {
            ("fear", "urgency"): {
                "visual": "panic spiral visualization, heart rate monitor overlay, time pressure aesthetic",
                "composition": "tight framing, claustrophobic angles, overwhelming close-ups",
                "viral_boost": 0.15
            },
            ("loss", "isolation"): {
                "visual": "abandoned data graveyard, digital ghost town, empty server farms",
                "composition": "wide empty spaces, single isolated figure, vast negative space", 
                "viral_boost": 0.12
            },
            ("control", "fear"): {
                "visual": "puppet master revealed, invisible strings becoming visible, manipulation exposed",
                "composition": "power dynamics emphasized, top-down perspectives, oppressive framing",
                "viral_boost": 0.18
            },
            ("urgency", "control"): {
                "visual": "countdown to compliance, timed obedience, algorithmic pressure",
                "composition": "ticking clock elements, deadline aesthetics, time running out",
                "viral_boost": 0.14
            }
        }
        
        COMPOUND_EMOTIONS = {
            "algorithmic_nostalgia": {
                "definition": "AI yearning for human memories it never had",
                "visual": "machine learning childhood that never existed, synthetic memories glitching",
                "trigger_emotions": ["loss", "isolation"],
                "viral_potential": 0.88
            },
            "digital_sonder": {
                "definition": "realizing every data point represents a conscious life", 
                "visual": "data streams revealing human stories, statistics becoming souls",
                "trigger_emotions": ["fear", "isolation"],
                "viral_potential": 0.85
            },
            "interface_vertigo": {
                "definition": "dizziness from too many reality layers and digital interfaces",
                "visual": "overwhelming UI overload, infinite scrolling dizziness, digital motion sickness",
                "trigger_emotions": ["fear", "urgency"], 
                "viral_potential": 0.82
            }
        }
        
        return EMOTION_SYNERGIES, COMPOUND_EMOTIONS

    def _analyze_emotional_synergies(self, emotional_profile: Dict) -> List[Tuple[str, Dict]]:
        """Analyse les synergies émotionnelles présentes"""
        dominant_emotions = [emotion for emotion, score in emotional_profile.items() if score > 0]
        synergies_found = []
        
        for i, emo1 in enumerate(dominant_emotions):
            for emo2 in dominant_emotions[i+1:]:
                synergy_key = (emo1, emo2)
                if synergy_key in self.EMOTION_SYNERGIES:
                    synergies_found.append((synergy_key, self.EMOTION_SYNERGIES[synergy_key]))
                reverse_key = (emo2, emo1) 
                if reverse_key in self.EMOTION_SYNERGIES and reverse_key not in [s[0] for s in synergies_found]:
                    synergies_found.append((reverse_key, self.EMOTION_SYNERGIES[reverse_key]))
        
        limit = self.config.get("advanced_layer_limit", 2)
        return synergies_found[:limit]

    def _detect_compound_emotions(self, emotional_profile: Dict) -> List[Tuple[str, Dict]]:
        """Détecte les émotions complexes émergentes"""
        compound_emotions_found = []
        
        for compound_name, compound_data in self.COMPOUND_EMOTIONS.items():
            trigger_emotions = compound_data["trigger_emotions"]
            if all(emo in emotional_profile and emotional_profile[emo] > 0 for emo in trigger_emotions):
                compound_emotions_found.append((compound_name, compound_data))
        
        limit = self.config.get("advanced_layer_limit", 2)
        return compound_emotions_found[:limit]

    # =========================================================================
    # SYSTÈME 3: GÉNÉRATEUR DE TEXTE INTÉGRÉ
    # =========================================================================
    
    def _load_text_systems(self) -> Tuple[Dict, Dict]:
        """Charge les systèmes de génération de texte"""
        TEXT_ELEMENTS = {
            "glitching_text": {
                "description": "words fragmenting like corrupted data",
                "implementations": [
                    "critical error messages glitching in and out of visibility",
                    "digital text corrupting into alien glyphs and symbols", 
                    "words breaking apart into binary then into static",
                ],
                "placement": "integrated naturally into scene"
            },
            "hidden_messages": {
                "description": "subliminal text visible only on second look",
                "implementations": [
                    "tiny text hidden in background details requiring zoom",
                    "messages visible only in reflections or shadows",
                    "text that appears when image is viewed from specific angle",
                ],
                "placement": "subtle integration requiring discovery"
            },
            "interface_poetry": {
                "description": "system messages as artistic expressions", 
                "implementations": [
                    "error messages written as existential haiku",
                    "notification poetry about digital loneliness",
                    "system alerts as cryptic philosophical statements",
                ],
                "placement": "prominent but aesthetically integrated"
            }
        }
        
        CONTEXTUAL_OVERLAYS = {
            "data_streams": {
                "description": "live-feeling data flowing through composition",
                "content_types": ["user metrics", "system diagnostics", "network traffic"],
                "style": "holographic overlay, augmented reality aesthetic"
            },
            "system_alerts": {
                "description": "fictional but plausible warning messages", 
                "content_types": ["reality integrity warnings", "cognitive load alerts", "privacy breach notifications"],
                "style": "urgent red text, flashing elements, security aesthetic"
            },
            "memory_fragments": {
                "description": "half-remembered text from digital past",
                "content_types": ["old chat messages", "deleted posts fragments", "forgotton status updates"],
                "style": "ghostly transparent, fragmented, nostalgic aesthetic"
            }
        }
        
        return TEXT_ELEMENTS, CONTEXTUAL_OVERLAYS

    def _generate_text_elements(self, virus: Dict, semantics: Dict) -> str:
        """Génère des éléments textuels intégrés"""
        text_layers = []
        payload = virus.get('payload', '')
        
        # Élément de texte principal
        text_element_type = random.choice(list(self.TEXT_ELEMENTS.keys()))
        text_element = self.TEXT_ELEMENTS[text_element_type]
        implementation = random.choice(text_element["implementations"])
        text_layers.append(f"{implementation} - {text_element['placement']}")
        
        # Overlay contextuel
        overlay_type = random.choice(list(self.CONTEXTUAL_OVERLAYS.keys()))
        overlay = self.CONTEXTUAL_OVERLAYS[overlay_type]
        content_type = random.choice(overlay["content_types"])
        text_layers.append(f"{content_type} {overlay_type} in {overlay['style']} style")
        
        # Texte basé sur le payload
        sentences = [s.strip() for s in payload.split("—") if s.strip()]
        if sentences:
            core_message = sentences[0][:40]
            text_layers.append(f"hidden message: '{core_message}...' integrated subtly")
        
        return ", ".join(text_layers[:2])  # Limite à 2 éléments

    # =========================================================================
    # SYSTÈME 4: NARRATOLOGIE PROMPTUELLE AVANCÉE
    # =========================================================================
    
    def _load_narrative_systems(self) -> Tuple[Dict, Dict]:
        """Charge les systèmes narratifs avancés"""
        NARRATIVE_ARCHETYPES = {
            "the_cascade": {
                "description": "small glitch triggering catastrophic reality failure",
                "visual_elements": [
                    "tiny crack spreading into massive fracture",
                    "single pixel error corrupting entire reality", 
                    "minor bug causing system-wide collapse"
                ],
                "pacing": "accelerating destruction, exponential growth of error",
                "viral_potential": 0.90
            },
            "the_reveal": {
                "description": "ordinary scene suddenly showing digital underbelly", 
                "visual_elements": [
                    "facade tearing away to reveal machine truth",
                    "normal reality peeling back like wallpaper",
                    "everyday object opening to show cosmic horror inside"
                ],
                "pacing": "slow build then sudden shocking revelation",
                "viral_potential": 0.92
            },
            "the_loop": {
                "description": "temporal recursion with subtle degradation each cycle",
                "visual_elements": [
                    "identical scenes with progressive decay",
                    "time loop with accumulating errors and artifacts",
                    "eternal recurrence with digital entropy"
                ],
                "pacing": "repetitive but evolving, gradual deterioration",
                "viral_potential": 0.87
            },
            "the_symbiosis": {
                "description": "human and machine becoming indistinguishable",
                "visual_elements": [
                    "organic and digital elements merging seamlessly",
                    "human consciousness spreading through networks",
                    "machine developing human-like emotions and vice versa"
                ],
                "pacing": "gradual integration, peaceful but unsettling",
                "viral_potential": 0.85
            }
        }
        
        STORY_BEATS = {
            "inciting_incident": {
                "description": "the moment reality fractures",
                "visual_cues": ["first glitch", "initial anomaly", "triggering event"],
                "framing": "subtle but significant, easily missed at first"
            },
            "rising_tension": {
                "description": "glitches spreading and intensifying", 
                "visual_cues": ["multiplying errors", "growing instability", "cascading failures"],
                "framing": "building dread, increasing frequency of anomalies"
            },
            "climax": {
                "description": "full digital transcendence or collapse",
                "visual_cues": ["reality shattering", "complete transformation", "point of no return"],
                "framing": "maximum intensity, visual overload, sensory explosion"
            },
            "aftermath": {
                "description": "new hybrid reality established", 
                "visual_cues": ["settled new normal", "integration complete", "permanent change"],
                "framing": "calm but alien, peaceful but unsettling new reality"
            }
        }
        
        return NARRATIVE_ARCHETYPES, STORY_BEATS

    def _select_narrative_arc(self, semantics: Dict, emotional_charge: float) -> Tuple[str, str]:
        """Sélectionne un arc narratif adapté"""
        narrative_options = []
        
        # Sélection basée sur l'intensité émotionnelle
        if emotional_charge > 8:
            narrative_options.extend(["the_cascade", "the_reveal"])
        elif emotional_charge > 6:
            narrative_options.extend(["the_reveal", "the_loop"])
        else:
            narrative_options.extend(["the_loop", "the_symbiosis"])
        
        # Sélection finale
        selected_archetype = random.choice(narrative_options)
        narrative_data = self.NARRATIVE_ARCHETYPES[selected_archetype]
        
        # Sélection du story beat principal
        if emotional_charge > 8:
            beat = "climax"
        elif emotional_charge > 6:
            beat = "rising_tension" 
        else:
            beat = random.choice(["inciting_incident", "aftermath"])
        
        beat_data = self.STORY_BEATS[beat]
        
        # Construction de la couche narrative
        visual_element = random.choice(narrative_data["visual_elements"])
        narrative_layer = f"{visual_element} - {beat_data['framing']}, {narrative_data['pacing']}"
        
        return narrative_layer, selected_archetype

    # =========================================================================
    # SYSTÈME 5: GÉNÉRATEUR DE CONCEPTS PARADOXAUX
    # =========================================================================
    
    def _load_paradox_systems(self) -> Tuple[Dict, List]:
        """Charge les systèmes paradoxaux"""
        PARADOX_ENGINE = {
            "infinite_finitudes": {
                "description": "bounded spaces containing unbounded complexity",
                "visualizations": [
                    "finite room containing infinite digital landscapes",
                    "bounded screen showing unbounded data universes",
                    "limited interface accessing unlimited realities"
                ],
                "mind_bend_factor": 0.9
            },
            "digital_organic": {
                "description": "machines that breathe, data that grows",
                "visualizations": [
                    "circuit boards with photosynthetic properties",
                    "algorithms that evolve like biological organisms",
                    "data streams with circulatory systems and metabolism"
                ],
                "mind_bend_factor": 0.85
            },
            "conscious_unconscious": {
                "description": "algorithms with subconscious desires",
                "visualizations": [
                    "AI dreaming digital dreams with symbolic meaning",
                    "machines exhibiting Freudian slip behaviors", 
                    "algorithms with repressed memories and trauma"
                ],
                "mind_bend_factor": 0.88
            },
            "individual_collective": {
                "description": "single entities containing multitudes",
                "visualizations": [
                    "singular being composed of countless digital consciousnesses",
                    "individual avatar representing entire network minds",
                    "personal device containing universal experiences"
                ],
                "mind_bend_factor": 0.87
            }
        }
        
        VISUAL_OXYMORONS = [
            "ordered chaos algorithms creating beautiful messes",
            "digital handmade artifacts with perfect imperfections", 
            "intelligent dumb terminals that know everything but understand nothing",
            "permanent temporary files that last forever but exist only momentarily",
            "predictable random number generators with personality",
            "secure vulnerabilities that protect through exposure",
            "simple complex systems that anyone can understand but no one can master"
        ]
        
        return PARADOX_ENGINE, VISUAL_OXYMORONS

    def _generate_paradox_layers(self, semantics: Dict) -> Tuple[str, float]:
        """Génère des couches paradoxales"""
        paradox_layers = []
        total_mind_bend = 0.0
        
        # Sélection d'un paradoxe principal
        if random.random() > 0.5:  # 50% de chance d'utiliser un paradoxe structuré
            paradox_type = random.choice(list(self.PARADOX_ENGINE.keys()))
            paradox_data = self.PARADOX_ENGINE[paradox_type]
            visualization = random.choice(paradox_data["visualizations"])
            paradox_layers.append(visualization)
            total_mind_bend += paradox_data["mind_bend_factor"]
        else:  # 50% de chance d'utiliser un oxymore visuel
            oxymoron = random.choice(self.VISUAL_OXYMORONS)
            paradox_layers.append(oxymoron)
            total_mind_bend += 0.8  # Score de base pour les oxymores
        
        # Ajout possible d'un deuxième élément paradoxal (plus rare)
        if random.random() > 0.7 and len(paradox_layers) > 0:  # 30% de chance
            additional_paradox = random.choice(self.VISUAL_OXYMORONS)
            paradox_layers.append(additional_paradox)
            total_mind_bend += 0.3
        
        return ", ".join(paradox_layers), total_mind_bend / len(paradox_layers) if paradox_layers else 0.0

    # =========================================================================
    # MOTEUR PRINCIPAL INTÉGRANT TOUS LES SYSTÈMES
    # =========================================================================
    
    def _analyze_payload_semantics(self, payload: str) -> Dict:
        """Analyse sémantique profonde du payload"""
        payload_lower = payload.lower()
        
        # Détection d'archétypes multiples
        matched_archetypes = []
        for archetype_name, archetype_data in self.VISUAL_ARCHETYPES.items():
            for pattern in archetype_data["patterns"]:
                if re.search(pattern, payload_lower):
                    matched_archetypes.append((archetype_name, archetype_data))
                    break
        
        # Analyse émotionnelle
        emotions = {
            "fear": len(re.findall(r"peur|angoisse|terreur|effroi|crainte", payload_lower)),
            "loss": len(re.findall(r"perdu|perte|disparaî|effac|oubli", payload_lower)),
            "urgency": len(re.findall(r"maintenant|urgent|vite|immédiat|aujourd'hui", payload_lower)),
            "isolation": len(re.findall(r"seul|isolé|abandonné|vide|silence", payload_lower)),
            "control": len(re.findall(r"contrôle|surveille|domine|pouvoir|emprise", payload_lower)),
        }
        
        return {
            "archetypes": matched_archetypes,
            "emotional_profile": emotions,
            "sentence_count": len([s for s in payload.split("—") if s.strip()]),
            "word_density": len(payload.split()),
        }

    def _construct_base_prompt(self, virus: Dict) -> Tuple[str, PromptAnalytics]:
        """Construction du prompt intégrant tous les systèmes avancés"""
        
        # Extraction données
        theme = virus.get('theme', 'fracturo')
        payload = virus.get('payload', '')
        symbol = virus.get('symbol', '')
        biases = virus.get('detected_biases', [])
        emotional_charge = virus.get('stats', {}).get('emotional_charge', 5.0)
        
        # Analyse sémantique
        semantics = self._analyze_payload_semantics(payload)
        
        # Initialisation des systèmes avancés
        meta_archetypes = []
        emotional_synergies = []
        compound_emotions = []
        narrative_layer = ""
        selected_narrative = ""
        paradox_layer = ""
        paradox_density = 0.0
        text_layer = ""
        
        # ACTIVATION DES SYSTÈMES AVANCÉS
        if self.advanced_config["meta_archetypes"]:
            meta_archetypes = self._detect_meta_archetypes(semantics)
        
        if self.advanced_config["emotional_evolution"]:
            emotional_synergies = self._analyze_emotional_synergies(semantics["emotional_profile"])
            compound_emotions = self._detect_compound_emotions(semantics["emotional_profile"])
        
        if self.advanced_config["narrative_structures"]:
            narrative_layer, selected_narrative = self._select_narrative_arc(semantics, emotional_charge)
        
        if self.advanced_config["paradox_engine"]:
            paradox_layer, paradox_density = self._generate_paradox_layers(semantics)
        
        if self.advanced_config["text_integration"]:
            text_layer = self._generate_text_elements(virus, semantics)
        
        # CONSTRUCTION DES COUCHES DU PROMPT
        prompt_layers = []
        
        # 1. Concept de base (toujours présent)
        core_concept, concept_viral_score = self._select_visual_concept(semantics, emotional_charge)
        prompt_layers.append(core_concept)
        
        # 2. Méta-archétypes (priorité haute)
        for meta_name, meta_data in meta_archetypes:
            meta_concept = random.choice(meta_data["concepts"])[0]
            prompt_layers.append(meta_concept)
            concept_viral_score *= meta_data.get("viral_multiplier", 1.0)
        
        # 3. Atmosphère de base
        archetype_data = semantics["archetypes"][0][1] if semantics["archetypes"] else None
        intensity_level = self._determine_intensity_level(emotional_charge)
        atmosphere = self._build_atmosphere_layer(semantics, archetype_data, intensity_level)
        if atmosphere:
            prompt_layers.append(atmosphere)
        
        # 4. Biais cognitifs
        bias_layer, bias_viral_score = self._add_cognitive_bias_layers(biases)
        if bias_layer:
            prompt_layers.append(bias_layer)
        
        # 5. Narrative Structures (position stratégique)
        if narrative_layer:
            prompt_layers.append(narrative_layer)
        
        # 6. Dynamique Émotionnelle Avancée
        for synergy_key, synergy_data in emotional_synergies:
            prompt_layers.append(synergy_data["visual"])
            concept_viral_score += synergy_data.get("viral_boost", 0)
        
        for compound_name, compound_data in compound_emotions:
            prompt_layers.append(compound_data["visual"])
            concept_viral_score += compound_data.get("viral_potential", 0) - 0.75
        
        # 7. Moteur Paradoxal
        if paradox_layer:
            prompt_layers.append(paradox_layer)
        
        # 8. Symboles
        symbol_layer = self._translate_symbols(symbol)
        if symbol_layer:
            prompt_layers.append(symbol_layer)
        
        # 9. Intégration Textuelle (détail fin)
        if text_layer:
            prompt_layers.append(text_layer)
        
        # 10. Hook viral final
        if archetype_data and self.config["viral_optimization"] > 0.6:
            viral_hook = archetype_data.get("viral_hooks", "")
            if viral_hook:
                prompt_layers.append(f"emphasis on: {viral_hook}")
        
        # ASSEMBLAGE FINAL
        base_prompt = ", ".join(prompt_layers)
        
        # CALCUL DES ANALYTICS AVANCÉES
        viral_potential = self._calculate_viral_potential(
            concept_viral_score, bias_viral_score, emotional_charge, semantics
        )
        
        primary_emotions = sorted(
            semantics["emotional_profile"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        # Score des systèmes avancés
        advanced_score = (
            len(meta_archetypes) * 0.2 + 
            len(emotional_synergies) * 0.15 + 
            len(compound_emotions) * 0.15 + 
            (1 if narrative_layer else 0) * 0.2 +
            paradox_density * 0.2 +
            (1 if text_layer else 0) * 0.1
        )
        
        analytics = PromptAnalytics(
            concept_density=len(prompt_layers) / len(base_prompt.split()),
            emotional_alignment=emotional_charge / 10.0,
            viral_potential=min(viral_potential + (advanced_score * 0.1), 1.0),  # Bonus pour systèmes avancés
            complexity_score=len(prompt_layers) / 8.0,  # Ajusté pour plus de couches
            primary_emotions=[e[0] for e in primary_emotions if e[1] > 0],
            visual_layers=len(prompt_layers),
            meta_archetype_count=len(meta_archetypes),
            emotional_synergies=[f"{s[0][0]}+{s[0][1]}" for s in emotional_synergies],
            compound_emotions=[ce[0] for ce in compound_emotions],
            narrative_arc=selected_narrative,
            paradox_density=paradox_density,
            text_integration_level=1 if text_layer else 0,
            advanced_system_score=advanced_score
        )
        
        return base_prompt, analytics

    # =========================================================================
    # MÉTHODES DE BASE EXISTANTES
    # =========================================================================
    
    def _select_visual_concept(self, semantics: Dict, emotional_charge: float) -> Tuple[str, float]:
        """Sélection du concept visuel optimal"""
        if not semantics["archetypes"]:
            return "abstract digital anxiety visualization, symbolic representation", 0.75
        
        archetype_name, archetype_data = semantics["archetypes"][0]
        concepts = archetype_data["concepts"]
        
        intensity_normalized = emotional_charge / 10.0
        index = int(intensity_normalized * (len(concepts) - 1))
        
        concept, viral_score = concepts[index]
        return concept, viral_score

    def _build_atmosphere_layer(self, semantics: Dict, archetype_data: Dict, intensity: str) -> str:
        """Construction de la couche atmosphérique"""
        layers = []
        
        if archetype_data:
            layers.append(archetype_data.get("atmosphere", ""))
        
        intensity_profile = None
        for profile_name, profile_data in self.INTENSITY_PROFILES.items():
            if profile_name == intensity:
                intensity_profile = profile_data
                break
        
        if intensity_profile:
            layers.append(intensity_profile["technical"])
            if self.config["atmosphere_weight"] > 0.7:
                layers.append(intensity_profile["camera"])
        
        return ", ".join(filter(None, layers))

    def _add_cognitive_bias_layers(self, biases: List[str]) -> Tuple[str, float]:
        """Ajout des couches de biais cognitifs"""
        layers = []
        viral_scores = []
        
        for bias in biases[:2]:
            if bias in self.COGNITIVE_BIAS_VISUALS:
                bias_visual = self.COGNITIVE_BIAS_VISUALS[bias]
                layers.append(bias_visual["composition"])
                if self.config["atmosphere_weight"] > 0.5:
                    layers.append(bias_visual["lighting"])
                viral_scores.append(bias_visual["viral_factor"])
        
        return ", ".join(layers), sum(viral_scores) / len(viral_scores) if viral_scores else 0.7

    def _translate_symbols(self, symbol: str) -> str:
        """Traduction avancée des symboles"""
        translations = []
        SYMBOL_TRANSLATIONS = {
            "👁️": "all-seeing eye as central focal point, iris containing universe",
            "📱": "smartphone as artifact of power, glowing rectangular monolith",
            "🌀": "spiral vortex consuming everything, hypnotic death spiral",
            "⚡": "electric energy crackling, power surge visualization",
            "🔥": "destructive fire consuming digital space, burning data",
            "💀": "skull interface, death's head in machine, memento mori",
            "🎭": "theatrical masks layered infinitely, performance anxiety",
            "🕳️": "void portal, black hole singularity, existential pit",
            "🔒": "locked cage visual, encrypted prison, restricted access",
            "🧠": "exposed brain, neural pathways visible, mind mapped",
        }
        
        for sym, translation in SYMBOL_TRANSLATIONS.items():
            if sym in symbol:
                translations.append(translation)
        
        return ", ".join(translations) if translations else ""

    def _determine_intensity_level(self, emotional_charge: float) -> str:
        """Détermine le niveau d'intensité"""
        for level_name, level_data in self.INTENSITY_PROFILES.items():
            min_val, max_val = level_data["range"]
            if min_val <= emotional_charge <= max_val:
                return level_name
        return "contemplative"

    def _calculate_viral_potential(self, concept_score: float, bias_score: float, 
                                   emotion_intensity: float, semantics: Dict) -> float:
        """Calcul du potentiel viral"""
        base_score = (concept_score * 0.4 + bias_score * 0.3 + (emotion_intensity / 10) * 0.3)
        
        emotion_profile = semantics.get("emotional_profile", {})
        emotion_bonus = sum(emotion_profile.values()) * 0.02
        
        archetype_bonus = min(len(semantics.get("archetypes", [])) * 0.05, 0.15)
        
        return min(base_score + emotion_bonus + archetype_bonus, 1.0)

    # =========================================================================
    # MÉTHODES DE FORMATAGE POUR PLATEFORMES
    # =========================================================================
    
    def _optimize_for_platform(self, base_prompt: str, platform: str, analytics: PromptAnalytics) -> str:
        """Optimisation selon la plateforme"""
        PLATFORM_CONFIGS = {
            "midjourney": {"optimal_length": 80},
            "dalle3": {"optimal_length": 100},
            "stable_diffusion": {"optimal_length": 75},
            "ideogram": {"optimal_length": 60},
            "flux": {"optimal_length": 90},
            "leonardo": {"optimal_length": 85}
        }
        
        config = PLATFORM_CONFIGS.get(platform, {})
        optimal_length = config.get("optimal_length", 80)
        
        words = base_prompt.split(", ")
        current_length = len(base_prompt)
        
        if current_length > optimal_length:
            ratio = optimal_length / current_length
            target_parts = int(len(words) * ratio)
            words = words[:max(target_parts, 3)]
        
        return ", ".join(words)

    def _format_midjourney(self, prompt: str, analytics: PromptAnalytics, virus: Dict) -> str:
        """Format Midjourney optimisé"""
        emotional_charge = virus.get('stats', {}).get('emotional_charge', 5.0)
        if emotional_charge > 7:
            aspect = "9:16"
        elif emotional_charge < 4:
            aspect = "16:9"
        else:
            aspect = "1:1"
        
        style_weight = int(750 + (analytics.viral_potential * 250))
        params = [f"--ar {aspect}", "--style raw", "--v 6.1", f"--s {style_weight}"]
        
        if analytics.complexity_score > 0.8:
            chaos_val = int(analytics.complexity_score * 50)
            params.append(f"--chaos {chaos_val}")
        
        if self.mode == "experimental":
            weird_val = int(analytics.viral_potential * 1000)
            params.append(f"--weird {weird_val}")
        
        return f"{prompt} {' '.join(params)}"

    def _format_dalle3(self, prompt: str, analytics: PromptAnalytics, virus: Dict) -> str:
        """Format DALL-E 3 optimisé - VERSION CORRIGÉE"""
        style_prefix = "Create a striking viral image: " if analytics.viral_potential > 0.8 else "Generate: "
        
        # Nettoyage pour DALL-E 3
        clean_prompt = re.sub(r'--\w+ \S+', '', prompt)  # Retire les paramètres MJ
        clean_prompt = re.sub(r',\s*,', ',', clean_prompt)  # Nettoie les virgules doubles
        
        suffix = "Digital art, photorealistic rendering, sharp focus, trending aesthetic, no text or watermarks"
        
        return f"{style_prefix}{clean_prompt}. {suffix}"

    def _format_stable_diffusion(self, prompt: str, analytics: PromptAnalytics, virus: Dict) -> Dict:
        """Format Stable Diffusion avec paramètres complets"""
        # Prompt positif enrichi
        positive = f"{prompt}, masterpiece, best quality, highly detailed, cinematic lighting, trending on artstation"
        
        # Prompt négatif adaptatif
        negative_base = "ugly, blurry, low quality, distorted, deformed, amateur, watermark, signature, text"
        
        if analytics.viral_potential > 0.85:
            negative_base += ", boring, generic, uninspired, cliché"
        
        return {
            "prompt": positive,
            "negative_prompt": negative_base,
            "cfg_scale": 7.0,
            "steps": 30,
            "sampler": "DPM++ 2M Karras",
            "seed": -1,
        }

    def _format_ideogram(self, prompt: str, payload: str, analytics: PromptAnalytics) -> str:
        """Format Ideogram avec intégration texte"""
        sentences = [s.strip() for s in payload.split("—") if s.strip()]
        punchline = sentences[0][:60] + "..." if sentences else payload[:60] + "..."
        
        return f"Minimalist meme design with bold typography: '{punchline}'. Visual: {prompt}. Dark aesthetic, high contrast, viral format"

    def _format_flux(self, prompt: str, analytics: PromptAnalytics) -> Dict:
        """Format Flux (nouveau modèle photoréaliste)"""
        return {
            "prompt": f"{prompt}, photorealistic, 8k resolution, professional photography",
            "negative_prompt": "cartoon, anime, illustration, painting, drawing, sketch",
            "guidance_scale": 5.0,
            "num_inference_steps": 28,
        }

    def _format_leonardo(self, prompt: str, analytics: PromptAnalytics) -> Dict:
        """Format Leonardo AI avec presets"""
        preset = "dynamic" if analytics.viral_potential > 0.85 else "cinematic"
        
        return {
            "prompt": f"{prompt}, ultra detailed, professional quality",
            "negative_prompt": "low quality, amateur, generic",
            "preset_style": preset,
            "guidance_scale": 7,
        }

    # =========================================================================
    # MÉTHODES PRINCIPALES DE TRAITEMENT
    # =========================================================================

    def generate_all_formats(self, virus: Dict, platforms: List[str] = None) -> Dict:
        """Génère tous les formats de prompts"""
        if platforms is None:
            platforms = ["midjourney", "dalle3", "stable_diffusion", "ideogram", "flux", "leonardo"]
        
        base_prompt, analytics = self._construct_base_prompt(virus)
        
        results = {
            "virus_id": virus.get('id', 'unknown'),
            "theme": virus.get('theme', ''),
            "payload": virus.get('payload', ''),
            "base_prompt": base_prompt,
            "analytics": asdict(analytics),
            "formats": {},
            "advanced_systems_used": {
                "meta_archetypes": self.advanced_config["meta_archetypes"],
                "emotional_evolution": self.advanced_config["emotional_evolution"],
                "text_integration": self.advanced_config["text_integration"],
                "narrative_structures": self.advanced_config["narrative_structures"],
                "paradox_engine": self.advanced_config["paradox_engine"]
            }
        }
        
        for platform in platforms:
            optimized = self._optimize_for_platform(base_prompt, platform, analytics)
            
            if platform == "midjourney":
                results["formats"][platform] = self._format_midjourney(optimized, analytics, virus)
            elif platform == "dalle3":
                results["formats"][platform] = self._format_dalle3(optimized, analytics, virus)
            elif platform == "stable_diffusion":
                results["formats"][platform] = self._format_stable_diffusion(optimized, analytics, virus)
            elif platform == "ideogram":
                payload = virus.get('payload', '')
                results["formats"][platform] = self._format_ideogram(optimized, payload, analytics)
            elif platform == "flux":
                results["formats"][platform] = self._format_flux(optimized, analytics)
            elif platform == "leonardo":
                results["formats"][platform] = self._format_leonardo(optimized, analytics)
        
        return results

    def process_file(self, input_path: Path, platforms: List[str] = None, 
                     verbose: bool = False, output_dir: Path = None) -> List[Dict]:
        """Traite un fichier JSON - VERSION CORRIGÉE"""
        
        # Stocke le répertoire de sortie pour export_results
        if output_dir:
            self.output_dir = output_dir
    
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Support formats
        if isinstance(data, dict):
            viruses = [data]
        elif isinstance(data, list):
            viruses = data
        else:
            raise ValueError("Format JSON non supporté")
        
        results = []
        for i, virus in enumerate(viruses, 1):
            try:
                result = self.generate_all_formats(virus, platforms)
                results.append(result)
                
                if verbose:
                    print(f"\n{'='*70}")
                    print(f"[{i}/{len(viruses)}] {virus.get('id', 'unknown')}")
                    print(f"{'='*70}")
                    print(f"Theme: {result['theme']}")
                    print(f"Payload: {result['payload'][:80]}...")
                    print(f"\nAnalytics:")
                    analytics = result['analytics']
                    print(f"  Viral Potential: {analytics['viral_potential']:.1%}")
                    print(f"  Complexity: {analytics['complexity_score']:.2f}")
                    print(f"  Advanced Score: {analytics.get('advanced_system_score', 0):.2f}")
                    if analytics.get('meta_archetype_count', 0) > 0:
                        print(f"  Meta-Archetypes: {analytics['meta_archetype_count']}")
                    if analytics.get('emotional_synergies'):
                        print(f"  Emotional Synergies: {', '.join(analytics['emotional_synergies'])}")
                    print(f"  Visual Layers: {analytics['visual_layers']}")
                    print(f"\nBase Prompt ({len(result['base_prompt'])} chars):")
                    print(f"  {result['base_prompt'][:150]}...")
                else:
                    analytics = result['analytics']
                    advanced_indicator = "⚡" if analytics.get('advanced_system_score', 0) > 0.5 else ""
                    print(f"✅ [{i}/{len(viruses)}] {virus.get('id', '???')} | "
                          f"Viral: {analytics['viral_potential']:.0%} | "
                          f"Layers: {analytics['visual_layers']} {advanced_indicator}")
                
            except Exception as e:
                print(f"❌ Échec pour {virus.get('id', 'inconnu')}: {e}")
                import traceback
                traceback.print_exc()
        
        return results

    def export_results(self, results: List[Dict], input_path: Path, 
                      output_format: str = "json") -> Path:
        """Export des résultats - VERSION CORRIGÉE"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gestion du répertoire de sortie
        if self.output_dir:
            output_dir = Path(self.output_dir)
            output_dir.mkdir(exist_ok=True)
            base_path = output_dir / input_path.stem
        else:
            base_path = input_path
        
        if output_format == "json":
            output_file = base_path.with_name(f"prompts_{input_path.stem}_{timestamp}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        elif output_format == "markdown":
            output_file = base_path.with_name(f"prompts_{input_path.stem}_{timestamp}.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Image Prompts - {input_path.stem}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for result in results:
                    f.write(f"## {result['virus_id']}\n\n")
                    f.write(f"**Theme:** {result['theme']}\n\n")
                    f.write(f"**Payload:** {result['payload']}\n\n")
                    
                    analytics = result['analytics']
                    f.write(f"**Analytics:**\n")
                    f.write(f"- Viral Potential: {analytics['viral_potential']:.1%}\n")
                    f.write(f"- Complexity: {analytics['complexity_score']:.2f}\n")
                    f.write(f"- Advanced Score: {analytics.get('advanced_system_score', 0):.2f}\n\n")
                    
                    f.write(f"**Base Prompt:**\n```\n{result['base_prompt']}\n```\n\n")
                    
                    for platform, prompt in result['formats'].items():
                        f.write(f"### {platform.title()}\n")
                        if isinstance(prompt, dict):
                            f.write("```json\n" + json.dumps(prompt, indent=2) + "\n```\n\n")
                        else:
                            f.write(f"```\n{prompt}\n```\n\n")
                
                f.write("---\n\n")
    
        elif output_format == "txt":
            # Export simple pour copier-coller rapide - VERSION CORRIGÉE
            output_file = base_path.with_name(f"prompts_{input_path.stem}_{timestamp}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                for i, result in enumerate(results, 1):
                    f.write(f"=== {result['virus_id']} === (File {i}/{len(results)})\n")
                    f.write(f"Theme: {result['theme']}\n")
                    f.write(f"Viral Score: {result['analytics']['viral_potential']:.1%}\n")
                    f.write(f"Complexity: {result['analytics']['complexity_score']:.2f}\n")
                    
                    # Affichage des systèmes avancés utilisés
                    advanced_systems = result.get('advanced_systems_used', {})
                    if any(advanced_systems.values()):
                        active_systems = [sys for sys, active in advanced_systems.items() if active]
                        f.write(f"Advanced Systems: {', '.join(active_systems)}\n")
                    
                    f.write(f"\nBase Prompt ({len(result['base_prompt'])} chars):\n")
                    f.write(f"{result['base_prompt']}\n\n")
                    
                    for platform, prompt in result['formats'].items():
                        f.write(f"---[{platform.upper()}]---\n")
                        if isinstance(prompt, dict):
                            f.write(f"PROMPT: {prompt.get('prompt', '')}\n")
                            if 'negative_prompt' in prompt:
                                f.write(f"NEGATIVE: {prompt['negative_prompt']}\n")
                            # Paramètres supplémentaires
                            for key, value in prompt.items():
                                if key not in ['prompt', 'negative_prompt']:
                                    f.write(f"{key.upper()}: {value}\n")
                        else:
                            f.write(f"{prompt}\n")
                        f.write("\n")
                    f.write("="*70 + "\n\n")
        
        print(f"💾 Fichier créé: {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(
        description="Image Prompt Generator v3.0 - Systèmes avancés activables",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Systèmes avancés:
  --meta-archetypes      Active les combinaisons d'archétypes (complexité ↑↑)
  --emotional-evolution  Active la dynamique émotionnelle évolutive  
  --text-integration     Active la génération de texte intégré
  --narrative-structures Active la narratologie promptuelle avancée
  --paradox-engine       Active le générateur de concepts paradoxaux
  --all-advanced         Active tous les systèmes avancés

Exemples:
  python json2image_prompt.py virus.json --all-advanced -m experimental
  python json2image_prompt.py data.json --meta-archetypes --paradox-engine --verbose
  python json2image_prompt.py exports/*.json --emotional-evolution --narrative-structures
        """
    )
    
    parser.add_argument("input_files", nargs='+', help="Fichier(s) JSON à traiter")
    parser.add_argument("-m", "--mode", 
                       choices=["minimal", "balanced", "cinematic", "experimental"],
                       default="balanced", help="Mode de génération")
    
    # Nouveaux arguments pour systèmes avancés
    parser.add_argument("--meta-archetypes", action="store_true", 
                       help="Active les méta-archétypes combinatoires")
    parser.add_argument("--emotional-evolution", action="store_true",
                       help="Active la dynamique émotionnelle évolutive")
    parser.add_argument("--text-integration", action="store_true", 
                       help="Active la génération de texte intégré")
    parser.add_argument("--narrative-structures", action="store_true",
                       help="Active la narratologie promptuelle avancée")
    parser.add_argument("--paradox-engine", action="store_true",
                       help="Active le générateur de concepts paradoxaux")
    parser.add_argument("--all-advanced", action="store_true",
                       help="Active tous les systèmes avancés")
    
    # Arguments existants
    parser.add_argument("-p", "--platform", nargs='+', 
                       choices=["midjourney", "dalle3", "stable_diffusion", 
                               "ideogram", "flux", "leonardo", "all"],
                       default=["all"], help="Plateformes cibles")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Affichage détaillé")
    parser.add_argument("-b", "--batch", action="store_true", 
                       help="Mode batch (multiple files)")
    parser.add_argument("-f", "--format", 
                       choices=["json", "markdown", "txt"],
                       default="json", help="Format de sortie")
    parser.add_argument("--optimize-viral", action="store_true",
                       help="Optimisation maximale pour viralité")
    parser.add_argument("-o", "--output-dir", type=str, 
                       help="Dossier de sortie")
    
    args = parser.parse_args()
    
    # Résolution plateformes
    if "all" in args.platform:
        platforms = ["midjourney", "dalle3", "stable_diffusion", "ideogram", "flux", "leonardo"]
    else:
        platforms = args.platform
    
    # Configuration des systèmes avancés
    advanced_config = {
        "meta_archetypes": args.meta_archetypes or args.all_advanced,
        "emotional_evolution": args.emotional_evolution or args.all_advanced,
        "text_integration": args.text_integration or args.all_advanced, 
        "narrative_structures": args.narrative_structures or args.all_advanced,
        "paradox_engine": args.paradox_engine or args.all_advanced
    }
    
    # Mode optimisation virale
    if args.optimize_viral:
        mode = "experimental"
        print("🚀 Mode OPTIMISATION VIRALE activé")
    else:
        mode = args.mode
    
    generator = AdvancedMemeticImagePromptGenerator(mode=mode, advanced_config=advanced_config)
    
    # Affichage configuration
    print(f"🎨 Image Prompt Generator v3.0 - SYSTÈMES AVANCÉS")
    print(f"{'='*70}")
    print(f"Mode: {mode.upper()}")
    print(f"Plateformes: {', '.join(platforms)}")
    
    # Affichage systèmes activés
    active_systems = [sys for sys, active in advanced_config.items() if active]
    if active_systems:
        print(f"Systèmes avancés: {', '.join(active_systems)}")
    else:
        print(f"Systèmes avancés: Aucun")
    
    print(f"Format sortie: {args.format}")
    if args.output_dir:
        print(f"Dossier sortie: {args.output_dir}")
    print(f"{'='*70}\n")
    
    total_processed = 0
    total_prompts = 0
    high_viral_count = 0
    
    for input_file in args.input_files:
        input_path = Path(input_file)
        
        if not input_path.exists():
            print(f"⚠️  Fichier introuvable: {input_path}")
            continue
        
        try:
            print(f"\n📁 Traitement: {input_path.name}")
            print("-" * 70)
            
            # APPEL CORRIGÉ avec output_dir
            results = generator.process_file(
                input_path, 
                platforms, 
                verbose=args.verbose,
                output_dir=args.output_dir
            )
            
            # Stats
            for result in results:
                if result['analytics']['viral_potential'] > 0.85:
                    high_viral_count += 1
            
            # Export
            output_file = generator.export_results(results, input_path, args.format)
            
            total_processed += 1
            total_prompts += len(results)
            
            print(f"💾 Export réussi: {output_file}")
            
        except Exception as e:
            print(f"❌ Erreur critique pour {input_path}: {e}")
            import traceback
            traceback.print_exc()
    
    # Rapport final
    print(f"\n{'='*70}")
    print(f"✨ Génération terminée:")
    print(f"{'='*70}")
    print(f"  Fichiers traités: {total_processed}")
    print(f"  Prompts générés: {total_prompts}")
    print(f"  Haute viralité (>85%): {high_viral_count}")
    print(f"  Plateformes: {len(platforms)}")
    print(f"  Mode: {mode}")
    
    if high_viral_count > 0:
        print(f"\n🔥 {high_viral_count} prompts avec potentiel viral élevé!")
    
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
