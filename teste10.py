from typing import Union


class Cat:
    def __init__(self, test: Union[str, "Cat"]):
        print(type(test))


def main():
    a = Cat("miaou")
    Cat(a)
    print(type("Cat"))

    print(type(str | int))
    print(Union[str, "Cat"])


if __name__ == "__main__":
    main()
