from py.block.activateur.activateur import ActivateurPlatforme
from py.objet.zone import Zone3D
from py.interface.class_clavier import Clavier


class Bouton(ActivateurPlatforme):
    """Bouton est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int, rayon_dectect: int):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti)
        self.__rayon_dectect = rayon_dectect

    
    def get_zone_dectect(self) -> Zone3D:
        """permet de savoir si le bloc logique est actif
        Args:
            axe (int, optional): axe de la zone de détection. Defaults to -1, ce qui signifie que la zone de détection est dans les 3 axes.
                                la valeur de axe correspond à l'axe qui ne sera pas pris en compte pour la zone de détection.
                                axe = 0 pour l'axe x, axe = 1 pour l'axe y, axe = 2 pour l'axe z.
        

        """
        pos= []
        taille = []
        for i in range(3):
                pos.append(self.get_pos()[i] - self.__rayon_dectect)
                taille.append(self.get_size()[i] + self.__rayon_dectect*2)

class BoutonPush(Bouton):
    """Bouton_push est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int, rayon_dectect: int):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti, rayon_dectect)
    
    def activation(self, map):
        """permet d'activer le bloc logique"""
        clavier:Clavier = map.get_game().clavier
        touche : dict[str, int] = map.get_game().get_touche()
        joueur: Zone3D = map.get_playeur()

        if clavier.get_pression(touche["interaction"]) == "presser" and self.__rayon_dectect.collision(joueur.get_pos(), joueur.get_size()):
            self.set_activer(True)
        else:
            self.set_activer(False)


class BoutonSwitch(Bouton):
    """Bouton_switch est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int, zone_dectect: Zone3D):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti, zone_dectect)
    
    def activation(self, map):
        """permet d'activer le bloc logique"""
        clavier:Clavier = map.get_game().clavier
        touche : dict[str, int] = map.get_game().get_touche()
        joueur: Zone3D = map.get_playeur()

        if clavier.get_pression(touche["interaction"]) == "vien_presser" and self.__rayon_dectect.collision(joueur.get_pos(), joueur.get_size()):
            self.set_activer(not self.get_activer())


class BoutonImpulse(Bouton):
    """Bouton_impulse est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int, zone_dectect: Zone3D):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti, zone_dectect)
    
    def activation(self, map):
        """permet d'activer le bloc logique"""
        clavier:Clavier = map.get_game().clavier
        touche : dict[str, int] = map.get_game().get_touche()
        joueur: Zone3D = map.get_playeur()

        if clavier.get_pression(touche["interaction"]) == "vien_presser" and self.__rayon_dectect.collision(joueur.get_pos(), joueur.get_size()):
            self.set_activer(True)
        else:
            self.set_activer(False)

