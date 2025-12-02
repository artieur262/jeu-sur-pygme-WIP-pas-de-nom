"""Module de gestion de la caméra dans le jeu.
Ce module contient la classe Camera qui permet de gérer
la position et le zoom de la caméra dans le jeu.
"""
from py.objet.zone import Zone2D


class Camera:
    """La classe Camera permet de gérer la position et le zoom de la caméra dans le jeu."""

    def __init__(
        self, position: Zone2D,  zoom: float = 1.0
    ) -> None:
        """Initialise la caméra avec une position et un zoom.

        Args:
            position (Zone2D): La zone 2D représentant la position de la caméra.
            zoom (float, optional): Le niveau de zoom de la caméra. Par défaut à 1.0.
        """
        self.position = position
        self.zoom = zoom    