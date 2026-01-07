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
        self._entre: str = entre
        self._index_texture: int = 0

    def get_index_texture(self) -> int:
        """permet de recuperer l'index du diapo"""
        return self._index_texture

    def set_index_texture(self, index_texture: int) -> None:
        """permet de definir l'index du diapo"""
        self._index_texture = index_texture

    def get_len_texture_pack(self) -> int:
        """permet de recuperer la longueur du texture pack"""
        return len(self._texture_pack)

    def ajouter_map(self, map_: "Map") -> None:
        """ajoute la map"""
        map_.add_activable(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_activable(self)

    def activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique"""
        self._actualise_signal(map_)
        self.actualise_index_texture()
        self._set_image_list(self._texture_pack[self._index_texture])
        self.actualiser_image()

    def actualiser_image(self) -> None:
        """permet de mettre a jour l'image en fonction de l'etat"""
        self._set_image_list(self._texture_pack[self._index_texture])

    def _actualise_signal(self, map_: "Map") -> None:
        """permet de mettre a jour l'etat de l'activable"""
        self._index_texture: int = map_.in_signal(self._entre)

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")


class DiapoBoucle(Diapo):
    """cette class permet de faire un diapo en boucle
    dés qu'elle arrive a la fin elle recommence au début
    """

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        self.set_index_texture(self.get_index_texture() % self.get_len_texture_pack())


class DiapoAllerRetour(Diapo):
    """cette class permet de faire un diapo aller retour
    dés qu'elle arrive a la fin elle va dans l'autre sens
    """

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        mod = self.get_len_texture_pack() - 1
        self.set_index_texture(self.get_index_texture() % mod)
        if self.get_index_texture() > mod:
            self.set_index_texture(mod * 2 - self.get_index_texture())


class DiapoFin(Diapo):
    """cette class permet de faire un diapo unique
    dés qu'elle arrive a la fin elle reste a la dernière image
    """

    def actualise_index_texture(self) -> None:
        """permet de mettre a jour l'index du diapo"""
        if self.get_index_texture() >= self.get_len_texture_pack():
            self.set_index_texture(self.get_len_texture_pack() - 1)
