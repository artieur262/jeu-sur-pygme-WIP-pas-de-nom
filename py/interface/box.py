import pygame
from py.objet.objetVisuel import ObjetVisuel

class Box(ObjetVisuel):
    """Box est une zone qui a une image et un texte
    Args:
        ObjetVisuel (ObjetVisuel): est la zone de l'objet graphique
    """

    def __init__(self, taille : tuple[int, int], ellement : list[ObjetVisuel] ):
        super().__init__((0, 0), taille)
        self.ellement = ellement

    def set_pos(self, valu: tuple[int, int]):
        """defini la position de l'objet"""
        decalage = soustract_2_tuple(valu, self.coordonnee)
        super().set_pos(valu)
        for i in self.ellement:
            i.add_pos(decalage)
    

    def set_size(self, valu):
        super().set_size(valu)
        self.actualiser()
    
        

    def actualiser(self,box:"Box" = None):
        """repositionne les ellement dans la box"""
        for i in self.ellement:
            if isinstance(i, "Box"):
                i.actualiser(self)
            


    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ):
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        for i in self.ellement:
            i.afficher(decalage, surface)


class VBox(Box):
    """Box est une zone qui a une image et un texte
    Args:
        ObjetVisuel (ObjetVisuel): est la zone de l'objet graphique
        position_H (str): est la position de la box (left, center, right)
        position_V (str): est la position de la box (up, center, down)
        justify_content (str): est la justification du contenu (space-between, space-around, space-evenly)
    """

    def __init__(self, taille : tuple[int, int], ellement : list[ObjetVisuel]):
        super().__init__(taille, ellement)
        self.ecart = 0
        self.ecart_auto = True
        self.position_H = "center"
        self.position_V = "center"
        self.justify_content = "space-between"

        self.actualiser()
    
    def somme_hauteur_ellement(self) -> int:
        """somme la longueur de tout les ellement"""
        return sum([i.get_size()[1] for i in self.ellement])

    def __actualiser_ecart(self):
        """actualise l'ecart entre les ellement"""
        if self.ecart_auto:
            match self.justify_content:
                case "space-between":
                    self.ecart = (self.taille[1] - self.somme_hauteur_ellement()) / (len(self.ellement) - 1)
                case "space-around":
                    self.ecart = (self.taille[1] - self.somme_hauteur_ellement()) / len(self.ellement) 
                case "space-evenly":
                    self.ecart = (self.taille[1] - self.somme_hauteur_ellement()) / (len(self.ellement) + 1)            

    def __actualiser_position(self):
        """actualise la position des ellement"""
        self.__actualiser_ecart()
        centre = self.get_center()
        somme_hauteur = self.somme_hauteur_ellement()
        nbre_ellement = len(self.ellement)
        pos_suivant = 0
        match self.position_V:
                case "up":
                    pos_suivant = self.coordonnee[1]
                case "center":
                    match self.justify_content:
                        case "space-between":
                            pos_suivant = self.coordonnee[1]
                        case "space-around":
                            pos_suivant = self.coordonnee[1] + self.ecart / 2
                        case "space-evenly":
                            pos_suivant = self.coordonnee[1] + self.ecart 
                        case _:
                            pos_suivant = self.coordonnee[1]
                case "down":
                    pos_suivant=self.coordonnee[1] + self.get_size()[1] - somme_hauteur - (nbre_ellement-1) * self.ecart
                    


        for i, ellement in enumerate(self.ellement):
            taille_ellement = ellement.get_size()
            match self.position_H:
                case "left":
                    ellement.set_pos((self.coordonnee[0], 0))
                case "center":
                    ellement.set_pos((centre[0] - taille_ellement[0] / 2, 0))
                case "right":
                    ellement.set_pos((self.coordonnee[0] + self.get_size()[0] - taille_ellement[0], 0))
            pos_ellement = ellement.get_pos()
            # self.position_V:
            ellement.set_pos((pos_ellement[0], pos_suivant))
            pos_suivant += taille_ellement[1] + self.ecart

            

    def actualiser(self):
        """actualise la position des ellement"""
        self.__actualiser_position()
        super().actualiser()

    def ajouter_ellement(self, ellement: ObjetVisuel):
        """ajoute un ellement à la box"""
        self.ellement.append(ellement)
        self.actualiser()
        
