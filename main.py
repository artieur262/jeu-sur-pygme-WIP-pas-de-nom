import pygame
from py.interface.class_clavier import Clavier, Souris
# from py.graphique.graphique import screen
# from py.graphique.actualisation_pygame import actualise_event, change_fullscreen
from py.game.game import Game
from py.block.plateforme import Plateforme
from py.block.playeur import Playeur
# from py.block.activateur.bouton_flotant import BoutonPush, BoutonSwitch

# from py.block.


if __name__ == "__main__":
    clavier = Clavier()
    souris = Souris()
    touche = {
        "haut": pygame.K_z,
        "bas": pygame.K_s,
        "gauche": pygame.K_q,
        "droite": pygame.K_d,
        "sauter": pygame.K_SPACE,
        "interagir": pygame.K_e,
        "inventaire": pygame.K_i,
        "pause": pygame.K_ESCAPE,
        "debug": pygame.K_F12,
    }
    game = Game(clavier, souris, touche)
    map_ = game.map
    # map.add_plateforme(Plateforme([120, 0, 50], (10, 100, 100), (0, 0, 255)))
    obj1 = Plateforme([0, 150, 50], (10, 100, 100), (0, 225, 0))
    obj1.ajouter_map(map_)
    p1 = Playeur([0, 0, 0], 20, (255, 255, 255))
    p1.ajouter_map(map_)

    game.set_plan(0)
    game.run()
    pygame.quit()
    exit()
