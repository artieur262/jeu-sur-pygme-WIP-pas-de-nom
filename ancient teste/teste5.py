def afficher_tuple(t):
    """affiche un tuple"""
    if isinstance(t, tuple):
        print("taille 3:", t)
    elif isinstance(t, tuple):
        print("taille 2:", t)


def main():
    """est un test"""
    a = ("cat", 1, "4")
    b = ("chaton", 2)
    afficher_tuple(a)
    afficher_tuple(b)


if __name__ == "__main__":
    main()