class HBox(Box):
    """Box est une zone qui a une image et un texte
    Args:
        ObjetVisuel (ObjetVisuel): est la zone de l'objet graphique
        position_H (str): est la position de la box (left, center, right)
        position_V (str): est la position de la box (up, center, down)
        justify_content (str): est la justification du contenu (space-between, space-around, space-evenly)
    """

    def __init__(self, taille : tuple[int, int], ellement : list[ObjetVisuel]):
        super().__init__(taille, ellement)
        self.ecart = 0
        self.ecart_auto = True
        self.position_H = "center"
        self.position_V = "center"
        self.justify_content = "space-between"

        self.actualiser()

    def set_justify_content(self, justify_content: str) -> None:
        """set la justification du contenu
        args:
            justify_content (str): est la justification du contenu (space-between, space-around, space-evenly)
        """
        self.justify_content = justify_content
        self.__actualiser_position()
     

    def somme_longueur_ellement(self, fin:int = None) -> int:
        """somme la longueur de tout les ellement"""
        if fin is None:
            fin = len(self.ellement)
        return sum([self.ellement[i].get_size()[0] for i in range(fin)])

    def __actualiser_ecart(self):
        """actualise l'ecart entre les ellement"""
        if self.ecart_auto:
            match self.justify_content:
                case "space-between":
                    self.ecart = (self.taille[0] - self.somme_longueur_ellement()) / (len(self.ellement) - 1)
                case "space-around":
                    self.ecart = (self.taille[0] - self.somme_longueur_ellement()) / len(self.ellement) 
                case "space-evenly":
                    self.ecart = (self.taille[0] - self.somme_longueur_ellement()) / (len(self.ellement) + 1)


    def __actualiser_position(self):
        """actualise la position des ellement"""
        self.__actualiser_ecart()
        centre = self.get_center()
        somme_longueur = self.somme_longueur_ellement()
        nbre_ellement = len(self.ellement)
        pos_suivant = 0

        match self.position_H:
            case "left":
                pos_suivant = self.coordonnee[0]
            case "center":
                match self.justify_content:
                    case "space-between":
                        pos_suivant=self.coordonnee[0] 
                    case "space-around":
                        pos_suivant=self.coordonnee[0] + self.ecart / 2
                    case "space-evenly":
                        pos_suivant=self.coordonnee[0] + self.ecart 
                    case _:
                        pos_suivant=self.coordonnee[0]
            case "right":
                pos_suivant=self.coordonnee[0] + self.get_size()[0] - somme_longueur - (nbre_ellement-1) * self.ecart


        for i, ellement in enumerate(self.ellement):
            taille_ellement = ellement.get_size()
            
            match self.position_V:
                case "up":
                    ellement.set_pos((0, self.coordonnee[1]))
                case "center":
                    ellement.set_pos((0, centre[1] - taille_ellement[1] / 2))
                case "down":
                    ellement.set_pos((0, self.coordonnee[1] + self.get_size()[1] - taille_ellement[1]))
            pos_ellement = ellement.get_pos()
            # self.position_H:
            ellement.set_pos((pos_suivant, pos_ellement[1]))
            pos_suivant += taille_ellement[0] + self.ecart
    
    def actualiser(self):
        """actualise la position des ellement"""
        self.__actualiser_position()
        super().actualiser()
    
    def ajouter_ellement(self, ellement: ObjetVisuel):
        """ajoute un ellement à la box"""
        self.ellement.append(ellement)
        self.actualiser()



def soustract_2_tuple(t1:tuple[int,int], t2:tuple[int,int]) -> tuple[int,int]:
    """soustrait deux tuple de deux int"""
    return (t1[0] - t2[0], t1[1] - t2[1])