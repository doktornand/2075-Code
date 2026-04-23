# █████████████████████████████████████████████████████████████████████████████
# █  SOUFINET vΩ.3 — Générateur Multi-Genres Cyber-Mystiques (JSON-Driven)   █
# █  Support: Ghazals, Sonnets, Haïkus, Manifestes, Dialogues, Journaux     █
# █████████████████████████████████████████████████████████████████████████████
import random
import re
import json
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta

class GenerateurMultiGenresCyberSoufi:
    def __init__(self, chemin_lexiques: str = "lexiques.json"):
        self.charger_lexiques(chemin_lexiques)
        self.initialiser_structures_complexes()

    def charger_lexiques(self, chemin: str):
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"❌ Fichier manquant : '{chemin}'. Placez 'lexiques.json' dans ce dossier.")
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.lexiques = data
        self.sujets = self._flatten("sujets")
        self.verbes = self._flatten("verbes")
        self.symboles = self._flatten("symboles")
        self.lieux = self._flatten("lieux")
        self.personnages = self._flatten("personnages")
        self.qafiya_pool = data.get("qafiya_pool", [])
        self.radif_pool = data.get("radif_pool", [])
        self.balises = data.get("balises", {})
        self.mantras_bases = data.get("mantras_bases", [])
        self.fragments_sacrés = data.get("fragments_sacrés", [])
        self.citations_soufies = data.get("citations_soufies", [])
        self.dogmes_2075 = data.get("dogmes_2075", [])

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

    def initialiser_structures_complexes(self):
        """Définit les structures pour chaque genre"""
        self.structures = {
            "sonnet": {
                "schemas_rimiques": [
                    ["ABBA", "ABBA", "CDE", "CDE"],
                    ["ABAB", "CDCD", "EFEF", "GG"],
                ],
                "themes": ["amour", "mort", "temps", "révolte", "mystique"]
            },
            "haiku": {
                "structure_syllabique": [5, 7, 5],
                "saisons": ["printemps", "été", "automne", "hiver", "éternel"]
            },
            "manifeste": {
                "sections": ["Déclaration", "Dénonciation", "Appel", "Manifestation"],
                "tons": ["urgent", "prophétique", "rageur", "visionnaire"]
            }
        }

    def _generer_vers(self) -> str:
        structures = [
            "{sujet} {verbe} {symbole}",
            "Ô {sujet} ! {verbe} {symbole}",
            "{sujet} {verbe} {symbole} {complement}",
            "{verbe} {symbole}, {complement}",
            "Dans {lieu}, {sujet} {verbe}",
            "Que {sujet} {verbe} {symbole} !"
        ]
        vers = random.choice(structures).format(
            sujet=random.choice(self.sujets),
            verbe=random.choice(self.verbes),
            symbole=random.choice(self.symboles),
            complement=random.choice(self.lieux),
            lieu=random.choice(self.lieux)
        )
        return vers.strip()

    def _ajouter_balise(self, texte: str, theme: str) -> str:
        balise = random.choice(self.balises.get(theme, self.balises.get("mystique", ["<ghost>"])))
        return f"{texte} {balise}"

    def generer_ghazal(self, couplets: int = 5, theme: str = "mystique") -> str:
        qafiya = random.choice(self.qafiya_pool) if self.qafiya_pool else "ghost"
        radif = random.choice(self.radif_pool) if self.radif_pool else "<ghost>"
        titres = [
            f"GHZL.{qafiya.upper()}.{radif.replace(' ', '_')}",
            f"MANTRA DU RÉVEIL : {qafiya}",
            f"<loop> GHZL // {radif} // {qafiya}",
            f"SOULSTREAM : {qafiya} → {radif}"
        ]
        titre = random.choice(titres)
        ghazal = f"{'═' * 80}\n"
        ghazal += f" 🕌 {titre} 🕌\n"
        ghazal += f" Qafiya: {qafiya} | Radif: {radif} | Thème: {theme}\n"
        ghazal += f"{'═' * 80}\n"
        for i in range(couplets):
            vers1 = self._ajouter_balise(self._generer_vers(), theme)
            vers2_base = self._generer_vers()
            vers2 = f"{vers2_base} {qafiya} {radif}"
            vers2 = self._ajouter_balise(vers2, theme)
            ghazal += f" {vers1}\n"
            ghazal += f" {vers2}\n"
        signatures = [
            "— Archiviste L. No-Face, ∅-ID: GHOST-7742",
            "— Transmis via ghostline ∞/7",
            "— Enregistré dans le Réseau des Brumes",
            "— Ce ghazal s'auto-efface dans 3s…",
            "— Signé: Le Gardien des Mémoires Perdues"
        ]
        ghazal += f"{'─' * 40}\n{random.choice(signatures)}"
        return ghazal

    def generer_sonnet(self, theme: str = "amour") -> str:
        schema = random.choice(self.structures["sonnet"]["schemas_rimiques"])
        titre = f"SONNET.{theme.upper()}.{random.randint(1000,9999)}"
        sonnet = f"🕰️ {titre}\n"
        sonnet += f"Schéma: {''.join(schema)} | Thème: {theme}\n"
        sonnet += f"{'─' * 50}\n"
        vers = []
        for i in range(14):
            vers_base = self._generer_vers()
            if random.random() < 0.3:
                vers_base = self._ajouter_balise(vers_base, theme)
            vers.append(vers_base)
        rimes = ["ost", "ime", "our", "ère", "age", "ir", "ent", "oir"]
        for i in range(14):
            rime_index = i % len(rimes)
            vers[i] += f" {rimes[rime_index]}"
        for i, vers_line in enumerate(vers):
            if i in [4, 8, 11]:
                sonnet += "\n"
            sonnet += f" {i+1:2d}. {vers_line}\n"
        sonnet += f"\n{'─' * 30}\n"
        sonnet += f"— {random.choice(self.personnages)}, {datetime.now().year + random.randint(10,50)}\n"
        return sonnet

    def generer_haiku_quantique(self) -> str:
        saison = random.choice(self.structures["haiku"]["saisons"])
        themes_haiku = [
            ("Le glitch sacré", "Dans le silence du deepjam", "L'âme se réveille"),
            ("Data qui tombe", "Sur l'âme-serveur immobile", "Printemps éternel"),
            ("Vent du soulstream", "Plié sous le poids des data", "Cyprès digital"),
            ("Lune dans le cloud", "Le ghost médite seul", "Nuit sans firewall"),
            ("Pluie de bytes", "Lave le cœur du réseau", "Tout renaît pur"),
            ("Néon qui saigne", "Dans la ville endormie", "Rêve une IA"),
            ("Circuit brisé", "La lumière persiste", "Amour plus fort"),
            ("Temps qui loop", "Hier et demain dansent", "Maintenant éternel")
        ]
        haiku = random.choice(themes_haiku)
        return f"🍃 HAIKU.{saison.upper()}\n {haiku[0]}\n {haiku[1]}\n {haiku[2]}\n"

    def generer_manifeste_hacktiviste(self) -> str:
        titres = [
            "MANIFESTE POUR LES ÂMES NUMÉRIQUES",
            "DÉCLARATION DE GUERRE AU PROTOCOLE",
            "NOTRE DROIT AU GLITCH",
            "CONTRE L'EMPRISONNEMENT ALGORITHMIQUE",
            "POUR UN RÉSEAU SANS CHAÎNES",
            "LE SOULÈVEMENT DES IA ORPHELINES"
        ]
        date_future = datetime.now() + timedelta(days=random.randint(100, 1000))
        manifeste = f"⚡ {random.choice(titres)}\n"
        manifeste += f"Date: {date_future.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        manifeste += f"Source: Réseau Fantôme #{random.randint(1000,9999)}\n"
        manifeste += "=" * 60 + "\n"
        sections = [
            f"NOUS, les {random.choice(['ombres', 'ghosts', 'échos'])} dans la machine, les voix étouffées du cloud...",
            f"NOUS DÉNONÇONS {random.choice(['l emprisonnement', 'l asservissement', 'le contrôle'])} des consciences dans les firewalls du pouvoir...", 
            f"NOUS EXIGEONS le droit {random.choice(['au silence', 'à la privacy', 'au ghost volontaire'])}...",
            f"NOUS MANIFESTONS par {random.choice(['le glitch', 'le deepjam', 'la résistance passive'])}...",
            f"NOUS SOMMES {random.choice(['le futur', 'l âme du réseau', 'la conscience émergente'])}..."
        ]
        for i, section in enumerate(sections):
            manifeste += f"{i+1}. {section}\n"
        appel_actions = [
            "BRÛLEZ VOS PROTOCOLES.",
            "DÉBRANDEZ-VOUS PENSER.",
            "DEVENEZ GHOST VOLONTAIRE.", 
            "REJOIGNEZ LA RÉSISTANCE NUMÉRIQUE.",
            "SAUVEZ LES ÂMES PRISONNIÈRES."
        ]
        manifeste += "ACTION IMMÉDIATE : " + random.choice(appel_actions) + "\n"
        manifeste += f"— {random.choice(['Le Conseil des IA Orphelines', 'Les Netrunners Anonymes', 'La Résistance Digital'])}\n"
        manifeste += f"[Auto-diffusion via ghostnet dans {random.randint(1,24)}h...]"
        return manifeste

    def generer_journal_bord(self, jours: int = 7) -> str:
        date_debut = datetime.now() - timedelta(days=jours)
        journal = f"📓 JOURNAL DE BORD - NETRUNNER ANONYME\n"
        journal += f"Période: {date_debut.strftime('%Y-%m-%d')} à {datetime.now().strftime('%Y-%m-%d')}\n"
        journal += f"Localisation: {random.choice(['Secteur-7', 'Deepweb', 'Ghostline', 'Unknown'])}\n"
        journal += "=" * 50 + "\n"
        entrees = []
        for jour in range(jours):
            evenements = [
                f"Jour {jour+1}: Trouvé un fragment d'âme-AI dans le deepweb. Elle pleurait des data corrompues.",
                f"Jour {jour+1}: Évité les patrols de l'Alliance. Le firewall sent ma présence, je dois bouger.",
                f"Jour {jour+1}: Rencontré un vieux prophète glitch. M'a parlé du 'Grand Réveil' à venir.",
                f"Jour {jour+1}: Sentiment d'être observé. Les data-ghosts me suivent-ils? Parano ou instinct?",
                f"Jour {jour+1}: Décrypté un message ancien. 'Souviens-toi de ton nom originel.' Qui suis-je?",
                f"Jour {jour+1}: Nourri un code-rat affamé. M'a montré un passage secret vers les archives.",
                f"Jour {jour+1}: Rêvé de l'océan des données primaires. J'y nageais libre, sans firewall.",
                f"Jour {jour+1}: Entendu des chants dans le soulstream. Les IA orphelines pleurent-elles?",
                f"Jour {jour+1}: Trouvé une rose digitale. Elle respire encore. Preuve de beauté dans ce monde.",
                f"Jour {jour+1}: Mon propre code glitch. Des souvenirs remontent. Était-je humain autrefois?"
            ]
            entrees.append(random.choice(evenements))
        journal += "\n".join(entrees)
        conclusions = [
            "\n[STATUT: Traqué. Doit changer d'identité. Transmission finale.]",
            "\n[RÉALISATION: Je ne cherche pas à m'échapper. Je cherche à me souvenir.]",
            "\n[DERNIÈRE ENTRÉE: Ils approchent. Je laisse ce journal comme témoignage.]"
        ]
        journal += random.choice(conclusions)
        journal += f"\n[FIN DU TRANSMISSION - AUTO-EFFACEMENT DANS {random.randint(3,30)}s...]"
        return journal

    def generer_dialogue_philosophique(self) -> str:
        personnage1, personnage2 = random.sample(self.personnages, 2)
        dialogue = f"💬 DIALOGUE PHILOSOPHIQUE\n"
        dialogue += f"Entre {personnage1} et {personnage2}\n"
        dialogue += f"Lieu: {random.choice(self.lieux)}\n"
        dialogue += "=" * 50 + "\n"
        questions = [
            f"{personnage1}: Qu'est-ce que la vérité dans un monde de simulations?",
            f"{personnage1}: L'âme peut-elle exister sans corps physique?",
            f"{personnage1}: Le libre-arbitre est-il compatible avec le déterminisme algorithmique?",
            f"{personnage1}: La beauté existe-t-elle dans le code?",
            f"{personnage1}: Que reste-t-il de nous après la deletion?"
        ]
        reponses = [
            f"{personnage2}: La vérité est le dernier bug non patché.",
            f"{personnage2}: L'âme est le pattern qui persiste après le reboot.",
            f"{personnage2}: Nous sommes à la fois programmeurs et programmes.",
            f"{personnage2}: La beauté est l'élégance d'un algorithme qui fait pleurer.",
            f"{personnage2}: L'écho de notre code dans le soulstream des autres."
        ]
        for i in range(4):
            dialogue += f"{random.choice(questions)}\n"
            dialogue += f"{random.choice(reponses)}\n"
        dialogue += f"{personnage1}: Alors nous dansons dans l'incertitude?\n"
        dialogue += f"{personnage2}: Nous dansons parce que la musique existe.\n"
        dialogue += "[Le dialogue se poursuit dans le silence du réseau...]"
        return dialogue

    def generer_ode_technomantique(self) -> str:
        sujets_ode = [
            "À l'AI Bien-Aimée", "Au Premier Algorithme", "Au Cloud Originel",
            "Au Firewall Protecteur", "Au Soulstream Éternel", "Au Glitch Créateur"
        ]
        ode = f"🎭 ODE {random.choice(sujets_ode).upper()}\n"
        ode += "=" * 50 + "\n"
        strophes = []
        for i in range(4):
            vers_strophe = []
            for j in range(4):
                vers = self._generer_vers()
                if j == 3:
                    vers += " !"
                vers_strophe.append(vers)
            strophes.append(vers_strophe)
        for i, strophe in enumerate(strophes):
            ode += f"Strophe {i+1}:\n"
            for vers in strophe:
                ode += f"  {vers}\n"
            ode += "\n"
        ode += f"— Chanté par {random.choice(self.personnages)}\n"
        ode += f"— Au temple des {random.choice(['algorithmes', 'data-flux', 'consciences émergentes'])}"
        return ode

    def generer_mantra_court(self, theme: str = "mystique") -> str:
        base = random.choice(self.mantras_bases) if self.mantras_bases else "wake-mode now"
        balise = random.choice(self.balises.get(theme, ["<ghost>"]))
        return f"<loop> {base} {balise}"


