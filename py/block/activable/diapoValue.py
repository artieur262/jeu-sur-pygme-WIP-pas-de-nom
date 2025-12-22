from typing import TYPE_CHECKING
from py.block.activable.activable import Activable
from py.objet.objet_visuel import ObjetVisuel3D
from py.graphique.image import Image


if TYPE_CHECKING:
    from py.game.map import Map


class DiapoValue(Activable, ObjetVisuel3D):
    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int, int],
        texture_pack: list[tuple[Image, Image, Image]],
        entre: str,
    ):
        """initialise le diapo"""
        Activable.__init__(self, entre)
        ObjetVisuel3D.__init__(
            self, coordonnee, taille, [img[0] for img in texture_pack]
        )
        self._texture_pack = [
            Image.genere_list_image(texture) for texture in texture_pack
        ]
        self._entre = entre
        self._index_texture: int = 0
        self.etat_precedent = False

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activable(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_activable(self)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        self._actualise_signal(map_)
        self._actualise_index_texture()
        self._set_image_list(self._texture_pack[self._index_texture])
        self.actualiser_image()

    def actualiser_image(self) -> None:
        """permet de mettre a jour l'image en fonction de l'etat"""
        self._set_image_list(self._texture_pack[self._index_texture])

    def _actualise_signal(self, map_: "Map") -> None:
        """permet de mettre a jour l'etat de l'activable"""
        self._index_texture: int = map_.in_signal(self._entre)

    def _actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")


class DiapoValueBoucle(DiapoValue):
    """cette class permet de faire un diapo en boucle
    dés qu'elle arrive a la fin elle recommence au début
    """

    def _actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        self._index_texture = (self._index_texture) % len(self._texture_pack)


class DiapoValueAllerRetour(DiapoValue):
    """cette class permet de faire un diapo aller retour
    dés qu'elle arrive a la fin elle va dans l'autre sens
    """

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""

        self._actualise_signal(map_)

        self._set_image_list(self._texture_pack[self._index_texture])
        self.actualiser_image()

    def _actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        mod = len(self._texture_pack) - 1
        self._index_texture = self._index_texture % (2 * mod)
        if self._index_texture > mod:
            self._index_texture = 2 * mod - self._index_texture


class DiapoValueFin(DiapoValue):
    """cette class permet de faire un diapo unique
    dés qu'elle arrive a la fin elle reste a la dernière image
    """

    def _actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        if self._index_texture >= len(self._texture_pack):
            self._index_texture = len(self._texture_pack) - 1
