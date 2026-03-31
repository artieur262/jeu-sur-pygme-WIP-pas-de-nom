class A1:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class B2(A1):
    def __init__(self, x, y, z):
        # le super ne fonctionne pas dans ce cas, il faut appeler le constructeur
        #   de la classe parente directement
        # car sinon, le constructeur de C3 va écraser les attributs x et y de A1
        A1.__init__(self, x, y)

        self.z = z


class C3(A1):
    def __init__(self, x, y, beautiful: bool):
        super().__init__(x, y)
        self.beautiful = beautiful


class D4(B2, C3):
    def __init__(self, x, y, z, beautiful: bool):
        B2.__init__(self, x, y, z)
        C3.__init__(self, x, y, beautiful)


def main():
    d = D4(1, 2, 3, True)
    print(d.x, d.y, d.z, d.beautiful)


if __name__ == "__main__":
    main()
