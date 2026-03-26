from py.interface.element_it import ElementInterface
from py.objet.objet_visuel import ObjetVisuel2D


class ScrolBar(ObjetVisuel2D, ElementInterface):
    """ScrolBar est une interface qui affiche une barre de scrol

    Args:
        coordonnee (list[int]): est la coordonnee de la barre de scrol
        taille (tuple[int, int]): est la taille de la barre de scrol
    """

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int],
        borne: tuple[int, int],
        texture_fond: str,
        texture_barre: str,
        axe: int,
        parent: ElementInterface = None,
    ):
        ObjetVisuel2D.__init__(self, coordonnee, taille, texture_fond)
        ElementInterface.__init__(self, coordonnee, taille, False, parent)
        self.axe = axe
        self.borne = borne
        self.texture_barre = ObjetVisuel2D(
            [i for i in self.get_pos()],
            (taille[0], taille[1] // 4) if axe == 0 else (taille[0] // 4, taille[1]),
            texture_barre,
        )
        self.texture_barre.add_pos_in_axe(axe, borne[0])

    def actualise_taille(self):
        """actualise_taille actualise la taille de la barre de scrol"""
        pass  # pylint: disable=unnecessary-pass
        # à faire

    def get_ratio(self):
        """get_ratio retourne le ratio de la barre de scrol

        Returns:
            float: le ratio de la barre de scrol
        """
        return (
            +self.texture_barre.get_pos()[self.axe]
            - self.get_pos()[self.axe]
            - self.borne[0]
        ) / (self.get_size()[self.axe] - self.borne[1] - self.borne[0])

    def afficher(self, decalage=None, surface=None):
        return super().afficher(decalage, surface) and self.texture_barre.afficher(
            decalage, surface
        )


class ScrolBarHorizontal(ScrolBar):
    """ScrolBarHorizontal est une interface qui affiche une barre de scrol horizontal"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int],
        borne: tuple[int, int],
        texture_fond: str,
        texture_barre: str,
        parent: ElementInterface = None,
    ):
        super().__init__(
            coordonnee,
            taille,
            borne,
            texture_fond,
            texture_barre,
            0,
            parent,
        )


class ScrolBarVertical(ScrolBar):
    """ScrolBarVertical est une interface qui affiche une barre de scrol vertical"""

    def __init__(
        self,
        coordonnee: list[int],
        taille: tuple[int, int],
        borne: tuple[int, int],
        texture_fond: str,
        texture_barre: str,
        parent: ElementInterface = None,
    ):
        super().__init__(
            coordonnee,
            taille,
            borne,
            texture_fond,
            texture_barre,
            1,
            parent,
        )
