"""module pour actualiser les événement de pygame"""

# pylint: disable=no-member
from graphique import screen, pygame
from class_clavier import Clavier, Souris


def actualise_event(clavier: Clavier, souris: Souris):
    """actualise les événement et retourne les événement autre que les touches et les cliques"""
    event_autre = set()
    souris.actualise_position()
    souris.actualise_all_clique()
    clavier.actualise_all_touche()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            event_autre.add("quitter")
        elif event.type == pygame.VIDEORESIZE:
            event_autre.add("redimentione")

        elif event.type == pygame.KEYDOWN:
            if event.key in clavier.dict_touches:
                clavier.change_pression(event.key, "vien_presser")
        elif event.type == pygame.KEYUP:
            if event.key in clavier.dict_touches:
                clavier.change_pression(event.key, "vien_lacher")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in souris.dict_clique:
                souris.change_pression(event.button, "vien_presser")

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in souris.dict_clique:
                souris.change_pression(event.button, "vien_lacher")
    return event_autre


def get_fullscreen():
    """retourne si on est en plein écran"""
    return screen.get_flags() & pygame.FULLSCREEN


def change_fullscreen(
    touche_f11: str,
):
    """change le mode plein écran"""
    global screen  # pylint: disable=global-statement
    if touche_f11 == "vien_presser":
        if get_fullscreen():
            screen.fill((0, 0, 0))
            pygame.display.update()
            # premet d'eviter un bug graphique avec le plein écran
            # le bug est un clignotement noir de l'écran quand on change de mode
            # si l'écran est noir donc on ne le voit pas
            # oui je corrige un bug graphique à la schlague
            # car en plus le bug vien de pygame et pas de moi
            screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)

        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # pygame.display.update()
