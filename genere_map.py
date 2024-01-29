from class_obj import *
import save


def convert_map(map_: list[Block | Logique]):
    return [x.convert_save() for x in map_]


LIEN_FICHIER_MAP = "map/"
LIEN = "tuto_6.json"
rule = {"face": 1, "valeur_de_fin": 10, "gravite": (0, 0, 0)}
map = [
    Playeur((0, 25, 220), 30, (255, 255, 255)),
    Block((-50, -100, 0), (50, 250, 300), (125, 125, 125)),
    Block((0, 0, 0), (800, 50, 50), (125, 125, 125)),
    Block((0, 0, 250), (800, 50, 50), (125, 125, 125)),
    Block_core(
        (200, 0, 200),
        (50, 50, 50),
        1,
        [
            "texture/the core atente v4.svg",
            "texture/the core demare v4.svg",
            "texture/the core charger v4.svg",
        ],
        {"1": "0", "0": "1"},
    ),
    Interupteur(1, (200, 0, 250), (50, 50, 50), (0, 0, 255)),
    #
    Block((-50, -100, 200), (850, 50, 50), (125, 125, 125)),
    Block((-50, 100, 200), (850, 50, 50), (125, 125, 125)),
    Block((800, -100, 0), (50, 250, 300), (125, 125, 125)),
    #
    Block((250, -100, 230), (50, 250, 20), (125, 125, 125)),
    Block((250, -100, 50), (50, 250, 170), (125, 125, 125)),
    #
    Block_core(
        (350, 0, 200),
        (50, 50, 50),
        2,
        [
            "texture/the core atente v4.svg",
            "texture/the core demare v4.svg",
            "texture/the core charger v4.svg",
        ],
        {"1": "0", "0": "1"},
    ),
    #
    Block((400, -100, 0), (50, 120, 300), (125, 125, 125)),
    Interupteur(2, (400, 30, 0), (50, 70, 300), (0, 0, 255)),
    #
    Zone_acitve(10, (750, -50, 50), (50, 150, 200), (255, 255, 0, 200)),
    #
    Block_texte(
        (0, 0, 50),
        (250, 50, 150),
        (200, 200, 200, 0),
        (255, 255, 255),
        "Et si on changeait\nde face pour\npasser dans\ncette fissure ?",
        "monospace",
        20,
    ),
]

contenu = [rule, convert_map(map)]
# print(contenu)
save.save_json(LIEN_FICHIER_MAP + LIEN, contenu)
