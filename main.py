import pygame
from py.interface.class_clavier import Clavier, Souris
from py.graphique.graphique import screen
from py.graphique.actualisation_pygame import actualise_event, change_fullscreen
from py.game.game import Game
from py.block.plateforme import Plateforme
from py.block.playeur import Playeur


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
    }
    game = Game(clavier, souris, touche)
    map=game.map
    map.add_plateforme(Plateforme([120, 0, 50], (10, 100, 100), (0, 0, 255)))
    map.add_plateforme(Plateforme([150, 0, 50], (10, 100, 100), (0,225,0)))
    map.add_playeur(Playeur([0, 0, 0], (20, 20, 10), (255,255,255)))
    game.set_plan(2)
    game.run()
    pygame.quit()
    exit()