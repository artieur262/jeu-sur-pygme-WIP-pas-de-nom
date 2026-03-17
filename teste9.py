import random


def crier(arg):
    print(arg)


def miauler():
    crier("miaou")


def nomer(prenom, nom):
    print(f"{prenom} {nom}")


def get_callable(fn, *args, **kwargs) -> callable:
    """get une fonction avec des arguments

    Args:
        fn (callable): est la fonction a appeler
        *args: sont les arguments de la fonction sous forme de tuple
        **kwargs: sont les arguments de la fonction sous forme de dictionnaire


    Returns:
        callable: est la fonction avec les arguments
    """
    print(f"get_callable: {fn.__name__} avec args: {args} et kwargs: {kwargs}")

    def runner():
        return fn(*args, **kwargs)

    return runner


def a():
    srdgopdfkgp = random.randint(0, 100)

    def b():
        print(srdgopdfkgp)

    return b


def main():
    fonc1: callable = miauler
    fonc2: callable = lambda: crier("wouf")
    fonc3: callable = get_callable(crier, "wouf")
    fonc4: callable = get_callable(
        nomer, "Jean", nom="Dupont"
    )  # nomer("Jean", nom="Dupont")
    fonc1()
    fonc2()
    fonc3()
    fonc4()

    b = a()

    print("b: ", b)
    b()
    b()


if __name__ == "__main__":
    main()
