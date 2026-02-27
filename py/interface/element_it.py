class ElementInterface:
    """Interface pour les éléments interactifs.

    args:
        taille_auto (bool): indique si la taille de l'élément doit être automatiquement ajustée en fonction de son contenu.
        parent (ElementInterface, optional): est l'interface parente. Defaults to None.
    """

    def __init__(self, taille_auto: bool, parent: "ElementInterface" = None) -> None:
        """initialise l'interface

        Args:
            parent (ElementInterface, optional): est l'interface parente. Defaults to None.
        """
        self._taille_auto = taille_auto
        self._parent = parent

    def get_taille_auto(self) -> bool:
        """get la taille auto de l'interface"""
        return self._taille_auto

    def get_parent(self) -> "ElementInterface":
        """get l'interface parente de l'interface"""
        return self._parent

    def set_parent(self, parent: "ElementInterface") -> None:
        """set l'interface parente de l'interface"""
        self._parent = parent
