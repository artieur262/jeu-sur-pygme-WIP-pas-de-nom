import pygame

from py.graphique.texture_generateur import FONCTIONS, TextureGenerateur
from py.graphique.actualisation_pygame import actualise_event, change_fullscreen, screen
from py.interface.class_clavier import Clavier, Souris
from py.interface.bouton import Bouton, ModeBouton
from py.objet.objet_visuel import ObjetVisuel2D


def main1():
    """test pour la classe TextureGenerateur"""
    event = {}
    souris = Souris()
    clavier = Clavier()
    texture_gen = TextureGenerateur(
        FONCTIONS["cercle_avec_bordure"], (255, 0, 0), (0, 255, 0), 5
    )
    texture = texture_gen.generer_texture((200, 200))

    while "quitter" not in event:
        event = actualise_event(clavier, souris)
        if "redimentione" in event:
            print("redimentione")
        if clavier.get_pression(pygame.K_f) == 1:
            change_fullscreen()
        screen.fill((0, 0, 0))
        screen.blit(texture, (100, 100))
        pygame.display.flip()
    pygame.quit()
    exit()


def main2():
    """test pour la classe TextureGenerateur"""
    event = {}
    souris = Souris()
    clavier = Clavier()
    bouton = Bouton(
        [100, 100],
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

    objet = ObjetVisuel2D(
        (100, 100),
        (200, 50),
        TextureGenerateur(FONCTIONS["rectange_full_couleur"], (125, 125, 125)),
    )

    while "quitter" not in event:
        event = actualise_event(clavier, souris)
        if "redimentione" in event:
            print("redimentione")
        if clavier.get_pression(pygame.K_f) == 1:
            change_fullscreen()
        if bouton.point_dans_objet(souris.get_pos()):
            if souris.get_pression(1) >= 1:
                print("clique")
                bouton.set_animation(2)
            else:
                print("hover")
                bouton.set_animation(1)
        else:
            bouton.set_animation(0)
        screen.fill((0, 0, 0))
        objet.afficher((-100, -100))
        bouton.afficher()
        pygame.display.flip()
    pygame.quit()
    exit()


if __name__ == "__main__":
    main2()
