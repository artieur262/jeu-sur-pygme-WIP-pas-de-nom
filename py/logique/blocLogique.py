class Logique:
    def __init__(self, entre, sorti:int):
        """initialise le bloc logique"""
        self.entre = entre 
        self.sorti = sorti

    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        pass

class LogiqueAND(Logique):
    def __init__(self, entre:set[int], sorti:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
    
    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if input & self.entre == self.entre:
            output.add(self.sorti)

class LogiqueOR(Logique):
    def __init__(self, entre:set[int], sorti:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
    
    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if len(input & self.entre) > 0:
            output.add(self.sorti)
    

class LogiqueXOR(Logique):
    def __init__(self, entre:set[int], sorti:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
    
    def activer(self, input:set[int], output:set[int]) -> None:
        """permet """
        if len(input & self.entre) > 0 and not input & self.entre == self.entre:
            output.add(self.sorti)


class LogiqueNOT(Logique):
    def __init__(self, entre:int, sorti:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
    
    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if self.entre not in input:
            output.add(self.sorti)

class LogiqueTimer(Logique):
    def __init__(self, entre:int, sorti:int, duree:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre : int
        self.duree = duree
        self.temps = set()
    
    def actualiser_temps(self) -> None:
        """actualise le temps"""
        new_temps = set()
        for t in self.temps:
            if t > 0:
                new_temps.add(t-1)

    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        self.actualiser_temps()
        if 0 in self.temps:
            output.add(self.sorti)
        if self.entre in input:
            self.temps.add(self.duree)


class LogiqueLevier(Logique):
    def __init__(self, entre:int, sorti:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.etat = False

    def lock_unlock(self) -> None:
        """permet de changer l'etat du levier"""
        self.etat = not self.etat

    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        if self.entre in input:
            self.lock_unlock()

        if self.etat:
            output.add(self.sorti)
            
class LogiqueChangementEtat(Logique):
    def __init__(self, entre:int, sorti:int):
        """initialise le bloc logique"""
        super().__init__(entre, sorti)
        self.entre = entre
        self.sorti = sorti
        self.etat = False

    def activer(self, input:set[int], output:set[int]) -> None:
        """permet d'activer le bloc logique et ajouter les sorties dans le signal de output"""
        se_trouve = self.entre in input
        if self.etat != se_trouve:
            output.add(self.sorti)

        self.etat = se_trouve
        
        
        
