"""contient les different bloc logique"""

from py.game.Map import Map


class Logique:
    """classe mere des blocs logique
    """
    def __init__(self, entre, sorti: int):
        """initialise le bloc logique"""
        self.entre = entre
        self.sorti = sorti

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        raise NotImplementedError("la fonction n'est pas encore implémenté")

    def ajouter_map(self, map_ :"Map") -> None:
        """ajoute la map"""
        map_.add_logique(self)

    def retirer_map(self, map_: "Map") -> None:
        """retire la map"""
        map_.remove_logique(self)


class LogiqueAND(Logique):
    """classe qui active la sortie si toutes les entrées sont activées
    """
    def __init__(self, entre: set[int], sorti: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if input_ & self.entre == self.entre:
            output.add(self.sorti)


class LogiqueOR(Logique):
    """classe qui active la sortie si une des entrées est activée
    """
    def __init__(self, entre: set[int], sorti: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if len(input_ & self.entre) > 0:
            output.add(self.sorti)


class LogiqueXOR(Logique):
    """classe qui active la sortie si une des entrées est activée
    """
    def __init__(self, entre: set[int], sorti: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet"""
        if len(input_ & self.entre) > 0 and not input_ & self.entre == self.entre:
            output.add(self.sorti)


class LogiqueNOT(Logique):
    """retourne l'inverse de l'entrée 
    """
    def __init__(self, entre: int, sorti: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if self.entre not in input_:
            output.add(self.sorti)


class LogiqueTimer(Logique):
    """classe qui active la sortie après un certain temps
    """
    def __init__(self, entre: int, sorti: int, duree: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre: int
        self.duree = duree
        self.temps = set()

    def actualiser_temps(self) -> None:
        """actualise le temps"""
        new_temps = set()
        for t in self.temps:
            if t > 0:
                new_temps.add(t - 1)

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        self.actualiser_temps()
        if 0 in self.temps:
            output.add(self.sorti)
        if self.entre in input_:
            self.temps.add(self.duree)


class LogiqueLevier(Logique):
    """classe qui active la sortie si le levier est activé
    """
    def __init__(self, entre: int, sorti: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.etat = False

    def lock_unlock(self) -> None:
        """permet de changer l'etat du levier"""
        self.etat = not self.etat

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if self.entre in input_:
            self.lock_unlock()

        if self.etat:
            output.add(self.sorti)


class LogiqueChangementEtat(Logique):
    """s'active s'il y a un changement. 
    """
    def __init__(self, entre: int, sorti: int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.etat = False

    def get_activation(self, input_: set[int], output: set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        se_trouve = self.entre in input_
        if self.etat != se_trouve:
            output.add(self.sorti)

        self.etat = se_trouve
