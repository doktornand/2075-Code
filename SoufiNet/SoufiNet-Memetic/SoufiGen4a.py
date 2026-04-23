import json
import random

class GenerateurGhazalCyberSoufi:
    def __init__(self, lexique_path="lexiques.json"):
        with open(lexique_path, "r", encoding="utf-8") as f:
            self.lex = json.load(f)

    def generer_vers(self, theme="amour_divin", inclure_balise=True, style="rythmé"):
        pref = random.choice(self.lex["préfixes_sacrés"])
        trad = random.choice(self.lex["thèmes"][theme]["traditionnel"])
        cyber = random.choice(self.lex["thèmes"][theme]["cyber"])
        suffix = random.choice(self.lex["suffixes_cyber"]) if random.random() > 0.5 else ""

        # Fusion poétique
        vers = f"{pref} {trad} {cyber}{suffix} !"

        if inclure_balise:
            balise = random.choice(self.lex["balises_oniriques"])
            vers += f" {balise}"

        return vers

    def generer_ghazal(self, nb_vers=6, theme="amour_divin"):
        return [self.generer_vers(theme=theme) for _ in range(nb_vers)]

# Exemple d'utilisation
if __name__ == "__main__":
    gen = GenerateurGhazalCyberSoufi()
    for vers in gen.generer_ghazal(theme="rêve_partagé"):
        print("- " + vers)