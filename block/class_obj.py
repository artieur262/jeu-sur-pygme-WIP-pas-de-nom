"""est module de class"""
# pylint: disable=unused-import wildcard-import unused-wildcard-import
# from typing import Any

# # from typing
# import traceback


from .class_block import *
from .block_activable import (
    PlateformeMouvante,
    BlockLumiere,
    BlockCore,
    TunelDimensionelBrigitte,
)
from .block_logique import LogiqueNot, Logique, LogiqueTimer, LogiqueChangement
from .block_activateur import Interupteur, ZoneActive

# traceback.print_stack()


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
        """actualise la taille du joueur en fonction de la face"""
        if face == 0:
            self._taille = [self._taille_int, self._taille_int, 1]
        elif face == 1:
            self._taille = [self._taille_int, 1, self._taille_int]
        elif face == 2:
            self._taille = [1, self._taille_int, self._taille_int]
        else:
            raise ValueError(f"la face n'est pas reconnu : face = {face}")

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


class BlockTexte(Block):
    """est un block qui affiche du texte"""

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
        for face_graphique in self.graphique:
            for image in face_graphique.images:
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
        return BlockTexte(
            dic["coor"],
            dic["taille"],
            dic["color"],
            dic["texte_color"],
            dic["texte"],
            dic["police_name"],
            dic["police_taille"],
            texture=dic["texture"],
        )


def genere_obj(
    liste: list[dict],
) -> dict[
    str,
    list[
        Block
        | PlateformeMouvante
        | Playeur
        | Interupteur
        | ZoneActive
        | BlockLumiere
        | BlockTexte
        | BlockCore
        | TunelDimensionelBrigitte
        | Logique
        | LogiqueNot
        | LogiqueTimer
        | LogiqueChangement
    ],
]:
    """genere les objets à partir d'une liste de dictionaire"""
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
            sorti["texte"].append(BlockTexte.convert_load(obj))
        elif obj["type"] == "player":
            sorti["playeur"].append(Playeur.convert_load(obj))

        elif obj["type"] == "interupteur":
            sorti["interupteur"].append(Interupteur.convert_load(obj))
        elif obj["type"] == "zone":
            sorti["zone_acitve"].append(ZoneActive.convert_load(obj))

        elif obj["type"] == "lumière":
            sorti["lumière"].append(BlockLumiere.convert_load(obj))
        elif obj["type"] == "plaforme":
            sorti["plaforme"].append(PlateformeMouvante.convert_load(obj))
        elif obj["type"] == "core":
            sorti["core"].append(BlockCore.convert_load(obj))
        elif obj["type"] == "tunel_dimensionel":
            sorti["tunel_dimensionel"].append(
                TunelDimensionelBrigitte.convert_load(obj)
            )

        elif obj["type"] == "logique":
            sorti["logique"].append(Logique.convert_load(obj))
        elif obj["type"] == "not":
            sorti["logique"].append(LogiqueNot.convert_load(obj))
        elif obj["type"] == "timer":
            sorti["logique"].append(LogiqueTimer.convert_load(obj))
        elif obj["type"] == "changement":
            sorti["logique"].append(LogiqueChangement.convert_load(obj))
    return sorti
