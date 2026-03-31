from py.objet.objet_visuel import ObjetVisuel2D
from py.interface.element_it import ElementInterface
from py.graphique.image import Image


class ObjetVisuel2DInterface(ObjetVisuel2D, ElementInterface):
    """ObjetVisuel2DIterface est une interface qui affiche un objet graphique

    Args:
        coordonnee (list[int]): est la coordonnee de l'objet graphique
        taille (tuple[int, int]): est la taille de l'objet graphique
        texture (Image | str): est la texture de l'objet graphique
        parent (ElementInterface, optional): est le parent de l'objet graphique. Defaults to None.
        auto_actualise (bool, optional): est si l'objet graphique doit être actualisé automatiquement. Defaults to True.
    """

    def __init__(
        self,
        pos: tuple[int, int],
        taille: tuple[int, int],
        texture: Image | str,
        parent: ElementInterface = None,
        auto_actualise: bool = True,
    ):
        ObjetVisuel2D.__init__(self, pos, taille, texture)
        ElementInterface.__init__(self, pos, taille, False, parent)
        self._auto_actualise = auto_actualise

    def actualise_taille(self):
        """actualise la taille de la visualisation en fonction de ses elements"""
        pass  # pylint: disable=unnecessary-pass
        # à faire
