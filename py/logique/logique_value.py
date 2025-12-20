from typing import TYPE_CHECKING

from py.logique.bloc_logique import Logique

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
