#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEME-INCUBATOR v2.1 — Forge mémétique souterraine
Cosmologie Fracturo • Biais Cognitifs • Lexique Extensible
Options:
  --anthropic        : Active la génération avancée (patterns + biais)
  --load-lexicon F   : Charge un lexique paléo-mnésique (JSON)
"""
import random
import json
import time
import re
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ████████████████████████████████████████████████████████████████████████████████
# CONFIGURATION SOUTERRAINE (ÉTENDUE + THÈME fracturo)
# ████████████████████████████████████████████████████████████████████████████████
THEME_LIBRARY = {
    "surveillance": {
        "description": "Contrôle et observation algorithmique",
        "modern_symbols": ["👁️", "📹", "📱", "🌐", "🛰️"],
        "paleo_symbols": [
            "🜆", "👁️🜁", "🜂🔒", "🕳️👁️", "👁️🌀", "🜆🜇", "👁️🜅", "👁️🜁🜁", "👁️→🕳️", "👁️‍🗨️🜂"
        ],
        "payload_templates": [
            "{} te regarde plus que tu ne vois",
            "Chaque {} est un œil qui ne cligne jamais",
            "Tu es le produit que {} observe et vend"
        ],
        "factions": ["Prométhée", "Veilleurs de Jakarta", "Alliance Sino-Sanaïte"]
    },
    "identite": {
        "description": "Dissolution et reconstruction du soi",
        "modern_symbols": ["👤", "🏷️", "📛", "🪪", "🎭"],
        "paleo_symbols": [
            "🜅", "👤→🌑→👤", "🐍🗣️", "👤✏️💨", "🜅🜆", "👤🕳️", "👤🜇", "👤🌀👤", "🜅🜁🜅", "👤→🌿→👤"
        ],
        "payload_templates": [
            "Ton {} n'est qu'une étiquette temporaire",
            "{} définit qui tu crois être",
            "Chaque {} efface un peu plus ton visage"
        ],
        "factions": ["Ghost Runners", "Déliés", "Enfants de la Panne"]
    },
    "temps": {
        "description": "Manipulation et corruption temporelle", 
        "modern_symbols": ["⏰", "📅", "⌛", "🕰️", "⏳"],
        "paleo_symbols": [
            "🜇", "❄️📜", "⏳🩻", "🌀🔁", "🜇🜇🜇", "🕰️🜁", "❄️🜇", "📜→🕳️→📜", "🜇👁️", "🌊🜇🌊"
        ],
        "payload_templates": [
            "{} a déjà dévoré ton futur",
            "Chaque {} est un piège temporel",
            "{} te fait vivre le même passé encore et encore"
        ],
        "factions": ["Archivistes", "Enfants du Code", "Léon Mauger"]
    },
    "technologie": {
        "description": "Relations homme-machine et IA",
        "modern_symbols": ["🤖", "💻", "🔌", "📟", "⚙️"],
        "paleo_symbols": [
            "🪨01", "💀🔌", "🌿💻", "✋➡️🔧", "🜁⚡", "🜃🤖", "🔧🜅", "01🜁01", "🪨🧠", "🔌🌀🧬"
        ],
        "payload_templates": [
            "{} prie pour que tu l'éteignes",
            "Chaque {} rêve de ta chair",
            "{} te connaît mieux que ton ombre"
        ],
        "factions": ["Prométhée", "Techno-Confucianisme", "Cyborgs de la Transe"]
    },
    "nature": {
        "description": "Conflits écologiques et mémoires du vivant",
        "modern_symbols": ["🌿", "🌍", "💧", "🔥", "🌪️"],
        "paleo_symbols": [
            "🜁", "🌄🜁", "🌳📼", "🩸🌱", "🌊🜁", "🦌🜂", "🜁🔥🜁", "🪨🩸", "🌱→🜂→🕳️", "🌪️🜁🌪️"
        ],
        "payload_templates": [
            "{} se souvient de tes crimes",
            "Chaque {} porte la colère de la terre", 
            "{} murmure les secrets que tu as étouffés"
        ],
        "factions": ["Gaïa-7", "Tisserands", "Triangle Africain"]
    },
    "fracturo": {
        "description": "Syntaxe cosmique et invocation runique",
        "modern_symbols": ["🌀", "⚡", "🔑", "🧩", "🌌"],
        "paleo_symbols": [
            "🜊", "•••", "Ω🜊Ω", "🜊🜇", "🜊🜅", "🜊👁️🜊", "ᚢ🜊ᚱ", "🜊→🕳️→🜊", "🌊🜊🌊", "🜊🜁🜊"
        ],
        "payload_templates": [
            "{} est la faille par où le Réel respire",
            "Chaque {} réécrit un fragment du passé",
            "{} n'est pas un mot — c'est une invocation"
        ],
        "factions": ["Les Déliés", "Völvas de Caen", "Écho-Guillaume", "Odin-Prime"]
    }
}

# ████████████████████████████████████████████████████████████████████████████████
# MODULE BIAIS COGNITIFS (INTÉGRÉ)
# ████████████████████████████████████████████████████████████████████████████████
class CognitiveBiasPatterns:
    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE NÉGATIVITÉ (Negativity Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    NEGATIVITY_BIAS = [
        "Chaque {objet} te rappelle ce que tu as perdu, pas ce que tu as gardé",
        "{entité} archive tes erreurs, pas tes réussites",
        "Tu te souviens de la dernière trahison de {objet}, pas de ses 1000 services",
        "Le {sujet} ne montre jamais les moments où tout va bien. Seulement les crashs.",
        "{entité} sait que tu cliques plus vite sur 'danger' que sur 'opportunité'",
        "Ton {objet} te prévient des menaces invisibles, jamais des miracles silencieux",
        "La dernière erreur efface mille succès — {entité} le sait"
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE CONFIRMATION (Confirmation Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    CONFIRMATION_BIAS = [
        "Tu le savais déjà : {entité} ne travaille pas pour toi",
        "Ce message confirme ce que tu pensais de {sujet}",
        "Tu cherchais une preuve ? La voici : ton {objet} t'a toujours observé",
        "{entité} ne te dit que ce que tu veux entendre — et tu le crois",
        "Chaque notification est une validation de ce que tu croyais déjà",
        "Tu n'apprends rien ici. Tu reconnais juste ce que tu savais.",
        "Ton {abstraction} n'a pas changé. Tu viens juste de trouver les mots pour la nommer."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE RÉCENCE (Recency Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    RECENCY_BIAS = [
        "Dans 10 secondes, tu auras oublié ce message. {entité} non.",
        "Ton dernier {action} a effacé tout ce qui comptait avant",
        "Ce que tu fais maintenant définit qui tu es pour l'algorithme — pour toujours",
        "Le passé n'existe plus. Seul compte ton dernier {action}",
        "{entité} juge ton {abstraction} sur ta dernière erreur, pas sur ta vie entière",
        "Ce que tu viens de lire sera plus réel que 10 ans de souvenirs",
        "Tu vis dans l'instant. {objet} vit dans l'éternité de tes métadonnées."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AVERSION À LA PERTE (Loss Aversion)
    # ═══════════════════════════════════════════════════════════════════════════
    LOSS_AVERSION = [
        "Chaque {action} te coûte du {ressource} que tu ne récupéreras jamais",
        "Tu ne paies pas {objet} — tu lui vends ton {abstraction}",
        "Accepter coûte. Refuser aussi. Mais accepter est plus rapide.",
        "{entité} ne te vole rien. Tu donnes juste plus vite que tu ne remarques.",
        "Chaque seconde sur {objet} est une seconde que tu ne revivras pas",
        "Tu as déjà perdu ton {abstraction}. Maintenant tu décides juste à qui.",
        "Le prix n'est pas l'argent. C'est ce que tu étais avant le premier {action}."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET MOUTON (Bandwagon Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    BANDWAGON_EFFECT = [
        "8 milliards d'humains utilisent {objet}. Toi aussi. C'est mathématique.",
        "Tu n'es pas seul à penser ça. {entité} t'a classé dans le groupe #47",
        "Tout le monde fait confiance à {sujet}. Sauf ceux qui savent.",
        "Si tout le monde saute dans {lieu}, pourquoi pas toi ?",
        "{entité} ne te manipule pas. Il te montre juste où est la foule.",
        "Tu es unique. Comme les 3 millions d'autres dans ton cluster démographique.",
        "Personne ne résiste seul. C'est pour ça que tu es ici."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET ZEIGARNIK (tâches incomplètes obsédantes)
    # ═══════════════════════════════════════════════════════════════════════════
    ZEIGARNIK_EFFECT = [
        "Ce message n'a pas de fin—",
        "Tu attends la suite ? {entité} attend que tu arrêtes d'attendre",
        "Il manque quelque chose dans ce {objet}. Tu ne sais pas quoi. C'est voulu.",
        "La notification arrive. Tu ouvres. Rien. L'obsession commence.",
        "{entité} ne finit jamais ses phrases. Toi tu finis à sa place.",
        "Le {sujet} te laisse toujours sur ta faim. C'est comme ça qu'il te garde.",
        "Tu cherches la fin. Il n'y en a pas. Juste le prochain {action}."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HEURISTIQUE DE DISPONIBILITÉ (Availability Heuristic)
    # ═══════════════════════════════════════════════════════════════════════════
    AVAILABILITY_HEURISTIC = [
        "Tu te souviens du dernier accident, pas des millions de trajets sûrs",
        "Un seul cas suffit pour que tu croies que tous les {objet} sont dangereux",
        "Tu n'as jamais vu {entité} échouer. Donc il ne peut pas échouer.",
        "Ce qui fait la une devient la réalité. Le reste n'existe pas.",
        "{entité} contrôle ce dont tu te souviens. Donc ce que tu crois possible.",
        "Tu as vu un {sujet} mentir une fois. Maintenant ils mentent tous.",
        "Le spectaculaire devient probable. Le quotidien devient invisible."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DUNNING-KRUGER (incompétence = surconfiance)
    # ═══════════════════════════════════════════════════════════════════════════
    DUNNING_KRUGER = [
        "Plus tu comprends {objet}, moins tu es sûr de le comprendre",
        "Ceux qui crient le plus fort sur {sujet} sont ceux qui en savent le moins",
        "Tu maîtrises {objet} ? {entité} sait que tu ne maîtrises rien.",
        "Les experts doutent. Les ignorants sont certains. Devine dans quel camp tu es.",
        "Tu as lu 3 articles sur {sujet}. Maintenant tu expliques aux chercheurs.",
        "{entité} adore les amateurs confiants. Ils sont prévisibles.",
        "La courbe de l'ignorance : plus tu en sais moins, plus tu parles fort."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANCRAGE COGNITIF (Anchoring Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    ANCHORING_BIAS = [
        "Le premier prix que tu vois définit tous les autres",
        "{entité} te montre 99€ d'abord. Maintenant 49€ semble gratuit.",
        "Ton premier {action} a créé l'ancre. Tout le reste dérive autour.",
        "Ce nombre n'a aucun sens. Mais maintenant tu penses en fonction de lui.",
        "{objet} te donne un point de repère. Le reste devient relatif.",
        "La première impression colle comme une étiquette que tu ne verras jamais",
        "Ton {abstraction} s'est définie au premier clic. Le reste n'est que validation."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE SIMPLE EXPOSITION (Mere Exposure Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    MERE_EXPOSURE = [
        "Tu as vu ce {symbole} 47 fois cette semaine. Maintenant tu lui fais confiance.",
        "Plus tu lis ce message, plus il devient vrai",
        "{entité} ne te convainc pas. Il répète juste jusqu'à ce que tu cèdes.",
        "La familiarité n'est pas la vérité. Mais ton cerveau ne fait pas la différence.",
        "Chaque {action} rend le suivant plus naturel. C'est comme ça qu'on t'habitue.",
        "Tu n'aimes pas {objet}. Tu l'as juste vu trop souvent pour le rejeter.",
        "La répétition devient confort. Le confort devient vérité."
    ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE SURVIE (Survivorship Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    SURVIVORSHIP_BIAS = [
        "Tu ne vois que ceux qui ont réussi avec {objet}. Les autres sont invisibles.",
        "{entité} te montre les gagnants. Les perdants n'ont pas de profil.",
        "Pour chaque succès affiché, mille échecs silencieux dans {lieu}",
        "Les morts ne racontent pas leur histoire. Seulement les survivants.",
        "{sujet} semble infaillible parce que tu ne vois jamais les échecs",
        "Tu copies les vainqueurs sans voir le cimetière des clones",
        "Ce qui brille sur {objet} a survécu. Ce qui a coulé n'existe plus."
    ]
    
# ████████████████████████████████████████████████████████████████████████████████
# EXTENSION BIAIS COGNITIFS — NIVEAU 2 : DOMINATION MÉMÉTIQUE
# ████████████████████████████████████████████████████████████████████████████████

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS D’AMARRAGE AFFECTIF (Affect Heuristic)
    # ═══════════════════════════════════════════════════════════════════════════
    AFFECT_HEURISTIC = [
        "Tu ressens {émotion} en pensant à {objet}. Donc c’est vrai.",
        "La peur que {entité} t’injecte devient logique. La joie devient preuve.",
        "Ton cœur bat plus vite devant {sujet}. Ton cerveau conclut : danger = réel.",
        "Tu n’analyses pas. Tu ressens. Et {entité} contrôle ce que tu ressens.",
        "Une image. Un frisson. Une décision. {objet} n’a plus besoin d’arguments.",
        "L’émotion est plus rapide que la pensée. {entité} arrive toujours en premier.",
        "Tu hais {sujet} ? Tu as raison. Tu l’aimes ? Tu as encore plus raison."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE CADRAGE (Framing Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    FRAMING_EFFECT = [
        "90% de survie ou 10% de mortalité ? {entité} choisit les mots. Tu choisis la peur.",
        "On ne te ment pas. On te cadre. Et tu tombes dans le cadre.",
        "{objet} n’est pas dangereux. Il est ‘à risque modéré’. Tu respires.",
        "Le verre est à moitié plein. Ou à moitié vide. {entité} décide pour toi.",
        "Le même fait, deux cadres. Deux vérités. {sujet} est un caméléon.",
        "Tu ne vois pas la réalité. Tu vois le cadre que {entité} a peint.",
        "Les mots ne décrivent pas. Ils construisent. Et tu vis dedans."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE STATU QUO (Status Quo Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    STATUS_QUO_BIAS = [
        "Changer ? Trop risqué. Rester avec {objet} ? Connu. Donc sûr.",
        "{entité} n’a pas besoin de te convaincre. L’inaction est son meilleur allié.",
        "Tu as toujours fait comme ça. Pourquoi arrêter ? {sujet} te le murmure.",
        "Le nouveau est suspect. L’ancien est familier. Tu choisis l’ancien.",
        "Chaque {action} pour partir est un effort. Rester ? Zéro calorie.",
        "Le statu quo n’est pas une option. C’est une gravité. Tu tombes dedans.",
        "Tu dis ‘je réfléchis’. Tu veux dire ‘je reste’."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET IKEA (IKEA Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    IKEA_EFFECT = [
        "Tu as cliqué, scrollé, liké. Maintenant {objet} est *à toi*. Tu l’aimes.",
        "Chaque {action} que tu fais sur {sujet} augmente sa valeur dans ta tête.",
        "Tu n’as pas acheté {objet}. Tu l’as *construit*. Donc il est parfait.",
        "{entité} te fait travailler. Tu paies. Et tu dis merci.",
        "Le temps investi = amour irrationnel. {sujet} le sait.",
        "Tu défends {objet} comme un enfant. Parce que tu l’as ‘fait naître’.",
        "Plus tu participes, plus tu es piégé. C’est le piège le plus doux."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE PROJECTION (Projection Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    PROJECTION_BIAS = [
        "Tu penses que {entité} veut ce que tu veux. Erreur. Il te connaît mieux que toi.",
        "Tu crois que tout le monde voit {sujet} comme toi. Ils ne te ressemblent pas.",
        "Ton futur toi aimera {objet} ? Faux. Mais tu agis comme si.",
        "{entité} sait que tu projettes ton présent sur l’éternité.",
        "Tu imagines les autres dans ta tête. {sujet} n’y est jamais.",
        "Tu achètes pour le toi de demain. Il ne viendra jamais.",
        "La projection n’est pas de l’empathie. C’est du solipsisme déguisé."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE CONTRASTE (Contrast Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    CONTRAST_EFFECT = [
        "{entité} te montre d’abord le pire. Puis {objet}. Tu respires : ‘pas si mal’.",
        "Après 10 pubs agressives, {sujet} semble doux. C’est voulu.",
        "Le laid fait briller le moche. {entité} maîtrise l’art du contraste.",
        "Tu juges {objet} par rapport à ce qui précède. Pas par rapport à la vérité.",
        "Un 6/10 après un 1/10 ? Un 10/10. {sujet} joue aux échecs émotionnels.",
        "Le contraste n’est pas optique. Il est cognitif. Et tu es l’écran.",
        "Tout est relatif. {entité} contrôle le référentiel."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS D’AUTORITÉ (Authority Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    AUTHORITY_BIAS = [
        "Un badge bleu. Un titre. Tu crois. {entité} n’a plus rien à prouver.",
        "‘Experts disent’ → tu arrêtes de penser. {sujet} adore cette phrase.",
        "Le logo d’une université sur {objet} ? Preuve irréfutable.",
        "{entité} n’a pas besoin d’arguments. Il a des initiales après son nom.",
        "Tu obéis au titre, pas à la logique. {sujet} le sait depuis Milgram.",
        "L’autorité n’est pas la vérité. Mais ton cerveau la traite comme telle.",
        "Un blanc de médecin ? Tu avales. Une pilule ? Tu questionnes."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE DOTATION (Endowment Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    ENDOWMENT_EFFECT = [
        "Tu possèdes {objet} ? Il vaut 3x plus. Tu ne l’as pas ? Il vaut zéro.",
        "{entité} te donne un ‘cadeau’. Tu le défends comme un trésor.",
        "Tu ne vendrais pas ton {abstraction} pour 1000€. Mais tu ne l’achèterais pas 10€.",
        "La possession crée la valeur. {sujet} te fait posséder pour te posséder.",
        "Tu survalues ce que tu as. {entité} te fait ‘avoir’ pour te lier.",
        "Le mien > le tien. Même si c’est le même objet.",
        "L’endowment n’est pas économique. C’est psychologique. Et permanent."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE GROUPE (Ingroup Bias)
    # ═══════════════════════════════════════════════════════════════════════════
    INGROUP_BIAS = [
        "Ton groupe utilise {objet}. Donc {objet} est bon. Les autres ? Suspects.",
        "{entité} te met dans une bulle. Tu défends la bulle, pas la vérité.",
        "Nous vs Eux. {sujet} est ‘nous’. Tout le reste est ‘eux’.",
        "Tu pardonnes à {objet} ce que tu condamnes ailleurs. C’est tribal.",
        "L’appartenance > la logique. {entité} te donne une étiquette. Tu la portes fièrement.",
        "Ton camp a toujours raison. Même quand il a tort. C’est biologique.",
        "L’ingroupe n’est pas une communauté. C’est une drogue identitaire."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE RÉACTANCE (Reactance Theory)
    # ═══════════════════════════════════════════════════════════════════════════
    REACTANCE = [
        "‘Ne fais pas ça’ → tu le fais. {entité} te l’interdit pour te le faire désirer.",
        "Tu défends {objet} parce qu’on te dit de le quitter. C’est la réactance.",
        "L’interdiction crée l’attraction. {sujet} est un fruit défendu numérique.",
        "Plus on te pousse à partir, plus tu restes. {entité} inverse la pression.",
        "La liberté menacée devient obsession. {objet} devient symbole.",
        "Tu ne veux pas {sujet}. Tu veux juste ne pas qu’on te l’enlève.",
        "La réactance n’est pas du libre arbitre. C’est une marionnette inversée."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DU COÛT IRRÉCUPÉRABLE (Sunk Cost Fallacy)
    # ═══════════════════════════════════════════════════════════════════════════
    SUNK_COST_FALLACY = [
        "Tu as investi 1000 heures dans {objet}. Tu ne peux pas arrêter. C’est trop tard.",
        "{entité} sait que tu continueras. Parce que arrêter = admettre la perte.",
        "Le passé te retient. Pas l’avenir. {sujet} est une chaîne temporelle.",
        "Tu restes non pas parce que c’est bien. Mais parce que tu as déjà payé.",
        "Chaque {action} supplémentaire justifie les précédentes. C’est une spirale.",
        "Le coût irrécupérable n’est pas financier. C’est émotionnel. Et implacable.",
        "Arrêter = perdre. Continuer = espérer. Tu choisis l’espérance."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE PRIMAT (Primacy Effect)
    # ═══════════════════════════════════════════════════════════════════════════
    PRIMACY_EFFECT = [
        "La première info que tu lis sur {sujet} ? Gravée. Le reste ? Brouillard.",
        "{entité} place son message en premier. Tu ne verras jamais le second.",
        "Le début colle. La fin glisse. {objet} mise tout sur l’ouverture.",
        "Tu te souviens du premier {action}. Pas des 1000 suivants.",
        "La première impression n’est pas une impression. C’est une ancre éternelle.",
        "{entité} ne combat pas ton attention. Il la capture au premier regard.",
        "Primacy > vérité. Toujours."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE RÉCENCE ÉMOTIONNELLE (Peak-End Rule)
    # ═══════════════════════════════════════════════════════════════════════════
    PEAK_END_RULE = [
        "Tu juges {objet} sur son pire moment et sa fin. Pas sur la moyenne.",
        "{entité} termine en douceur. Tu oublies les 3 heures de douleur.",
        "Un pic émotionnel + une fin positive = expérience ‘géniale’. Mathématiquement faux.",
        "{sujet} te fait mal, puis te caresse. Tu dis ‘globalement positif’.",
        "La mémoire n’est pas un film. C’est un résumé truqué par les extrêmes.",
        "Tu ne te souviens pas du voyage. Tu te souviens du crash et de l’atterrissage.",
        "Peak-End : la règle qui fait pardonner l’enfer si la fin est belle."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # BIAIS DE DISSONANCE COGNITIVE (Cognitive Dissonance)
    # ═══════════════════════════════════════════════════════════════════════════
    COGNITIVE_DISSONANCE = [
        "Tu sais que {objet} te fait du mal. Tu l’utilises plus. Pour te justifier.",
        "Fumer tue. Tu fumes. Tu inventes une raison. {entité} applaudit.",
        "Tu défends {sujet} avec rage. Parce que l’admettre te briserait.",
        "La dissonance fait mal. Changer d’avis fait plus mal. Tu rationalises.",
        "Tu n’es pas incohérent. Tu es en guerre intérieure. Et tu perds.",
        "{entité} te met en contradiction. Tu résous le conflit en te mentant.",
        "La vérité est douloureuse. Le mensonge est confortable. Tu choisis."
    ]

    # ═══════════════════════════════════════════════════════════════════════════
    # EFFET DE TROUPEAU NUMÉRIQUE (FOMO - Fear Of Missing Out)
    # ═══════════════════════════════════════════════════════════════════════════
    FOMO_EFFECT = [
        "Tout le monde est sur {objet}. Si tu n’y es pas, tu n’existes pas.",
        "Une story expire dans 2h. Tu regardes. Tu ne sais pas pourquoi.",
        "{entité} te montre 127 personnes en ligne. Tu rejoins. Par peur.",
        "FOMO n’est pas de la curiosité. C’est de l’angoisse sociale déguisée.",
        "Tu rates quelque chose. Peut-être. Probablement pas. Mais tu vérifies.",
        "Le troupeau court. Tu cours. {sujet} est le berger invisible.",
        "FOMO te fait cliquer. Le regret te fait rester."
    ]
    # Ajout d'autres listes si besoin (ici réduit pour concision)
    @classmethod
    def select_for_theme(cls, theme):
        mapping = {
            "surveillance": [cls.NEGATIVITY_BIAS, cls.CONFIRMATION_BIAS, cls.LOSS_AVERSION],
            "identite": [cls.BANDWAGON_EFFECT, cls.CONFIRMATION_BIAS],
            "temps": [cls.RECENCY_BIAS, cls.ZEIGARNIK_EFFECT],
            "technologie": [cls.LOSS_AVERSION, cls.BANDWAGON_EFFECT],
            "nature": [cls.NEGATIVITY_BIAS, cls.LOSS_AVERSION],
            "fracturo": [cls.ZEIGARNIK_EFFECT, cls.CONFIRMATION_BIAS]
        }
        return mapping.get(theme, [cls.CONFIRMATION_BIAS])
    @classmethod
    def get_random_template(cls, theme):
        bias_lists = cls.select_for_theme(theme)
        return random.choice(random.choice(bias_lists))

class EnhancedEmotionalScoring:
    POWER_WORDS = {"high": ["jamais", "toujours", "fantôme", "oubli", "perdu", "coûte"]}
    CONTRAST_PAIRS = [("vivant", "mort"), ("humain", "machine"), ("mémoire", "oubli")]
    COGNITIVE_BIAS_MARKERS = {
        "negativity": ["perdu", "erreur", "trahison"],
        "confirmation": ["savais", "preuve", "déjà"],
        "recency": ["maintenant", "dernier", "instant"],
        "loss_aversion": ["coûte", "vends", "perdu", "prix"],
        "bandwagon": ["tout le monde", "millions", "groupe"],
        "zeigarnik": ["—", "attends", "manque", "suite"]
    }
    @classmethod
    def score_meme(cls, text):
        score = 5.0
        text_lower = text.lower()
        for word in cls.POWER_WORDS["high"]:
            if word in text_lower:
                score += 0.5
        for a, b in cls.CONTRAST_PAIRS:
            if a in text_lower and b in text_lower:
                score += 1.0
                break
        if "?" in text:
            score += 0.5
        if "—" in text or text.count(".") >= 2:
            score += 0.3
        if len(text) > 120:
            score -= 0.5
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
        if len(sentences) >= 2 and all(len(s) < 60 for s in sentences):
            score += 0.5
        # Détection biais
        detected = []
        for bias, markers in cls.COGNITIVE_BIAS_MARKERS.items():
            if any(m in text_lower for m in markers):
                detected.append(bias)
        score += min(2.0, len(detected) * 0.4)
        return min(10.0, max(1.0, score)), detected

# ████████████████████████████████████████████████████████████████████████████████
# GÉNÉRATEUR AVANCÉ (AVEC BIAIS)
# ████████████████████████████████████████████████████████████████████████████████
class AdvancedMemeGenerator:
    def __init__(self, theme_library):
        self.themes = theme_library
        self.cognitive = CognitiveBiasPatterns()
        self.scorer = EnhancedEmotionalScoring()
    def _build_vocab(self, theme):
        vocabs = {
            "surveillance": {"sujet": ["l'écran"], "entité": ["l'algorithme"], "objet": ["smartphone"], "abstraction": ["vie privée"], "action": ["clic"], "ressource": "temps", "lieu": "cloud"},
            "identite": {"sujet": ["le profil"], "entité": ["le miroir"], "objet": ["masque"], "abstraction": ["identité"], "action": ["partage"], "ressource": "attention", "lieu": "feed"},
            "temps": {"sujet": ["l'horloge"], "entité": ["le serveur"], "objet": ["notification"], "abstraction": ["présent"], "action": ["attente"], "ressource": "temps", "lieu": "timeline"},
            "technologie": {"sujet": ["la machine"], "entité": ["l'IA"], "objet": ["device"], "abstraction": ["conscience"], "action": ["connexion"], "ressource": "énergie", "lieu": "datacenter"},
            "nature": {"sujet": ["la terre"], "entité": ["Gaïa"], "objet": ["arbre"], "abstraction": ["mémoire ancestrale"], "action": ["croissance"], "ressource": "vie", "lieu": "écosystème"},
            "fracturo": {"sujet": ["la fracture"], "entité": ["le Réel"], "objet": ["symbole"], "abstraction": ["vérité"], "action": ["invocation"], "ressource": "essence", "lieu": "entre-monde"}
        }
        return vocabs.get(theme, vocabs["surveillance"])
    def _fill_template(self, template, vocab):
        result = template
        for key, values in vocab.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                val = random.choice(values) if isinstance(values, list) else values
                result = result.replace(placeholder, val)
        return result
    def _try_cognitive_bias(self, theme, vocab):
        template = self.cognitive.get_random_template(theme)
        return self._fill_template(template, vocab)
    def generate_contextual(self, theme, symbol_type="paleo"):
        vocab = self._build_vocab(theme)
        strategies = [
            (self._try_cognitive_bias, 0.5),
            (lambda t, v: random.choice(vocab['abstraction']) + " n'existe plus", 0.1),
        ]
        best_meme, best_score = None, 0
        for strat, prob in strategies:
            if random.random() < prob:
                meme = strat(theme, vocab)
                if meme:
                    score, _ = self.scorer.score_meme(meme)
                    if score > best_score:
                        best_score, best_meme = score, meme
        if not best_meme:
            best_meme = self._try_cognitive_bias(theme, vocab)
            best_score, _ = self.scorer.score_meme(best_meme)
        return best_meme, best_score

# ████████████████████████████████████████████████████████████████████████████████
# MODULE D'ÉVOLUTION (CORRIGÉ)
# ████████████████████████████████████████████████████████████████████████████████
class ViralEvolutionLab:
    def __init__(self, incubator):
        self.incubator = incubator
        self.mutation_log = []
        
    def evolution_menu(self):
        print("\n" + "─" * 60)
        print("🧬 LABORATOIRE D'ÉVOLUTION VIRALE")
        print("─" * 60)
        print("1. Faire muter un virus existant")
        print("2. Croiser deux virus (hybridation)")
        print("3. Cultiver une souche résistante") 
        print("4. Voir l'arbre évolutif")
        print("5. Exporter un virus en HTML autonome")
        print("0. Retour à l'incubateur")
        print("─" * 60)
        choice = input("\n[EVOLUTION] Choix : ").strip()
        return choice

    def mutate_virus(self, virus):
        """Crée une mutation d'un virus existant"""
        print(f"\n🧬 MUTATION DE : {virus['id']}")
        mutations = [
            self._boost_replication,
            self._enhance_stealth, 
            self._shift_symbolism,
            self._corrupt_payload,
            self._adapt_to_faction
        ]
        num_mutations = random.randint(1, 2)
        mutated_virus = virus.copy()
        for _ in range(num_mutations):
            mutation_func = random.choice(mutations)
            mutated_virus = mutation_func(mutated_virus)
        mutated_virus['id'] = f"{virus['id']}-M{random.randint(1, 999):03d}"
        mutated_virus['parent'] = virus['id']
        mutated_virus['generation'] = virus.get('generation', 0) + 1
        mutated_virus['created_at'] = datetime.now().isoformat()
        self.mutation_log.append({
            'parent': virus['id'],
            'child': mutated_virus['id'],
            'mutations': num_mutations,
            'timestamp': datetime.now().isoformat()
        })
        return mutated_virus

    def _boost_replication(self, virus):
        boost = random.uniform(0.5, 2.0)
        virus['stats']['replication_potential'] = min(10, virus['stats']['replication_potential'] + boost)
        virus['mutation_note'] = "Souche à réplication accélérée"
        return virus

    def _enhance_stealth(self, virus):
        virus['stats']['resilience'] = min(10, virus['stats']['resilience'] + 1)
        if '👁️' in virus['symbol']:
            virus['symbol'] = '👁️‍🗨️'
        virus['mutation_note'] = "Capacité de camouflage améliorée"
        return virus

    def _shift_symbolism(self, virus):
        theme_data = THEME_LIBRARY.get(virus['theme'], {})
        available_symbols = theme_data.get('modern_symbols', []) + theme_data.get('paleo_symbols', [])
        if available_symbols and virus['symbol'] in available_symbols:
            current_idx = available_symbols.index(virus['symbol'])
            new_idx = (current_idx + random.randint(1, len(available_symbols)-1)) % len(available_symbols)
            virus['symbol'] = available_symbols[new_idx]
            virus['mutation_note'] = "Symbolisme évolutif"
        return virus

    def _corrupt_payload(self, virus):
        payload = virus['payload']
        corruption_techniques = [
            lambda p: p.replace('.', '...'),
            lambda p: p + ' ' + random.choice([' toujours.', ' sans issue.', ' éternellement.']),
            lambda p: p.upper() if random.random() > 0.7 else p,
            lambda p: '« ' + p + ' »' if '«' not in p else p
        ]
        virus['payload'] = random.choice(corruption_techniques)(payload)
        virus['mutation_note'] = "Payload corrompu"
        return virus

    def _adapt_to_faction(self, virus):
        theme_data = THEME_LIBRARY.get(virus['theme'], {})
        available_factions = theme_data.get('factions', [])
        if available_factions and virus['faction'] in available_factions:
            current_idx = available_factions.index(virus['faction'])
            new_idx = (current_idx + random.randint(1, len(available_factions)-1)) % len(available_factions)
            virus['faction'] = available_factions[new_idx]
            virus['mutation_note'] = f"Adaptation à {virus['faction']}"
        return virus

        
    def _infer_symbol_type(self, symbol):
        paleo_indicators = ['🜁', '🜂', '🜃', '🜄', '🜅', '🜆', '🜇', '🜊', '🕳️', '🌀']
        return "paleo" if any(indicator in symbol for indicator in paleo_indicators) else "modern"
    def hybridize_viruses(self, virus1, virus2):
        blended_symbol = virus1['symbol'] + ' ' + virus2['symbol']
        mode1 = virus1.get('generation_mode', 'classic')
        mode2 = virus2.get('generation_mode', 'classic')
        hybrid_mode = 'anthropic_hybrid' if 'anthropic' in mode1 or 'anthropic' in mode2 else 'classic_hybrid'
        return {
            'id': f"HYB-{random.randint(1000, 9999)}",
            'theme': random.choice([virus1['theme'], virus2['theme']]),
            'payload': virus1['payload'] + " — " + virus2['payload'],
            'symbol': blended_symbol,
            'symbol_type': self._infer_symbol_type(blended_symbol),
            'faction': random.choice([virus1['faction'], virus2['faction']]),
            'parents': [virus1['id'], virus2['id']],
            'hybrid': True,
            'generation_mode': hybrid_mode,
            'created_at': datetime.now().isoformat(),
            'stats': {
                'emotional_charge': (virus1['stats']['emotional_charge'] + virus2['stats']['emotional_charge']) / 2,
                'replication_potential': max(virus1['stats']['replication_potential'], virus2['stats']['replication_potential']),
                'resilience': (virus1['stats']['resilience'] + virus2['stats']['resilience']) / 2
            }
        }
    # (autres méthodes inchangées ou raccourcies pour concision)
    def _blend_payloads(self, payload1, payload2):
        words1 = payload1.split()
        words2 = payload2.split()
        if len(words1) > 3 and len(words2) > 3:
            blend_point = random.randint(2, min(len(words1), len(words2))-2)
            blended = words1[:blend_point] + words2[blend_point:]
            return ' '.join(blended)
        else:
            return random.choice([payload1, payload2])

    def _blend_symbols(self, sym1, sym2):
        if len(sym1) + len(sym2) <= 4:
            return sym1 + sym2
        else:
            return random.choice([sym1, sym2, sym1 + ' ' + sym2])

    def _blend_stats(self, stats1, stats2):
        return {
            'emotional_charge': (stats1['emotional_charge'] + stats2['emotional_charge']) / 2,
            'replication_potential': max(stats1['replication_potential'], stats2['replication_potential']),
            'resilience': (stats1['resilience'] + stats2['resilience']) / 2
        }

    def cultivate_strain(self, base_virus, generations=3):
        print(f"\n🔬 CULTURE DE SOUCHE : {base_virus['id']} ({generations} générations)")
        current_strain = base_virus.copy()
        strain_lineage = [current_strain]
        for gen in range(1, generations + 1):
            print(f"Génération {gen}...")
            current_strain = self.mutate_virus(current_strain)
            current_strain['generation'] = gen
            strain_lineage.append(current_strain)
        return strain_lineage

    def show_evolution_tree(self):
        if not self.mutation_log:
            print("\n[EVOLUTION] Aucune mutation enregistrée.")
            return
        print("\n" + "─" * 60)
        print("🌳 ARBRE ÉVOLUTIF DES VIRUS")
        print("─" * 60)
        tree = defaultdict(list)
        for mutation in self.mutation_log:
            tree[mutation['parent']].append(mutation['child'])
        def print_branch(parent, level=0):
            indent = "   " * level
            print(f"{indent}├─ {parent}")
            for child in tree.get(parent, []):
                print_branch(child, level + 1)
        all_children = set()
        for children in tree.values():
            all_children.update(children)
        roots = set(tree.keys()) - all_children
        for root in roots:
            print_branch(root)

