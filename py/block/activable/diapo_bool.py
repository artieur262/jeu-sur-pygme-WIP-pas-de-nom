from typing import TYPE_CHECKING

from py.block.activable.diapo_value import (
    DiapoValue,
    DiapoValueAllerRetour,
    DiapoValueBoucle,
    DiapoValueFin,
)
from py.graphique.image import Image

if TYPE_CHECKING:
    from py.game.map import Map


class DiapoBool(DiapoValue):
    """cette class permet de faire un diapo en fonction d'un etat boolean
    si l'etat est vrai elle avance dans le diapo
    si l'etat est faux elle recule dans le diapo
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture_pack: list[tuple[Image, Image, Image]],
        entre: int | tuple[str, int, str] | tuple[str, int],
    ):
        """initialise le diapo boolean"""
        super().__init__(coordonnee, taille, texture_pack, entre)
        self._entre = entre
        self._activer = False
        self.etat_precedent = False

    def get_activer(self) -> bool:
        """permet de savoir si le bloc logique est actif"""
        return self._activer

    def set_activer(self, activer: bool) -> None:
        """permet de changer l'etat du bloc logique"""
        self._activer = activer

    def _actualise_signal(self, map_):
        present_entre = map_.in_signal(self._entre)
        self._activer = present_entre and not self.etat_precedent
        self.etat_precedent = present_entre

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")


class DiapoBoolAllerRetour(DiapoValueAllerRetour, DiapoBool):
    """cette class permet de faire un diapo en aller retour en fonction d'un etat boolean
    si l'etat est vrai elle avance dans le diapo
    si l'etat est faux elle recule dans le diapo
    """

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        if self.get_activer():
            self._index_texture += 1
            DiapoBoolAllerRetour.actualise_index_texture(self)


class DiapoBoolBoucle(DiapoValueBoucle, DiapoBool):
    """cette class permet de faire un diapo en boucle en fonction d'un etat boolean
    si l'etat est vrai elle avance dans le diapo
    si l'etat est faux elle recule dans le diapo
    """

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        if self.get_activer():
            self._index_texture += 1
            DiapoBoolBoucle.actualise_index_texture(self)


class DiapoBoolFin(DiapoValueFin, DiapoBool):
    """cette class permet de faire un diapo qui s'arrete a la fin en fonction d'un etat boolean
    si l'etat est vrai elle avance dans le diapo
    si l'etat est faux elle recule dans le diapo
    """

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        if self.get_activer():
            self._index_texture += 1
            DiapoBoolFin.actualise_index_texture(self)
