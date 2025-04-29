from py.graphique.objetGraphique import ObjetGraphique
from py.interface.class_clavier import Souris


class Bouton(ObjetGraphique):
    """Bouton est un objet graphique qui a une image et un texte
    Args:
        ObjetGraphique (ObjetGraphique): est l'objet graphique
    """
    def __init__(self, coordonnee: list, textures: list[str], taille: tuple[int, int], mode: str = "clique"):
        """initialise le bouton"""
        super().__init__(coordonnee, textures, taille)
        self.mode = mode
        self.__actif = False
        self.__clique = False
        self.__survol = False
    
    def get_mode(self) -> str:
        """get le mode du bouton"""
        return self.mode

    def set_actif(self, actif: bool) -> None:
        """set l'etat actif du bouton"""
        self.__actif = actif
        self.actualise_animation()
    
    def get_actif(self) -> bool:
        """get l'etat actif du bouton"""
        return self.__actif
    
    def actualise_animation(self) -> None:
        """actualise l'animation du bouton"""
        match self.mode:
            case "on/off":
                if self.__actif:
                    if self.__survol:
                        self.set_animation(3)
                    else:
                        self.set_animation(2)
                elif self.__survol:
                    self.set_animation(1)
                else:
                    self.set_animation(0)
            case "clique":
                if self.__survol:
                    self.set_animation(1)
                else:
                    self.set_animation(0)

    def cliquer(self, pos:tuple[int,int]) -> bool:
        """permet de savoir si le bouton est cliqué"""
        self.__clique = self.point_dans_objet(pos)
        return self.__clique

    def get_clique(self) -> bool:
        """get l'etat du bouton"""
        return self.__clique
    
    def hover(self, pos:tuple[int,int]) -> bool:
        """permet de savoir si le bouton est survolé"""
        self.__survol = self.point_dans_objet(pos)
        self.actualise_animation()
        return self.__survol

    def get_survol(self) -> bool:
        """get l'etat du bouton"""
        return self.__survol



    

    
            
    
