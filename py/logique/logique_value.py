from typing import TYPE_CHECKING

from py.logique.bloc_logique import Logique
from py.autre.operateur import Operateur

if TYPE_CHECKING:
    from py.game.map import Map


class LogiqueValue(Logique):
    """cette class gère les objets logique boolean

    Args:
        Logique ():
    """

    def __init__(
        self,
        entre: set[str | int | tuple[str, int, str] | tuple[str, int]],
        sorti: str | int | tuple[str, int],
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, map_: "Map"):
        raise NotImplementedError()


class LogiqueSum(LogiqueValue):
    """classe qui additionne les entrées et envoie le résultat à la sortie"""

    def __init__(
        self,
        entre: set[str | int | tuple[str, int, str] | tuple[str, int]],
        sorti: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        map_.add_signal(
            (self.sorti, sum(map_.in_signal(indice) for indice in self.entre))
        )


class LogiqueMax(LogiqueValue):
    """classe qui envoie la valeur maximale des entrées à la sortie"""

    def __init__(
        self,
        entre: set[str | int | tuple[str, int, str] | tuple[str, int]],
        sorti: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        map_.add_signal(
            (self.sorti, max(map_.in_signal(indice) for indice in self.entre))
        )


class LogiqueMin(LogiqueValue):
    """classe qui envoie la valeur minimale des entrées à la sortie"""

    def __init__(
        self,
        entre: set[str | int | tuple[str, int, str] | tuple[str, int]],
        sorti: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        map_.add_signal(
            (self.sorti, min(map_.in_signal(indice) for indice in self.entre))
        )


class LogiqueAvg(LogiqueValue):
    """classe qui envoie la valeur moyenne des entrées à la sortie"""

    def __init__(
        self,
        entre: set[str | int | tuple[str, int, str] | tuple[str, int]],
        sorti: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        map_.add_signal(
            (
                self.sorti,
                sum(map_.in_signal(indice) for indice in self.entre) // len(self.entre),
            )
        )


class LogiqueCount(LogiqueValue):
    """classe qui compte le nombre d'entrées actives et envoie le résultat à la sortie"""

    def __init__(
        self,
        entre: set[str | int | tuple[str, int, str] | tuple[str, int]],
        sorti: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        map_.add_signal(
            (self.sorti, sum(1 for indice in self.entre if map_.in_signal(indice)))
        )


class LogiqueMultipriseValue(LogiqueValue):
    """cette class transmet une valeur d'un signal à plusieurs autres"""

    def __init__(
        self,
        entre: str,
        sorti: set[str],
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        valeur = map_.in_signal(self.entre)
        for sortie in self.sorti:
            map_.add_signal((sortie, valeur))


class LogiqueCopyValue(LogiqueValue):
    """cette class copie la valeur d'un signal à un autre"""

    def __init__(
        self,
        entre: str,
        sorti: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        valeur = map_.in_signal(self.entre)
        map_.add_signal((self.sorti, valeur))


class LogiqueOperate(LogiqueValue):
    """cette class applique une opération entre deux signaux et envoie le résultat à la sortie"""

    def __init__(
        self,
        entre: tuple[str, str],
        sorti: str,
        operateur: str,
    ):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.operateur = operateur

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        valeur1 = map_.in_signal(self.entre[0])
        valeur2 = map_.in_signal(self.entre[1])
        resultat = Operateur.operate(valeur1, valeur2, self.operateur)
        map_.add_signal((self.sorti, resultat))


class LogiqueValueChangement(LogiqueValue):
    """cette class détecte un changement de valeur d'un signal et envoie une activation à la sortie
    Args:
        entre (str): le signal d'entrée
        sorti (str | int | tuple[str, int]): le signal de sortie
        mode (str): le mode de détection du changement ("changement", "augmentation", "diminution")
    """

    def __init__(self, entre: str, sorti: int | tuple[str, int], mode: str = None):
        """initialise le bloc logique"""
        if mode is None:
            mode = "changement"
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.last_value = None
        self.mode = mode

    def get_activation(self, map_: "Map") -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        current_value = map_.in_signal(self.entre)
        if self.last_value is None:
            self.last_value = current_value
            return

        match self.mode:
            case "changement":
                if current_value != self.last_value:
                    map_.add_signal(self.sorti)
            case "augmentation":
                if current_value > self.last_value:
                    map_.add_signal(self.sorti)
            case "diminution":
                if current_value < self.last_value:
                    map_.add_signal(self.sorti)
            case _:
                raise ValueError(f"Mode inconnu: {self.mode}")
        self.last_value = current_value
