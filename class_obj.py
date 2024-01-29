"""est module de class"""
# pylint: disable=unused-import wildcard-import unused-wildcard-import
from typing import Any

# # from typing
# import traceback


from class_block import *
from block_activable import (
    PlateformeMouvante,
    Block_lumiere,
    Block_core,
    Tunel_dimensionel_Brigitte,
)
from block_logique import Logique_not, Logique, Logique_Timer, Logique_chagement
from block_activateur import Interupteur, Zone_acitve

# traceback.print_stack()


class Vec:
    def __init__(self):
        self.vec = numpy.array((0, 0, 0), dtype=self.DVEC)

    def __tick__(self):
        self()["v"] += self()["a"]
        self()["pos"] += self()["v"]

    def __call__(self):
        return self.vec

    def stop(self):
        self()["v"] = 0
        self()["a"] = 0

    DVEC = numpy.dtype([("pos", float, 3), ("v", float, 3), ("a", float, 3)])


# class BlocGlissant(Pave):
#     def cat(self):
#         pass


class Playeur(Block):
    """est le joueur"""

    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: int,
        color: tuple[int, int, int] = None,
        texture: list[str] = None,
    ):
        self._taille_int = taille
        self.vie = "en vie"
        self.etat = "tombe"
        super().__init__(coordonnee, (taille, taille, taille), color, texture=texture)

    def actualise_taille_playeur(self, face: str):
        if face == 0:
            self._taille = [self._taille_int, self._taille_int, 1]
        elif face == 1:
            self._taille = [self._taille_int, 1, self._taille_int]
        elif face == 2:
            self._taille = [1, self._taille_int, self._taille_int]
        else:
            raise ValueError(f"la face n'est pas reconnu : face = {face}")

    def depace_vecteur(self, list_collision: list[Block], vecteur: Vec):
        pass

    def deplace(self, list_block: list, axe: int, distance: int):
        deplacemment = super().deplace(list_block, axe, distance)
        if axe == 2 and distance > 0:
            self.etat = "par terre" if deplacemment else "tombe"
            # print(f"cat {self.etat}")

        elif axe == 2 and distance < 0:
            self.etat = "saute"

            # print(f"cat {self.etat}")
        return deplacemment

    def convert_save(self) -> dict:
        sorti = super().convert_save()
        sorti["type"] = "player"
        sorti["taille"] = self._taille_int
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        return Playeur(dic["coor"], dic["taille"], dic["color"], texture=dic["texture"])


class Block_texte(Block):
    def __init__(
        self,
        coordonnee: tuple[int, int, int],
        taille: tuple[int, int, int],
        color: tuple[int, int, int],
        texte_color: tuple[int, int, int],
        texte,
        police: pygame.font.Font,
        taille_police: int,
        animation: int = 0,
        texture=None,
    ):
        self._police_name = police
        self._police = pygame.font.SysFont(self._police_name, taille_police)
        self._texte = texte
        self._texte_color = texte_color
        super().__init__(
            coordonnee,
            taille,
            color,
            animation,
            texture,
        )

    def genere_graphique(self):
        super().genere_graphique()
        for x in self.graphique:
            for image in x.images:
                place_texte_in_texture(
                    image, self._texte, self._police, self._texte_color
                )

    def convert_save(self) -> dict:
        sortie = super().convert_save()
        sortie["type"] = "texte"
        sortie["texte"] = self._texte
        sortie["texte_color"] = self._texte_color
        sortie["police_name"] = self._police_name
        sortie["police_taille"] = self._police.get_height()
        return sortie

    @staticmethod
    def convert_load(dic: dict):
        return Block_texte(
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["texte_color"],
            dic["texte"],
            dic["police_name"],
            dic["police_taille"],
            texture=dic["texture"],
        )


def genere_obj(liste: list[dict]) -> dict[str, list]:
    sorti = {
        "interupteur": [],
        "playeur": [],
        "plaforme": [],
        "lumière": [],
        "block": [],
        "logique": [],
        "texte": [],
        "core": [],
        "tunel_dimensionel": [],
        "zone_acitve": [],
    }
    for obj in liste:
        # print(obj)
        if obj["type"] == "block":
            sorti["block"].append(Block.convert_load(obj))
        elif obj["type"] == "texte":
            sorti["texte"].append(Block_texte.convert_load(obj))
        elif obj["type"] == "player":
            sorti["playeur"].append(Playeur.convert_load(obj))

        elif obj["type"] == "interupteur":
            sorti["interupteur"].append(Interupteur.convert_load(obj))
        elif obj["type"] == "zone":
            sorti["zone_acitve"].append(Zone_acitve.convert_load(obj))

        elif obj["type"] == "lumière":
            sorti["lumière"].append(Block_lumiere.convert_load(obj))
        elif obj["type"] == "plaforme":
            sorti["plaforme"].append(PlateformeMouvante.convert_load(obj))
        elif obj["type"] == "core":
            sorti["core"].append(Block_core.convert_load(obj))
        elif obj["type"] == "tunel_dimensionel":
            sorti["tunel_dimensionel"].append(
                Tunel_dimensionel_Brigitte.convert_load(obj)
            )

        elif obj["type"] == "logique":
            sorti["logique"].append(Logique.convert_load(obj))
        elif obj["type"] == "not":
            sorti["logique"].append(Logique_not.convert_load(obj))
        elif obj["type"] == "timer":
            sorti["logique"].append(Logique_Timer.convert_load(obj))
        elif obj["type"] == "changement":
            sorti["logique"].append(Logique_chagement.convert_load(obj))
    return sorti
