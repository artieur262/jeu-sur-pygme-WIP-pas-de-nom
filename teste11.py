"""Test de la classe AB"""


class AB:
    """Classe AB qui prend en argument une méthode et ses arguments"""

    def __init__(self, methode: callable, *args, **kwargs):
        self.methode = methode
        self.args = args
        self.kwargs = kwargs

    def executer(self, nb: int):
        """Exécute la méthode avec les arguments donnés"""
        return self.methode(nb, *self.args, **self.kwargs)


def a1(nb: int, test: str):
    """Fonction a1 qui prend en argument un nombre et un test"""
    print(f"nb: {nb} et test: {test}")


def b2(nb: int, test: str, test2: str):
    """Fonction b2 qui prend en argument un nombre, un test et un test2"""
    print(f"nb: {nb} et test: {test} et test2: {test2}")


dict_fonc = {"a1": a1, "b2": b2}


def main():
    """Fonction principale"""
    ab = AB(a1, test="miaou")
    ab.executer(42)
    ab2 = AB(b2, "miaou", test2="i am a cat")
    ab2.executer(42)
    if a1 in dict_fonc.values():
        print("a1 est dans dict_fonc")


if __name__ == "__main__":
    main()
