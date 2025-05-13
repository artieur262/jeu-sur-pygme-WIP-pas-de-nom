from py.block.plateforme import Plateforme
# from py.game.game import Map

class Activateur(Plateforme):
    """Activateur est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur)
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
        pass

    def get_activation(self, output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if self.__activer:
            output.add(self.__sorti)
        
            