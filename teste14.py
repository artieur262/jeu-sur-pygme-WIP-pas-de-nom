import pygame
from py.menu.menu import Menu, ElementInterface
from py.interface.visu_it import ObjetVisuel2DInterface
from py.interface.box import Box
from py.interface.bouton import Bouton, ModeBouton
from py.interface.class_clavier import Clavier, Souris
from py.graphique.texture_generateur import FONCTIONS, TextureGenerateur
from py.graphique.actualisation_pygame import actualise_event, screen, Event


# from py.grap
class MenuTest(Menu):
    """MenuTest est une classe de test pour la classe Menu"""

    def tour(self, event: set[str]):
        screen.fill((0, 0, 0))
        self.afficher()
        pygame.display.flip()
        a: Bouton = self._element_mere.get_element()[0]
        if a.point_dans_objet((self.souris.get_pos())):
            if self.souris.get_pression(1) >= 2:
                a.set_animation(2)
            else:
                a.set_animation(1)
        else:
            a.set_animation(0)


def main():
    """test pour la classe Menu"""
    clavier = Clavier()
    souris = Souris()
    boite_mere = Box((0, 0), (300, 300), [], False)
    boite_mere.get_element()
    bouton1 = Bouton(
        [50, 50],
        [
            TextureGenerateur(
                FONCTIONS["rectange_avec_bordure"], (255, 0, 0), (125, 0, 0), 5
            ),
            TextureGenerateur(
                FONCTIONS["rectange_avec_bordure"], (0, 255, 0), (0, 125, 0), 5
            ),
            TextureGenerateur(
                FONCTIONS["rectange_avec_bordure"], (0, 0, 255), (0, 0, 125), 5
            ),
        ],
        (200, 50),
        ModeBouton.CLIQUE,
    )
    boite_mere.ajouter_element(bouton1)
    menu = MenuTest(clavier, souris, boite_mere)
    menu.play()


if __name__ == "__main__":
    main()