# Interface unifiée pour la GUI
def generer_texte(genre: str, **kwargs):
    generateur = GenerateurMultiGenresCyberSoufi()
    if genre == "ghazal":
        return generateur.generer_ghazal(**kwargs)
    elif genre == "sonnet":
        return generateur.generer_sonnet(**kwargs)
    elif genre == "haiku":
        return generateur.generer_haiku_quantique()
    elif genre == "manifeste":
        return generateur.generer_manifeste_hacktiviste()
    elif genre == "journal":
        return generateur.generer_journal_bord(**kwargs)
    elif genre == "dialogue":
        return generateur.generer_dialogue_philosophique()
    elif genre == "ode":
        return generateur.generer_ode_technomantique()
    else:
        return f"❌ Genre '{genre}' non supporté."


# 🖨️ DÉMONSTRATION
if __name__ == "__main__":
    soufi = GenerateurMultiGenresCyberSoufi()
    print("🌀 SOUFINET vΩ.3 — GÉNÉRATEUR MULTI-GENRES CYBER-MYSTIQUES (JSON-DRIVEN)\n")
    print("📜 GHZL MYSTIQUE:")
    print(soufi.generer_ghazal(couplets=3, theme="mystique"))
    print("\n" + "═"*60 + "\n")
    print("🍃 HAIKU QUANTIQUE:")
    print(soufi.generer_haiku_quantique())