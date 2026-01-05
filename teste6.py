class A1:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def test1(self):
        raise NotImplementedError("A1 ne peut pas faire test1.")

    def test2(self):
        self.test1()


class B1:
    def test1(self: A1):
        print("test1 de B1 :", self.get_value())


class fusion(B1, A1):

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
