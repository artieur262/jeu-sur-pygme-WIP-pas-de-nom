"""
Ce module contient la fonction genere_image qui permet de generer une image a partir
    d'une str ou d'un tuple ou d'une surface ou d'une texture generateur
il contient la fonction:
- genere_image
"""

import pygame

from py.graphique.image import Image
from py.graphique.texture_generateur import TextureGenerateurFixe, TextureGenerateur


def genere_image(
    entre: (
        str
        | tuple[str, tuple[int, int]]
        | pygame.Surface
        | Image
        | TextureGenerateurFixe
        | TextureGenerateur
    ),
    taille: tuple[int, int] = None,
) -> Image:
    """genere une image a partir d'une str ou d'un tuple
    pour generer une image a partir d'un TextureGenerateur, la taille doit être spécifiée
    Args:
        entre (str or tuple): str ou tuple pour generer une image
        taille (tuple[int, int], optional): taille de l'image. Defaults to None.
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
    elif isinstance(entre, TextureGenerateurFixe):
        return entre.generer_texture_sans_taille()
    elif isinstance(entre, TextureGenerateur):
        if taille is None:
            raise ValueError(
                "la taille doit être spécifiée pour generer une image a partir"
                + " d'un TextureGenerateur"
            )
        return entre.generer_texture(taille)
    else:
        raise ValueError("est un type non pris en charge pour generer une image")
