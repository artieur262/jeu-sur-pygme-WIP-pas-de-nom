import pygame

from py.graphique.texture_generateur import FONCTIONS, TextureGenerateur
from py.graphique.actualisation_pygame import actualise_event, change_fullscreen, screen
from py.interface.class_clavier import Clavier, Souris

if __name__ == "__main__":
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
