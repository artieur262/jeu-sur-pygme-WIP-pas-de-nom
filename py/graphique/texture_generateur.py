"""Ce module contient la classe TextureGenerateur qui génère une texture à partir
d'un algorithme donné
"""

import pygame
from py.graphique.image import Image


class TextureGenerateur:
    """Génère une texture à partir d'un algorithme donné
    Args:
        algorithme (callable): est l'algorithme qui génère la texture
            l'algorithme doit être dans le module FONCTIONS
        *args: sont les arguments de l'algorithme
        **kwargs: sont les arguments de l'algorithme
    """

    def __init__(self, algorithme: callable, *args, **kwargs):
        self.__algorithme: callable = algorithme
        self.__args = args
        self.__kwargs = kwargs

    def generer_texture(self, taille: tuple[int, int]) -> Image:
        """Génère une texture à partir de l'algorithme donné"""
        return self.__algorithme(taille, *self.__args, **self.__kwargs)

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour pouvoir le sauvegarder"""
        return {
            "name": self.__class__.__name__,
            "algorithme": self.__algorithme.__name__,
            "args": self.__args,
            "kwargs": self.__kwargs,
        }

    @staticmethod
    def from_dict(data: dict) -> "TextureGenerateur":
        """Convertit un dictionnaire en objet"""
        algorithme = FONCTIONS[data["algorithme"]]
        args = data["args"]
        kwargs = data["kwargs"]
        return TextureGenerateur(algorithme, *args, **kwargs)


class TextureGenerateurFixe(TextureGenerateur):
    """Génère une texture à partir d'une texture fixe
    Args:
        algorithme (callable): est l'algorithme qui génère la texture
        taille (tuple[int, int]): est la taille de la texture
        *args: sont les arguments de l'algorithme
        **kwargs: sont les arguments de l'algorithme
    """

    def __init__(self, algorithme: callable, taille: tuple[int, int], *args, **kwargs):
        super().__init__(algorithme, taille, *args, **kwargs)
        self.taille = taille

    def generer_texture_sans_taille(self) -> Image:
        """Génère une texture à partir de la texture fixe"""
        return super().generer_texture(self.taille)

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour pouvoir le sauvegarder"""
        data = super().to_dict()
        data["taille"] = self.taille
        return data


def rectange_avec_bordure(
    taille: tuple[int, int],
    couleur_fond: tuple[int, int, int],
    couleur_bordure: tuple[int, int, int],
    bordure: int,
):
    """Génère une texture de bordure"""
    surface = pygame.Surface(taille)
    surface.fill(couleur_fond)
    pygame.draw.rect(surface, couleur_bordure, (0, 0, taille[0], taille[1]), bordure)
    return Image(surface)


def cercle_avec_bordure(
    taille: tuple[int, int],
    couleur_fond: tuple[int, int, int],
    couleur_bordure: tuple[int, int, int],
    bordure: int,
):
    """Génère une texture de bordure"""
    surface = pygame.Surface(taille)
    surface.fill((0, 0, 0))

    pygame.draw.circle(
        surface,
        couleur_bordure,
        (taille[0] // 2, taille[1] // 2),
        min(taille) // 2,
    )
    pygame.draw.circle(
        surface,
        couleur_fond,
        (taille[0] // 2, taille[1] // 2),
        min(taille) // 2 - bordure,
    )
    return Image(surface)


def rectange_full_couleur(taille: tuple[int, int], couleur: tuple[int, int, int]):
    """Génère une texture rectangle pleine de couleur"""
    surface = pygame.Surface(taille)
    surface.fill(couleur)
    return Image(surface)


FONCTIONS: dict[str, callable] = {
    I.__name__: I
    for I in (rectange_avec_bordure, cercle_avec_bordure, rectange_full_couleur)
}
