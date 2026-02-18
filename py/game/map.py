from typing import TYPE_CHECKING
from py.autre.operateur import Operateur

if TYPE_CHECKING:
    from py.game.game import Game
    from py.block.playeur import Playeur
    from py.block.plateforme import Plateforme
    from py.block.activateur.activateur import Activateur
    from py.block.activable.activable import Activable
    from py.logique.bloc_logique import Logique
    from py.objet.objet_visuel import ObjetVisuel3D
    from py.objet.zone import Zone3D
    from py.block.special import Special
    from py.block.actualisable import Actualisable

    # from py.block.tunel import TunelSimple
    # from py.block.activable.core import Core
# from py.logique.bloc_logique import Logique


class Map:
    """Map est une classe qui permet de gerer la map
    Args:
        Map (Map): est la map
    """

    def __init__(self, game: "Game"):
        """initialise la map"""
        self.__game: "Game" = game
        self.__colision: set["Zone3D"] = set()
        self.__playeur: "Playeur" = None
        self.__afficher: set["ObjetVisuel3D"] = set()
        self.__graviter: bool = False
        self.__logique: set["Logique"] = set()
        self.__activateur: set["Activateur"] = set()
        self.__activable: set["Activable"] = set()
        self.__poussable: set = set()

        self.__actualisable: set["Actualisable"] = set()
        self.__special: dict[tuple[int, int], list["Special"]] = dict()

        self.__signal_presence: set[int] = set()
        self.__signal_valeur: dict[str, int] = dict()
        self.__signal_valeur_comportement: dict[str, tuple[str, int]] = dict()
        self.__new_signal_presence: set[int] = None
        self.__new_signal_valeur: dict[str, int] = None

    def play_turn(self) -> None:
        """permet de jouer un tour de jeu"""
        self.actualiser_logique()
        self.special_active_input()
        self.actualiser_actualisable()

    def actualiser_actualisable(self) -> None:
        """actualise la map"""
        for i in self.__actualisable:
            i.actualiser(self)

    def special_active_input(self):
        """permet d'activer les special en fonction des entrées du clavier
        puis active les special concerné avec les entrées du clavier en parametre
        """
        for key, value in self.__special.items():
            if self.get_game().get_clavier().get_pression(key[0]) == key[1]:
                for special in value:
                    special.active_input(key, self)

    def add_signal(self, signal: int | tuple[str, int]) -> None:
        """ajoute un signal actif"""
        if isinstance(signal, tuple):
            self.__signal_valeur[signal[0]] = signal[1]
        elif isinstance(signal, int):
            self.__signal_presence.add(signal)
        else:
            raise TypeError("le signal doit etre un int ou un tuple[str,int]")

    def add_new_signal(self, signal: int | tuple[str, int]):
        """ajoute un signal actif dans les futurs signal"""
        if isinstance(signal, tuple):
            self.__new_signal_valeur[signal[0]] = signal[1]
        elif isinstance(signal, int):
            self.__new_signal_presence.add(signal)
        else:
            raise TypeError("le signal doit etre un int ou un tuple[str,int]")

    def in_signal(
        self, sorti: str | int | tuple[str, int] | tuple[str, int, str]
    ) -> int | bool:
        """permet de savoir si un signal est actif ou de recupere la valeur d'un signal"""

        if isinstance(sorti, str):
            if sorti in self.__signal_valeur:
                return self.__signal_valeur[sorti]
            else:
                raise KeyError(f"le signal {sorti} n'existe pas dans la map")

        elif isinstance(sorti, int):
            return sorti in self.__signal_presence
        elif isinstance(sorti, tuple):
            if len(sorti) == 2:
                if isinstance(sorti[0], str) and isinstance(sorti[1], int):
                    if sorti[0] in self.__signal_valeur:
                        return self.__signal_valeur[sorti[0]] == sorti[1]
                    else:
                        raise KeyError(f"le signal {sorti[0]} n'existe pas dans la map")
                else:
                    raise TypeError("le tuple doit contenir (str, int)")
            elif len(sorti) == 3:
                if (
                    isinstance(sorti[0], str)
                    and isinstance(sorti[1], int)
                    and isinstance(sorti[2], str)
                ):
                    if sorti[0] in self.__signal_valeur:
                        return Operateur.compare(
                            self.__signal_valeur[sorti[0]], sorti[1], sorti[2]
                        )
                    else:
                        raise KeyError(f"le signal {sorti[0]} n'existe pas dans la map")
                else:
                    raise TypeError("le tuple doit contenir (str, int, str)")

            else:
                raise ValueError("le tuple doit contenir 2 ou 3 elements")

    def reset_new_signal(self):
        """reset les futurs signaux"""
        self.__new_signal_presence: set[int] = set()
        self.__new_signal_valeur: dict[str, int] = dict()
        for key, value in self.__signal_valeur_comportement.items():
            self.__new_signal_valeur[key] = value[1]

    def actualiser_logique(self) -> None:
        """actualise l'activation des blocs logiques"""
        self.reset_new_signal()
        for i in self.__logique:
            i.get_activation(self.__signal_presence, self.__new_signal_valeur)
        self.__signal_presence = self.__new_signal_valeur

    def get_game(self) -> "Game":
        """get le jeu"""
        return self.__game

    def set_game(self, game: "Game") -> None:
        """set le jeu"""
        self.__game = game

    def add_special(self, control: str, special: "Special") -> None:
        """ajoute un special à la map"""
        if control not in self.__special:
            self.__special[control] = []
        self.__special[control].append(special)

    def remove_special(self, control: str, special: "Special") -> None:
        """retire un special de la map"""
        if control in self.__special:
            self.__special[control].remove(special)
            if len(self.__special[control]) == 0:
                del self.__special[control]

    def add_activable(self, activable: "Activable") -> None:
        """ajoute un activable à la map"""
        self.__activable.add(activable)

    def remove_activable(self, activable: "Activable") -> None:
        """retire un activable de la map"""
        self.__activable.remove(activable)

    def add_actualisable(self, actualisable: "Actualisable") -> None:
        """ajoute un actualisable à la map"""
        self.__actualisable.add(actualisable)

    def remove_actualisable(self, actualisable: "Actualisable") -> None:
        """retire un actualisable de la map"""
        self.__actualisable.remove(actualisable)

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

    def get_affichable(self) -> set["ObjetVisuel3D"]:
        """affiche la map"""
        return self.__afficher

    def get_special(self) -> dict[str, list["Special"]]:
        """get les special"""
        return self.__special

    def get_colision(self) -> set["Zone3D"]:
        """get la map"""
        return self.__colision

    def get_playeur(self) -> "Playeur":
        """get le playeur"""
        return self.__playeur

    def get_graviter(self) -> bool:
        """get la graviter"""
        return self.__graviter

    def get_poussable(self) -> set:
        """get les objets poussable"""
        return self.__poussable

    def get_signal_presence(self) -> set[int]:
        """get le signal"""
        return self.__signal_presence

    def get_signal_valeur(self) -> dict[str, int]:
        """get le dictionnaire des signaux de valeur"""
        return self.__signal_valeur

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

    def intersect_signal(self, signaux: set[int]) -> bool:
        """permet de savoir si un signal est actif"""
        return len(self.__signal_presence & signaux) > 0

    def contient_signal(self, signaux: set[int]) -> bool:
        """permet de savoir si un signal est actif"""
        return len(self.__signal_presence & signaux) == len(signaux)
