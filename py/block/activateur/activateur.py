from py.block.plateforme import Plateforme
# from py.game.game import Map



class Activateur:
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, sorti: int):
        """initialise le bouton"""
        self.__sorti = sorti
        self.__activer = False

    def get_activer(self) -> bool:
        """permet de savoir si le bloc logique est actif"""
        return self.__activer

    def set_activer(self, activer: bool) -> None:
        """permet de changer l'etat du bloc logique"""
        self.__activer = activer

    def activation(self, map) -> None:
        """permet d'activer le bloc logique"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def get_activation(self, output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if self.__activer:
            output.add(self.__sorti)
    
    def ajouter_map(self, map) -> None:
        """ajoute la map"""
        map.add_activateur(self)


class ActivateurPlatforme(Plateforme, Activateur):
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """
    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int):
        """initialise le bouton"""
        Plateforme.__init__(self, coordonnee, taille, couleur)
        Activateur.__init__(self, sorti)

    def ajouter_map(self, map):
        Activateur.ajouter_map(self,map)
        Plateforme.ajouter_map(self,map)