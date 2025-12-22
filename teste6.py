class A1:
    def __init__(self, value):
        self.value = value

    def test1(self):
        raise NotImplementedError("A1 ne peut pas faire test1.")

    def test2(self):
        raise NotImplementedError("A1 ne peut pas faire test2.")


class B1:
    def __init__(self, value):
        self.value = value
        print("B1 initialisé avec value =", value)

    def test3(self):
        print("B1 fait test3.")


class C1(A1):

    def __init__(self, value):
        super().__init__(value)

    def test1(self):
        print("B1 fait test1.")

    def test2(self):
        print(self.value)


class fusion(C1, B1):

    def cat(self):
        print("fusion de A1 et B1")


if __name__ == "__main__":
    a = A1(10)
    # b = B1()
    c = fusion(10)
    # d = fusion()
    print(a.value)  # Output: 10
    # print(b.value)  # Output: 0
    print(c.value)  # Output: 10
    # print(d.value)  # Output: 0
    c.test2()  # Output: 10
