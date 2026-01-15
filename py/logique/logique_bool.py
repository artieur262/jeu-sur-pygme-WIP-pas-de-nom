from typing import TYPE_CHECKING

from py.logique.bloc_logique import Logique

if TYPE_CHECKING:
    from py.game.map import Map


class LogiqueBool(Logique):
    """cette class gère les objets logique boolean

    Args:
        Logique ():
    """

    def __init__(
        self,
        entre: set[int | tuple[str, int, str] | tuple[str, int]],
        sorti: int | tuple[str, int],
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, map_: "Map"):
        raise NotImplementedError()


class LogiqueAND(LogiqueBool):
    """classe qui active la sortie si toutes les entrées sont activées"""

    # def __init__(
    #     self,
    #     entre: set[int | tuple[str, int, str] | tuple[str, int]],
    #     sorti: int | tuple[str, int],
    # ):
    #     """initialise le bloc logique"""
    #     super().__init__(entre, sorti)

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        active = True
        for indice in self.entre:
            if not map_.in_signal(indice):
                active = False
                break  # ce break est là que pour de l'optimisation
        if active:
            map_.add_new_signal(self.sorti)


class LogiqueOR(LogiqueBool):
    """classe qui active la sortie si une des entrées est activée"""

    # def __init__(
    #     self,
    #     entre: set[int | tuple[str, int, str] | tuple[str, int]],
    #     sorti: int | tuple[str, int],
    # ):
    #     """initialise le bloc logique"""
    #     super().__init__(entre, sorti)

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        active = False
        for indice in self.entre:
            if map_.in_signal(indice):
                active = True
                break  # ce break est là que pour de l'optimisation
        if active:
            map_.add_new_signal(self.sorti)


class LogiqueXOR(LogiqueBool):
    """classe qui active la sortie si une des entrées est activée"""

    # def __init__(
    #     self,
    #     entre: set[int | tuple[str, int, str] | tuple[str, int]],
    #     sorti: int | tuple[str, int],
    # ):
    #     """initialise le bloc logique"""
    #     super().__init__(entre, sorti)

    def get_activation(self, map_: "Map") -> None:

        or_ = False
        and_ = True
        i = 0
        while (not or_ or and_) and i < len(self.entre):
            indice = self.entre[i]
            if map_.in_signal(indice):
                or_ = True
            else:
                and_ = False
            indice += 1
        if or_ and not and_:
            map_.add_new_signal(self.sorti)


class LogiqueNOT(LogiqueBool):
    """retourne l'inverse de l'entrée"""

    def __init__(
        self,
        entre: int | tuple[str, int, str] | tuple[str, int],
        sorti: int | tuple[str, int],
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if not map_.in_signal(self.entre):
            map_.add_new_signal(self.sorti)


class LogiqueTimer(LogiqueBool):
    """classe qui active la sortie après un certain temps"""

    def __init__(
        self,
        entre: int | tuple[str, int, str] | tuple[str, int],
        sorti: int | tuple[str, int],
        duree: int,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre: int
        self.duree = duree
        self.temps: set[int] = set()

    def actualiser_temps(self) -> None:
        """actualise le temps"""
        new_temps = set()
        for t in self.temps:
            if t > 0:
                new_temps.add(t - 1)

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        self.actualiser_temps()
        if 0 in self.temps:
            map_.add_new_signal(self.sorti)
        if map_.in_signal(self.entre):
            self.temps.add(self.duree)


class LogiqueLevier(LogiqueBool):
    """classe qui active la sortie si le levier est activé"""

    def __init__(
        self,
        entre: int | tuple[str, int, str] | tuple[str, int],
        sorti: int | tuple[str, int],
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.etat = False

    def lock_unlock(self) -> None:
        """permet de changer l'etat du levier"""
        self.etat = not self.etat

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if map_.in_signal(self.entre):
            self.lock_unlock()

        if self.etat:
            map_.add_new_signal(self.sorti)


class LogiqueChangementEtat(LogiqueBool):
    """s'active s'il y a un changement."""

    def __init__(
        self,
        entre: int | tuple[str, int, str] | tuple[str, int],
        sorti: int | tuple[str, int],
        mode: str = None,
    ):
        """initialise le bloc logique"""
        if mode is None:
            mode = "change"
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.etat_precedant = False
        self.mode = mode

    def __mode_change(self, new_etat: bool) -> bool:
        """permet de savoir si l'etat a changé"""
        match self.mode:
            case "change":
                return new_etat != self.etat_precedant
            case "change_go_on":
                return new_etat and new_etat != self.etat_precedant
            case "change_go_off":
                return not new_etat and new_etat != self.etat_precedant
            case _:
                raise ValueError(f"Mode inconnu: {self.mode}")

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        new_etat = map_.in_signal(self.entre)
        if self.__mode_change(new_etat):
            map_.add_new_signal(self.sorti)
        self.etat_precedant = new_etat


class LogiqueMultipriseBool(LogiqueBool):
    """cette class ajoute la posibilité d'activer plusieurs signaux si un signal est activé"""

    def __init__(
        self,
        entre: int | tuple[str, int, str] | tuple[str, int],
        sorti: set[int | tuple[str, int]],
    ):
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti

    def get_activation(self, map_: "Map"):
        if map_.in_signal(self.entre):
            for i in self.sorti:
                map_.add_new_signal(self.sorti[i])
