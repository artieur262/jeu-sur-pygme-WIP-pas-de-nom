from py.block.activateur.activateur import Activateur
from py.objet.zone import Zone3D
from py.interface.class_clavier import Clavier

class Bouton(Activateur):
    """Bouton est une zone qui a pour but d'être affiché sur une surface
    Args:
        Zone (Zone): est la zone de l'objet graphique
    """

    def __init__(self, coordonnee: list[int], taille: tuple[int, int, int], couleur: tuple[int, int, int], sorti: int, zone_dectect: Zone3D):
        """initialise le bouton"""
        super().__init__(coordonnee, taille, couleur, sorti)
        self.__zone_dectect = zone_dectect



class BoutonPush(Bouton):
    """Bouton_push est une zone qui a pour but d'être affiché sur une surface
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

        if clavier.get_pression(touche["interaction"]) == "presser" and self.__zone_dectect.collision(joueur.get_pos(), joueur.get_size()):
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

        if clavier.get_pression(touche["interaction"]) == "vien_presser" and self.__zone_dectect.collision(joueur.get_pos(), joueur.get_size()):
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

        if clavier.get_pression(touche["interaction"]) == "vien_presser" and self.__zone_dectect.collision(joueur.get_pos(), joueur.get_size()):
            self.set_activer(True)
        else:
            self.set_activer(False)