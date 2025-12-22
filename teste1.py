# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods, missing-module-docstring


class Chat:
    def __init__(self, name):
        self.name = name

    def meow(self):
        print(f"{self.name} says Meow!")

    def faire_calin(self):
        print(f"{self.name} is cuddling! meow!")

    def chase_laser(self):
        print(f"{self.name} is chasing the laser pointer!")


class Bebe:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def cry(self):
        print(f"{self.name} says Wahhh!")

    def voir_age(self):
        return self.age

    def faire_calin(self):
        print(f"{self.name} is cuddling! wahhh!")

    # def chase_laser(self):
    #     raise NotImplementedError("Bebe ne peut pas chasser le pointeur laser.")


class Chaton(Bebe, Chat):
    def __init__(self, name, age):
        Bebe.__init__(self, name, age)
        Chat.__init__(self, name)


if __name__ == "__main__":
    bebe_chat = Chaton("Kitty", 1)
    bebe_chat.cry()  # Output: Kitty says Wahhh!
    bebe_chat.meow()  # Output: Kitty says Meow!
    print(bebe_chat.age)  # Output: 1
    bebe_chat.faire_calin()  # Output: Kitty is cuddling! wahhh!
    try:
        bebe_chat.chase_laser()  # Raises NotImplementedError
    except NotImplementedError as e:
        print(e)
