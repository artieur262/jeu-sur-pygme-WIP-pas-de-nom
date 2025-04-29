from py.objet.objetUnicolor import ObjetUnicolor3D


class Plateforme(ObjetUnicolor3D):
    """Plateforme est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int]):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur)
    


