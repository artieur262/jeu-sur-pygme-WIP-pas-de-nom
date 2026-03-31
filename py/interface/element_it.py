import pygame
from py.objet.zone import Zone2D


class ElementInterface(Zone2D):
    """Interface pour les éléments interactifs.

    args:
        taille_auto (bool): indique si la taille de l'élément doit être automatiquement ajustée
            en fonction de son contenu.
        parent (ElementInterface, optional): est l'interface parente. Defaults to None.
    """

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        taille_auto: bool,
        parent: "ElementInterface" = None,
    ) -> None:
        """initialise l'interface

        Args:
            parent (ElementInterface, optional): est l'interface parente. Defaults to None.
        """
        Zone2D.__init__(self, position, size)
        self._taille_auto = taille_auto
        self._parent = parent

    def get_parent(self) -> "ElementInterface":
        """get l'interface parente de l'interface"""
        return self._parent

    def set_parent(self, parent: "ElementInterface") -> None:
        """set l'interface parente de l'interface"""
        if self._parent is not None and parent is not None:
            raise ValueError("L'interface a déjà un parent.")
        self._parent = parent

    def retirer_parent(self) -> None:
        """retire l'interface parente de l'interface"""
        self._parent = None

    def actualise_taille(self) -> None:
        """actualise la taille de la box en fonction de ses element"""
        raise NotImplementedError(
            "Cette méthode doit être implémentée par les sous-classes."
        )

    def afficher(
        self, decalage: tuple[int, int] = None, surface: pygame.Surface | None = None
    ) -> None:
        """affiche l'interface sur la surface donnée

        Args:
            surface (pygame.Surface): est la surface sur laquelle afficher l'interface
        """
        raise NotImplementedError(
            "Cette méthode doit être implémentée par les sous-classes."
        )
