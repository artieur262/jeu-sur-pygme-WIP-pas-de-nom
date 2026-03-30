"""
Ce module contient la fonction genere_image qui permet de generer une image a partir
    d'une str ou d'un tuple ou d'une surface ou d'une texture generateur
il contient la fonction:
- genere_image
"""

import pygame

from py.graphique.image import Image
from py.graphique.texture_generateur import TextureGenerateur


def genere_image(
    entre: (
        str | tuple[str, tuple[int, int]] | pygame.Surface | Image | TextureGenerateur
    ),
) -> Image:
    """genere une image a partir d'une str ou d'un tuple
    Args:
        entre (str or tuple): str ou tuple pour generer une image
    Returns:
        Image: image generé
    """
    if isinstance(entre, str):
        return Image(entre)
    elif isinstance(entre, tuple):
        return Image(entre[0], entre[1])
    elif isinstance(entre, pygame.Surface):
        return Image(entre)
    elif isinstance(entre, Image):
        return entre
    elif isinstance(entre, TextureGenerateur):
        return entre.generer_texture()
    else:
        raise ValueError("entre doit être une str ou un tuple")
