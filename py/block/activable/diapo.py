from typing import TYPE_CHECKING
from py.block.activable.activable import Activable
from py.objet.objet_visuel import ObjetVisuel3D
from py.graphique.image import Image


if TYPE_CHECKING:
    from py.game.map import Map


class Diapo(Activable, ObjetVisuel3D):
    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture_pack: list[tuple[Image, Image, Image]],
        entre: int,
    ):
        """initialise le diapo"""
        Activable.__init__(self, entre)
        ObjetVisuel3D.__init__(
            self, coordonnee, taille, [img[0] for img in texture_pack]
        )
        self._texture_pack = [
            Image.genere_list_image(texture) for texture in texture_pack
        ]
        self._index_texture = 0
        self.etat_precedent = False

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activable(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_activable(self)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def actualiser_image(self) -> None:
        """permet de mettre a jour l'image en fonction de l'etat"""
        self._set_image_list(self._texture_pack[self._index_texture])

    def _actualise_activer(self, map_: "Map") -> None:
        """permet de mettre a jour l'etat de l'activable"""
        present_entre = map_.in_signal(self._entre)
        self._activer = present_entre and not self.etat_precedent
        self.etat_precedent = present_entre


class DiapoBoucle(Diapo):
    """cette class permet de faire un diapo en boucle
    dés qu'elle arrive a la fin elle recommence au début
    """

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        self._actualise_activer(map_)
        if self.get_activer():
            self._index_texture = (self._index_texture + 1) % len(self._texture_pack)
            self._set_image_list(self._texture_pack[self._index_texture])
            self.actualiser_image()


class DiapoAllerRetour(Diapo):
    """cette class permet de faire un diapo aller retour
    dés qu'elle arrive a la fin elle va dans l'autre sens
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture_pack: list[tuple[Image, Image, Image]],
        entre: int,
    ):
        """initialise le diapo aller retour"""
        super().__init__(coordonnee, taille, texture_pack, entre)
        self._direction = 1

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""

        self._actualise_activer(map_)

        if self.get_activer():
            self._index_texture += self._direction
            if self._index_texture >= len(self._texture_pack):
                self._index_texture = len(self._texture_pack) - 2
                self._direction = -1
            elif self._index_texture < 0:
                self._index_texture = 1
                self._direction = 1
            self._set_image_list(self._texture_pack[self._index_texture])
            self.actualiser_image()


class DiapoFin(Diapo):
    """cette class permet de faire un diapo unique
    dés qu'elle arrive a la fin elle reste a la dernière image
    """

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        self._actualise_activer(map_)
        if self.get_activer():
            if self._index_texture < len(self._texture_pack) - 1:
                self._index_texture += 1
                self._set_image_list(self._texture_pack[self._index_texture])
                self.actualiser_image()
