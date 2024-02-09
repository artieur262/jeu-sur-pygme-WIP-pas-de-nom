"""Module pour l'éditeur de niveau."""

# Importation des modules

from block.class_obj import (
    ObjetGraphique,
    gener_texture,
    place_texte_in_texture,
    pygame,
    screen,
    #
    Block,
    BlockTexte,
    Playeur,
    #
    Interupteur,
    ZoneActive,
    BlockLumiere,
    PlateformeMouvante,
    #
    BlockCore,
    TunelDimensionelBrigitte,
    RedimentioneurPlayer,
    Graviteur,
    #
    Logique,
    LogiqueChangement,
    LogiqueNot,
    LogiqueTimer,
)

from interface.option import actualise_event, change_fullscreen
from interface.choix_level import ChoisirLevel
from save import save_json, open_json


class MapMaker:
    def __init__(
        self,
        info_map: dict[str, list[dict[str, list | dict | int | float | str]]],
        map_: list[dict[str, list | dict | int | float | str]],
        police: str = "monospace",
        taille_police: int = 20,
    ):
        self.police = pygame.font.SysFont(police, taille_police)
        self._info_map = info_map
        self._map = map_
        self.scrool = 0
        self.select = None
        self.suprime_doublon_name()
        self.ajoute_name()
        self.actualise_map()

    def actualise_map(self):
        """Actualise la map en fonction des objets."""
        self.graf_obj: list[tuple[str, ObjetGraphique]] = []

        corlor_type = {
            "block": ((100, 100, 100), (50, 50, 50), (255, 255, 255)),  # gris foncé
            "texte": ((200, 100, 0), (150, 50, 0), (255, 255, 255)),  # orange
            "player": ((200, 200, 200), (150, 150, 150), (0, 0, 0)),  # gris clair
            "interupteur": ((0, 200, 200), (0, 150, 150), (0, 0, 0)),  # cyan
            "zone": ((200, 200, 0), (150, 150, 0), (0, 0, 0)),  # jaune
            "lumière": ((100, 100, 100), (50, 50, 50), (255, 255, 255)),  # gris foncé
            "plaforme": ((0, 0, 200), (0, 0, 150), (255, 255, 255)),  # bleu
            "core": ((0, 200, 0), (0, 150, 0), (0, 0, 0)),  # vert
            "tunel_dimensionel": (
                (200, 0, 200),
                (150, 0, 150),
                (255, 255, 255),
            ),  # violet
            "redimentioneur": ((200, 100, 100), (150, 50, 50), (255, 255, 255)),  # rose
            "graviteur": ((200, 0, 0), (100, 0, 0), (255, 255, 255)),  # rouge
            # logique
            "logique": ((0, 200, 0), (0, 150, 0), (0, 0, 0)),  # vert
            "changement": ((200, 200, 0), (150, 150, 0), (0, 0, 0)),  # jaune
            "logique_not": ((200, 0, 0), (150, 0, 0), (255, 255, 255)),  # rouge
            "logique_timer": ((0, 0, 200), (0, 0, 150), (255, 255, 255)),  # bleu
        }

        for i, obj in enumerate(self._map):

            self.graf_obj.append(
                (
                    obj["name"],
                    ObjetGraphique(
                        [0, i * 25],
                        [
                            place_texte_in_texture(
                                gener_texture((200, 25), couleur),
                                obj["name"],
                                self.police,
                                corlor_type[obj["type"]][2],
                            )
                            for couleur in corlor_type[obj["type"]][0:2]
                        ],
                    ),
                )
            )

    def affiche(self):
        """Affiche les objets de la map."""

        for obj in self.graf_obj:
            obj[1].afficher((0, self.scrool))

    def nom_present(self, nom: str) -> bool:
        """Retourne True si le nom est déjà présent dans la map."""
        for obj in self._map:
            if obj["name"] == nom:
                return True
        return False

    def suprime_doublon_name(self):
        """Suprime les doublons de nom dans la liste des objets."""
        deja_vu = set()
        for obj in self._map:
            if "name" in obj.keys():
                if obj["name"] in deja_vu:
                    name = obj["name"]
                    for obj_ in self._map:
                        if obj_["name"] == name:
                            obj_["name"] = None
                else:
                    deja_vu.add(obj["name"])
            else:
                obj["name"] = None

    def ajoute_name(self):
        """Ajoute un nom à tout les objets qui n'en ont pas."""
        nom_present = set()
        for obj in self._map:
            if obj["name"] is not None:
                nom_present.add(obj["name"])
        for obj in self._map:
            if obj["name"] is None:
                i = 1
                while "block" + str(i) in nom_present:
                    i += 1

                obj["name"] = obj["type"] + str(i)
                nom_present.add(obj["name"])


def main():
    """Fonction principale."""
    map_teste = open_json("map/tuto/tuto_1.json")  # "map/map_teste.json"
    map_maker = MapMaker(map_teste[0], map_teste[1])
    clock = pygame.time.Clock()
    map_maker.actualise_map()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                quit()

        screen.fill((0, 0, 0))
        map_maker.affiche()
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
