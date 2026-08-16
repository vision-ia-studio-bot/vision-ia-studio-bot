import random

QUOTES = [
    "Le succès est la somme de petits efforts répétés chaque jour.",
    "N'abandonne jamais.",
    "Chaque jour est une nouvelle occasion de progresser.",
    "La discipline est le pont entre les objectifs et les résultats.",
    "Les grandes réalisations commencent par une simple décision.",
    "Crois en toi.",
    "Le travail d'aujourd'hui construit les résultats de demain.",
    "La persévérance est la clé du succès.",
    "Transforme tes obstacles en opportunités.",
    "Continue d'avancer, même lentement."
]


def get_quote():
    return random.choice(QUOTES)
