import pygame
from py.graphique.actualisation_pygame import actualise_event, screen, Event
from py.interface.class_clavier import Clavier, Souris
from py.interface.element_it import ElementInterface


class Menu:
    """Menu est une interface qui affiche un objet graphique"""

    def __init__(
        self,
        clavier: Clavier,
        souris: Souris,
        element_mere: ElementInterface,
    ):
        """initialise le menu"""
        self.clavier = clavier
        self.souris = souris
        self._element_mere = element_mere
        self._encours = False

    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = screen,
    ) -> bool:
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        Returns:
            bool: si l'objet est affiché
        """
        if decalage is None:
            decalage = (0, 0)
        if surface is None:
            surface = pygame.display.get_surface()
        return self._element_mere.afficher(decalage, surface)

    def actualise_taille(self):
        """actualise la taille de la visualisation en fonction de ses elements"""
        self._element_mere.set_size(screen.get_size())
        self._element_mere.actualise_taille()

    def play(self):
        """permet de faire le menu jouer"""
        self._encours = True
        while self._encours:
            # Logique de jeu du menu
            event = actualise_event(self.clavier, self.souris)

            if Event.QUITTER in event:
                self.stop()
            if Event.REDIMENTIONE in event:
                # Gérer le redimensionnement
                self.actualise_taille()
            self.tour(event)

    def tour(self, event: set[Event]):
        """permet de faire le menu faire un tour"""
        raise NotImplementedError(
            "La méthode tour doit être implémentée dans une classe fille."
        )

    def stop(self):
        """permet de faire le menu s'arrêter"""
        self._encours = False
