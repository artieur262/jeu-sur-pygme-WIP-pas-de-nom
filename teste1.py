class Chat :
    def __init__(self, name):
        self.name = name

    def meow(self):
        print(f"{self.name} says Meow!")

class Bebe:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def cry(self):
        print(f"{self.name} says Wahhh!")
    
    def age(self):
        return self.age

class BebeChat(Bebe, Chat):
    def __init__(self, name, age):
        Bebe.__init__(self, name, age)
        Chat.__init__(self, name)
    

if __name__ == "__main__":
    bebe_chat = BebeChat("Kitty", 1)
    bebe_chat.cry()  # Output: Kitty says Wahhh!
    bebe_chat.meow()  # Output: Kitty says Meow!
    print(bebe_chat.age)  # Output: 1