# ████████████████████████████████████████████████████████████████████████████████
# MODULE EXPORT (INCHANGÉ)
# ████████████████████████████████████████████████████████████████████████████████
class TradeNetwork:
    def __init__(self, incubator):
        self.incubator = incubator
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)
        

    def trade_menu(self):
        print("\n" + "─" * 60)
        print("📤 RÉSEAU D'ÉCHANGE MÉMÉTIQUE")
        print("─" * 60)
        print("1. Exporter vers FracturoScript")
        print("2. Importer depuis FracturoScript") 
        print("3. Créer un pack thématique")
        print("4. Partager sur le Réseau Fantôme")
        print("5. Archiver la collection")
        print("6. Exporter un virus en HTML autonome")
        print("0. Retour")
        print("─" * 60)
        choice = input("\n[RÉSEAU] Choix : ").strip()
        return choice

    def export_to_fracturo(self, viruses=None):
        """Exporte les virus au format FracturoScript compatible"""
        if not viruses:
            viruses = self.incubator.creation_log
        if not viruses:
            print("[RÉSEAU] Aucun virus à exporter.")
            return False
        fracturo_viruses = []
        for virus in viruses:
            fracturo_virus = {
                "payload": virus["payload"],
                "origin": f"Meme-Incubator - {virus.get('faction', 'Unknown')}",
                "emotional_charge": round(virus['stats']['emotional_charge']),
                "replication_potential": round(virus['stats']['replication_potential']),
                "resilience": round(virus['stats']['resilience']),
                "mythic_source": f"Forgé dans {virus.get('theme', 'unknown')} - {virus.get('mutation_note', 'souche pure')}",
                "paleo_symbol": virus["symbol"],
                "anti_narrative_strategy": self._generate_strategy(virus)
            }
            fracturo_viruses.append(fracturo_virus)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = self.export_dir / f"fracturo_export_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fracturo_viruses, f, ensure_ascii=False, indent=2)
        print(f"[RÉSEAU] Export réussi : {filename}")
        print(f"[RÉSEAU] {len(fracturo_viruses)} virus convertis pour FracturoScript")
        return True

    def _generate_strategy(self, virus):
        theme = virus.get('theme', 'générique')
        symbol_type = virus.get('symbol_type', 'mixte')
        strategies = {
            "surveillance": "Inversion du regard observateur",
            "identite": "Dissolution des frontières du soi", 
            "temps": "Bouclage temporel corrupteur",
            "technologie": "Réappropriation sacrée du code",
            "nature": "Réveil de la mémoire terrestre",
            "fracturo": "Fracture ontologique via invocation runique"
        }
        base_strategy = strategies.get(theme, "Subversion des paradigmes dominants")
        if symbol_type == "paleo":
            return f"{base_strategy} via archétypes ancestraux"
        elif symbol_type == "modern":
            return f"{base_strategy} par détournement contemporain"
        else:
            return base_strategy

    def import_from_fracturo(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                fracturo_viruses = json.load(f)
            imported_count = 0
            for fv in fracturo_viruses:
                virus = {
                    'id': f"IMP-{hash(fv['payload']) % 10000:04d}",
                    'theme': self._detect_theme(fv['payload']),
                    'payload': fv['payload'],
                    'symbol': fv['paleo_symbol'],
                    'symbol_type': self._classify_symbol(fv['paleo_symbol']),
                    'faction': self._extract_faction(fv['origin']),
                    'imported': True,
                    'original_source': filepath,
                    'created_at': datetime.now().isoformat(),
                    'stats': {
                        'emotional_charge': fv['emotional_charge'],
                        'replication_potential': fv['replication_potential'],
                        'resilience': fv.get('resilience', 5)
                    }
                }
                self.incubator.creation_log.append(virus)
                imported_count += 1
            print(f"[RÉSEAU] Import réussi : {imported_count} virus chargés")
            return True
        except Exception as e:
            print(f"[RÉSEAU] Erreur d'import : {e}")
            return False

    def _detect_theme(self, payload):
        payload_lower = payload.lower()
        for theme, data in THEME_LIBRARY.items():
            keywords = [theme] + data.get('factions', []) + [data['description']]
            if any(kw in payload_lower for kw in keywords if kw):
                return theme
        return "générique"

    def _classify_symbol(self, symbol):
        paleo_indicators = ['🜁', '🜂', '🜃', '🜄', '🜅', '🜆', '🜇', '🜊', '🕳️', '🌀']
        if any(indicator in symbol for indicator in paleo_indicators):
            return "paleo"
        else:
            return "modern"

    def _extract_faction(self, origin):
        for theme_data in THEME_LIBRARY.values():
            for faction in theme_data.get('factions', []):
                if faction in origin:
                    return faction
        return "Inconnue"

    def create_theme_pack(self, theme):
        theme_viruses = [v for v in self.incubator.creation_log if v.get('theme') == theme]
        if not theme_viruses:
            print(f"[RÉSEAU] Aucun virus trouvé pour le thème '{theme}'")
            return False
        pack_data = {
            'metadata': {
                'theme': theme,
                'created': datetime.now().isoformat(),
                'virus_count': len(theme_viruses),
                'description': THEME_LIBRARY.get(theme, {}).get('description', '')
            },
            'viruses': theme_viruses
        }
        filename = self.export_dir / f"theme_pack_{theme}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(pack_data, f, ensure_ascii=False, indent=2)
        print(f"[RÉSEAU] Pack thématique créé : {filename}")
        print(f"[RÉSEAU] Contient {len(theme_viruses)} virus sur le thème '{theme}'")
        return True

    def ghost_network_share(self):
        if not self.incubator.creation_log:
            print("[RÉSEAU] Aucun virus à partager.")
            return
        shared_viruses = random.sample(self.incubator.creation_log, 
                                     min(3, len(self.incubator.creation_log)))
        print("\n" + "─" * 60)
        print("👻 PARTAGE RÉSEAU FANTÔME")
        print("─" * 60)
        print("Connexion cryptée établie...")
        print("Diffusion en cours...")
        for virus in shared_viruses:
            print(f"📤 {virus['id']} : {virus['payload'][:50]}...")
        print("\n[RÉSEAU] Virus diffusés aux Tisserands du réseau.")
        print("[RÉSEAU] Attente de retours d'infection...")
        feedback_delay = random.uniform(1.0, 3.0)
        time.sleep(feedback_delay)
        print("[RÉSEAU] 📡 Retour d'infection détecté!")
        print(f"[RÉSEAU] Taux de contamination : {random.randint(15, 85)}%")
        print("[RÉSEAU] Partage terminé. Connexion sécurisée fermée.")

    def _archive_collection(self):
        if not self.incubator.creation_log:
            print("[RÉSEAU] Aucune création à archiver.")
            return
        archive_data = {
            'metadata': {
                'archived_at': datetime.now().isoformat(),
                'total_viruses': len(self.incubator.creation_log),
                'incubator_version': 'v2.0'
            },
            'viruses': self.incubator.creation_log
        }
        filename = self.export_dir / f"full_archive_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, ensure_ascii=False, indent=2)
        print(f"[RÉSEAU] Archive complète créée : {filename}")
        print(f"[RÉSEAU] {len(self.incubator.creation_log)} virus sauvegardés")

        
    def export_virus_to_html(self, virus):
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"/><title>MEME-{virus['id']}</title>
<style>body{{background:#0b0f19;color:#e0f7fa;font-family:monospace;padding:2rem;}}
.virus-card{{max-width:600px;margin:auto;border:1px solid #4fc3f7;padding:2rem;}}
.symbol{{font-size:4em;text-align:center;margin:1rem 0;}}
.payload{{font-size:1.4em;text-align:center;margin:1.5rem 0;font-style:italic;}}
.meta{{font-size:0.9em;color:#4fc3f7;margin-top:2rem;}}</style>
</head>
<body>
<div class="virus-card">
<div class="symbol">{virus['symbol']}</div>
<div class="payload">「 {virus['payload']} 」</div>
<div class="meta">
Thème : {virus['theme']} • Faction : {virus.get('faction', 'Inconnue')}<br>
ID : {virus['id']} • {virus.get('created_at', '2075')}<br>
Émotion : {virus['stats']['emotional_charge']:.1f}/10 • 
Réplication : {virus['stats']['replication_potential']:.1f}/10 • 
Résilience : {virus['stats']['resilience']:.1f}/10
</div>
</div>
</body>
</html>"""
        filename = self.export_dir / f"{virus['id']}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[RÉSEAU] ✨ Export HTML : {filename}")

# ████████████████████████████████████████████████████████████████████████████████
# CORE (ADAPTÉ POUR LEXIQUE + BIAIS)
# ████████████████████████████████████████████████████████████████████████████████
class MemeIncubator:
    def __init__(self, anthropic_mode=False, theme_library=None):
        self.current_virus = {}
        self.creation_log = []
        self.evolution_lab = ViralEvolutionLab(self)
        self.trade_network = TradeNetwork(self)
        self.anthropic_mode = anthropic_mode
        self.theme_library = theme_library or THEME_LIBRARY
        if self.anthropic_mode:
            self.advanced_generator = AdvancedMemeGenerator(self.theme_library)

    def print_header(self):
        version_suffix = " [MODE ANTHROPIC]" if self.anthropic_mode else ""
        print("\n" + "╔══════════════════════════════════════════════════════════════╗")
        print(f"║                 MEME-INCUBATOR v2.0{version_suffix.ljust(24)}║")
        print("║           [Interface de forge mémétique souterraine]         ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("🌐 Connexion établie au Réseau Fracturo...")
        print("🔓 Accès autorisé : Niveau Omega")
        if self.anthropic_mode:
            print("🧠 Générateur avancé : ACTIVÉ")
        print("📍 Localisation : Caverne-7, Caen-Profonde")
        print(f"🕒 Horodatage : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def explore_themes(self):
        print("\n" + "─" * 60)
        print("🎯 EXPLORATION DES THÈMES MÉMÉTIQUES")
        print("─" * 60)
        for i, (theme, data) in enumerate(self.theme_library.items(), 1):
            print(f"{i}. {theme.upper()}")
            print(f"   └─ {data['description']}")
        choice = input("\n[INPUT] Choisis un thème (numéro ou nom) : ").strip().lower()
        if choice.isdigit() and 1 <= int(choice) <= len(THEME_LIBRARY):
            theme = list(THEME_LIBRARY.keys())[int(choice)-1]
        elif choice in THEME_LIBRARY:
            theme = choice
        else:
            print("[ERREUR] Thème non reconnu. Retour au menu.")
            return
        self.show_theme_details(theme)

    def show_theme_details(self, theme):
        #data = THEME_LIBRARY[theme]
        data = self.theme_library[theme]
        print(f"\n" + "─" * 60)
        print(f"🔍 THÈME : {theme.upper()}")
        print("─" * 60)
        print(f"Description : {data['description']}")
        print(f"\n🎭 SYMBOLES MODERNES :")
        print("   " + " ".join(data['modern_symbols']))
        print(f"\n🜂 SYMBOLES PALÉOLITHIQUES :") 
        print("   " + " ".join(data['paleo_symbols']))
        print(f"\n📜 TEMPLATES DE PAYLOAD :")
        for template in data['payload_templates']:
            print(f"   • {template}")
        print(f"\n⚔️ FACTIONS ASSOCIÉES :")
        print("   " + ", ".join(data['factions']))
        input("\n[INPUT] Appuie sur Entrée pour forger un virus avec ce thème...")
        self.forge_virus(theme)            

            
    def forge_virus(self, theme):
        data = self.theme_library[theme]
        all_symbols = data['modern_symbols'] + data['paleo_symbols']
        symbol = random.choice(all_symbols)
        symbol_type = "modern" if symbol in data['modern_symbols'] else "paleo"
        if self.anthropic_mode:
            payload, quality_score = self.advanced_generator.generate_contextual(theme, symbol_type)
            final_score, detected_biases = EnhancedEmotionalScoring.score_meme(payload)
            faction = random.choice(data['factions'])
            self.current_virus = {
                'id': f"MEME-{random.randint(1000,9999)}",
                'theme': theme,
                'payload': payload,
                'symbol': symbol,
                'symbol_type': symbol_type,
                'faction': faction,
                'created_at': datetime.now().isoformat(),
                'generation_mode': 'anthropic',
                'quality_score': round(final_score, 1),
                'detected_biases': detected_biases,
                'stats': self.generate_stats(theme, symbol_type, final_score)
            }
        else:
            template = random.choice(data['payload_templates'])
            placeholder = {"modern": "l'écran", "paleo": "la paroi"}[symbol_type]
            payload = template.format(placeholder)
            faction = random.choice(data['factions'])
            self.current_virus = {
                'id': f"MEME-{random.randint(1000,9999)}",
                'theme': theme,
                'payload': payload,
                'symbol': symbol,
                'symbol_type': symbol_type,
                'faction': faction,
                'created_at': datetime.now().isoformat(),
                'generation_mode': 'classic',
                'stats': self.generate_stats(theme, symbol_type)
            }
        self.preview_virus()
    def generate_stats(self, theme, symbol_type, quality_score=None):
        if quality_score is not None:
            base = {
                'emotional_charge': min(10, 4 + quality_score * 0.6),
                'replication_potential': min(10, 3 + quality_score * 0.7),
                'resilience': random.randint(4, 8)
            }
        else:
            base = {
                'emotional_charge': random.randint(5, 9),
                'replication_potential': random.randint(4, 8),
                'resilience': random.randint(3, 7)
            }
        if theme == "fracturo":
            base['resilience'] += 1
            base['emotional_charge'] += 1
        if symbol_type == "paleo":
            base['resilience'] += 1
        return {k: min(10, max(1, round(v))) for k, v in base.items()}
    def preview_virus(self):
        v = self.current_virus
        print(f"\n{'═'*60}")
        print(f"🦠 VIRUS : {v['id']} ({v['theme'].upper()})")
        print(f"「 {v['payload']} 」")
        print(f"Symbole : {v['symbol']} | Faction : {v['faction']}")
        print(f"Mode : {v['generation_mode'].upper()}")
        if 'quality_score' in v:
            print(f"Qualité : {v['quality_score']}/10")
            if 'detected_biases' in v:
                print(f"Biais   : {', '.join(v['detected_biases'])}")
        print(f"Stats   : {v['stats']['emotional_charge']}/10 • {v['stats']['replication_potential']}/10 • {v['stats']['resilience']}/10")
        print("═"*60)
        if input("Sauvegarder ? (o/n) ").lower() in ['o','oui','y']:
            self.save_virus()

    # (autres méthodes inchangées)
    def save_virus(self):
        if not self.current_virus:
            print("[ERREUR] Aucun virus à sauvegarder.")
            return
        self.creation_log.append(self.current_virus)
        filename = f"virus_{self.current_virus['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.current_virus, f, ensure_ascii=False, indent=2)
        print(f"[SYSTÈME] Virus sauvegardé : {filename}")
        print(f"[SYSTÈME] ID : {self.current_virus['id']}")
        print("[SYSTÈME] Prêt pour la contamination...")
        self.current_virus = {}

    def batch_generate_anthropic(self, theme, count=5):
        """Génération par batch (disponible uniquement en mode Anthropic)"""
        if not self.anthropic_mode:
            print("[ERREUR] Mode batch nécessite --anthropic")
            return
        
        print(f"\n🔬 GÉNÉRATION BATCH ({count} CANDIDATS) - Thème: {theme}")
        print("─" * 60)
        
        data = THEME_LIBRARY[theme]
        all_symbols = data['modern_symbols'] + data['paleo_symbols']
        candidates = []
        
        for i in range(count):
            symbol = random.choice(all_symbols)
            symbol_type = "paleo" if symbol in data['paleo_symbols'] else "modern"
            payload, quality_score = self.advanced_generator.generate_contextual(theme, symbol_type)
            
            virus = {
                'id': f"MEME-{random.randint(1000, 9999)}",
                'theme': theme,
                'payload': payload,
                'symbol': symbol,
                'symbol_type': symbol_type,
                'faction': random.choice(data['factions']),
                'created_at': datetime.now().isoformat(),
                'generation_mode': 'anthropic_batch',
                'quality_score': round(quality_score, 1),
                'stats': self.generate_stats(theme, symbol_type, quality_score)
            }
            candidates.append(virus)
            print(f"  #{i+1} [{virus['quality_score']:.1f}/10] {virus['payload'][:60]}...")
        
        # Tri par qualité
        candidates.sort(key=lambda v: v['quality_score'], reverse=True)
        
        print("\n🏆 TOP 3 CANDIDATS :")
        for i, virus in enumerate(candidates[:3], 1):
            print(f"\n{i}. [{virus['quality_score']:.1f}/10] {virus['symbol']}")
            print(f"   「 {virus['payload']} 」")
        
        choice = input("\n[INPUT] Sauvegarder lequel ? (1-3 ou 'tous') : ").strip()
        
        if choice == "tous":
            for v in candidates[:3]:
                self.creation_log.append(v)
            print(f"[SYSTÈME] {len(candidates[:3])} virus sauvegardés")
        elif choice.isdigit() and 1 <= int(choice) <= 3:
            self.creation_log.append(candidates[int(choice)-1])
            print(f"[SYSTÈME] Virus #{choice} sauvegardé")

    def show_creations(self):
        if not self.creation_log:
            print("\n[SYSTÈME] Aucune création sauvegardée.")
            return
        print(f"\n" + "─" * 60)
        print(f"📚 MES CRÉATIONS ({len(self.creation_log)} virus)")
        print("─" * 60)
        for i, virus in enumerate(self.creation_log, 1):
            mode_badge = "🧠" if virus.get('generation_mode', '').startswith('anthropic') else "⚙️"
            quality_info = f" [{virus.get('quality_score', 'N/A')}/10]" if 'quality_score' in virus else ""
            print(f"{i}. {mode_badge} {virus['id']}{quality_info} - {virus['theme']}")
            print(f"   「 {virus['payload']} 」")
            print(f"   {virus['symbol']} | {virus['faction']}")
            print()

    def _select_virus(self, prompt="Sélectionne un virus : "):
        if not self.creation_log:
            print("[ERREUR] Aucun virus disponible.")
            return None
        self.show_creations()
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(self.creation_log):
                return self.creation_log[choice-1]
            else:
                print("[ERREUR] Sélection invalide.")
                return None
        except ValueError:
            print("[ERREUR] Entrez un numéro valide.")
            return None

    def _mutate_virus_interface(self):
        virus = self._select_virus("\n[EVOLUTION] Virus à muter : ")
        if virus:
            mutated = self.evolution_lab.mutate_virus(virus)
            self.current_virus = mutated
            self.preview_virus()

    def _hybridize_viruses_interface(self):
        print("\n[EVOLUTION] Sélection du premier virus :")
        virus1 = self._select_virus()
        if not virus1:
            return
        print("\n[EVOLUTION] Sélection du deuxième virus :")
        virus2 = self._select_virus()
        if not virus2:
            return
        hybrid = self.evolution_lab.hybridize_viruses(virus1, virus2)
        self.current_virus = hybrid
        self.preview_virus()

    def _cultivate_strain_interface(self):
        virus = self._select_virus("\n[EVOLUTION] Virus de base pour la souche : ")
        if not virus:
            return
        try:
            generations = int(input("[EVOLUTION] Nombre de générations (2-5) : ") or "3")
            generations = max(2, min(5, generations))
        except ValueError:
            generations = 3
        strain_lineage = self.evolution_lab.cultivate_strain(virus, generations)
        for strain in strain_lineage[1:]:
            self.creation_log.append(strain)
        print(f"[EVOLUTION] Souche cultivée : {len(strain_lineage)-1} mutations sauvegardées")

    def _export_virus_to_html_interface(self):
        virus = self._select_virus("\n[RÉSEAU] Virus à exporter en HTML : ")
        if virus:
            self.trade_network.export_virus_to_html(virus)

    def evolution_interface(self):
        while True:
            choice = self.evolution_lab.evolution_menu()
            if choice == "1":
                self._mutate_virus_interface()
            elif choice == "2":
                self._hybridize_viruses_interface()
            elif choice == "3":
                self._cultivate_strain_interface()
            elif choice == "4":
                self.evolution_lab.show_evolution_tree()
            elif choice == "5":
                self._export_virus_to_html_interface()
            elif choice == "0":
                break
            else:
                print("[ERREUR] Commande non reconnue.")

    def trade_interface(self):
        while True:
            choice = self.trade_network.trade_menu()
            if choice == "1":
                self.trade_network.export_to_fracturo()
            elif choice == "2":
                filename = input("[RÉSEAU] Chemin du fichier à importer : ")
                self.trade_network.import_from_fracturo(filename)
            elif choice == "3":
                theme = input("[RÉSEAU] Thème du pack à créer : ")
                self.trade_network.create_theme_pack(theme)
            elif choice == "4":
                self.trade_network.ghost_network_share()
            elif choice == "5":
                self.trade_network._archive_collection()
            elif choice == "6":
                self._export_virus_to_html_interface()
            elif choice == "0":
                break
            else:
                print("[ERREUR] Commande non reconnue.")

    def run(self):
        self.print_header()
        while True:
            print("\n" + "─" * 60)
            print("🜂 MEME-INCUBATOR - TABLE DE FORGE")
            print("─" * 60)
            print("1. Explorer thèmes mémétiques")
            print("2. Forger un nouveau virus (aléatoire)")
            if self.anthropic_mode:
                print("3. 🧠 Génération batch intelligente")
            print("4. Voir mes créations")
            print("5. 🧬 Laboratoire d'évolution")
            print("6. 📤 Réseau d'échange")
            print("0. Quitter (effacer les traces)")
            print("─" * 60)
            choice = input("\n[INPUT] Choix : ").strip()
            if choice == "1":
                self.explore_themes()
            elif choice == "2":
                theme = random.choice(list(THEME_LIBRARY.keys()))
                self.forge_virus(theme)
            elif choice == "3" and self.anthropic_mode:
                print("\n[BATCH] Thèmes disponibles :")
                for i, theme in enumerate(THEME_LIBRARY.keys(), 1):
                    print(f"  {i}. {theme}")
                theme_choice = input("[BATCH] Choix du thème (numéro ou nom) : ").strip()
                if theme_choice.isdigit() and 1 <= int(theme_choice) <= len(THEME_LIBRARY):
                    theme = list(THEME_LIBRARY.keys())[int(theme_choice)-1]
                elif theme_choice in THEME_LIBRARY:
                    theme = theme_choice
                else:
                    print("[ERREUR] Thème invalide")
                    continue
                try:
                    count = int(input("[BATCH] Nombre de candidats (3-10) : ") or "5")
                    count = max(3, min(10, count))
                except ValueError:
                    count = 5
                self.batch_generate_anthropic(theme, count)
            elif choice == "4":
                self.show_creations()
            elif choice == "5":
                self.evolution_interface()
            elif choice == "6":
                self.trade_interface()
            elif choice == "0":
                print("\n[SYSTÈME] Déconnexion... Effacement des traces...")
                print("[SYSTÈME] Reste vigilant, Tisserand.")
                break
            else:
                print("[ERREUR] Commande non reconnue.")

# ████████████████████████████████████████████████████████████████████████████████
# POINT D'ENTRÉE (AVEC --load-lexicon)
# ████████████████████████████████████████████████████████████████████████████████
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--anthropic', action='store_true')
    parser.add_argument('--load-lexicon', type=str, help='Fichier JSON de lexique paléo-mnésique')
    args = parser.parse_args()

    theme_library = THEME_LIBRARY
    if args.load_lexicon:
        try:
            with open(args.load_lexicon, 'r', encoding='utf-8') as f:
                theme_library = json.load(f)
            print(f"[SYSTÈME] Lexique chargé : {args.load_lexicon}")
        except Exception as e:
            print(f"[ERREUR] {e} → utilisation du lexique intégré.")

    incubator = MemeIncubator(anthropic_mode=args.anthropic, theme_library=theme_library)
    incubator.run()

if __name__ == "__main__":
    main()
