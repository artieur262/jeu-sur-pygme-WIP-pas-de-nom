from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py.game.game import Game
    from py.block.playeur import Playeur
    from py.block.plateforme import Plateforme
    from py.block.activateur.activateur import Activateur
    from py.block.activable.activable import Activable
    from py.logique.bloc_logique import Logique
    from py.objet.objet_visuel import ObjetVisuel3D
    from py.objet.zone import Zone3D

# from py.logique.bloc_logique import Logique


class Map:
    """Map est une classe qui permet de gerer la map
    Args:
        Map (Map): est la map
    """

    def __init__(self, game="Game"):
        """initialise la map"""
        self.__game = game
        self.__colision: set["Zone3D"] = set()
        self.__playeur: "Playeur" = None
        self.__afficher: set["ObjetVisuel3D"] = set()
        self.__graviter: bool = False
        self.__logique: set["Logique"] = set()
        self.__activateur: set["Activateur"] = set()
        self.__activable: set["Activable"] = set()
        self.__poussable: set = set()
        self.__signal: set[int] = set()

    def actualiser_activation(self) -> None:
        """actualise l'activation des blocs logiques"""
        nouveau_signal: set[int] = set()
        for i in self.__logique:
            i.get_activation(self.__signal, nouveau_signal)
        self.__signal = nouveau_signal

    def add_plateforme(self, plateforme: "Plateforme") -> None:
        """ajoute une plateforme à la map"""
        self.__colision.add(plateforme)
        self.__afficher.add(plateforme)

    def add_activable(self, activable: "Activable") -> None:
        """ajoute un activable à la map"""
        self.__activable.add(activable)

    def remove_activable(self, activable: "Activable") -> None:
        """retire un activable de la map"""
        self.__activable.remove(activable)

    def remove_plateforme(self, plateforme: "Plateforme") -> None:
        """retire une plateforme de la map"""
        self.__colision.remove(plateforme)
        self.__afficher.remove(plateforme)

    def add_colision(self, zone: "Zone3D") -> None:
        """ajoute une zone de colision à la map"""
        self.__colision.add(zone)

    def remove_colision(self, zone: "Zone3D") -> None:
        """retire une zone de colision de la map"""
        self.__colision.remove(zone)

    def add_afficher(self, objet: "ObjetVisuel3D") -> None:
        """ajoute un objet à afficher à la map"""
        self.__afficher.add(objet)

    def remove_afficher(self, objet: "ObjetVisuel3D") -> None:
        """retire un objet à afficher de la map"""
        self.__afficher.remove(objet)

    def add_playeur(self, playeur: "Playeur") -> None:
        """ajoute un playeur à la map"""
        self.__playeur = playeur
        self.__afficher.add(playeur)
        self.__colision.add(playeur)

    def add_logique(self, logique: "Logique") -> None:
        """ajoute une logique à la map"""
        self.__logique.add(logique)

    def remove_logique(self, logique: "Logique") -> None:
        """retire une logique de la map"""
        self.__logique.remove(logique)

    def affichable(self) -> set["ObjetVisuel3D"]:
        """affiche la map"""
        return self.__afficher

    def get_game(self) -> "Game":
        """get le jeu"""
        return self.__game

    def get_colision(self) -> set["Zone3D"]:
        """get la map"""
        return self.__colision

    def get_playeur(self) -> "Playeur":
        """get le playeur"""
        return self.__playeur

    def get_graviter(self) -> bool:
        """get la graviter"""
        return self.__graviter

    def get_signal(self) -> set[int]:
        """get le signal"""
        return self.__signal

    def add_poussable(self, poussable: object) -> None:
        """ajoute un objet poussable à la map"""
        self.__poussable.add(poussable)

    def add_activateur(self, activateur: "Activateur") -> None:
        """ajoute un activateur à la map"""
        self.__activateur.add(activateur)

    def remove_activateur(self, activateur: "Activateur") -> None:
        """retire un activateur de la map"""
        self.__activateur.remove(activateur)

    def remove_playeur(self, playeur: "Playeur") -> None:
        """retire le playeur de la map"""
        self.__afficher.remove(playeur)
        self.__colision.remove(playeur)
        self.__playeur = None

    def remove_poussable(self, poussable: object) -> None:
        """retire un objet poussable de la map"""
        self.__poussable.remove(poussable)

    def in_signal(self, signal: int) -> bool:
        """permet de savoir si un signal est actif"""
        return signal in self.__signal

    def intersect_signal(self, signaux: set[int]) -> bool:
        """permet de savoir si un signal est actif"""
        return len(self.__signal & signaux) > 0

    def contient_signal(self, signaux: set[int]) -> bool:
        """permet de savoir si un signal est actif"""
        return len(self.__signal & signaux) == len(signaux)
